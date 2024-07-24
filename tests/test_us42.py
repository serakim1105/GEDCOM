import pytest
from datetime import datetime
from parseDate import safe_parse_date, parse_date

date_full = '10 JAN 2000'
date_no_day = 'JAN 2000'
date_no_day_mo = '2000'

def test_1_us42(): 
    assert us39([date1])