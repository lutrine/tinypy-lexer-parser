import re
import tkinter as tk
from tkinter import ttk

line_number = 0
code_lines = []
code = ""

tokenlist = []
intoken = [("empty", "empty")]

def cut_one_line_tokens(line):
    output = []
    op = re.compile(r"[=+>*]")  # Operator regex formula
    key = re.compile(r"(if|else|int|float)\b")  # Keyword regex formula
    sep = re.compile(r'[():";]')  # Separator regex formula
    str_lit = re.compile( r'"')  # String_Literal regex formula (i know it looks wrong, just trust)
    iden = re.compile(r"([A-Za-z])([A-Za-z0-9]+)?")  # Identifier regex formula
    flo = re.compile(r"(?<![\d.A-Za-z])-?[0-9]+?\.[0-9]+\b(?![\d.A-Za-z])")  # Float_literal regex formula
    int_lit = re.compile( r"(?<![\d.A-Za-z])-?\d+\b(?![\d.A-Za-z])")  # Int_Literal regex formula

    while True:
        if line == "":
            break
        if op.match(line):  # check for operators
            lex = op.match(line)
            tup = "<operator," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif key.match(line):  # check for Identifiers
            lex = key.match(line)
            tup = ("<keyword," + lex.group(0) + ">")  # [match object].group(0) is the actual thing the regex formula found in its entirety
            output.append(tup)
            line = line[lex.end() :]

        elif sep.match(line):  # check for separators
            lex = sep.match(line)
            tup = "<separator," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]
            if lex.group(0) == '"':
                if str_lit.search(line):  # if a " separator is found, look for another " and all characters inbetween are a String_Literal
                    relex = str_lit.search(line)
                    retup = "<string_literal," + line[: relex.start()] + ">"
                    output.append(retup)
                    reretup = "<separator," + relex.group(0) + ">"
                    output.append(reretup)
                    line = line[relex.end() :]

        elif iden.match(line):  # check for Identifier
            lex = iden.match(line)
            tup = "<identifier," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif flo.match(line):  # check for Float_Literal
            lex = flo.match(line)
            tup = "<float_literal," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        elif int_lit.match(line):  # look for Int_Literal
            lex = int_lit.match(line)
            tup = "<int_literal," + lex.group(0) + ">"
            output.append(tup)
            line = line[lex.end() :]

        else:
            line = line[1:]

    return output

def accept_token():
    global intoken
    tree_text.insert(tk.END, f"      accept token from the list: " + intoken[1] + "\n")
    intoken = tokenlist.pop(0)


def math():
    tree_text.insert(tk.END, f"\n\tParent node math, finding child nodes"+ "\n")
    global intoken
    multi()
    accept_token()
    if intoken[1] == "+":
        tree_text.insert(tk.END, f"child node (token):" + intoken[1]+ "\n")
        accept_token()
        multi()
    else:
        tree_text.insert(tk.END, f"math expects a '+' after a multi"+ "\n")


def multi():
    tree_text.insert(tk.END, f"\n\tParent node multi, finding child nodes"+ "\n")
    global intoken
    if intoken[0] == "int_literal":
        tree_text.insert(tk.END, f"child node (internal): int_literal"+ "\n")
        tree_text.insert(tk.END, f"   int_literal has child node (token):" + intoken[1]+ "\n")
        accept_token()
        if intoken[1] == "*":
            tree_text.insert(tk.END, f"child node (token):" + intoken[1]+ "\n")
            accept_token()

            tree_text.insert(tk.END, f"child node (internal): multi"+ "\n")
            multi()
        else:
            tree_text.insert(tk.END, f"multi expects a '*' after an int_literal"+ "\n")
    elif intoken[0] == "float_literal":
        tree_text.insert(tk.END, f"child node (internal): float_literal"+ "\n")
        tree_text.insert(tk.END, f"   float_literal has child node (token):" + intoken[1]+ "\n")
    else:
        tree_text.insert(tk.END, f"multi expects a int or a float"+ "\n")


def math_exp():
    tree_text.insert(tk.END, f"\n----parent node math_exp, finding children nodes:"+ "\n")
    global intoken
    typeT, token = intoken
    if typeT == "keyword":
        tree_text.insert(tk.END, f"child node (internal): keyword"+ "\n")
        tree_text.insert(tk.END, f"   type has child node (token):" + token+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect Keyword as the first element of the math_expression!\n")
        return

    if intoken[0] == "identifier":
        tree_text.insert(tk.END, f"child node (internal): identifier"+ "\n")
        tree_text.insert(tk.END, f"   identifier has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect identifier as the second element of the math_expression!"+ "\n")
        return

    if intoken[1] == "=":
        tree_text.insert(tk.END, f"child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect = as the third element of the math_expression!"+ "\n")
        return

    tree_text.insert(tk.END, f"Child node (internal): math"+ "\n")
    math()

def if_exp():
    tree_text.insert(tk.END, f"\n----parent node if_exp, finding children nodes:"+ "\n")
    global intoken
    typeT, token = intoken

    if typeT == "keyword":
        tree_text.insert(tk.END, f"child node (internal): keyword"+ "\n")
        tree_text.insert(tk.END, f"   keyword has child node (token):" + token+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect keyword as the first element of the if_expression!\n")
        return

    if intoken[1] == "(":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect ( as the second element of the if_expression!"+ "\n")
        return

    tree_text.insert(tk.END, f"Child node (internal): comparison_exp"+ "\n")
    comparison_exp()

    if intoken[1] == ")":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
    else:
        tree_text.insert(tk.END, f"expect ) as the fourth element of the if_expression!"+ "\n")
        return

def comparison_exp():
    tree_text.insert(tk.END, f"\n----parent node comparison_exp, finding children nodes:"+ "\n")
    global intoken
    typeT, token = intoken

    if typeT == "identifier":
        tree_text.insert(tk.END, f"child node (internal): identifier"+ "\n")
        tree_text.insert(tk.END, f"   identifier has child node (token):" + token+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect identifier as the first element of the comparison_expression!\n"+ "\n")
        return

    if intoken[1] == ">":
        tree_text.insert(tk.END, f"child node (internal): operator"+ "\n")
        tree_text.insert(tk.END, f"   operator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect operator > as the second element of the comparison_expression!\n"+ "\n")
        return

    if typeT == "identifier":
        tree_text.insert(tk.END, f"child node (internal): identifier"+ "\n")
        tree_text.insert(tk.END, f"   identifier has child node (token):" + token+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect Identifier as the third element of the comparison_expression!\n")
        return

def print_exp():
    tree_text.insert(tk.END, f"\n----parent node print_exp, finding children nodes:"+ "\n")
    global intoken
    typeT, token = intoken

    if typeT == "identifier" and token == "print":
        tree_text.insert(tk.END, f"child node (internal): identifier"+ "\n")
        tree_text.insert(tk.END, f"   keyword has child node (token):" + token+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect identifier print as the first element of the print_expression!\n")
        return

    if intoken[1] == "(":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect ( as the second element of the print_expression!"+ "\n")
        return

    if intoken[1] == "\"":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect \" as the third element of the print_expression!"+ "\n")
        return

    if intoken[0] == "string_literal":
        tree_text.insert(tk.END, f"child node (internal): string_literal"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect string_literal as the fourth element of the print_expression!"+ "\n")
        return

    if intoken[1] == "\"":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
        accept_token()
    else:
        tree_text.insert(tk.END, f"expect \" as the fifth element of the print_expression!"+ "\n")
        return

    if intoken[1] == ")":
        tree_text.insert(tk.END, f"child node (internal): separator"+ "\n")
        tree_text.insert(tk.END, f"   separator has child node (token):" + intoken[1]+ "\n")
    else:
        tree_text.insert(tk.END, f"expect ) as the sixth element of the print_expression!"+ "\n")
        return

def exp():
    tree_text.insert(tk.END, f"\n----parent node exp, finding children nodes:"+ "\n")
    global intoken
    typeT, token = intoken
    if typeT == "keyword":
        tree_text.insert(tk.END, f"child node (internal): keyword"+ "\n")
        tree_text.insert(tk.END, f"   keyword has child node (token):" + token+ "\n")
        if intoken[1] == "float":
            math_exp()
        elif intoken[1] == "if":
            if_exp()
        else:
            tree_text.insert(tk.END, f"expect float or if as the first keyword of the expression!"+ "\n")
            return
    elif typeT == "identifier":
        if token == "print":
            tree_text.insert(tk.END, f"child node (internal): identifier"+ "\n")
            tree_text.insert(tk.END, f"   identifier has child node (token):" + token+ "\n")
            print_exp()
    else:
        tree_text.insert(tk.END, f"Invalid Expression"+ "\n")
        return

def cleanup(tokens):
    cleanlist = []
    for x in tokens:
        temp = x[1:-1].split(",")
        tup = (temp[0],temp[1])
        cleanlist.append(tup)

    return cleanlist

def parser(tokens):
    global intoken
    global tokenlist
    tokenlist = cleanup(tokens)
    intoken = tokenlist.pop(0)
    exp()
    try:
        accept_token()
    except:
        tree_text.insert(tk.END, f"Parse Tree Error: No ; or :"+ "\n")
    else:
        if intoken[1] == ";" or intoken[1] == ":":
            tree_text.insert(tk.END, f"\nparse tree building success!"+ "\n\n")

    return



def next_line():
    global line_number, code_lines, code
    output_text.focus_set()
    output_text.config(state=tk.NORMAL)

    if line_number == len(code_lines) - 1:
        # If we have reached the end of the code lines, reset the line number
        line_number = 0
        code_lines = []
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        tree_text.config(state=tk.NORMAL)
        tree_text.delete("1.0", tk.END)

    if not code_lines:
        code = code_text.get("1.0", tk.END)
        code_lines = code.split("\n")

    output_text.insert(tk.END, f"###Tokens for Line {line_number}###\n")
    output_text.insert(tk.END, f"{cut_one_line_tokens(code_lines[line_number])}\n\n")
    output_text.config(state=tk.DISABLED)

    tree_text.config(state=tk.NORMAL)
    tree_text.insert(tk.END, f"###Parse Tree for Line {line_number}###\n\n")

    parser(cut_one_line_tokens(code_lines[line_number]))
    tree_text.config(state=tk.DISABLED)

    line_number += 1
    line_number_text.config(state=tk.NORMAL)
    line_number_text.delete("1.0", tk.END)
    line_number_text.insert(tk.END, f"{line_number}")
    line_number_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Lexical Analyzer and Parser for TinyPie")
root.bind("<Escape>", lambda e: root.quit())

# Parent frame
parent_frame = ttk.Frame(root, padding=10)
parent_frame.pack(side="top")

# Code frame
code_frame = tk.Frame(parent_frame)
code_frame.pack(side="left")  # Set side to "left"

code_label = ttk.Label(code_frame, text="Source Code", padding=5)
code_label.pack()

code_text = tk.Text(code_frame, height=10, width=50)
code_text.pack(padx=5)

# Output frame
output_frame = ttk.Frame(parent_frame)
output_frame.pack(side="left")  # Set side to "right"

output_label = ttk.Label(output_frame, text="Tokens", padding=5)
output_label.pack()

output_text = tk.Text(output_frame, height=10, width=50)
output_text.pack(padx=5)
output_text.config(state=tk.DISABLED)  # Set initial state to disabled

tree_frame = ttk.Frame(parent_frame)
tree_frame.pack(side="left", fill="x")

tree_label = ttk.Label(tree_frame, text="Parse Tree", padding=5)
tree_label.pack()

tree_text = tk.Text(tree_frame, height=10, width=50)
tree_text.pack(padx=5)
tree_text.config(state=tk.DISABLED)

# Button frame
button_frame = ttk.Frame(root, padding=5)
button_frame.pack(fill="both")

line_frame = ttk.Frame(button_frame)
line_frame.pack(expand=True)

line_number_frame = ttk.Frame(button_frame)
line_number_frame.pack(side="left", expand=True)

run_button = ttk.Button(button_frame, text="Next line", command=next_line)
run_button.pack(side="left", expand=True)

line_number_label = ttk.Label(line_number_frame, text="Line number:")
line_number_label.pack()

line_number_text = tk.Text(line_number_frame, height=1, width=5)
line_number_text.pack()

quit_button = ttk.Button(button_frame, text="Quit", command=root.quit)
quit_button.pack(side="left", expand=True)

root.update()
root.minsize(root.winfo_width(), root.winfo_height())

root.mainloop()


