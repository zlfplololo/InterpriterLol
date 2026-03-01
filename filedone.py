#filedone.py - executing .il files
import tokenizer as tk
import parser_interpreter as intr
import sys
filename = sys.argv[1]
trash = ''
with open(filename, "r") as file:
    lines = file.read()
    lines2 = lines.split('\n')
    print(lines2)
    alines = tk.execute_tokenizer(lines)
    itpt = intr.Interpriter()
    i = 0
    while i < len(alines):
        ret, trash = itpt.interpret(alines[i])
        alines[i] = tk.execute_tokenizer(lines2[i])[0]
        if ret == -2:
            break
        elif ret > -1:
            i = ret -1
        i+=1
sys.exit()
