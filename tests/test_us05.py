import pytest
from ProjectAgile import us05, parse_gedcom_file
from datetime import datetime

def create_date(wedding_date = "NA", husband_name = "NA", husband_death_date = "NA", wife_name = "NA", wife_death_date = "NA"):
    return [   
    [
        {'Married': wedding_date,
        'HusbandName': husband_name,
        'WifeName': wife_name}
    ],
    
        [
            {'Name': husband_name,
            'Death': husband_death_date},
             
            {'Name': wife_name,
            'Death': wife_death_date}
        ] 
    ]

fam_indi = create_date()

def test_1_us05(): 
    fam_indi = create_date("20 OCT 2050", "Justin /Lee/", "1 JAN 2015", "Anna /Lee/", "23 OCT 2018")
    fam1 = fam_indi[0]
    indi1 = fam_indi[1]
    assert us05(indi1, fam1) == [f'Error: US05: Marriage date not listed before either spouse death.']
    
def test_2_us05(): 
    fam2, indi2 = create_date("20 OCT 1942", "Cameron /Lee/", "1 FEB 1930", "Sarah /Lee", "20 OCT 1920")
    assert us05(indi2, fam2) == [f'Error: US05: Marriage date not listed before either spouse death.']
    
def test_3_us05(): 
    fam3, indi3 = create_date("20 NOV 2300", "Andrew /Lee/", "21 JAN 2030", "Hannah /Lee/", "12 APR 2014")
    assert us05(indi3,fam3) == [f'Error: US05: Marriage date not listed before either spouse death.']
    
def test_4_us05(): 
    fam4, indi4 = create_date("20 JUN 2100", "Cody /Lee/", "1 JAN 2010", "Kim /Lee/", "1 APR 2024")
    assert us05(indi4, fam4) == [f'Error: US05: Marriage date not listed before either spouse death.']
    
def test_5_us05(): 
    fam5, indi5 = create_date("20 OCT 2030", "Eva /Lee/", "1 JAN 2015", "Evan /Lee/", "1 JAN 2200")
    assert us05(indi5, fam5) == [f'Error: US05: Marriage date not listed before either spouse death.']
