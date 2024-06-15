def us30(individuals,families):
    # living_individuals = []
    # living_married_individuals = []
    errors = []
    print("\nAll living married individuals:")
    for fam in families:

        husband_id = fam["HusbandName"]
        for husband_id in fam["HusbandName"]:
            for indi in individuals:
                if indi["Name"] == husband_id:
                    errors.append(f'ERROR: INDIVIDUAL: US30: {indi["ID"]}: Not living and married.')
    return errors
