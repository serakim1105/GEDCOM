import pytest
from ProjectAgile import us05
from datetime import datetime

def compare_date(wedding_date = "NA", death_date = "NA"):
    return {
        'WeddingDay': wedding_date,
        'DeathDay': death_date
    }

def test_1_us05(): 
    dateCheck1 = create_date("20 OCT 1942", "1 JAN 2015")
    assert us05([dateCheck1])
    
def test_2_us05(): 
    dateCheck2 = create_date("20 OCT 1942", "1 FEB 2018")
    assert us05([dateCheck2])
    
def test_3_us05(): 
    dateCheck3 = create_date("20 NOV 1950", "21 JAN 2200")
    assert us05([dateCheck3])
    
def test_4_us05(): 
    dateCheck4 = create_date("20 JUN 2000", "1 JAN 2100")
    assert us05([dateCheck4])
    
def test_5_us05(): 
    dateCheck5 = create_date("20 OCT 2030", "1 JAN 2015")
    assert us05([dateCheck5])
