import pytest
from datetime import datetime
from ProjectAgile import us03, parse_gedcom_file

def create_individual(id = "NA", birth_date = "NA", death_date = "NA", name = "NA"):
    return {
        "ID": id,
        "Birthday": birth_date,
        "Death": death_date,
        "Name": name
    }

# birth and death 
def test_1_us03():
    # Test case 2: Individual who is alive but not married
    indi1 = create_individual("I05", "1 JAN 2024", "2 AUG 2019", "Justin /Lee/")
    assert us03([indi1]) == [f'ERROR: INDIVIDUAL: US03: {indi1["ID"]}:{indi1["Name"]}:{indi1["Birthday"]}:{indi1["Death"]} - Birth date not before death date.']
    
def test_2_us03(): 
    indi2 = create_individual("I08", "20 NOV 2050", "21 JAN 2035", "Cody /Lee/" )
    assert us03([indi2]) == [f'ERROR: INDIVIDUAL: US03: {indi2["ID"]}:{indi2["Name"]}:{indi2["Birthday"]}:{indi2["Death"]} - Birth date not before death date.']
    
def test_3_us03():  
    indi3 = create_individual("I09", "20 JUN 2220", "1 JAN 2100", "Austin /Lee/")
    assert us03([indi3]) == [f'ERROR: INDIVIDUAL: US03: {indi3["ID"]}:{indi3["Name"]}:{indi3["Birthday"]}:{indi3["Death"]} - Birth date not before death date.']
    
def test_4_us03(): 
    indi4 = create_individual("I10", "20 OCT 2030", "1 JAN 2013", "Sarah /Lee/")
    assert us03([indi4]) == [f'ERROR: INDIVIDUAL: US03: {indi4["ID"]}:{indi4["Name"]}:{indi4["Birthday"]}:{indi4["Death"]} - Birth date not before death date.']
    
def test_5_us03(): 
    indi5 = create_individual("I10", "20 OCT 2100", "1 JAN 2023", "Cameron /Lee/")
    assert us03([indi5]) == [f'ERROR: INDIVIDUAL: US03: {indi5["ID"]}:{indi5["Name"]}:{indi5["Birthday"]}:{indi5["Death"]} - Birth date not before death date.']