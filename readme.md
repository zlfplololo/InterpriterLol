# Commands

so, the commands are:


| name | args | what it does |
| :--- | :--- | :--- |
| write | **value:**<br>• String<br>• number<br>• List<br>• Reference | writes out the value into the terminal (or wherever you're running this) |
| goto | **value:**<br>• Number (without a fractional part) | goes to the line specified in the value (note that the lines start with 0) |
| get | **value:**<br>• String | prompts the value to the user, storing the user input as a string |
| getnum | **value:**<br>• String | prompts the value to the user, storing the user input as a number |


# References

so, a Reference is a pointer, but high level, so, what it basically
does, is makes a variable be setable by a variable. so, for example, if
b is a reference to a (denoted like `~a`), then setting b would reset a
instead, and you need to use `~=` to reset the value of b.

# Variables

so, variables are created and set like this,
`name = value`, but, if you set it to a reference, however (like this:
`name = ~variable`), any attempt at setting the variable will result in
the variable in the reference to be set. and if you want to reset the
variable that is a reference, you need to use this: `name ~= newvalue`.

# Lists

indexed as `list[index]`, written as
`[element1, element2, ...]`

# Strings

so, strings can both be sourrounded by `'` and `"`

# Technicall stuff

so, the first one is that true and false default to 1 and 0, the
numbers, whitch means you can do crazy stuff.

also, this language does not have an and or an or, so, since true is 1
and false is 0, we can replace theese concepts

`and`: `(condition1 + condition2)/2 == 1`

`or`: `(condition1 + contition2)/2 > 0`

`not`: `(conditon1 - 1)*-1`

also, less than or equal is `=<` insted of `<=` to better match its
counterpart `>=`

every number is a python* float by default, but stored as a string, so if you input `write(1)` it will output `1`, but if you input `write(1-0)` it will output 1.0

Btw it is called a number in the code

# Terminology
float -> number

string

list/array

nonexistant standart terminology -> reference

(...) -> group (when a part or a math expression)

the `...` inside the () -> collection

### why does this work?

well, as we can see, the conditions sum up 2 if both are true, so, we
can get the average in order to determine how many are true (0 - all
false, 1 - all true, 0.5 - 1 true), and then we can set a limit on how
much of them are true (`> 0` - atleast 1, `== 1` - all of them) and we
can do this for any number of conditions

for `not`, its simple, 0 = -1, 1 = 0, and then we just flip the negative
in order to get 0 = 1, 1 = 0

# Examples

### hello, world!

    write("Hello, world!")

### Truth machine

    goto(3)
    goto(5)
    goto(7)
    num = getnum("1 or 0: ")
    goto((((num == 1) + (num == 0))/2 > 0) +1)
    write("error")
    goto(14)
    goto((num == 1) +8)
    goto(10)
    goto(13)
    write(0)
    goto(14)
    write(1)
    goto(12)

### Fizzbuzz

    goto(3)
    goto(19)
    goto(6)
    i = 0.0
    i = i+1
    goto((i =< 100) + 1)
    goto((i%15 == 0) + 7)
    goto((i%5 == 0) +10)
    write("fizzbuzz")
    goto(4)
    goto((i%3 == 0) +13)
    write("buzz")
    goto(4)
    goto(15)
    goto(17)
    write(i)
    goto(4)
    write("fizz")
    goto(4)
