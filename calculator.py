
import math

# --- Variables needed for the program ---
# Dictionary for precedence first one for stack-precedence and second one for in-precedence
precedence = {"+": (1, 1), "-": (1, 1), "*": (2, 2), "/": (2, 2), "~": (5, 6), "^": (3, 4), "(": (-1, 7),
              ")": (0, 0), "[": (-1, 7), "]": (0, 0), "{": (-1, 7), "}": (0, 0), "sin": (5, 6), "cos": (5, 6),
              "tan": (5, 6), "cot": (5, 6), "arcsin": (5, 6), "arccos": (5, 6), "arctan": (5, 6), "arcctg": (5, 6),
              "ln": (5, 6), "log": (5, 6)}

matches = {"(": ")", "[": "]", "{": "}"}


# unaryFunctions = {"~": lambda x: -x, "cos": math.cos, -> another way to do it!

# --- Helper functions for the calculator ---

def isOperator(op):
    return op in ["+", "-", "*", "/", "^", "(", ")", "[", "]", "{", "}"] or isUnaryOperator(op)


def isUnaryOperator(op):
    return op in ["~", "sin", "cos", "tan", "cot", "arcsin", "arccos", "arctan", "arcctg", "ln", "log"]


def popHigherOrEqualOps(opStack, val, postfix):
    # Pop out of the stack as long as the stack-precedence of top is greater or equal in-precedence of new op
    while len(opStack) > 0 and precedence[opStack[-1]][0] >= precedence[val][1]:
        postfix.append(opStack.pop())


def doUnaryFunction(op, unique):
    # Perform needed operation
    if op == "~":
        return -unique
    elif op == "sin":
        return math.sin(unique)
    elif op == "cos":
        return math.cos(unique)
    elif op == "tan":
        return math.tan(unique)
    elif op == "cot":
        return 1 / math.tan(unique)
    elif op == "arcsin":
        return math.asin(unique)
    elif op == "arccos":
        return math.acos(unique)
    elif op == "arctan":
        return math.atan(unique)
    elif op == "arcctg":
        return math.pi / 2 - math.atan(unique)
    elif op == "ln":
        return math.log(unique, math.e)
    else:
        return math.log10(unique)


def doBinaryFunction(op, left, right):
    if op == "+":
        return left + right
    elif op == "-":
        return left - right
    elif op == "*":
        return left * right
    elif op == "/":
        return left / right
    else:
        return left ** right


# --- Main functions for input expression and evaluation ---

def splitExpression(expr):
    # Remove all whitespaces from expression
    expr = "".join(expr.split())
    # Init empty list to store all operators and operands and loop through expression
    lst = []
    i = 0
    while i < len(expr):
        # Loop to find the next number or function name (if any)
        op = expr[i]
        if op.isnumeric() or op == "." or op.isalpha():
            # Parse either number or function name
            while i + 1 < len(expr) and (expr[i + 1].isnumeric() or expr[i + 1] == "." or expr[i + 1].isalpha()):
                op += expr[i + 1]
                i += 1
        # Add the value to list and increase index
        lst.append(op)
        i += 1
    return lst


def infixToPostfix(lstExpr):
    # Declaring a stack to hold operators, a string to hold the final expression and rank
    opStack = []
    postfix = []
    rank = 0
    lastOp = False
    # Loop through list of values
    for i, val in enumerate(lstExpr):
        # Check the type of operator
        if val.isnumeric():
            # If numeric, add it to postfix expr, increase rank and set lastOp as fals
            postfix.append(val)
            rank += 1
            lastOp = False
        elif isOperator(val):
            # Check if operator is a minus unary to replace
            if val == "-" and (i == 0 or lastOp):
                val = "~"
            # Pop and append the next operators needed
            popHigherOrEqualOps(opStack, val, postfix)
            # Check if we have a closing operator or not
            if val in matches.values():
                # Pop out from stack until respective opening operator is found
                lastOp = False
                found = False
                while len(opStack) > 0 and not found:
                    # Check if opening is found
                    op = opStack.pop()
                    if op in matches.keys():
                        # Check that right opening is found
                        if matches[op] == val:
                            found = True
                        else:
                            break
                    else:
                        postfix.append(op)
                # Check if opening was not found at all
                if not found:
                    raise ValueError("Incorrect matches for brackets")
            else:
                # Push new operator to stack, set lastOp as True and decrease rank (if needed)
                opStack.append(val)
                lastOp = True
                if val not in matches.keys() and not isUnaryOperator(val):
                    rank -= 1
        else:
            raise ValueError("Incorrect type encountered")
        # Finally, check if rank is within accepted bounds
        if rank < 0:
            raise ValueError("Operand was expected")
        elif rank > 1:
            raise ValueError("Operator was expected")
    # Once the loop through values end, we check for remaining operators and add them to postfix
    while len(opStack) > 0:
        # Pop from stack and check valid cases
        op = opStack.pop()
        if op in matches.keys():
            raise ValueError("Incorrect matches for brackets")
        if not isUnaryOperator(op):
            rank -= 1
        if rank < 0:
            raise ValueError("Operand was expected")
        postfix.append(op)
    # Finally, return postfix expression (as a list)
    return postfix


# Evaluate function for a given postfix expression
def evaluate(postfix):
    # Init stack for operands
    opStack = []
    # Loop through postfix to find the result
    for val in postfix:
        # Check two possible cases
        if val.isnumeric():
            opStack.append(float(val))
        else:
            # We have either a binary or unary operator
            if isUnaryOperator(val):
                unique = opStack.pop()
                opStack.append(doUnaryFunction(val, unique))
            else:
                right = opStack.pop()
                left = opStack.pop()
                opStack.append(doBinaryFunction(val, left, right))
    # Finally, return the remaining result from the stack
    return opStack.pop()


print(evaluate(infixToPostfix(splitExpression("-5.78+-(4-2.23)+sin(0)*cos(1)/(1+tan(2*-ln(-3+2*(1.23+arcsin(99.111"))))










