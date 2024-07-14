import pytest
from datetime import datetime
from ProjectAgile import us39, parse_gedcom_file

def create_date(wedding_date = "NA"):
    return {
        'Married': wedding_date,
    }

def test_1_us39(): 
    date1 = create_date("20 OCT 1942")
    assert us39([date1])

def test_2_us39():
    date2 = create_date("15 AUG 1942")
    assert us39([date2])

def test_3_us39():
    date3 = create_date("1 DEC 2000")
    assert us39([date3])

def test_4_us39():
    date4 = create_date("1 NOV 2015")
    assert us39([date4])

def test_5_us39():
    date5 = create_date("30 JUL 2000")
    assert us39([date5])