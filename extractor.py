# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2024, Paul Cunningham'

import logging
import pathlib
import camelot
import petl
import re

logger = logging.getLogger()

POST_CODE_AREA_RE = r'([A-Z]){1,2}'

# Page 1-7 are Zone 1
# Page 7 are Zone 2 and Zone 3
# Zone is in column 0
# Area is in Column 1
# Location is in Column 2
# Zone is in Column 3
# Post Codes Columns 4 - 12


class Extractor(object):

    def __init__(self, input_filename):
        self.input_filename = input_filename
        self.unique_area_location_table = None
        self.unique_postcode_table = None

    def init_temp_tables(self):
        self.unique_area_location_table = petl.empty().setheader(['Area', 'Location'])
        self.unique_postcode_table = petl.empty().setheader(['Post Code', 'Area'])

    @staticmethod
    def supported_file_extensions():
        return ['.json', '.csv', '.xlsx']

    def post_code_generator(self, row):
        for col in row:
            if col != '':
                yield col, re.search(POST_CODE_AREA_RE, col).group(0)

    def extract_table(self, table, skip_row_count):
        table = petl.fromdataframe(table.df, include_index=False)
        table = petl.skip(table, skip_row_count)
        table = petl.cutout(table, "Zone")
        page_unique_area_location = petl.selectne(table, "Area", '').cut("Area", "Location")
        self.unique_area_location_table = petl.stack(self.unique_area_location_table, page_unique_area_location)
        page_post_codes_table = petl.cutout(table, "Area", "Location")
        page_unique_postcode_table = petl.rowmapmany(page_post_codes_table, self.post_code_generator,
                                                     header=['Post Code'])
        self.unique_postcode_table = petl.stack(self.unique_postcode_table, page_unique_postcode_table)

    def convert_table(self, zone):

        area_location_lookup = petl.lookup(self.unique_area_location_table, 'Area', 'Location')

        # Add the Zone, Location columns
        output_table = petl.addfield(self.unique_postcode_table, "Zone", zone, 0)
        output_table = petl.addfield(output_table, "Location", None, 3)

        # fill in Location via lookup use Area as key
        output_table = petl.convert(
            output_table,
            'Location',
            lambda v, row: area_location_lookup[row["Area"]][0],
            pass_row=True
        )

        return output_table

    def extract(self):

        zone_1_tables_page_1_6 = camelot.read_pdf(self.input_filename, flavor='stream', pages='1-6')
        zone_1_tables_page_7 = camelot.read_pdf(self.input_filename, flavor='stream', pages='7', table_areas=['40, 770, 537, 537'])
        zone_2_tables_page_7 = camelot.read_pdf(self.input_filename, flavor='stream', pages='7',
                                                table_areas=['40,510,537,320'])

        zone_3_tables_page_7 = camelot.read_pdf(self.input_filename, flavor='stream', pages='7',
                                                table_areas=['40,290,537,180'])

        # Zone 1 Page 1 - 6
        self.init_temp_tables()
        for table in zone_1_tables_page_1_6:
            self.extract_table(table, skip_row_count=3)

        # fix up problematic areas ('KT', 'Kingston-Upon-Thames'), ('SE', 'London - South East')
        self.unique_area_location_table = petl.convert(
            self.unique_area_location_table,
            "Location",
            lambda v: 'Kingston-Upon-Thames',
            where=lambda r: r['Area'] == 'KT'
        )

        self.unique_area_location_table = petl.convert(
            self.unique_area_location_table,
            "Location",
            lambda v: 'London - South East',
            where=lambda r: r['Area'] == 'SE'
        )

        output_table = self.convert_table(1)

        # Zone 1 Page 7
        self.init_temp_tables()
        for table in zone_1_tables_page_7:
            self.extract_table(table, skip_row_count=4)
        output_table = petl.stack(output_table, self.convert_table(1))

        # Zone 2 Page 7
        self.init_temp_tables()
        for table in zone_2_tables_page_7:
            self.extract_table(table, skip_row_count=2)
        output_table = petl.stack(output_table, self.convert_table(2))

        # Zone 3 Page 7
        self.init_temp_tables()
        for table in zone_3_tables_page_7:
            self.extract_table(table, skip_row_count=2)
        output_table = petl.stack(output_table, self.convert_table(3))

        return output_table

    def save_to(self, output_filename):

        ext = pathlib.Path(output_filename).suffix.lower()
        if ext not in Extractor.supported_file_extensions():
            logger.error(
                f"Unsupported output file:{ext}, extensions supported are: {','.join(Extractor.supported_file_extensions())}")
            return

        output_table = self.extract()
        ext = pathlib.Path(output_filename).suffix.lower()
        if ext == '.xlsx':
            petl.io.xlsx.toxlsx(output_table, output_filename)
        elif ext == '.csv':
            petl.tocsv(output_table, output_filename)
        elif ext == '.json':
            petl.tojson(output_table, output_filename)
