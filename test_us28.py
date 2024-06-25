import pytest
from ProjectAgile import us28, parse_gedcom_file
from datetime import datetime

# Helper function to create a mock individual
def create_individual(id, name, birth_date = "NA"):
    return {
        "ID": id,
        "Name": name,
        "Birthday": birth_date
    }

individuals = []
individuals.append(indi01)
individuals.append(indi02)
individuals.append(indi03)
individuals.append(indi04)
individuals.append(indi05)

def test_1_us28(): 
    indi1 = create_indi("I01", "Christine /Anthony/", "20 OCT 1942") #siblings
    assert us28([indi1]) == [f'ERROR: INDIVIDUAL: US28: {indi1["ID"]}: Not a sibling or not yet born.']


def test_2_us28():
    indi2 = create_indi("I02", "Sarah /Paul/", "18 OCT 1930") #siblings
    assert us28([indi2]) == [f'ERROR: INDIVIDUAL: US28: {indi2["ID"]}: Not a sibling or not yet born.']

def test_3_us28(): 
    indi3 = create_indi("I03", "Taylor /Smith/", "18 DEC 1989") #siblings
    assert us28([indi3]) == [f'ERROR: INDIVIDUAL: US28: {indi3["ID"]}: Not a sibling or not yet born.']


def test_4_us28():
    indi4 = create_indi("I04", "Kristina /Anthony/", "20 OCT 1950") #siblings
    assert us28([indi1]) == [f'ERROR: INDIVIDUAL: US28: {indi2["ID"]}: Not a sibling or not yet born.']

def test_5_us28():
    indi5 = create_indi("I05", "Navya /Pai/", "NA") #not born
    assert us28([indi1]) == [f'ERROR: INDIVIDUAL: US28: {indi2["ID"]}: Not a sibling or not yet born.']

if __name__ == "__main__":
    pytest.main()