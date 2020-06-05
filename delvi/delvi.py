import sys
from enum import Enum

class TokenType(Enum):
    Name = 0

    String = 1
    Char = 2
    Integer = 3
    Float = 4
    Bool = 5

    KwStr    = 5
    KwChar   = 6
    KwInt    = 7
    KwFloat  = 8
    KwBool   = 9

    LBrace = 10
    RBrace = 11
    LParen = 12
    RParen = 13
    LBracket = 14
    RBracket = 15

    Comma = 16
    Colon = 17
    ColonColon = 18
    Semi = 19

    Tilde  = 20
    Bar    = 21
    BarBar = 42

    LArrow = 22
    RArrow = 23
    DArrow = 24

    Dot = 25
    DotDot = 26

    Cross = 27
    Dash  = 28
    Star  = 29
    Slash = 30

    Eq   = 31
    EqEq = 32
    LtEq = 33
    GtEq = 34
    Lt   = 65
    Gt   = 66

    CrossEq = 35
    DashEq  = 36
    StarEq  = 37
    SlashEq = 38

    Bang = 39
    BangEq = 40
    
    Amp = 45
    AmpAmp = 46

    Underscore = 47

    CrossCross = 48
    DashDash = 49

    KwLet = 50
    KwReturn = 51
    KwMatch = 52
    KwFn = 53
    KwEnum = 54
    KwStruct = 55
    KwFor = 56
    KwIn = 57
    KwLoop = 58
    KwIf = 59
    KwElse = 60

    Newline = 100
    SlashSlash = 101

def single_resolve(char):
    if char == "{":
        return TokenType.LBrace
    if char == "}":
        return TokenType.RBrace
    if char == "(":
        return TokenType.LParen
    if char == ")":
        return TokenType.RParen
    if char == "[":
        return TokenType.LBracket
    if char == "]":
        return TokenType.RBracket
    if char == "~":
        return TokenType.Tilde
    if char == ";":
        return TokenType.Semi
    if char == ",":
        return TokenType.Comma
    return None

def str_get(buf, i):
    if i >= len(buf):
        return None
    return buf[i]

def tokenise(buf):
    toks = []

    cur_ptr = 0
    while True:
        cur_char = str_get(buf, cur_ptr)

        if cur_char is None:
            break
        
        single = single_resolve(cur_char)
        if single is not None:
            toks.append((single, cur_ptr, 1))
            cur_ptr += 1
            continue

        nxt_char = str_get(buf, cur_ptr + 1)

        if cur_char == ":":
            if nxt_char == ":":
                toks.append((TokenType.ColonColon, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Colon, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "|":
            if nxt_char == "|":
                toks.append((TokenType.BarBar, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Bar, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "&":
            if nxt_char == "&":
                toks.append((TokenType.AmpAmp, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Amp, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == ".":
            if nxt_char == ".":
                toks.append((TokenType.DotDot, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Dot, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "=":
            if nxt_char == "=":
                toks.append((TokenType.EqEq, cur_ptr, 2))
                cur_ptr += 2
            elif nxt_char == ">":
                toks.append((TokenType.DArrow, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Eq, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "+":
            if nxt_char == "+":
                toks.append((TokenType.CrossCross, cur_ptr, 2))
                cur_ptr += 2
            elif nxt_char == "=":
                toks.append((TokenType.CrossEq, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Cross, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "-":
            if nxt_char == "-":
                toks.append((TokenType.DashDash, cur_ptr, 2))
                cur_ptr += 2
            elif nxt_char == "=":
                toks.append((TokenType.DashEq, cur_ptr, 2))
                cur_ptr += 2
            elif nxt_char == ">":
                toks.append((TokenType.RArrow, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Dash, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "*":
            if nxt_char == "=":
                toks.append((TokenType.StarEq, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Star, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "/":
            if nxt_char == "/":
                while str_get(buf, cur_ptr) != "\n":
                    cur_ptr += 1
                cur_ptr -= 1
                continue
            elif nxt_char == "=":
                toks.append((TokenType.SlashEq, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Slash, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "<":
            if nxt_char == "=":
                toks.append((TokenType.LtEq, cur_ptr, 2))
                cur_ptr += 2
            if nxt_char == "-":
                toks.append((TokenType.LArrow, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Lt, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == ">":
            if nxt_char == "=":
                toks.append((TokenType.GtEq, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Gt, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char == "!":
            if nxt_char == "=":
                toks.append((TokenType.BangEq, cur_ptr, 2))
                cur_ptr += 2
            else:
                toks.append((TokenType.Bang, cur_ptr, 1))
                cur_ptr += 1
            continue

        if cur_char.isalnum() or cur_char == "_":
            end_ptr = cur_ptr + 1
            while True:
                peek_char = str_get(buf, end_ptr)
                if peek_char is not None and peek_char.isalnum() or peek_char == "_":
                    end_ptr += 1
                else:
                    break
            toks.append((TokenType.Name, cur_ptr, end_ptr - cur_ptr, buf[cur_ptr:end_ptr]))
            cur_ptr = end_ptr
            continue
        
        if cur_char == "\"":
            end_ptr = cur_ptr + 1
            while True:
                peek_char = str_get(buf, end_ptr)
                end_ptr += 1
                if peek_char == "\"":
                    break
            toks.append((TokenType.String, cur_ptr, end_ptr - cur_ptr, buf[cur_ptr:end_ptr]))
            cur_ptr = end_ptr
            continue

        if cur_char == "'":
            end_ptr = cur_ptr + 1
            while True:
                peek_char = str_get(buf, end_ptr)
                end_ptr += 1
                if peek_char == "'":
                    break
            toks.append((TokenType.Char, cur_ptr, end_ptr - cur_ptr, buf[cur_ptr:end_ptr]))
            cur_ptr = end_ptr
            continue

        if cur_char == "\n":
            toks.append((TokenType.Newline, cur_ptr, 1))
            cur_ptr += 1
            continue

        if cur_char.isspace():
            cur_ptr += 1
            continue

        else:
            print(cur_char)
            return


    return toks

def main():
    buf = sys.stdin.read()
    toks = tokenise(buf)
    for tok in toks:
        if tok[0].name == "Newline":
            print(); continue;
        print("{:<10}: {}".format(tok[0].name, str(tok[1:])))

if __name__ == "__main__":
    main()
