#filedone.py - executing .il files
import tokenizer as tk
import parser_interpreter as intr
import sys
filename = sys.argv[1]
trash = ''
with open(filename, "r") as file:
    lines = file.readlines()
    alines = []
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    for i in range(len(lines)):
        alines.append(tk.execute_tokenizer(lines[i]))
    itpt = intr.Interpriter()
    i = 0
    while i < len(lines):
        ret, trash = itpt.interpret(alines[i])
        alines[i] = tk.execute_tokenizer(lines[i])
        if ret == -2:
            break
        elif ret > -1:
            i = ret -1
        i+=1
sys.exit()
