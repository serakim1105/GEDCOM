import pytest
from ProjectAgile import us25

individuals = [
    {'line': 1, 'ID': 'I01', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 2, 'ID': 'I05', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 3, 'ID': 'I02', 'Name': 'Jane /Jones/', 'Gender': 'F', 'Birthday': '10 APR 1810', 'Death': '25 JUN 1890', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 4, 'ID': 'I03', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']}, 
    {'line': 5, 'ID': 'I04', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']},
    ]

families = [
    {'line': 6, 'ID': 'F01', 'Married': '1 MAR 1970', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Justin /Lee/', 'Wife': 'I02', 'WifeName': 'Anna /Lee/', 'Children': ['I01','I05']},
    {'line': 7, 'ID': 'F02', 'Married': '1 AUG 1995', 'Divorced': 'NA', 'Husband': 'I05', 'HusbandName': 'Cody /Lee/', 'Wife': 'I03', 'WifeName': 'Hannah /Lee/', 'Children': ['I02','I03','I04']},
    ]




def test_1_us25(): # 2 children with same first name and dob (1 duplicate in each fam)
    assert len(us25(individuals, families)) == 2

def test_2_us25(): # 1 dup individuals
    individuals.pop()
    assert len(us25(individuals, families)) == 1

