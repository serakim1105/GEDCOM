import pytest
from Pro3_2 import us02, parse_gedcom_line, parse_gedcom_file
#import Pro3_2
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
    {'ID': 'F01', 'Married': '1 MAR 1970', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Justin /Lee/', 'Wife': 'I02', 'WifeName': 'Anna /Lee/', 'Children': ['I05']},
    {'ID': 'F02', 'Married': '1 AUG 1995', 'Divorced': 'NA', 'Husband': 'I05', 'HusbandName': 'Cody /Lee/', 'Wife': 'I03', 'WifeName': 'Hannah /Lee/', 'Children': ['I06']},
    {'ID': 'F03', 'Married': '1 DEC 1999', 'Divorced': 'NA', 'Husband': 'I05', 'HusbandName': 'Cody /Lee/', 'Wife': 'I04', 'WifeName': 'Judy /Lee/', 'Children': ['I07']}
]

def test_1_us02(): 
    assert us02(individuals, families) == [] #should pass
    

def test_2_us02(): # change marriage date prior to husband/wifes DOB
    families[0]["Married"] = '1 MAR 1949'
    assert us02(individuals, families) == ['ERROR: US02: Justin /Lee/ married after his birthday.', 'ERROR: US02: Anna /Lee/ married after her birthday.'] #should pass

if __name__ == "__main__":
    pytest.main()