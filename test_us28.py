import pytest
from ProjectAgile import us28, parse_gedcom_file
from datetime import datetime

# Helper function to create a mock individual
def create_indi(id, name, age, child):
    return {
        "ID": id,
        "Name": name,
        "Age": age, 
        "Child": child
    }
families = [
    {'ID': 'F01', 'Married': '1 MAR 1980', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Chris /Anthony/', 'Wife': 'I02', 'WifeName': 'Sriya /Bhamidipati/', 'Children': ['I03', 'I04']}
]

families2 = [
    {'ID': 'F02', 'Married': '1 MAR 1995', 'Divorced': 'NA', 'Husband': 'I10', 'HusbandName': 'C /W/', 'Wife': 'I09', 'WifeName': 'S /B/', 'Children': ['I06', 'I07']}
]

families3 = [
    {'ID': 'F03', 'Married': '1 MAR 2017', 'Divorced': 'NA', 'Husband': 'I07', 'HusbandName': 'D /B/', 'Wife': 'I08', 'WifeName': 'R /B/', 'Children': ['I11']}
]

def test_1_us28(): 
    indi3 = create_indi("F01", "Taylor /Smith/", "18", "I03") #siblings
    assert us28([indi3], families)

def test_2_us28():
    indi4 = create_indi("F01", "Kristina /Smith/", "20", "I04") #siblings
    assert us28([indi4], families)

def test_3_us28(): 
    indi3 = create_indi("F02", "Alan /Wonderland/", "7", "I06") #siblings
    assert us28([indi3], families)

def test_4_us28():
    indi4 = create_indi("F02", "Alice /Wonderland/", "8", "I07") #siblings
    assert us28([indi4], families)

def test_5_us28():
    indi5 = create_indi("F03", "Alice /Wonderland/", "8", "I07") #siblings
    assert us28([indi5], families)


def test_5_us28():
    indi5 = create_indi("F03", "Kyle /Vannier/", "8", "I11") #siblings
    assert us28([indi5], families)

# def test_3_us28(): 
#     assert us28([indi3],families) == [f'ERROR: INDIVIDUAL: US28: {indi3["ID"]}: Not a sibling or not yet born.']


# def test_4_us28():
#     assert us28([indi1],families) == [f'ERROR: INDIVIDUAL: US28: {indi2["ID"]}: Not a sibling or not yet born.']

# def test_5_us28():
#     assert us28([indi1],families) == [f'ERROR: INDIVIDUAL: US28: {indi2["ID"]}: Not a sibling or not yet born.']

if __name__ == "__main__":
    pytest.main()