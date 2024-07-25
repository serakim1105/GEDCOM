import pytest
from datetime import datetime
from ProjectAgile import us30, us31, parse_gedcom_file
##import static org.junit.Assert.assertTrue

# Helper function to create a mock individual
def create_individual(id, death_date = "NA", spouse = ["NA"], line="NA", ):
    return {
        "line": line,
        "ID": id,
        "Name": "Test Name",
        "Gender": "NA",
        "Birth": "NA",
        "Death": death_date,
        "Child": "NA",
        "Spouse": spouse
    }

def test_1():
    # Test case 1: Individual who is not alive and was married
    indi1 = create_individual("I03", "1 OCT 1996", ["F02"], 1)
    assert us30([indi1]) == [f'Line 1 - Individual I03: Not living and married.']

def test_2():
    # Test case 2: Individual who is alive but not married
    indi2 = create_individual("I04", "NA", ["NA"], 2)
    assert us30([indi2]) == [f'Line 2 - Individual I04: Not living and married.']

def test_3():
    # Test case 2: Individual who is not alive and never married
    indi3 = create_individual("I05", "Nov 5 2000", ["NA"], 3)
    assert us30([indi3]) == [f'Line 3 - Individual I05: Not living and married.']

def test_4():
    # Test case 2: Individual who died today and not married
    deathToday = datetime.today().strftime("%d %b %Y")
    indi4 = create_individual("I10", deathToday, "NA", 4)
    indi4 = create_individual("I10", {deathToday}, ["NA"], 5)
    assert us30([indi4]) == [f'Line 5 - Individual I10: Not living and married.']


def test_5():
    # Test case 2: Living Individual who is alive but not married
    indi5 = create_individual("I08", "NA", ["NA"], 6)
    assert us30([indi5]) == [f'Line 6 - Individual I08: Not living and married.']


if __name__ == "__main__":
    pytest.main()
