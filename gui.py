import tkinter as tk
from tkinter import ttk
import lexer as lex

line_number = 0
code_lines = []
code = ""


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

    if not code_lines:
        code = code_text.get("1.0", tk.END)
        code_lines = code.split("\n")

    output_text.insert(tk.END, f"{lex.cut_one_line_tokens(code_lines[line_number])}\n")
    output_text.config(state=tk.DISABLED)

    line_number += 1
    line_number_text.config(state=tk.NORMAL)
    line_number_text.delete("1.0", tk.END)
    line_number_text.insert(tk.END, f"{line_number}")
    line_number_text.config(state=tk.DISABLED)


root = tk.Tk()
root.title("Lexical Analyzer for TinyPie")
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
output_frame.pack(side="right")  # Set side to "right"

output_label = ttk.Label(output_frame, text="Tokens", padding=5)
output_label.pack()

output_text = tk.Text(output_frame, height=10, width=50)
output_text.pack(padx=5)
output_text.config(state=tk.DISABLED)  # Set initial state to disabled

tree_frame = ttk.Frame(parent_frame)
tree_frame.pack(side="right", fill="x")

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
