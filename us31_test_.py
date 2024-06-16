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
    indi1 = create_individual()
   assert us31([indi1]) == [f'ERROR: INDIVIDUAL: US31: I03: Is not alive and single over 30.']


def test_2():
    # Test case 2: Individual who is alive but not married
    indi1 = create_individual()
   assert us31([indi2]) == [f'ERROR: INDIVIDUAL: US31: I04: Is not alive and single over 30.']


def test_3():
    # Test case 2: Individual who is not alive and never married
    indi3 = create_individual()
   assert us31([indi3]) == [f'ERROR: INDIVIDUAL: US31: I05: Is not alive and single over 30.']

def test_4():
    # Test case 2: Individual who died today and not married
    deathToday = datetime.today().strftime("%d %b %Y")
    indi4 = create_individual()
    indi4 = create_individual()
   assert us31([indi4]) == [f'ERROR: INDIVIDUAL: US31: I10: Is not alive and single over 30.']

def test_5():
    # Test case 2: Individual who is not alive but had multiple spouses
    
    indi4 = create_individual("I04")
   assert us31([indi5]) == [f'ERROR: INDIVIDUAL: US31: I11: Is not alive and single over 30.']

if __name__ == "__main__":
    pytest.main()
