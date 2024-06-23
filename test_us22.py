import pytest
from ProjectAgile import us22

individuals = [{'ID': 'I01', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, {'ID': 'I02', 'Name': 'Jane /Jones/', 'Gender': 'F', 'Birthday': '10 APR 1810', 'Death': '25 JUN 1890', 'Child': 'NA', 'Spouse': ['F01']}, {'ID': 'I02', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']}, ]
families = [{'ID': 'F01', 'Married': '15 JUL 1850', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Sam /Smith/', 'Wife': 'I02', 'WifeName': 'Jimmy /Smith/', 'Children': ['I03', 'I04', 'I05']}, {'ID': 'F01', 'Married': '15 JUL 1850', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Sam /Smith/', 'Wife': 'I02', 'WifeName': 'Jimmy /Smith/', 'Children': ['I03', 'I04', 'I05']}]

def test_1_us22(): # Dupliate in individuals, duplicate in families
    assert len(us22(individuals, families)) == 2

def test_2_us22(): # same as above, checking exact return value
    assert us22(individuals, families) == ['Duplicate individual ID, I02, for Jimmy /Smith/', 'Duplicate family ID, F01, with marriage date 15 JUL 1850']
    
def test_3_us22():
    # 2 duplicate IDs in individuals, 1 duplicate ID in families
    individuals2 = individuals
    individuals2.append({'ID': 'I02', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']})
    assert len(us22(individuals2, families)) == 3

def test_4_us22():
    # 2 duplicate IDs in individuals, 0 in families
    individuals2 = individuals
    families.pop()
    assert len(us22(individuals2, families)) == 2