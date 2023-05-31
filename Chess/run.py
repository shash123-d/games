import main

try:
    exec(open("main.py").read())
except FileNotFoundError:
    pass
