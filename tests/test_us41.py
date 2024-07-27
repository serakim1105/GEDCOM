import pytest
from datetime import datetime
from parseDate import safe_parse_date, parse_date

date_full = '10 JAN 2000'
date_no_day = 'JAN 2000'
date_no_day_mo = '2000'
date_na = 'NA'

def test_1_us41(): 
    assert safe_parse_date(date_full) == '10 JAN 2000'

def test_2_us41(): 
    assert safe_parse_date(date_no_day) == '1 JAN 2000'

def test_3_us41(): 
    assert safe_parse_date(date_no_day_mo) == '1 JAN 2000'

def test_4_us41(): 
    assert safe_parse_date(date_na) == 'NA'