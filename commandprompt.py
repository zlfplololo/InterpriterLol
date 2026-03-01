#commandprompt.py - .il command prompt
import tokenizer as tk
import parser_interpreter as intr
import time
itpt = intr.Interpriter()
print("Setting up...")
time.sleep(1)
print("Done!")
while True:
    a = input('>>> ')
    if a.lower() == 'exit':
        break
    itpt.interpret(tk.execute_tokenizer(a)[0])
