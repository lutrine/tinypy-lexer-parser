import tkinter as tk
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

# Code frame
code_frame = tk.Frame(root)
code_frame.pack(side="left")  # Set side to "left"

code_label = tk.Label(code_frame, text="Source Code Here:")
code_label.pack()

code_text = tk.Text(code_frame, height=10, width=50)
code_text.pack()

run_button = tk.Button(code_frame, text="Next line", command=next_line)
run_button.pack(side="left")

line_number_label = tk.Label(code_frame, text=f"Line number")
line_number_label.pack(side="right")

line_number_text = tk.Text(code_frame, height=1, width=5)
line_number_text.pack(side="right")

# Output frame
output_frame = tk.Frame(root)
output_frame.pack(side="right")  # Set side to "right"

output_label = tk.Label(output_frame, text="Output:")
output_label.pack()

output_text = tk.Text(output_frame, height=10, width=50)
output_text.pack()
output_text.config(state=tk.DISABLED)  # Set initial state to disabled

quit_button = tk.Button(output_frame, text="Quit", command=root.quit)
quit_button.pack(side="right")

root.mainloop()
