import pytest
from datetime import datetime
from ProjectAgile import us30, us31, parse_gedcom_file
##import static org.junit.Assert.assertTrue

# Helper function to create a mock individual
def create_individual(id, birth_date = "NA", death_date = "NA", spouse = ["NA"], line="NA"):
    return {
        "ID": id,
        "Name": "Test Name",
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": spouse,
        "line": line
    }

def test_1():
    # Test case 1: Living Individual who is single and above 30
    indi1 = create_individual("I01", "01 JAN 1950", "NA", ["F01"], 1)
    assert us31([indi1]) == [f'Line {indi1["line"]} - US31: INDIVIDUAL: {indi1["ID"]}: Is not alive or single above 30.']

def test_2():
    # Test case 2: Living Individual who is single and above 30
    indi2 = create_individual("I04", "12 OCT 2000", "NA", ["NA"], 2)
    assert us31([indi2]) == [f'Line {indi2["line"]} - US31: INDIVIDUAL: {indi2["ID"]}: Is not alive or single above 30.']

def test_3():
    # Test case 2: Living Individual who is single and above 30
    indi3 = create_individual("I05", "5 NOV 1980", "15 OCT 1998", ["NA"], 3)
    assert us31([indi3]) == [f'Line {indi3["line"]} - US31: INDIVIDUAL: {indi3["ID"]}: Is not alive or single above 30.']

def test_4():
    # Test case 2: Living Individual who is single and above 30
    birthToday = datetime.today().strftime("%d %b %Y")
    indi4 = create_individual("I05", birthToday, "NA", ["NA"], 4)
    assert us31([indi4]) == [f'Line {indi4["line"]} - US31: INDIVIDUAL: {indi4["ID"]}: Is not alive or single above 30.']

def test_5():
    # Test case 2: Living Individual who is single and above 30
    birthToday = datetime.today().strftime("%d %b %Y")
    indi5 = create_individual("I08", birthToday, "NA", ["F02"], 5)
    assert us31([indi5]) == [f'Line {indi5["line"]} - US31: INDIVIDUAL: {indi5["ID"]}: Is not alive or single above 30.']


if __name__ == "__main__":
    pytest.main()

