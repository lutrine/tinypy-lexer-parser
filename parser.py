# TODO: implement the parser
# BNF:
# exp -> if_exp | print_exp | math_exp

# math_exp -> float Identifier = math;
# math -> multi + multi
# multi -> Int_Literal*multi | Float_Literal

# if_exp -> if ( comparison_exp ) :
# comparison_exp -> identifier > identifier

# print_exp -> print ( " String_Literal " );

# tokenlist = [("Keyword", "float"), ("Identifier", "var2"), ("Operator", "="), ("Int_Literal", "2"), ("Operator", "*"), ("Float_Literal", "1.1"),
#              ("Operator", "+"), ("Int_Literal", "4"), ("Operator", "*"), ("Int_Literal", "3"), ("Operator", "*"),
#              ("Float_Literal", "2.3"), ("Seperator", ";")]
tokenlist = []
intoken = [("empty", "empty")]


def accept_token():
    global intoken
    print("      accept token from the list: " + intoken[1])
    intoken = tokenlist.pop(0)


def math():
    print("\tParent node math, finding child nodes")
    global intoken
    multi()
    accept_token()
    if intoken[1] == "+":
        print("child node (token):" + intoken[1])
        accept_token()
        multi()
    else:
        print("math expects a '+' after a multi")


def multi():
    print("\tParent node multi, finding child nodes")
    global intoken
    if intoken[0] == "Int_Literal":
        print("child node (internal): Int_Literal")
        print("   int_literal has child node (token):" + intoken[1])
        accept_token()
        if intoken[1] == "*":
            print("child node (token):" + intoken[1])
            accept_token()

            print("child node (internal): multi")
            multi()
        else:
            print("multi expects a '*' after an int_literal")
    elif intoken[0] == "Float_Literal":
        print("child node (internal): Float_Literal")
        print("   float_literal has child node (token):" + intoken[1])
    else:
        print("multi expects a int or a float")


def math_exp():
    print("\n----parent node math_exp, finding children nodes:")
    global intoken
    typeT, token = intoken
    if typeT == "Keyword":
        print("child node (internal): Keyword")
        print("   type has child node (token):" + token)
        accept_token()
    else:
        print("expect Keyword as the first element of the math_expression!\n")
        return

    if intoken[0] == "Identifier":
        print("child node (internal): Identifier")
        print("   Identifier has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect Identifier as the second element of the math_expression!")
        return

    if intoken[1] == "=":
        print("child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect = as the third element of the math_expression!")
        return

    print("Child node (internal): math")
    math()

def if_exp():
    print("\n----parent node math_exp, finding children nodes:")
    global intoken
    typeT, token = intoken

    if typeT == "Keyword":
        print("child node (internal): Keyword")
        print("   keyword has child node (token):" + token)
        accept_token()
    else:
        print("expect Keyword as the first element of the if_expression!\n")
        return

    if intoken[1] == "(":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect ( as the second element of the if_expression!")
        return

    print("Child node (internal): comparison_exp")
    comparison_exp()
    accept_token()

    if intoken[1] == ")":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
    else:
        print("expect ) as the fourth element of the if_expression!")
        return

def comparison_exp():
    print("\n----parent node math_exp, finding children nodes:")
    global intoken
    typeT, token = intoken

    if typeT == "Identifier":
        print("child node (internal): Identifier")
        print("   identifier has child node (token):" + token)
        accept_token()
    else:
        print("expect Identifier as the first element of the comparison_expression!\n")
        return

    if intoken[1] == ">":
        print("child node (internal): Operator")
        print("   operator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect operator > as the second element of the comparison_expression!\n")
        return

    if typeT == "Identifier":
        print("child node (internal): Identifier")
        print("   identifier has child node (token):" + token)
        accept_token()
    else:
        print("expect Identifier as the third element of the comparison_expression!\n")
        return

def print_exp():
    print("\n----parent node math_exp, finding children nodes:")
    global intoken
    typeT, token = intoken

    if typeT == "Identifier" and token == "print":
        print("child node (internal): Identifier")
        print("   keyword has child node (token):" + token)
        accept_token()
    else:
        print("expect Identifier print as the first element of the print_expression!\n")
        return

    if intoken[1] == "(":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect ( as the second element of the print_expression!")
        return

    if intoken[1] == "\"":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect \" as the third element of the print_expression!")
        return

    if intoken[0] == "String_Literal":
        print("child node (internal): String_Literal")
        print("   separator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect string_literal as the fourth element of the print_expression!")
        return

    if intoken[1] == "\"":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
        accept_token()
    else:
        print("expect \" as the fifth element of the print_expression!")
        return

    if intoken[1] == ")":
        print("child node (internal): Separator")
        print("   separator has child node (token):" + intoken[1])
    else:
        print("expect ) as the sixth element of the print_expression!")
        return

def exp():
    print("\n----parent node exp, finding children nodes:")
    global intoken
    typeT, token = intoken
    if typeT == "Keyword":
        print("child node (internal): Keyword")
        print("   keyword has child node (token):" + token)
        if token == "float":
            math_exp()
        elif token == "if":
            if_exp()
        else:
            print("expect float or if as the first keyword of the expression!")
            return
    elif typeT == "Identifier":
        if token == "print":
            print("child node (internal): Identifier")
            print("   identifier has child node (token):" + token)
            print_exp()
    else:
        print("Invalid Expression")
        return

def parser(tokens):
    global intoken
    global tokenlist
    tokenlist = tokens
    intoken = tokenlist.pop(0)
    exp()
    accept_token()
    if intoken[1] == ";" or intoken[1] == ":":
        print("\nparse tree building success!")
    return

def cleanup(tokens):
    return
