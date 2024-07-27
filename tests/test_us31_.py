import pytest
from datetime import datetime
from ProjectAgile import us30, us31, parse_gedcom_file


# Helper function to create a mock individual
def create_individual(id, birth_date = "NA", death_date = "NA", spouse = ["NA"]):
    return {
        "ID": id,
        "Name": "Test Name",
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": spouse
    }

def test_1():
    # Test case 1: Living Individual who is single and above 30
    indi1 = create_individual("I01", "01 JAN 1950", "NA", ["NA"])
    assert us31([indi1]) 

def test_2():
    # Test case 2: Living Individual who is single and above 30
    indi2 = create_individual("I04", "12 OCT 1900", "NA", ["NA"])
    assert us31([indi2])

def test_3():
    # Test case 2: Living Individual who is single and above 30
    indi3 = create_individual("I05", "5 NOV 1980", "NA", ["NA"])
    assert us31([indi3])

def test_4():
    # Test case 2: Living Individual who is single and above 30
    indi4 = create_individual("I05", "5 NOV 1980", "NA", ["NA"])
    assert us31([indi4])

def test_5():
    # Test case 2: Living Individual who is single and above 30
    indi5 = create_individual("I08", "5 NOV 1985", "NA", ["NA"])
    assert us31([indi5])


if __name__ == "__main__":
    pytest.main()