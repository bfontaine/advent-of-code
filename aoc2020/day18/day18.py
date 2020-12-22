from typing import Optional


class Token:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value

    def __str__(self):
        if self.value is None:
            return self.name

        return f"{self.name}({self.value})"


TOKENS = {
    '(': 'LPAREN',
    ')': 'RPAREN',
    '*': 'STAR',
    '+': 'PLUS',
}


def apply_op(tok: Token, term1, term2):
    print(term1, tok, term2)
    if tok.name == 'PLUS':
        return term1 + term2
    # STAR
    return term1 * term2


def tokenize_operation(s):
    tokens = []
    current_number = ""

    for c in s:
        if c in {'(', ')', '*', '+', ' '}:
            if current_number:
                tokens.append(Token('INT', int(current_number)))
                current_number = ""

            if c != ' ':
                tokens.append(Token(TOKENS[c]))
            continue

        # number
        current_number += c

    if current_number:
        tokens.append(Token('INT', int(current_number)))

    return tokens


"""
homework := expression

Problem #1:
  expression := term | expression '+' term | expression '*' term
  term := <int> | '(' expression ')'

Problem #2:
  expression := sub_expression | expression '*' sub_expression
  sub_expression := term | sub_expression '+' term
  term := <int> | '(' expression ')'
"""


class Interpreter:
    def __init__(self, tokens, advanced_maths=False):
        self.advanced_maths = advanced_maths
        self.tokens = list(reversed(tokens))  # to allow .pop()
        self.current_token: Optional[Token] = None
        self.next_token()

        # operations supported at the 'expression' level (lower priority)
        self._expression_operations = {'STAR', } if self.advanced_maths else {'PLUS', 'STAR'}

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop()
        else:
            self.current_token = Token('EOF')
        print("TOKEN", self.current_token)

    def expression(self):
        total = self.sub_expression()

        while self.current_token.name in self._expression_operations:
            operation = self.current_token
            self.next_token()
            n2 = self.sub_expression()
            total = apply_op(operation, total, n2)

        return total

    def sub_expression(self):
        total = self.term()

        if not self.advanced_maths:
            return total

        while self.current_token.name == 'PLUS':
            self.next_token()
            total += self.term()

        return total

    def homework(self):
        result = self.expression()
        if self.current_token.name != 'EOF':
            raise Exception("Expected EOF, got %s" % self.current_token)

        return result

    def term(self):
        if self.current_token.name == 'LPAREN':
            self.next_token()  # LPAREN
            result = self.expression()
            self.next_token()  # RPAREN
            return result

        if self.current_token.name == 'INT':
            result = self.current_token.value
            self.next_token()
            return result

        raise Exception("Expected LPAREN or INT, got %s" % self.current_token)


def read_homework(filename):
    operations_tokens = []
    with open(filename) as f:
        for line in f:
            operations_tokens.append(tokenize_operation(line.strip()))

    return operations_tokens


def run(problem, homework):
    advanced_maths = problem == 2
    print(sum(Interpreter(tokens, advanced_maths=advanced_maths).homework() for tokens in homework))


if __name__ == '__main__':
    run(2, read_homework("input.txt"))
