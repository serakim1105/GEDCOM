import pytest
from datetime import datetime
from ProjectAgile import us30, us31, parse_gedcom_file

# Helper function to create a mock individual
def create_individual(id, name = "NA", birth_date = "NA", death_date = "NA", spouse = ["NA"]):
    return {
        "ID": id,
        "Name": name,
        "Birth": birth_date,
        "Death": death_date,
        "Spouse": spouse
    }

def test_1():
    # Test case 1: Individual who is not alive and was married
    indi1 = create_individual("I03", "Justin /Lee/" ,"1 OCT 1996", "NA", ["F01"])
    assert us30([indi1])

def test_2():
    # Test case 2: Individual who is alive but not married
    indi2 = create_individual("I04", "Sarah /Lee/", "12 DEC 2015", "NA", ["F02"])
    assert us30([indi2])

def test_3():
    # Test case 2: Individual who is not alive and never married
    indi3 = create_individual("I05", "Christine /Lee/", "5 NOV 2000", "NA", ["F03"])
    assert us30([indi3])
    
def test_4():
    # Test case 2: Individual who died today and not married
    indi4 = create_individual("I10", "Megan /Lee/", "12 DEC 2013", "NA", ["F04"])
    assert us30([indi4])


def test_5():
    # Test case 2: Living Individual who is alive but not married
    indi5 = create_individual("I08", "Lee /Lee/" ,"15 SEP 2020", "NA", ["F05"])
    assert us30([indi5])


if __name__ == "__main__":
    pytest.main()