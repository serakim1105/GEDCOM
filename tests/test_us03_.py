import pytest
from ProjectAgile import us03
from datetime import datetime

def compare_date(birth_date = "NA", death_date = "NA"):
    return {
        'BirthDay': birth_date,
        'DeathDay': death_date
    }

def test_1_us03(): 
    dateCheck1 = create_date("20 OCT 1942", "1 JAN 2013")
    assert us03([dateCheck1])
    
def test_2_us03(): 
    dateCheck2 = create_date("20 OCT 1942", "1 FEB 2018")
    assert us03([dateCheck2])
    
def test_3_us03(): 
    dateCheck3 = create_date("20 NOV 1930", "21 JAN 2200")
    assert us03([dateCheck3])
    
def test_4_us03(): 
    dateCheck4 = create_date("20 JUN 2000", "1 JAN 2100")
    assert us03([dateCheck4])
    
def test_5_us03(): 
    dateCheck3 = create_date("20 OCT 2030", "1 JAN 2013")
    assert us03([dateCheck3])