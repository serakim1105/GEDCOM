import pytest
from Pro3_2 import us29, parse_gedcom_line, parse_gedcom_file
#import Pro3_2
from datetime import datetime

# def test_answer():
#     assert Pro3_2.func(3) == 5#, "should have been 4"


# Helper function to create a mock individual
def create_indi(id, name, death_date="NA"):
    return {
        "ID": id,
        "Name": name,
        "Death": death_date,
    }

def test_us29(): #this does not work as us29_test()
    indi01 = create_indi("I01", "Christine /Anthony/", "20 OCT 1942")
    assert us29([indi01]) == ["Christine /Anthony/"]

if __name__ == "__main__":
    pytest.main()