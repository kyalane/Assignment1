# Assignment1
Purpose

This project is a Python password generator that creates either memorable or random passwords. It demonstrates the use of built-in Python modules, functions, classes, file handling, and basic best practices.

How to Use

Input:
Choose a password type: memorable or random.
For memorable passwords:
Number of words
Allowed letter cases (lower, upper, title)
For random passwords:
Password length
Whether to include punctuation
Any characters that should not be allowed
Output:
A generated password printed to the console.
The password and the time it was created are saved to a file named
Generated_Passwords.txt.
Memorable passwords are stored in the Memorable/ directory.
Random passwords are stored in the Random/ directory.
If the directories do not exist, they are created automatically.
Running the program with the --demo flag generates 1,000 passwords, randomly choosing between memorable and random types, to confirm everything works correctly.
Libraries / Modules Used
random
string
sys
pathlib
datetime
typing
