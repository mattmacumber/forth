#!/usr/bin/env python

import sys


class Forth():
    def __init__(self):
        self.stack = list()
        self.dictionary = dict()

    def eval(self, symbols):
        while len(symbols) > 0:
            symbol = symbols.pop(0)
            if symbol not in self.dictionary and not symbol.startswith('."') and symbol not in '. : CR DUP DROP TUCK OVER ROT IF I AND OR NOT MOD < > = 0= + - * / SPACES DO BEGIN WHILE REPEAT EMIT'.split() and not symbol.isdecimal():
                raise "UNKNOWN INSTRUCTION "
            try:
                if symbol == 'I':
                    symbol = str(self.stack[-1])

                if symbol.isdecimal():
                    self.stack.append(int(symbol))
                if symbol == ".":
                    print(self.stack.pop(), end=' ')
                if symbol == ".S":
                    print("<", len(self.stack), ">", self.stack, end=' ')

                if symbol == "CR":
                    print("")
                if symbol == "SPACES":
                    print(" "*self.stack.pop(), end='')
                if symbol == "SPACE":
                    print(" ", end='')

                if symbol == "EMIT":
                    print(chr(self.stack.pop()), end=' ')
                if symbol.startswith('."'):
                    print(symbol[2:-1], end=' ')

                if symbol == "+":
                    val = self.stack.pop() + self.stack.pop()
                    self.stack.append(val)
                if symbol == "-":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = b - a
                    self.stack.append(val)
                if symbol == "*":
                    val = self.stack.pop() * self.stack.pop()
                    self.stack.append(val)
                if symbol == "/":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = int(b / a)
                    self.stack.append(val)

                if symbol == "<":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = 1 if b < a else 0
                    self.stack.append(val)
                if symbol == ">":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = 1 if b > a else 0
                    self.stack.append(val)
                if symbol == "=":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = 1 if a == b else 0
                    self.stack.append(val)
                if symbol == "0=":
                    a = self.stack.pop()
                    val = 1 if a == 0 else 0
                    self.stack.append(val)

                if symbol == "NOT":
                    a = self.stack.pop()
                    val = 1 if a != 0 else 0
                    self.stack.append(val)

                if symbol == "AND":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a and b)

                if symbol == "OR":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a or b)

                if symbol == "SWAP":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                if symbol == "2SWAP":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    c = self.stack.pop()
                    d = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                    self.stack.append(c)
                    self.stack.append(d)

                if symbol == "DUP":
                    self.stack.append(self.stack[-1])
                if symbol == "2DUP":
                    self.stack.append(self.stack[-1])

                if symbol == "ROT":
                    self.stack[-3], self.stack[-2], self.stack[-1] = self.stack[-2], self.stack[-1], self.stack[-3]

                if symbol == "TUCK":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    self.stack.append(a)
                    self.stack.append(b)
                    self.stack.append(a)

                if symbol == "OVER":
                    self.stack.append(self.stack[-2])

                if symbol == "DROP":
                    self.stack.pop()
                if symbol == "2DROP":
                    self.stack.pop()
                    self.stack.pop()

                if symbol == "MOD":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = b % a
                    self.stack.append(val)

                if symbol == "/MOD":
                    a = self.stack.pop()
                    b = self.stack.pop()
                    val = b % a
                    self.stack.append(val)
                    val = int(b / a)
                    self.stack.append(val)

                if symbol == "DO":
                    index = self.stack[-1]
                    limit = self.stack[-2]
                    # self.stack.append(limit)
                    # self.stack.append(index)
                    body = list()
                    while symbols[0] != 'LOOP':
                        s = symbols.pop(0)
                        body.append(s)
                    symbols.pop(0)  # drop the LOOP

                    while index != limit:
                        self.eval(body.copy())
                        index = self.stack.pop()+1
                        limit = self.stack.pop()
                        self.stack.append(limit)
                        self.stack.append(index)

                if symbol == "IF":
                    cond = self.stack.pop()

                    body = list()
                    val = symbols.pop(0)
                    while val != "THEN" and val != "ELSE":
                        body.append(val)
                        val = symbols.pop(0)

                    if len(symbols) > 0:
                        val = symbols.pop(0)

                    body2 = list()

                    while val != "THEN":
                        body2.append(val)
                        val = symbols.pop(0)

                    if cond != 0:
                        self.eval(body)
                    else:
                        self.eval(body2)

                if symbol in self.dictionary:
                    self.eval(self.dictionary[symbol].copy())

                if symbol == ":":
                    name = symbols.pop(0)
                    body = list()
                    while symbols[0] != ';':
                        s = symbols.pop(0)
                        body.append(s)
                    symbols.pop()  # drop the ;
                    self.dictionary[name] = body

            except IndexError as e:
                print(e)

        sys.stdout.flush()

        return None


def repl():
    forth = Forth()
    line = "OK"
    while line != '':
        line = sys.stdin.readline().strip()
        forth.eval(line.split())


if __name__ == "__main__":
    # repl()
    forth = Forth()

    prog = ['10 0 DO CR ."Hello" LOOP CR',
            ': STAR 42 EMIT ;',
            ': STARS 0 DO STAR LOOP ;',
            ': MARGIN CR 8 SPACES ;',
            ': BLIP MARGIN STAR ;',
            ': BAR MARGIN 5 STARS ;',
            ': F BAR BLIP BAR BLIP BLIP CR ;',
            'F',
            ': FLOOR5  DUP 6 < IF DROP 5 ELSE 1 - THEN ;',
            '1 FLOOR5 CR .',
            ' 8 FLOOR5 CR .',
            '5 12 > IF ."Bigger" THEN',
            '15 12 > IF ."Bigger" THEN',
            '1 DUP 6 < IF DROP 5 ELSE 1 - THEN CR .',
            '8 DUP 6 < IF DROP 5 ELSE 1 - THEN CR .',
            ': BOXTEST 6 > ROT 22 > ROT 19 > AND AND IF ."Big_enough" THEN ;',
            '23 20 7 BOXTEST',

            ': Fizz? 3 MOD 0= DUP IF ."Fizz" THEN ;',
            ': Buzz? 5 MOD 0= DUP IF ."Buzz" THEN ;',
            ': ?print IF . THEN ;',
            ': FizzBuzz 101 1 DO CR  I  DUP Fizz? OVER Buzz? OR  NOT ?print LOOP ;',
            'FizzBuzz',

            ': n         DUP .         1 + ;',
            ': f         ."Fizz"     1 + ;',
            ': b         ."Buzz"     1 + ;',
            ': fb        ."FizzBuzz" 1 + ;',
            ': fb10     n n f n b f n n f b ;',
            ': fb15     fb10 n f n n fb ;',
            ': fb100   fb15 fb15 fb15 fb15 fb15 fb15 fb10 ;',
            ': fizzbuzz      1 fb100 DROP ;',
            'fizzbuzz',
            ': gcd BEGIN DUP WHILE TUCK MOD REPEAT DROP ;',
            '51 34 gcd .',

            ': ?print IF . THEN ;',
            ': .set BEGIN DUP WHILE ?print >R 1 + R> 1 RSHIFT REPEAT DROP DROP ;',
            ': .powerset 0 DO ."(" 1 I .set .")" CR LOOP ;',
            ': powerset 1 3 .powerset ;',
            '3 2 1 powerset',


            ': perfect? 1 OVER 2 / 1 + 2 DO OVER I MOD 0 = IF I + THEN LOOP = ;',
            ' 6 perfect?',
            #' 31 perfect?',
            #' 33550336 perfect?',
            ]

    RC4 = """0 value ii        0 value jj
0 value KeyAddr   0 value KeyLen
create SArray   256 allot   ( state array of 256 bytes )
: KeyArray      KeyLen mod   KeyAddr ;

: get_byte      + c@ ;
: set_byte      + c! ;
: as_byte       255 and ;
: reset_ij      0 TO ii   0 TO jj ;
: i_update      1 +   as_byte TO ii ;
: j_update      ii SArray get_byte +   as_byte TO jj ;
: swap_s_ij
    jj SArray get_byte
       ii SArray get_byte  jj SArray set_byte
    ii SArray set_byte
;

: rc4_init ( KeyAddr KeyLen -- )
    256 min TO KeyLen   TO KeyAddr
    256 0 DO   i i SArray set_byte   LOOP
    reset_ij
    BEGIN
        ii KeyArray get_byte   jj +  j_update
        swap_s_ij
        ii 255 < WHILE
        ii i_update
    REPEAT
    reset_ij
;
: rc4_byte
    ii i_update   jj j_update
    swap_s_ij
    ii SArray get_byte   jj SArray get_byte +   as_byte SArray get_byte  xor
;"""

    for line in prog[:8]:
        forth.eval(line.split())
