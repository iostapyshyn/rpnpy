#!/usr/bin/env python3
""" Evaluate given RPN expression. """

import math
import random
import expression

try:
    import readline
    readline.clear_history()
except ImportError:
    pass

class RPNCalculator:
    """ Reverse Polish Notation calculator. """
    # Variable ans holds result of last operation.
    ans = 0
    def operator(self, tok):
        """ Return operator handler if tok is a valid operator. Otherwise return False. """
        def stacksum(stack):
            """ Return sum of all elements on stack (++ operator). """
            acc = 0
            while stack:
                acc += stack.pop()
            return acc

        def stackproduct(stack):
            """ Return product of all elements on stack (** operator). """
            acc = 1
            while stack:
                acc *= stack.pop()
            return acc

        # Operator handlers.
        operators = {
            '++': stacksum,
            '**': stackproduct,
            '+': lambda stack: stack.pop(-2) + stack.pop(),
            '-': lambda stack: stack.pop(-2) - stack.pop(),
            '*': lambda stack: stack.pop(-2) * stack.pop(),
            '/': lambda stack: stack.pop(-2) / stack.pop(),
            '%': lambda stack: stack.pop(-2) % stack.pop(),
            '^': lambda stack: stack.pop(-2) ** stack.pop(),
            '!': lambda stack: math.factorial(stack.pop()),
            'ln': lambda stack: math.log(stack.pop()),
            'log': lambda stack: math.log(stack.pop(-2), stack.pop()),
            'log2': lambda stack: math.log(stack.pop(), 2),
            'log10': lambda stack: math.log(stack.pop(), 10),
            'rand': lambda stack: random.random(),
            'sqrt': lambda stack: math.sqrt(stack.pop()),
            'exp': lambda stack: math.exp(stack.pop()),
            'sin': lambda stack: math.sin(stack.pop()),
            'cos': lambda stack: math.cos(stack.pop()),
            'tan': lambda stack: math.tan(stack.pop()),
            'sinh': lambda stack: math.sinh(stack.pop()),
            'cosh': lambda stack: math.cosh(stack.pop()),
            'tanh': lambda stack: math.tanh(stack.pop()),
            'arcsin': lambda stack: math.asin(stack.pop()),
            'arccos': lambda stack: math.acos(stack.pop()),
            'arctan': lambda stack: math.atan(stack.pop()),
            'arcsinh': lambda stack: math.asinh(stack.pop()),
            'arccosh': lambda stack: math.acosh(stack.pop()),
            'arctanh': lambda stack: math.atanh(stack.pop()),
            'max': lambda stack: max(stack.pop(), stack.pop()),
            'min': lambda stack: min(stack.pop(), stack.pop()),
            'abs': lambda stack: abs(stack.pop()),
            'ans': lambda stack: self.ans,
        }

        # Return operation handler if exists, otherwise return False.
        if tok in operators:
            return operators[tok]
        return False

    def eval(self, expr, stack=None):
        """ Evaluate RPN expression and return result. """
        if stack is None:
            stack = []
        for token in expr:
            # If token is a valid number, push to stack.
            if token.type == 'Literal':
                stack.append(token.value)

            elif token.type == 'Constant':
                if token.value == 'e':
                    stack.append(math.e)
                elif token.value == 'pi':
                    stack.append(math.pi)

            # If token is an operator, execute the operation.
            elif token.type == 'Operator' or token.type == 'Function':
                operation = self.operator(token.value)
                if not operation:
                    raise SyntaxError(f'unknown operator/function: "{token.value}"')

                self.ans = operation(stack)
                stack.append(self.ans)

            elif token.type == 'Separator':
                continue

            # Otherwise, raise exception.
            else: raise SyntaxError(f'unexpected {token.type}: "{token.value}"')

        if len(stack) != 1:
            raise Warning('there should be exactly one element left on stack')
        return stack

def interactive():
    """ Interactive mode. """
    calc = RPNCalculator()
    stack = []
    while True:
        try:
            expr = input('=> ')
            if expr in ['quit', 'exit']:
                break
            elif expr == 'pop':
                stack.pop()
            elif expr == 'clear':
                stack = []
            else: stack = calc.eval(expression.tokenize(expr), stack)
        except Warning:
            # Ignore that there is more than one element left on stack.
            pass
        except (SyntaxError, IndexError, ZeroDivisionError) as error:
            # Print error if occurred and continue.
            print(f'Error: {error}')
        except (KeyboardInterrupt, EOFError):
            print()
            break
        finally:
            # Print out the stack.
            for i, num in enumerate(stack):
                print('{:2<}: {}'.format(i, round(num, 6)))

def main():
    """ Run interactive mode. """
    interactive()

if __name__ == '__main__':
    main()
