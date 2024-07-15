import pytest
from datetime import datetime
from ProjectAgile import us03, parse_gedcom_file

def create_individual(id = "NA", birth_date = "NA", death_date = "NA"):
    return {
        "ID": id,
        "birth_date_str": birth_date,
        "death_date_str": death_date
    }

# birth and death 
def test_1_us03():
    # Test case 2: Individual who is alive but not married
    indi1 = create_individual("I05", "1 JAN 2024", "2 AUG 2019")
    assert us03([indi1]) == [f'ERROR: INDIVIDUAL: US03: I05: Birth date not before death date.']
    
def test_2_us03(): 
    indi2 = create_individual("I08", "20 NOV 1930", "21 JAN 2035")
    assert us03([indi2]) == [f'ERROR: INDIVIDUAL: US03: I05: Birth date not before death date.']
    
def test_3_us03():  
    indi3 = create_individual("I09", "20 JUN 2220", "1 JAN 2100")
    assert us03([indi3]) == [f'ERROR: INDIVIDUAL: US03: I05: Birth date not before death date.']
    
def test_4_us03(): 
    indi4 = create_individual("I10", "20 OCT 2030", "1 JAN 2013")
    assert us03([indi4]) == [f'ERROR: INDIVIDUAL: US03: I05: Birth date not before death date.']