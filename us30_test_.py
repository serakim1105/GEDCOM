import pytest
from datetime import datetime
from Pro3_2 import us30, us31, parse_gedcom_file
import static org.junit.Assert.assertTrue

# Helper function to create a mock individual
def create_individual(id, death_date= "NA", spouse = ["NA"]):
    return {
        "ID": id,
        "Name": "Test Name",
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": ["NA"]
    }

def test_1():
    # Test case 1: Individual who is not alive and was married
    indi1 = create_individual("I03", "1 OCT 1996", "F02")
   assert us30([indi1]) == [f'ERROR: INDIVIDUAL: US30: I03: Not  living and married.']


def test_2():
    # Test case 2: Individual who is alive but not married
    indi1 = create_individual("I04", "NA", "NA")
   assert us30([indi2]) == [f'ERROR: INDIVIDUAL: US30: I04: Not living and married.']


def test_3():
    # Test case 2: Individual who is not alive and never married
    indi3 = create_individual("I05", "Nov 5 2000", "NA")
   assert us30([indi3]) == [f'ERROR: INDIVIDUAL: US30: I05: Not living and married.']

def test_4():
    # Test case 2: Individual who died today and not married
    deathToday = datetime.today().strftime("%d %b %Y")
    indi4 = create_individual("I10", deathToday)
    indi4 = create_individual("I10", {deathToday}, "NA")
   assert us30([indi4]) == [f'ERROR: INDIVIDUAL: US30: I10: Not living and married.']

def test_5():
    # Test case 2: Individual who is not alive but had multiple spouses
    
    indi4 = create_individual("I04", "NA", "[F03,F04]")
   assert us30([indi5]) == [f'ERROR: INDIVIDUAL: US30: I12: Not living and married.']

if __name__ == "__main__":
    pytest.main()
