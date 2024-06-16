## List all living married individuals
def us30(individuals, families):
    living_individuals = []
    living_married_individuals = []
    errors = []
    print("\nAll living married individuals:")

    for fam in families:
        married = fam["Married"] != "NA"
        for indi in individuals:
            alive = indi["Death"] != "NA" 
            if alive and married:
                living_married_individuals.append(indi["Name"])
            else:
                errors.append(f'ERROR: INDIVIDUAL: US30: {indi["Name"]}: Not living and married.')
        return errors
