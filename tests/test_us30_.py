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
    assert us30([indi1]) == [f'Line {indi1["line"]} US30: INDIVIDUAL: {indi1["ID"]}: Not living and married.']

def test_2():
    # Test case 2: Individual who is alive but not married
    indi2 = create_individual("I04", "NA", ["NA"], 2)
    assert us30([indi2]) == [f'Line {indi2["line"]} US30: INDIVIDUAL: {indi2["ID"]}: Not living and married.']

def test_3():
    # Test case 2: Individual who is not alive and never married
    indi3 = create_individual("I05", "Nov 5 2000", ["NA"], 3)
    assert us30([indi3]) == [f'Line {indi3["line"]} US30: INDIVIDUAL: {indi3["ID"]}: Not living and married.']

def test_4():
    # Test case 2: Individual who died today and not married
    deathToday = datetime.today().strftime("%d %b %Y")
    indi4 = create_individual("I10", deathToday, "NA", 4)
    indi4 = create_individual("I10", {deathToday}, ["NA"], 5)
    assert us30([indi4]) == [f'Line {indi4["line"]} US30: INDIVIDUAL: {indi4["ID"]}: Not living and married.']


def test_5():
    # Test case 2: Living Individual who is alive but not married
    indi5 = create_individual("I08", "NA", ["NA"], 6)
    assert us30([indi5]) == [f'Line {indi5["line"]} US30: INDIVIDUAL: {indi5["ID"]}: Not living and married.']


if __name__ == "__main__":
    pytest.main()
