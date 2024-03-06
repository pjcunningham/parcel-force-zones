# coding: utf-8
__author__ = 'Paul Cunningham'
__copyright = 'Copyright 2024, Paul Cunningham'

import logging
import pytest
import petl

logger = logging.getLogger()


@pytest.fixture
def excel_table(shared_datadir):
    table = petl.fromxlsx(shared_datadir / 'output.xlsx')
    return table


def test_zone_1_count(excel_table):
    temp = petl.selecteq(excel_table, "Zone", 1)
    assert petl.nrows(temp) == 2713


def test_zone_2_count(excel_table):
    # 10 x 21 - 44
    temp = petl.selecteq(excel_table, "Zone", 2)
    assert petl.nrows(temp) == 166


def test_zone_3_count(excel_table):
    # 10 x 11 - 14
    temp = petl.selecteq(excel_table, "Zone", 3)
    assert petl.nrows(temp) == 96


# Selected Zone 1 Counts, 3 from each page, top, middle, bottom

# Zone 1, Page 1
def test_aberdeen_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'AB' and {Location} == 'Aberdeen'")
    assert petl.nrows(temp) == 21


def test_bristol_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'BS' and {Location} == 'Bristol'")
    assert petl.nrows(temp) == 40


def test_chemslford_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'CM' and {Location} == 'Chelmsford'")
    assert petl.nrows(temp) == 28


# Zone 1, Page 2
def test_colchester_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'CO' and {Location} == 'Colchester'")
    assert petl.nrows(temp) == 16


def test_doncaster_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'DN' and {Location} == 'Doncaster'")
    assert petl.nrows(temp) == 33


def test_exeter_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'EX' and {Location} == 'Exeter'")
    assert petl.nrows(temp) == 33


# Zone 1, Page 3
def test_falkirk_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'FK' and {Location} == 'Falkirk'")
    assert petl.nrows(temp) == 16


def test_hemel_hempstead_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'HP' and {Location} == 'Hemel Hempstead'")
    assert petl.nrows(temp) == 24


def test_llandrindod_wells_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'LD' and {Location} == 'Llandrindod Wells'")
    assert petl.nrows(temp) == 8


# Zone 1, Page 4
def test_leicester_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'LE' and {Location} == 'Leicester'")
    assert petl.nrows(temp) == 27


def test_milton_keynes_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'MK' and {Location} == 'Milton Keynes'")
    assert petl.nrows(temp) == 27


def test_norwich_wells_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'NR' and {Location} == 'Norwich'")
    assert petl.nrows(temp) == 36


# Zone 1, Page 5
def test_london_nw_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'NW' and {Location} == 'London'")
    assert petl.nrows(temp) == 13


def test_portsmouth_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'PO' and {Location} == 'Portsmouth'")
    assert petl.nrows(temp) == 34


def test_swansea_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'SA' and {Location} == 'Swansea'")
    assert petl.nrows(temp) == 53


# Zone 1, Page 6
def test_stevenage_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'SG' and {Location} == 'Stevenage'")
    assert petl.nrows(temp) == 19


def test_shrewsbury_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'SY' and {Location} == 'Shrewsbury'")
    assert petl.nrows(temp) == 26


def test_southall_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'UB' and {Location} == 'Southall'")
    assert petl.nrows(temp) == 12


def test_problematic_area_kingston_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'KT' and {Location} == 'Kingston-Upon-Thames'")
    assert petl.nrows(temp) == 24


def test_problematic_area_london_se_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 1 and {Area} == 'SE' and {Location} == 'London - South East'")
    assert petl.nrows(temp) == 29


# Selected Zone 2 Counts
def test_aberdeen_2_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 2 and {Area} == 'AB' and {Location} == 'Aberdeen'")
    assert petl.nrows(temp) == 13


def test_paisley_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 2 and {Area} == 'PA' and {Location} == 'Paisley'")
    assert petl.nrows(temp) == 48


def test_lerwick_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 2 and {Area} == 'ZE' and {Location} == 'Lerwick'")
    assert petl.nrows(temp) == 3


# Selected Zone 3 Counts
def test_belfast_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 3 and {Area} == 'BT' and {Location} == 'Belfast'")
    assert petl.nrows(temp) == 81


def test_truro_count(excel_table):
    temp = petl.select(excel_table, "{Zone} == 3 and {Area} == 'TR' and {Location} == 'Truro (Scilly Isles)'")
    assert petl.nrows(temp) == 5
