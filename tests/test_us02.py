import pytest
from ProjectAgile import us02_err, parse_gedcom_file
from datetime import datetime

# Sample data from sera.ged
individuals = [
    {'ID': 'I01', 'Name': 'Justin /Lee/', 'Gender': 'M', 'Birthday': '1 JAN 1950', 'Death': 'NA', 'Child': 'NA', 'Spouse': ['F01']},
    {'ID': 'I02', 'Name': 'Anna /Lee/', 'Gender': 'F', 'Birthday': '2 FEB 1951', 'Death': 'NA', 'Child': 'NA', 'Spouse': ['F01']},
    {'ID': 'I03', 'Name': 'Hannah /Lee/', 'Gender': 'F', 'Birthday': '1 MAY 1972', 'Death': '1 OCT 1996', 'Child': 'NA', 'Spouse': ['F02']},
    {'ID': 'I04', 'Name': 'Judy /Lee/', 'Gender': 'F', 'Birthday': '1 JUN 1972', 'Death': 'NA', 'Child': 'NA', 'Spouse': ['F03']},
    {'ID': 'I05', 'Name': 'Cody /Lee/', 'Gender': 'M', 'Birthday': '1 APR 1971', 'Death': 'NA', 'Child': 'F01', 'Spouse': ['F02', 'F03']},
    {'ID': 'I06', 'Name': 'Eva /Lee/', 'Gender': 'F', 'Birthday': '1 SEP 1996', 'Death': 'NA', 'Child': 'F02', 'Spouse': ['NA']},
    {'ID': 'I07', 'Name': 'Lincoln /Lee/', 'Gender': 'M', 'Birthday': '1 NOV 2001', 'Death': 'NA', 'Child': 'F03', 'Spouse': ['NA']}
]

families = [
    {'line': 1, 'ID': 'F01', 'Married': '1 MAR 1970', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Justin /Lee/', 'Wife': 'I02', 'WifeName': 'Anna /Lee/', 'Children': ['I05']},
    {'line': 2, 'ID': 'F02', 'Married': '1 AUG 1995', 'Divorced': 'NA', 'Husband': 'I05', 'HusbandName': 'Cody /Lee/', 'Wife': 'I03', 'WifeName': 'Hannah /Lee/', 'Children': ['I06']},
    {'line': 3, 'ID': 'F03', 'Married': '1 DEC 1999', 'Divorced': 'NA', 'Husband': 'I05', 'HusbandName': 'Cody /Lee/', 'Wife': 'I04', 'WifeName': 'Judy /Lee/', 'Children': ['I07']}, 
    {'line': 4, 'ID': 'F04', 'Married': '1 JAN 2024', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Justin /Lee/', 'Wife': 'I04', 'WifeName': 'Judy /Lee/'}
]
# test output of sample data
def test_1_us02(): 
    assert us02_err(individuals, families) == []
    
# test for both husband and wife being born after marriage
def test_2_us02(): 
    families_tmp = families
    families_tmp[0]["Married"] = '1 MAR 1949'
    assert us02_err(individuals, families_tmp) == ['Line 1 - F01: Justin /Lee/ married before his birthday.', 'Line 1 - F01: Anna /Lee/ married before her birthday.'], "Expected Justin and Anna both married before birthdays"

# test for empty .ged
def test_3_us02():
    result = us02_err([],[])
    assert len(result) == 0, "Expected no output"

# test more than one marriage before birthday
def test_4_us02():
    families_tmp2 = families
    families_tmp2[3]["Married"] = '1 MAR 1550'
    result = us02_err(individuals, families_tmp2)
    assert len(result) == 4, "Expected 4 results: F01 Justin, F01 Anna, F04 Justin, F04 Judy"

# test some marriages before birthday
# def test_5_us02():
#     individuals, families_tmp5 = parse_gedcom_file("messed_up_fam.ged")
#     families_tmp5[2]['Married'] = '1 MAR 1909'
#     result = us02_err(individuals, families_tmp5)
#     assert len(result) == 2, "Expected 2 results: F01 Sam Smith (from test_01_us02) born 1851, F03 Lyna Lester born 1910"

# tests for no marriages
def test_6_us02(): 
    result = us02_err(individuals, [])
    assert len(result) == 0, "Expected no marriages before birthday"

# test 
# def test_7_us02():
#     individuals, families = parse_gedcom_file("messed_up_fam.ged")
#     errors = us02_err(individuals, families)
#     print(errors)
#     assert len(errors) == 1


if __name__ == "__main__":
    pytest.main()