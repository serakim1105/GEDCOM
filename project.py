import sys

valid_tags = ["INDI", "NAME", "SEX", "BIRT", "DEAT", "FAMC", "FAMS", "FAM", "MARR", "HUSB", "WIFE", "CHIL", "DIV", "DATE", "HEAD", "TRLR", "NOTE"]

is_valid = "F"
    
def print_result(level, tag, is_valid, args):
    print(f"<-- {level}|{tag}|{is_valid}|{args}")

    
####
def main():
    filename = sys.orig_argv[2]
    file = open(filename, 'r')
    lines = file.readlines()

    for line in lines:
        print("--> " + line)#.strip()) #remove return char for easier reading
        
        tokens = line.split()
        if len(tokens) < 3:
            tokens.append("") # avoid TypeError & Overflow

        level = tokens[0]
        if tokens[1] in valid_tags:
            tag = tokens[1]
            args = ' '.join(tokens[2:])
            is_valid = "T"
            print_result(level, tag, is_valid, args + "\n")
        elif tokens[2] in valid_tags:
            tag = tokens[2]
            args = ''.join(tokens[1])
            is_valid = "T"
            print_result(level, tag, is_valid, args + "\n")
        else:
            tag = tokens[1]
            args = ' '.join(tokens[2:])
            is_valid = "F"
            print_result(level, tag, is_valid, args + "\n")
           
    

if __name__=="__main__":
    main()