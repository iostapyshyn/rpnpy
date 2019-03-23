#!/usr/bin/env python3

import collections
import rpn

Token = collections.namedtuple("Token", "type value")
Operator = collections.namedtuple("Operator", "prec assoc")

OPS = {
    '+': Operator(2, 'L'),
    '-': Operator(2, 'L'),
    '/': Operator(3, 'L'),
    '*': Operator(3, 'L'),
    '^': Operator(4, 'R'),
}

def tokenize(expr):
    """Splits mathematical expression into tokens."""
    tokens = []

    letter_buffer = []
    number_buffer = []

    def empty_buffers():
        nonlocal letter_buffer
        if letter_buffer:
            token = ''.join(letter_buffer)
            if token in ['e', 'pi']:
                tokens.append(Token('Constant', token))
            else:
                tokens.append(Token('Function', token))
            letter_buffer = []
        nonlocal number_buffer
        if number_buffer:
            if number_buffer == ['-']:
                tokens.append(Token('Operator', '-'))
            tokens.append(Token('Literal', float(''.join(number_buffer))))
            number_buffer = []

    for char in expr:
        if char.isdigit() or char in set('-.'):
            number_buffer.append(char)
        elif char.isalpha():
            if number_buffer:
                empty_buffers()
            letter_buffer.append(char)
        elif char in OPS:
            empty_buffers()
            tokens.append(Token('Operator', char))
        elif char in set('(['):
            empty_buffers()
            tokens.append(Token('LParen', char))
        elif char in set(')]'):
            empty_buffers()
            tokens.append(Token('RParen', char))
        elif char == ',':
            empty_buffers()
            tokens.append(Token('Separator', char))
        elif char.isspace():
            empty_buffers()
        else: raise SyntaxError('unexpected "{}"'.format(char))

    empty_buffers()

    return tokens

def shunting_yard(expr):
    """Shunting-yard algorithm implementation."""
    output = []
    stack = []
    for token in expr:
        if token.type in ['Literal', 'Constant']:
            # If token is a number, add to output queue.
            output.append(token)

        elif token.type == 'Function':
            # If token is a function, push to operator stack.
            stack.append(token)

        elif token.type == 'Separator':
            # If token is a function argument separator,
            # pop operators from stack into output queue until left bracket appears.
            while stack and stack[-1].type != 'LParen':
                output.append(stack.pop())
            if not stack:
                # If left bracket was not found, there are mismatched parentheses.
                raise SyntaxError("mismatched parentheses")

        elif token.type == 'Operator':
            # If token is an operator
            while (stack and stack[-1].type == 'Operator' and
                   # If operator is left associative and its precendence is less or equal than
                   # precendence of operators on stack.
                   (OPS[token.value].assoc == 'L' and
                    OPS[token.value].prec <= OPS[stack[-1].value].prec) or
                   # Or operator is right associative and its precendence is less than
                   # precendence of operators on stack.
                   (OPS[token.value].assoc == 'R' and
                    OPS[token.value].prec < OPS[stack[-1].value].prec)):
                # Pop operators from stack into output queue.
                output.append(stack.pop())
            # Add operator to output queue.
            stack.append(token)

        elif token.type == 'LParen':
            # If token is a left bracket, add it to output queue.
            stack.append(token)

        elif token.type == 'RParen':
            # If token is a right bracket, pop operators from stack
            # into output queue until left bracket is found.
            while (stack and stack[-1].type != 'LParen'):
                output.append(stack.pop())

            # Remove left bracket from stack, or raise exception if bracket is missing.
            if stack[-1].type == 'LParen':
                stack.pop()
            else: raise SyntaxError('mismatched parentheses')

            if stack and stack[-1].type == 'Function':
                # If there is a function on top of the stack, pop it into output queue.
                output.append(stack.pop())

    # Pop remaining operators from stack into output queue.
    while stack:
        if stack[-1].type in ['LParen', 'RParen']:
            # If there are bracket left on stack, there are mismatched parentheses.
            raise SyntaxError('mismatched parentheses')
        output.append(stack.pop())

    return output

def main():
    tokens = tokenize(input(" => "))
    rpnexpr = shunting_yard(tokens)
    print("RPN:")
    for token in rpnexpr:
        print(f'{token.value}', end=' ')
    print(" => ", rpn.RPNCalculator().eval(rpnexpr))

if __name__ == '__main__':
    main()
