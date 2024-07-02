import pytest
from ProjectAgile import us12, parse_gedcom_file

def create_indi(id, name, birth_date, death_date='NA'):
    return {
        'ID': id,
        'Name': name,
        'Birthday': birth_date,
        'Death': death_date,
    }
indi01 = create_indi('I01', 'Chris /Anthony/', '1 JAN 1900')     #just too old 
indi02 = create_indi('I02', 'Sriya /Bhamidipati/', '1 JAN 1900')  #way too old 
indi03 = create_indi('I03', 'Sera /Kim/', '1 JAN 1981')           #child

indi04 = create_indi('I04', 'C /A/', '1 JAN 1900', '1 JAN 1982')     #just too old at child's birth, then dies
indi05 = create_indi('I05', 'S /B/', '1 JAN 1900')        #way too old 
indi06 = create_indi('I06', 'S /K/', '1 JAN 1981')        #child

indi07 = create_indi('I07', 'C /A/', '1 JAN 1950')     #not too old
indi08 = create_indi('I08', 'S /B/', '1 JAN 1950')        #not too old 
indi09 = create_indi('I09', 'S /K/', '1 JAN 1981')        #child

individuals = []
individuals.append(indi01)
individuals.append(indi02)
individuals.append(indi03)

individuals2 = []
individuals2.append(indi04)
individuals2.append(indi05)
individuals2.append(indi06)

individuals3 = []
individuals3.append(indi04)
individuals3.append(indi05)
individuals3.append(indi06)

families = [
    {'ID': 'F01', 'Married': '1 MAR 1980', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Chris /Anthony/', 'Wife': 'I02', 'WifeName': 'Sriya /Bhamidipati/', 'Children': ['I03']}
]
families2 = [
    {'ID': 'F02', 'Married': '1 MAR 1980', 'Divorced': 'NA', 'Husband': 'I04', 'HusbandName': 'C /A/', 'Wife': 'I05', 'WifeName': 'S /B/', 'Children': ['I06']}
    ]
families3 = [
    {'ID': 'F03', 'Married': '1 MAR 1980', 'Divorced': 'NA', 'Husband': 'I07', 'HusbandName': 'C /A/', 'Wife': 'I08', 'WifeName': 'S /B/', 'Children': ['I09']}
    ]



def test_1_us12(): # both parents too old --> test passes by year (age) but not by day
    assert len(us12(individuals, families)) == 2

def test2_us12(): # father too old, mother not too old
    indi02['Birthday'] = '1 JAN 1930'
    assert len(us12(individuals, families)) == 1

def test3_us12(): # both parents too old & check with not living
    assert len(us12(individuals2, families2)) == 2

def test4_us12(): # both parents not too old
    assert len(us12(individuals3, families3)) == 0