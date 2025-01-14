import ast
import re
from collections.abc import Iterable

#Every reserved symbol
base_symbols_dict = {
    "x": "VAR",
    "a": "VAR",
    "b": "VAR",
    "tn": "TYPE",
    "tb": "TYPE",
    "ts": "TYPE",
    "ta": "TYPE",
    "T": "BOOL",
    "F": "BOOL",
    "L": "NUMBER",
    "I": "NUMBER",
    "N": "NULL",
    ",": "SEP",
    "==": "BOP",
    "!=": "BOP",
    ">": "BOP",
    "<": "BOP",
    ">=": "BOP",
    "<=": "BOP",
    "&": "BOP",
    "|": "BOP",
    "!": "BOP",
    "+": "OP",
    "-": "OP",
    "*": "OP",
    "/": "OP",
    "//": "OP",
    "%": "OP",
    "^": "OP",
    "~=": "TOP",
    ">>": "AOP",
    "_": "AOP",
    "#": "AOP",
    "@": "AOP",
    "?": "IF",
    ":": "COLON",
    "(": "PSTART",
    ")": "PEND",
    "{": "BSTART",
    "}": "BEND",
    "e": "FUNC",
    "o": "FUNC",
    "i": "FUNC",
    "r": "FUNC",
    "sc": "FUNC",
    "s": "FUNC",
    "l": "FUNC",
    "ar": "FUNC",
    "cv": "FUNC",
    "sr": "FUNC",
    "re": "FUNC"
}

#The symbols used by the program which will be filled when evaluate is run
important_symbols_dict = {}

#The longest symbol
max_symbol_length = max([len(x) for x in base_symbols_dict.keys()])

#Calls an error
def call_error(error):
    raise Exception(error)

#Reads text to look for symbols
def read_for_symbols(text, index):
    #Finds the amount of letters to look through. Either the max_symbol_length or the remaining length of the string
    letters_to_look_through = min(len(text) - index, max_symbol_length)

    #The word or character that will be returned
    final_word = ""

    #Loops through the text to find the possible symbol at each length
    for i in range(1, letters_to_look_through+1):
        #Gets the possible symbol through string slicing
        possible_symbol = text[index:index + i]

        #If it is in the set, it is set to final word
        if possible_symbol in important_symbols_dict:
            #This method will always return the longest option because it is what final word was last set to
            final_word = possible_symbol

    #If no word was set, it sets it to the singular character
    if not final_word:
        final_word = text[index]

    #Returns the final word
    return final_word

#Gets the type as a string of an element in tokens
def get_type(text, allow_minus=False):
    txt = str(text)
    #If the value is surrounded by quotes or it is a ts
    if txt[0] + txt[-1] == '""' or text == "STRING":
        return "STRING"

    #Replaces a dot to allow decimal checks
    text_num = txt.replace(".", "", 1)

    #If the value is a number, negative number, or tn
    if text_num.isdigit() or (text_num[0] == "-" and text_num[1:].isdigit()) or text == "NUMBER":
        return "NUMBER"

    #If the value is one of the list values, or tb
    if text_num.lower() in {"false", "true", "t", "f"} or text == "BOOL":
        return "BOOL"

    #If the value is enclosed by brackets, or ta
    if txt[0] == "[" and txt[-1] == "]" or text == "ARRAY":
        return "ARRAY"

    #If the value is a null value
    if txt.lower() in {"null", "n"}:
        return "NULL"

    #If we are tokenizing and need to get the type of a minus sign that denotes negation rather than subtraction
    if txt == "-" and allow_minus:
        return "OP"

    #If it doesn't match, it is an error
    return "ERROR"

#Turns a string of code into a list of readable tokens
def tokenize_code(code):
    #Initializes some important variables
    tokens = []
    token_types = []
    current_reading = ""
    i = 0
    quote_count = 0

    #Loops through every character
    while i < len(code):

        #Looks for the next piece of code. Could be anything from '2' to '"Hello"' to '+'
        symbol_reading = read_for_symbols(code, i)

        #If we find a quote, we add to quote count because we don't want to split code that is in quotes as it is a string
        if symbol_reading == '"':
            quote_count = (quote_count + 1) % 2

        #If symbol reading is not a keyword or we are in a string
        if symbol_reading not in important_symbols_dict or quote_count != 0:
            #If code is not white space or we are in a string
            if code[i] not in {" ", "\n"} or quote_count != 0:
                #We add it to current reading so that even though we are looking at individual characters, 200 or "Hello" are one token
                current_reading += code[i]
            #Increment counter
            i += 1
        else:
            #If what we have read is not whitespace
            if current_reading != " " and current_reading != "":
                #Appends what has been read to tokens and token_types and resets current reading
                tokens.append(current_reading)
                token_types.append(get_type(current_reading, True))
                current_reading = ""

            #Appends the keyword to tokens and its type to token_types
            tokens.append(str(symbol_reading))
            token_types.append(important_symbols_dict[symbol_reading])

            #Skips past that text to not read it twice
            i += len(symbol_reading)

        #If we are at the end of the text
        if i >= len(code):
            #If what we have read is not blank
            if current_reading != " " and current_reading != "":
                #Appends what has been read to tokens and token_types and resets current reading
                tokens.append(current_reading)
                token_types.append(get_type(current_reading))
                current_reading = ""

    #print(tokens, token_types)

    #If a type was of error
    if "ERROR" in token_types:
        call_error("Tokenization Error")



    return tokens, token_types

#Gets the tokens next to the operators
def get_operator_values(tokens, token_types, index):
    #Initializes variables to represent positioning of the tokens to the left and right of the operator
    left_pos = index - 1
    right_pos = index + 1

    #Creates a set that will be used to check if the type is proper
    valid_types = {"NUMBER", "STRING", "VAR", "FUNC", "BOOL", "ARRAY", "TYPE", "NULL"}

    #Checks the left token first
    if left_pos >= 0 and token_types[left_pos] in valid_types:
        left_value = left_pos
    #Returns index if valid token is not found to ensure list slicing will work
    else:
        left_value = index

    #Checks the right token next
    if right_pos < len(token_types) and token_types[right_pos] in valid_types:
        right_value = right_pos
    #Returns index if valid token is not found to ensure list slicing will work
    else:
        right_value = index

    #Returns the values as a tuple
    return left_value, right_value

#Gets the tokens in between the parenthesis
def get_parenthesis_code(tokens, index, front_parenthesis = "(", back_parenthesis=")"):
    #P_count ensures that we get the outer parenthesis and the code inside
    p_count = 0

    #Loops through the tokens starting at the index of the original parenthesis
    for i in range(index, len(tokens)):
        #Adds 1 if we reach a start parenthesis
        if tokens[i] == front_parenthesis:
            p_count += 1
        #Subtracts 1 if we reach an end parenthesis
        elif tokens[i] == back_parenthesis:
            p_count -= 1

            #Returns the index of the ending parenthesis if we are at the end parenthesis that matches the first start parenthesis
            if p_count == 0:
                return i

    #Error is called because we should have returned by this point. Reaching this point means that the last token, which we needed to be an end parenthesis, was something else
    call_error("Ending Parenthesis Not Found")

#Gets the tokens for the K parameter of the function
def get_token_index_code(tokens, token, index = 0):
    #Use p_count and b_count to ensure that we reach the token
    p_count = 0 if token != "(" else -1
    b_count = 0 if token != "{" else -1

    #Loops through tokens, starting at index, checking if token is a parenthesis/curly bracket
    for i in range(index, len(tokens)):
        if tokens[i] == "(":
            p_count += 1
        elif tokens[i] == ")":
            p_count -= 1
        elif tokens[i] == "{":
            b_count += 1
        elif tokens[i] == "}":
            b_count -= 1
        if tokens[i] == token and p_count == 0 and b_count == 0:
            return i
    return -1

#Verifies that text is of a certain type
def verify_type(text, comp_type, use_type_constants=False):
    if get_type(text) != comp_type:
        call_error(f"{text} is not the type {comp_type}")
    if text == comp_type and not use_type_constants:
        call_error("Using type constants in place of actual values of the type")

#Interprets tokens with operators
def interpret_operator(tokens, token_types, symbols_dict):
    op_types = []
    count = 0
    for i, n in enumerate(tokens):
        if str(n) in symbols_dict:
            count += 1
            op_types.append(symbols_dict[n])
    for i in range(count):
        n = 0
        for j, t in enumerate(tokens):
            if str(t) in symbols_dict:
                n = j
                break
        left_range, right_range = get_operator_values(tokens, token_types, n)
        if right_range != n:
            if len(tokens[left_range:n]) > 0:
                left_element = "".join(str(tokens[left_range:n][0]))
            else:
                left_element = "".join(str(tokens[left_range:n]))

            right_element = "".join(str(tokens[n + 1:right_range + 1][0]))
            response = op_types[i](left_element, right_element)
            tokens = tokens[0:left_range] + [response] + tokens[right_range + 1:]
            token_types = token_types[0:left_range] + [get_type(str(response))] + token_types[right_range + 1:]
    return tokens, token_types

#Converts a variable to a string if type of string
def convert_var(a):
    if type(a) == str:
        return '"' + format_string(a) + '"'
    return str(a)

#Converts token to python version of it
def convert_token_with_token_type(token, token_type):
    str_token = str(token)
    if token == token_type:
        return token
    elif token_type == "NUMBER":
        if "." not in str_token:
            return int(token)
        return float(token)
    elif token_type == "STRING":
        return str_token
    elif token_type == "ARRAY" or (str_token and str_token[0] == "[" and str_token[-1] == "]"):
        return ast.literal_eval(str_token)
    elif token_type == "BOOL" or str_token.lower() in {"t", "f", "true", "false"}:
        return ast.literal_eval(str_token)
    elif token_type == "NULL" or str_token.lower() in {"null", "n"}:
        return None
    return token

#Convers a token value to a boolean
def convert_to_bool(a):
    #Gets the value type and value
    value_type = get_type(a)
    value = convert_token_with_token_type(a, value_type)

    #Removes quotes if a string
    if value_type == "STRING":
        value = str(value[1:-1])

    #Returns the boolean representation
    return bool(value)

#Formats an array or string
def convert_to_list(a):
    #If it is a string, it is fine the way it is
    if get_type(a) == "STRING":
        lst = a

    #If it is the type of array
    elif get_type(a) == "ARRAY":
        #Assigns lst as the list without the brackets on its edge
        lst = str(a)[1:-1]

        #If the inside of the list has quotes around it, removes them and puts brackets instead
        if len(lst) > 0 and lst[0] == '"' and lst[-1] == '"':
            lst = "[" + lst[1:-1] + "]"

        #Adds brackets around entire list
        else:
            lst = "[" + lst + "]"
    #The default is to just surround the value with brackets
    else:
        lst = str([convert_token_with_token_type(a, get_type(a))])
    #Returns the list evaluated as a python type and formats it to put quotes around string elements in it
    return format_list(ast.literal_eval(lst))

#Formats string literals by removing extra quotes
def format_string(a):
    if type(a) is str and a[0] == '"' and a[-1] == '"':
        return a[1:-1]
    return a

#Formats a list to make strings in it have quotes around them
def format_list(lst):
    return_lst = []
    for i in lst:
        if type(i) is str and i[0] != '"' and i[-1] != '"':
            return_lst.append('"' + str(i) + '"')
        else:
            return_lst.append(convert_token_with_token_type(i, get_type(i)))
    return return_lst

#Basic Math Functions
def add(a, b):
    if get_type(a) == "STRING":
        verify_type(a, "STRING")
        verify_type(b, "STRING")
        return '"' + format_string(a) + format_string(b) + '"'
    elif get_type(a) == "NUMBER":
        verify_type(a, "NUMBER")
        verify_type(b, "NUMBER")
        return float(a) + float(b)
    elif get_type(a) == "ARRAY":
        verify_type(a, "ARRAY")
        verify_type(b, "ARRAY")
        return convert_to_list(a) + convert_to_list(b)
    else:
        call_error(f"{a} and {b} are not valid types for addition or concatenation")
def subtract(a, b):
    if a == "[]":
        a = "0"
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) - float(b)
def multiply(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) * float(b)
def divide(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) / float(b)
def int_divide(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return int(float(a) // float(b))
def mod(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return int(float(a) % float(b))
def exponent(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) ** float(b)

#Basic Boolean Functions
def equals(a, b):
    return convert_token_with_token_type(a, get_type(a)) == convert_token_with_token_type(b, get_type(b))
def not_equals(a, b):
    return a != b
def greater(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) > float(b)
def greater_equal(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) >= float(b)
def lesser(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) < float(b)
def lesser_equal(a, b):
    verify_type(a, "NUMBER")
    verify_type(b, "NUMBER")
    return float(a) <= float(b)
def type_func(a, b):
    return get_type(a) == get_type(b)
def inverse_equal(a ,b):
    verify_type(b, "BOOL")
    return not convert_to_bool(b)
def and_func(a, b):
    return convert_to_bool(a) and convert_to_bool(b)
def or_func(a, b):
    return convert_to_bool(a) or convert_to_bool(b)

#Basic Array Functions
def in_func(a, b):
    return convert_token_with_token_type(a, get_type(a)) in convert_to_list(b)
def at_func(a, b):
    if in_func(a, b):
        return convert_to_list(b).index(convert_token_with_token_type(a, get_type(a)))
    else:
        return -1
def count_func(a, b):
    return convert_to_list(b).count(convert_token_with_token_type(a, get_type(a)))
def skim_func(a, b):
    if get_type(a) == "STRING":
        #Gets rid of every duplicate element, removes quotes from every elements, and joins it in a string
        return "".join([x[1:-1] for x in convert_to_list(a) if x != convert_token_with_token_type(b, get_type(b))])
    return [x for x in convert_to_list(a) if x != convert_token_with_token_type(b, get_type(b))]

#Interprets inline if statements
def if_func(tokens, token_types, array, index, a, b):
    tokens = tokens.copy()
    token_types = token_types.copy()


    if_index = get_token_index_code(tokens, "?")

    colon_index = get_token_index_code(tokens, ":")
    colon_exists = True
    if colon_index == -1:
        colon_exists = False
        colon_index = len(tokens)

    boolean_expression = tokens[0:if_index]
    bl = interpret_code(boolean_expression, token_types[0:if_index], array, index, a, b)[0][0]
    start_index = 0
    end_index = 0
    if convert_to_bool(bl):
        start_index = if_index + 1
        end_index = colon_index
    else:
        start_index = colon_index + 1
        end_index = len(tokens)
    outcome = tokens[start_index:end_index]
    if colon_exists or convert_to_bool(bl):
        new_tokens, new_token_types = interpret_code(outcome, token_types[start_index:end_index], array, index, a, b)
    else:
        new_tokens, new_token_types = (["Null"], ["NULL"])
    tokens = new_tokens
    token_types = new_token_types
    return tokens, token_types

#These are the functions associated with the code functions
def e_func(**kwargs):
    return_lst = []
    k = kwargs['k']
    array = kwargs['array']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    a = kwargs['a']
    b = kwargs['b']

    #If there is no k, then it defaults to 1
    if k == "":
        k = "1"

    #Verifies that the parameter is a number
    verify_type(k, "NUMBER")

    #Convers the k
    k_value = int(float(k))

    #Loops through the array and interprets the part
    for i in range(0, len(array) // k_value):
        #Uses array slicing to figure out how many elements to work with at a time
        n = array[i * k_value:(i + 1) * k_value]

        if len(n) == 1:
            n = n[0]

        #Interprets and appends to return list
        tokens_info = interpret_code(tokens, token_types, n, i, a, b)
        return_lst.append(convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0]))

    #Returns the output list
    return return_lst

def o_func(**kwargs):
    k = kwargs['k']
    array = kwargs['array']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    a = kwargs['a']
    b = kwargs['b']

    #Verifies that the parameter is a number
    verify_type(k, "NUMBER")
    int_k = int(float(k))

    #Ensures k is within bounds of (0, L)
    if int_k < 0:
        call_error(f"Parameter {k} needs to be greater than or equal to zero")
    if int_k > len(array):
        call_error(f"Parameter {k} needs to be less than or equal the length of the array")

    #Interprets answer
    tokens_info = interpret_code(tokens, token_types, array, int_k, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    #If the value is iterable, it returns it
    if isinstance(answer, Iterable):
        #Will return everything together as one string if a string was offset
        if tokens_info[1][0] == "STRING":
            return '"' + format_string(answer)[int_k:] + '"'
        return answer[int_k:]
    else:
        call_error(f"The element {answer} can't be sliced")

def i_func(**kwargs):
    k = kwargs['k']
    array = kwargs['array']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    a = kwargs['a']
    b = kwargs['b']

    #Verifies that the parameter is a number and is within the Length
    verify_type(k, "NUMBER")
    int_k = int(float(k))

    #Ensures the value is not outside of the bounds of (-L, L)
    if abs(int_k) >= len(array):
        call_error("The parameter for the index function is too big for the array!")

    #If there are no tokens, interprets tokens as x
    if not tokens and not token_types:
        tokens = ["x"]
        token_types = ["VAR"]

    #Interprets answer
    tokens_info = interpret_code(tokens, token_types, array, int_k, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    #If the value is iterable, it returns it
    if isinstance(answer, Iterable):
        #Will return everything together as one string if a string was offset
        if tokens_info[1][0] == "STRING":
            return '"' + format_string(answer)[int_k] + '"'
        return answer[int_k]
    else:
        call_error(f"The element {answer} can't be indexed")

def r_func(**kwargs):
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    index = kwargs['index']
    a = kwargs['a']
    b = kwargs['b']

    #Interprets answer
    tokens_info = interpret_code(tokens, token_types, array, index, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    #Reverses the list if it is iterable
    if isinstance(answer, Iterable):
        return answer[::-1]
    else:
        call_error(f"The element {answer} can't be sliced")

def sc_func(**kwargs):
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    index = kwargs['index']
    a = kwargs['a']
    b = kwargs['b']

    #Gets the index of the comma and interprets it
    comma_index = get_token_index_code(tokens, ",")
    tokens_info = interpret_code(tokens[0:comma_index], token_types[0:comma_index], array, index, a, b)
    comma_section = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    #Returns the answer
    return interpret_code(tokens[comma_index + 1:], token_types[comma_index + 1:], comma_section, index, a,b)[0][0]

def s_func(**kwargs):
    k = kwargs['k']
    array = kwargs['array']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    a = kwargs['a']
    b = kwargs['b']

    #Verifies that the parameter is a number and within the bounds of (0, L)
    verify_type(k, "NUMBER")
    int_k = int(float(k))
    if int_k < 0:
        call_error(f"Parameter {k} needs to be greater than or equal to zero")
    if int_k > len(array):
        call_error(f"Parameter {k} needs to be less than or equal to the length of the array")

    #Interprets code
    tokens_info = interpret_code(tokens, token_types, array, int_k, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])
    # If the value is iterable, it returns it
    if isinstance(answer, Iterable):
        # Will return everything together as one string if a string was offset
        if tokens_info[1][0] == "STRING":
            return '"' + format_string(answer)[:int_k] + '"'
        return answer[:int_k]
    else:
        call_error(f"The element {answer} can't be sliced")

def l_func(**kwargs):
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    a = kwargs['a']
    b = kwargs['b']
    #Gets the initial value to start with from the first two elements of the array
    tokens_info = interpret_code(tokens, token_types, array, 0, array[0], array[1])
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    #Loops through the rest of the array to cumulate one final answer
    for i, value in enumerate(array[2:]):
        tokens_info = interpret_code(tokens, token_types, array, i + 1, answer, value)
        answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    return answer

def ar_func(**kwargs):
    k = kwargs['k']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    a = kwargs['a']
    b = kwargs['b']

    actual_k = 1

    #Sets actual_k to k parameter if given, defaulting to 1
    if k != "" and k is not None:
        verify_type(k, "NUMBER")
        if float(k) < 0:
            call_error(f"Parameter {k} needs to be greater than or equal to zero")
        actual_k = int(float(k))

    #Figures out where to split on commas
    array_parts = []
    comma_points = [-1]
    comma_point = get_token_index_code(tokens, ",")

    #Adds point to comma point arrays
    if comma_point != -1:
        comma_points.append(comma_point)

    #Loops through finding comma points until end of array is reached
    while tokens.count(",") >= len(comma_points) and comma_points[-1] != -1:
        comma_point = get_token_index_code(tokens, ",", comma_points[-1] + 1)
        if comma_point == -1:
            break
        comma_points.append(comma_point)

    #Adds the last comma point
    comma_points.append(len(tokens))

    #If there are no tokens, an empty array is returned
    if not tokens:
        return []

    #Interprets the tokens in each comma section
    for t in range(0, actual_k):
        for i, n in enumerate(comma_points[:-1]):
            #Uses list slicing and math to figure out token section and index
            tokens_info = interpret_code(tokens[n + 1:comma_points[i + 1]], token_types[n + 1:comma_points[i + 1]],
                                         array, i + (t * len(comma_points[:-1])), a, b)
            #Interprets answer
            comma_section = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])
            array_parts.append(comma_section)
    return array_parts

def cv_func(**kwargs):
    k = kwargs['k']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    index = kwargs['index']
    a = kwargs['a']
    b = kwargs['b']

    tokens_info = interpret_code(tokens, token_types, array, index, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])
    value = answer
    if tokens_info[1][0] == "STRING":
        value = str(answer[1:-1])

    if k == "NUMBER":
        answer_num = str(value).replace(".", "", 1)
        if type(value) is not str and type(value) is not list:
            return float(value)
        elif answer_num.isdigit() or (answer_num[0] == "-" and answer_num[1:].isdigit()):
            return float(value)
        else:
            call_error(f"Value '{answer}' can not be converted to number")
    elif k == "STRING":
        if type(value) is list:
            return "".join([format_string(x) for x in value])
        return str('"' + str(value) + '"')
    elif k == "ARRAY":
        if type(value) is str:
            return list(value)
        else:
            return [value]
    elif k == "BOOL":
        return bool(value)

def sr_func(**kwargs):
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    index = kwargs['index']
    a = kwargs['a']
    b = kwargs['b']

    #Creates a copy of the array
    sorted_array = array.copy()

    #Tries to sort it if possible
    try:
        sorted_array.sort()
    except:
        call_error(f"Array {array} can not be sorted!")

    #Interprets code inside, passing sorted array
    tokens_info = interpret_code(tokens, token_types, sorted_array, index, a, b)
    answer = convert_token_with_token_type(tokens_info[0][0], tokens_info[1][0])

    return answer

def re_func(**kwargs):
    k = kwargs['k']
    tokens = kwargs['tokens']
    token_types = kwargs['token_types']
    array = kwargs['array']
    index = kwargs['index']
    a = kwargs['a']
    b = kwargs['b']

    #Gets the index of the comma
    comma_index = get_token_index_code(tokens, ",")

    #Interprets the first side of the function (string to search for)
    regex_info = interpret_code(tokens[0:comma_index], token_types[0:comma_index], array, index, a, b)
    regex_expression = convert_token_with_token_type(regex_info[0][0], regex_info[1][0])

    #Interprets the second side of the function (string to search)
    main_string_info = interpret_code(tokens[comma_index + 1:], token_types[comma_index + 1:], array, index, a, b)
    main_string = convert_token_with_token_type(main_string_info[0][0], main_string_info[1][0])

    #Formats
    regex_expression = format_string(regex_expression)
    main_string = format_string(main_string)

    #Performs the proper operation
    if "#" in k:
        return len(re.findall(regex_expression, main_string))
    elif "_" in k:
        regex_search = re.search(regex_expression, main_string)
        return bool(regex_search)
    elif "@" in k:
        regex_search = re.search(regex_expression, main_string)
        if regex_search is None:
            return -1
        return regex_search.start()
    else:
        call_error(f"Parameter {k} is not valid! Needs to be '#', '_', or '@'")


#A dictionary function with function symbols corresponding to the function to run
base_function_dict = {
    "e": e_func,
    "o": o_func,
    "i": i_func,
    "r": r_func,
    "sc": sc_func,
    "s": s_func,
    "l": l_func,
    "ar": ar_func,
    "cv": cv_func,
    "sr": sr_func,
    "re": re_func
}
function_dict = {}

#Main function that interprets code
def interpret_code(tokens, token_types, array, index = 0, a = None, b = None):
    #Assigns the array of the scope to a and b if no value was provided
    if a is None:
        a = array
    if b is None:
        b = array
    #Creates copys of the tokens. It allows us to see if no changes have been made to know that there is a recursion error
    new_tokens = tokens.copy()
    new_token_types = token_types.copy()


    #Checks for a correct number of parenthesis
    if new_token_types.count("PSTART") != new_token_types.count("PEND"):
        call_error("ERROR: Starting Parenthesis don't correspond with Ending Parenthesis")

    #Checks that there are enough parenthesis for function
    if new_token_types.count("FUNC") > new_token_types.count("PSTART"):
        call_error("ERROR: Not enough parenthesis for the functions")

    # Interprets IF Statements
    if_spot = get_token_index_code(tokens, "?", 0)
    if if_spot != -1:
        new_tokens, new_token_types = if_func(new_tokens, new_token_types, array, index, a, b)


    #Interprets functions in the code by looping until all functions are parsed
    while new_token_types.count("FUNC") > 0:

        #Finds the first occurrence of func
        n = new_token_types.index("FUNC")

        #Gets the index of the end of the parameter for the function
        f_index = get_token_index_code(new_tokens, "(", n)

        #Gets the index of the end of the code
        f_end_index = get_parenthesis_code(new_tokens, f_index)

        #If the parenthesis comes right after the func, there is no k parameter
        if f_index - 1 == n:
            parameter = ""
        else:
            #The parameter is interpreted by looking at the index
            parameter = interpret_code(new_tokens[n + 1:f_index], new_token_types[n + 1:f_index], array, index)[0][0]

        #Arguments for custom functions
        kwargs = {
            'tokens': new_tokens[f_index + 1:f_end_index],
            'token_types': new_token_types[f_index + 1:f_end_index],
            'array': array,
            'index': index,
            'k': parameter,
            'a': a,
            'b': b
        }

        output = function_dict[new_tokens[n]](**kwargs)

        #Updates new_tokens and new_token_types to include output instead of function
        new_tokens = new_tokens[0:n] + [output] + new_tokens[f_end_index + 1:]
        new_token_types = new_token_types[0:n] + [get_type(str(output))] + new_token_types[f_end_index + 1:]

    #Interprets symbols
    symbol_constants = {"I", "L", "T", "F", "N", "x", "a", "b", "tn", "tb", "ts", "ta"}
    for i, n in enumerate(new_tokens):
        if str(n) not in symbol_constants:
            continue
        if n == "I":
            new_tokens[i] = str(index)
        elif n == "L":
            new_tokens[i] = str(len(array))
        elif n == "T":
            new_tokens[i] = "True"
        elif n == "F":
            new_tokens[i] = "False"
        elif n == "N":
            new_tokens[i] = "Null"
        elif n == "x":
            new_tokens[i] = convert_var(array)
            new_token_types[i] = get_type(new_tokens[i])
        elif n == "a":
            new_tokens[i] = convert_var(a)
            new_token_types[i] = get_type(new_tokens[i])
        elif n == "b":
            new_tokens[i] = convert_var(b)
            new_token_types[i] = get_type(new_tokens[i])
        elif n == "tn":
            new_tokens[i] = "NUMBER"
        elif n == "tb":
            new_tokens[i] = "BOOL"
        elif n == "ts":
            new_tokens[i] = "STRING"
        elif n == "ta":
            new_tokens[i] = "ARRAY"

    #Interprets Parenthesis
    for i in range(new_tokens.count("(")):
        if "(" not in new_tokens:
            break

        #Finds the index of the first parenthesis
        n = new_tokens.index("(")

        #Finds the ending parenthesis
        p_index = get_parenthesis_code(new_tokens, n)

        #Finds the tokens and types interpreted for the code in between the parenthesis
        nt, ntt = interpret_code(new_tokens[n+1:p_index], new_token_types[n+1:p_index], array, index)
        new_tokens = new_tokens[0:n] + nt + new_tokens[p_index+1:]
        new_token_types = new_token_types[0:n] + ntt + new_token_types[p_index+1:]

    # Interprets Curly brackets
    for i in range(new_tokens.count("{")):

        if "{" not in new_tokens:
            break

        # Finds the index of the first curly bracket
        n = new_tokens.index("{")

        # Finds the ending curly bracket
        p_index = get_parenthesis_code(new_tokens, n, "{", "}")

        # Finds the tokens and types interpreted for the code in between the curly brackets
        nt, ntt = interpret_code(new_tokens[n + 1:p_index], new_token_types[n + 1:p_index], array, index)
        new_tokens = new_tokens[0:n] + nt + new_tokens[p_index + 1:]
        new_token_types = new_token_types[0:n] + ntt + new_token_types[p_index + 1:]



    #Interpets operators

    #Array Operators
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "_": in_func,
        "#": count_func,
        "@": at_func,
        ">>": skim_func
    })

    #Exponent
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "^": exponent
    })

    #Multiplication, Division, Etc.
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "*": multiply,
        "/": divide,
        "%": mod,
        "//": int_divide
    })

    #Addition and subtraction
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "+": add,
        "-": subtract
    })

    #Inverse
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "!": inverse_equal,
    })

    #Boolean Operators
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "~=": type_func,
        ">=": greater_equal,
        "<=": lesser_equal,
        ">": greater,
        "<": lesser,
        "!=": not_equals,
        "==": equals
    })

    #And, Or
    new_tokens, new_token_types = interpret_operator(new_tokens, new_token_types, {
        "&": and_func,
        "|": or_func
    })

    #If we still have more code to interpret, we loop again
    if len(new_tokens) > 1:
        #If none of the tokens changed, we call an error because it will continue to be multiple tokens
        if new_tokens == tokens and new_token_types == token_types:
            call_error("Recursion Error with Code")
        #Recursion
        new_tokens, new_token_types = interpret_code(new_tokens, new_token_types, array, index)

    #Returns the tokens and types
    return new_tokens, new_token_types

#Evaluates an expression with an array, with any additional functions a user wants
def evaluate(array, expression, additions = None):
    global important_symbols_dict
    global function_dict
    global max_symbol_length
    if expression == "":
        return ""
    important_symbols_dict = base_symbols_dict.copy()
    function_dict = base_function_dict.copy()
    if additions:
        if type(additions) is not dict:
            call_error("Extra Functions need to be dictionary!")
        for i in additions:
            if i in important_symbols_dict:
                call_error("Symbol Already Exists!")
            important_symbols_dict[i] = "FUNC"
            function_dict[i] = additions[i]
        max_symbol_length = max([len(x) for x in important_symbols_dict.keys()])
    token_info = interpret_code(*tokenize_code(expression),array)
    answer = convert_token_with_token_type(token_info[0][0], token_info[1][0])
    return format_string(answer)