# ArrEx

Array Expressions - Shorthand Language for Array Manipulation




## Documentation

[Documentation](https://github.com/danielpagano202/ArrEx/blob/main/docs.json)


## Features

- Arithmetic
- Array Looping
- Conditional Statements
- Sorting
- Regex
- Customizable Functions


## Installation

Project is not on Pip yet, so it must be downloaded manually

```bash
  Work - In - Progress
```
    
## Getting Started

The main function that will be used is evaluate
```python
    import arrex.py as arrex

    lst = [1, 2, 3, 4, 5]

    output = arrex.evaluate(lst, "e(x + 1)")

    print(output) # [2, 3, 4, 5, 6]

```

In this code, evaluate will run the code, passing in lst to the scope (represented by 'x').

So, at the beginning of the code, x will equal [1, 2, 3, 4, 5]

In this language, certain functions like e() create a new scope.

Essentially, e() loops through each element of the x in scope.

So, it loops through the list, and sets the scope of x inside of it to the current element.

| Step | X | Code | Return | Comments
| :---:   | :---: | :---: | :---: | :---:
| 1 | [1, 2, 3, 4, 5] | e(x+1) | | Nothing returned yet
| 2 | 1 | x + 1 | 2 | Uses the first element and adds to it
| 3 | 2 | x + 1 | 3 | Pattern continues
| 4 | 3 | x + 1 | 4 ||
| 5 | 4 | x + 1 | 5 ||
| 6 | 5 | x + 1 | 6 ||
| 7 | [1, 2, 3, 4, 5] | [2, 3, 4, 5, 6] | [2, 3, 4, 5, 6] | The code was replaced with an array

## Function Parameters

Some functions have parameters that are either optional or required

For example, e() has an optional parameter that is written as: eK()

The k (defaulting to 1) represents how many elements are looked at in each pass through. 

For example:
```python
    import arrex.py as arrex

    lst = [1, 2, 3, 4, 5, 6]

    output = arrex.evaluate(lst, "e2(i0(x) + i1(x))")

    print(output) # [3, 7, 11]

```

| Step | X | Code | Return | Comments
| :---:   | :---: | :---: | :---: | :---:
| 1 | [1, 2, 3, 4, 5, 6] | e2(i0() + i1()) | | Nothing returned yet
| 2 | [1, 2] | i0(x) | 1 | Gets the first element of x
| 3 | [1, 2] | i1(x) | 2 | Gets the second element of x
| 4 | [1, 2] | i0(x) + i1(x) | 3 | Adds the two elements
| 5 | [3, 4] | i0(x) | 3 | Gets the first element of x
| 6 | [3, 4] | i1(x) | 4 | Gets the second element of x
| 7 | [3, 4] | i0(x) + i1(x) | 7 | Adds the two elements
| 8 | [5, 6] | i0(x) | 5 | Gets the first element of x
| 9 | [5, 6] | i1(x) | 6 | Gets the second element of x
| 10 | [5, 6] | i0(x) + i1(x) | 11 | Adds the two elements
| 11 | [1, 2, 3, 4, 5, 6] | [3, 7, 11] | [3, 7, 11] | The code was replaced with an array

In this, pairs of elements were added together.

The parameter can be distinguished for readability using `{}`

`e{2}(i0() + i1())`

## Types

There are four types:

- Number
- String
- Bool
- Array

Each one was its own use. However, in most cases strings and arrays work interchangably

For example, if the x is a string, then you can loop through each letter

## Operators

You have already seen the plus operator. There are a few more
| Name | Symbol | Use | Code | Comments
| :---:   | :---: | :---: | :---: | :---:
| Plus | + | Adding numbers, strings, or arrays | 1 + 2 | 3
| Minus | - | Subtracting numbers | 2 - 1 | 1, can be used for negation as in -3
| Multiplication | * | Multiplying numbers | 2 * 3 | 6
| Division | / | Dividing numbers | 5 / 4 | 1.25
| Parenthesis | () | Prioritize code or denotes function code | 3 / (1 + 4) | 0.6
|Curly Brackets| {} | Prioritize code and  make function parameters more readable | 3 / {1 + 4} | 0.6
| Exponent | ^ | Exponentiation | 2 ^ 3 | 8
| Modulus | % | Getting the remainder | 15 % 2 | 1
| Int Division | // | Gets the int part in division | 5 // 2 | 2, useful for making numbers integers
| Equal | == | Checking equality between values | 5 == 2 | False
| Not Equal | != | Checking inequality between values | 5 != 2 | True
| Greater than | > | Checking if a number is bigger than another | 5 > 2 | True
| Less than | < | Checking if a number is smaller than another | 5 < 2 | False
| Greater than or equal | >= | Checking if a number is bigger than or equal to another | 3 >= 3 | True
| Less than or equal | <= | Checking if a number is smaller than or equal to another | 3 <= 3 | True
| Boolean Not | ! | Negates a boolean | !T | False
| Comma | , | Separates certain code in some functions | ar(1, 2, 3, 4 ) | [1, 2, 3 ,4], ar makes an array
| Type equal | ~= | Checks if a value is a type | 3 ~= tn | True, tn means number type
| In | _ | Checks if a value is in an array | 3_ar(1, 2, 3, 4) | True
| Count | # | Checks how many times a value occurs in an array | 3#ar(1, 2, 3, 4, 3, 5) | 2
| At | @ | Checks where a value is in an array | 3@ar(1, 2, 3, 4) | 2
| Skim | >> | Removes all instances of a value in an array | ar(1, 2, 3, 4) >> 2 | [1, 3, 4]
| Conditional If | ? : | Does something different depending on if something is true or not | 3 == 3 ? 50 : 20 | 50



## Constants

There are a few constants in this programming language

- T for True
- F for False
- N for Null
- L for the length of X
- I for the index of X (defaults to 0)
- ta, tn, ts, tb for array type, number type, string type, or bool type

## Important functions

### ik()
The iK() function indexes the array inside of it.

- The parameter is required and must be within the range of the length of x
- The inside will default to x as in it i0() becomes i0(x)
- However, something like i0("Hello") returns "H"

### sc()
The sc() function allows you to change what the current scope is

```python
    import arrex.py as arrex

    lst = [1, 2, 3, 4, 5, 6]

    code = """
        sc( e2(i0(x) + i1(x)),  i0() * i1() * i2() ) 
    """

    output = arrex.evaluate(lst, code)

    print(output) # 231
```

In this code, the e2(i0(x) + i1(x)) will create the array [3, 7, 11]

We then set x to that using `sc(e2(i0(x) + i1(x)), ... )`

So, the code `i0() * i1() * i2()` has an x of [3, 7, 11] that it gets elements from.

### l()

The l function will loop through x, but cumulate everything into one value

```python
    import arrex.py as arrex

    lst = [1, 2, 3, 4, 5, 6]

    code = """
        l(a + b)
    """

    output = arrex.evaluate(lst, code)

    print(output) # 21
```

`a` represents the cumulated value (which starts equal to the first element)

`b` represents the new value to be added on

This means you can also use l() to find the max

```python
    import arrex.py as arrex

    lst = [1, 2, 3, 6, 5, 4]

    code = """
        l(b > a ? b : a)
    """

    output = arrex.evaluate(lst, code)

    print(output) # 6
```

### cv()

cvK() converts a value to another type

In this function, k is a type constant

So, it is written as ` cvta("Hello")` or `cvtn("3")`

Curly brackets help this to be more readable `cv{ta}("Hello")`

The only conversions that aren't possible are:

- Array to number
- String to number if string isn't a number

There are other functions, but these have important utility that should be known.

## How to support this project

⭐ Star the repository on Github. Thank you :)
