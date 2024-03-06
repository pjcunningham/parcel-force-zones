# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2024, Paul Cunningham'

import logging
import click
from extractor import Extractor

logger = logging.getLogger()


@click.command()
@click.argument('input-file', type=click.Path(exists=True, file_okay=True, dir_okay=False))
@click.argument('output-file', type=click.Path(file_okay=True, dir_okay=False))
def cli(input_file, output_file):

    extractor = Extractor(input_file)
    extractor.save_to(output_file)


if __name__ == "__main__":
    cli()
