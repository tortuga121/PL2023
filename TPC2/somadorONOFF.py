import sys
on = 1
total = 0
in_number = 0
number = ""
word = ""
for line in sys.stdin:
    for c in line.lower():

        if c.isnumeric():
            number = number + c
            word = ""

        elif c == '=':
            if on and number != '':
                total = total + int(number)
            print(total)
            number = ""

        elif c.isalpha():
            if on and number != "":
                total = total + int(number)

            if c == 'o' or c =='n' or c == 'f':
                word = word + c
                if word == "on":
                    on = 1
                    word = ""
                elif word == "off":
                    on = 0
                    word = ""
            else:
                word = ""
            number = ""
            