import pytest
from datetime import datetime, timedelta
from ProjectAgile import us38, parse_gedcom_file

# Helper function to create a mock individual
def create_individual(id, birth_date, name="NA", death_date="NA" ):
    return {
        "ID": id,
        "Name": name,
        "Gender": "NA",
        "Birthday": birth_date,
        "Death": death_date,
        "Child": "NA",
        "Spouse": ["NA"]
    }

def test_1_us38():
    # Test case 1: Individual with birth date not in the next 30 days
    indi1 = create_individual("I01", "1 JAN 1900")
    assert us38([indi1]) == []

def test_2_us38():
    # Test case 2: Indidvidual with birth date exactly today
    today = datetime.today().strftime("%d %b %Y")
    indi2 = create_individual("I02", today, "Sam")
    assert us38([indi2]) == [f'INDIVIDUAL: US38: ID: I02 Name Sam Birthday {today}']

def test_3_us38():
    # Test case 3: Indidvidual with birth date in next 30days
    next_date = (datetime.today() + timedelta(days=15)).strftime("%d %b %Y")
    # print(past_date)
    indi3 = create_individual("I03", next_date, "Dan")
    assert us38([indi3]) == [f'INDIVIDUAL: US38: ID: I03 Name Dan Birthday {next_date}']

def test_4_us38():
    # Test case : Indidvidual with birth date in next 30days but is not alive
    next_date = (datetime.today() + timedelta(days=15)).strftime("%d %b %Y")
    # print(past_date)
    indi3 = create_individual("I03", next_date, "Dan", "20 JAN 1990" )
    assert us38([indi3]) == []

def test_5_us38():
    # Test case: Check if expected 1 output come out of navya.ged for US38
    individuals, _ = parse_gedcom_file("navya.ged")
    errors = us38(individuals)
    print(errors)
    expected_num_errors = 1
    assert len(errors) == expected_num_errors

if __name__ == "__main__":
    pytest.main()