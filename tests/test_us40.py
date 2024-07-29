import pytest
from ProjectAgile import us22, parse_gedcom_file

# Testing List line numbers from GEDCOM source file when reporting errors, 
# using us22 output with sample data
individuals = [
    {'line': 1, 'ID': 'I01', 'Name': 'Sam /Smith/', 'Gender': 'M', 'Birthday': '15 MAR 1851', 'Death': '20 DEC 1880', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 2, 'ID': 'I02', 'Name': 'Jane /Jones/', 'Gender': 'F', 'Birthday': '10 APR 1810', 'Death': '25 JUN 1890', 'Child': 'NA', 'Spouse': ['F01']}, 
    {'line': 3, 'ID': 'I02', 'Name': 'Jimmy /Smith/', 'Gender': 'M', 'Birthday': '20 AUG 1830', 'Death': '30 NOV 1910', 'Child': 'F01', 'Spouse': ['NA']}, 
    ]
families = [
    {'line': 5, 'ID': 'F01', 'Married': '15 JUL 1850', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Sam /Smith/', 'Wife': 'I02', 'WifeName': 'Jimmy /Smith/', 'Children': ['I03', 'I04', 'I05']}, 
    {'line': 6, 'ID': 'F01', 'Married': '15 JUL 1850', 'Divorced': 'NA', 'Husband': 'I01', 'HusbandName': 'Sam /Smith/', 'Wife': 'I02', 'WifeName': 'Jimmy /Smith/', 'Children': ['I03', 'I04', 'I05']}]


def test_1_us22(): 
    assert us22(individuals, families) == ['Line 3 - Duplicate individual ID, I02, for Jimmy /Smith/', 'Line 6 - Duplicate family ID, F01, with marriage date 15 JUL 1850']
    
# Testing List line numbers from GEDCOM source file when reporting errors, 
# using us22 output with actual data
def print_errors(us_result, us_num, errs_or_anoms = 'Errors'):
        if us_result:
            print(f"\n__{us_num} {errs_or_anoms}__")

            for r in us_result:
                print(r)
        else:
            print(f"\n__No {errs_or_anoms} in {us_num}__.")

def test_2_us22():
    ind, fam = parse_gedcom_file('messed_up_fam.ged')
    errors_us22 = us22(ind, fam)
    print_errors(errors_us22, 'US22')
    assert us22(ind, fam).index("Line 190 - Duplicate individual ID, I15, for Rajesh /Pai/") == 1