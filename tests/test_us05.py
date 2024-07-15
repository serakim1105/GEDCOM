import pytest
from ProjectAgile import us05, parse_gedcom_file
from datetime import datetime

def create_date(wedding_date = "NA", husband_death_date = "NA", wife_death_date = "NA"):
    return {
        'WeddingDay': wedding_date,
        'HusbandDeathDay': husband_death_date,
        'WifeDeathDay': wife_death_date
    }

def test_1_us05(families): 
    dateCheck1 = create_date("20 OCT 2050", "1 JAN 2015","23 OCT 2018")
    assert us05([dateCheck1]) == [f'ERROR: WEDDINGDATE: US05: Not before death of either spouse.']
    
def test_2_us05(families): 
    dateCheck2 = create_date("20 OCT 1942", "1 FEB 1930", "20 OCT 1920")
    assert us05([dateCheck2]) == [f'ERROR: WEDDINGDATE: US05: Not before death of either spouse.']
    
def test_3_us05(families): 
    dateCheck3 = create_date("20 NOV 1950", "21 JAN 2200", "12 APR 2014")
    assert us05([dateCheck3]) == [f'ERROR: WEDDINGDATE: US05: Not before death of either spouse.']
    
def test_4_us05(families): 
    dateCheck4 = create_date("20 JUN 2000", "1 JAN 2100", "1 APR 2024")
    assert us05([dateCheck4]) == [f'ERROR: WEDDINGDATE: US05: Not before death of either spouse.']
    
def test_5_us05(families): 
    dateCheck5 = create_date("20 OCT 2030", "1 JAN 2015", "1 JAN 2015")
    assert us05([dateCheck5]) == [f'ERROR: WEDDINGDATE: US05: Not before death of either spouse.']
