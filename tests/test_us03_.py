import pytest
from ProjectAgile import us03
from datetime import datetime

def compare_date(birth_date = "NA", husband_death_date = "NA", wife_death_date = "NA"):
    return {
        'BirthDay': birth_date,
        'HusbandDeathDate': husband_death_date, 
        'WifeDeathDate': wife_death_date
    }

def test_1_us03(): 
    dateCheck1 = create_date("20 OCT 1942", "1 JAN 2013", "2 FEB 2015")
    assert us03([dateCheck1])
    
def test_2_us03(): 
    dateCheck2 = create_date("26 OCT 1973", "1 FEB 2018", "31 OCT 2008")
    assert us03([dateCheck2])
    
def test_3_us03(): 
    dateCheck3 = create_date("20 NOV 1930", "21 JAN 2035", "15 MAR 2035")
    assert us03([dateCheck3])
    
def test_4_us03(): 
    dateCheck4 = create_date("20 JUN 2000", "1 JAN 2100", "19 APR 2050")
    assert us03([dateCheck4])
    
def test_5_us03(): 
    dateCheck3 = create_date("20 OCT 2030", "1 JAN 2013", "10 FEB 2017")
    assert us03([dateCheck3])