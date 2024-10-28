import re


def cut_one_line_tokens(line):
    output = []
    op = re.compile(r"[=+>*]")  # Operator regex formula
    key = re.compile(r"(if|else|int|float)\b")  # Keyword regex formula
    sep = re.compile(r'[():";]')  # Separator regex formula
    str_lit = re.compile(
        r'"'
    )  # String_Literal regex formula (i know it looks wrong, just trust)
    iden = re.compile(r"([A-Za-z])([A-Za-z0-9]+)?")  # Identifier regex formula
    flo = re.compile(
        r"(?<![\d.A-Za-z])-?[0-9]+?\.[0-9]+\b(?![\d.A-Za-z])"
    )  # Float_literal regex formula
    int_lit = re.compile(
        r"(?<![\d.A-Za-z])-?\d+\b(?![\d.A-Za-z])"
    )  # Int_Literal regex formula

    while True:
        if line == "":
            break
        if op.match(line):  # check for operators
            lex = op.match(line)
            tup = "<Operator," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif key.match(line):  # check for Identifiers
            lex = key.match(line)
            tup = (
                "<Keyword," + lex.group(0) + ">"
            )  # [match object].group(0) is the actual thing the regex formula found in its entirety
            output.append(tup)
            line = line[lex.end() :]

        elif sep.match(line):  # check for separators
            lex = sep.match(line)
            tup = "<Separator," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]
            if lex.group(0) == '"':
                if str_lit.search(
                    line
                ):  # if a " separator is found, look for another " and all characters inbetween are a String_Literal
                    relex = str_lit.search(line)
                    retup = "<String_Literal," + line[: relex.start()] + ">"
                    output.append(retup)
                    reretup = "<Separator," + relex.group(0) + ">"
                    output.append(reretup)
                    line = line[relex.end() :]

        elif iden.match(line):  # check for Identifier
            lex = iden.match(line)
            tup = "<Identifier," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif flo.match(line):  # check for Float_Literal
            lex = flo.match(line)
            tup = "<Float_Literal," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif int_lit.match(line):  # look for Int_Literal
            lex = int_lit.match(line)
            tup = "<Int_Literal," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        else:
            line = line[1:]

    return output


if __name__ == "__main__":
    inputs = [
        "int  A1=5",
        "float BBB2     =1034.2",
        "float     cresult     =     A1     +BBB2     *      BBB2",
        'print("TinyPie")',
    ]

    for x in inputs:
        print("Test Input String: " + x)
        out = cut_one_line_tokens(x)
        print("Output <Type,Token> list: ", end="")
        print(out)
