"""The scheme_tokens module provides functions tokenize_line and tokenize_lines
for converting (iterators producing) strings into (iterators producing) lists
of tokens.  A token may be:

  * A number (represented as an int or float)
  * A boolean (represented as a bool)
  * A symbol (represented as a string)
  * A delimiter, including parentheses, dots, and single quotes

This file also includes some features of Scheme that have not been addressed
in the course, such as Scheme strings.

scheme_tokens 模块提供 tokenize_line 和 tokenize_lines 两个函数,用于把字符串
(或产生字符串的迭代器)转换成词法单元(token)列表(或产生列表的迭代器)。
一个 token 可以是:

  * 数字(用 int 或 float 表示)
  * 布尔值(用 bool 表示)
  * 符号(用字符串表示)
  * 分隔符,包括括号、点和单引号

本文件还包含一些课程中未涉及的 Scheme 特性,例如 Scheme 字符串。
"""

from ucb import main
import sys

_NUMERAL_STARTS = set("0123456789") | set('+-.')
_SYMBOL_CHARS = (set('!$%&*/:<=>?@^_~') | set("abcdefghijklmnopqrstuvwxyz") |
                 set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") | _NUMERAL_STARTS)
_STRING_DELIMS = set('"')
_WHITESPACE = set(' \t\n\r')
_SINGLE_CHAR_TOKENS = set("()[]'`")
_TOKEN_END = _WHITESPACE | _SINGLE_CHAR_TOKENS | _STRING_DELIMS | {',', ',@'}
DELIMITERS = _SINGLE_CHAR_TOKENS | {'.', ',', ',@'}
_MAX_TOKEN_LENGTH = 50


def chain(*iters):
    for iter in iters:
        yield from iter


def valid_symbol(s):
    """Returns whether s is a well-formed symbol.
    返回 s 是否是一个格式良好的符号。"""
    if len(s) == 0:
        return False
    for c in s:
        if c not in _SYMBOL_CHARS:
            return False
    return True

def next_candidate_token(line, k):
    """A tuple (tok, k'), where tok is the next substring of line at or
    after position k that could be a token (assuming it passes a validity
    check), and k' is the position in line following that token.  Returns
    (None, len(line)) when there are no more tokens.
    返回元组 (tok, k'):tok 是 line 中位置 k 及之后、可能成为一个 token 的
    下一个子串(假定它能通过合法性检查),k' 是该 token 之后的位置。
    没有更多 token 时返回 (None, len(line))。"""
    while k < len(line):
        c = line[k]
        if c == ';':
            return None, len(line)
        elif c in _WHITESPACE:
            k += 1
        elif c in _SINGLE_CHAR_TOKENS:
            if c == ']': c = ')'
            if c == '[': c = '('
            return c, k+1
        elif c == '#':  # Boolean values #t and #f(布尔值 #t 和 #f)
            return line[k:k+2], min(k+2, len(line))
        elif c == ',': # Unquote; check for @(unquote;检查后面是否跟着 @)
            if k+1 < len(line) and line[k+1] == '@':
                return ',@', k+2
            return c, k+1
        elif c in _STRING_DELIMS:
            if k+1 < len(line) and line[k+1] == c: # No triple quotes in Scheme(Scheme 中没有三引号)
                return c+c, k+2
            s = ""
            k += 1
            while k < len(line):
                c = line[k]
                if c == "\"":
                    check_token_length_warning(s, len(s) + 2)
                    return "\"" + s + "\"", k+1
                elif c == "\\":
                    if k + 1 == len(line):
                        raise SyntaxError("String ended abruptly")
                    next = line[k + 1]
                    if next == "n":
                        s += "\n"
                    else:
                        s += next
                    k += 2
                else:
                    s += c
                    k += 1
            raise SyntaxError("String ended abruptly")
        else:
            j = k
            while j < len(line) and line[j] not in _TOKEN_END:
                j += 1
            check_token_length_warning(line[k:j], min(j, len(line)) - k)
            return line[k:j], min(j, len(line))
    return None, len(line)

def tokenize_line(line):
    """The list of Scheme tokens on line.  Excludes comments and whitespace.
    返回 line 中的 Scheme token 列表。不包括注释和空白。"""
    result = []
    text, i = next_candidate_token(line, 0)
    while text is not None:
        if text in DELIMITERS:
            result.append(text)
        elif text == '#t' or text.lower() == 'true':
            result.append(True)
        elif text == '#f' or text.lower() == 'false':
            result.append(False)
        elif text == 'nil':
            result.append(text)
        elif text[0] in _SYMBOL_CHARS:
            number = False
            if text[0] in _NUMERAL_STARTS:
                try:
                    result.append(int(text))
                    number = True
                except ValueError:
                    try:
                        result.append(float(text))
                        number = True
                    except ValueError:
                        pass
            if not number:
                if valid_symbol(text):
                    result.append(text.lower())
                else:
                    raise ValueError("invalid numeral or symbol: {0}".format(text))
        elif text[0] in _STRING_DELIMS:
            result.append(text)
        else:
            error_message = [
                "warning: invalid token: {0}".format(text),
                " " * 4       + line,
                " " * (i + 4) + "^"
            ]
            raise ValueError("\n".join(error_message))
        text, i = next_candidate_token(line, i)
    return result

def check_token_length_warning(token, length):
    if length > _MAX_TOKEN_LENGTH:
        import warnings
        warnings.warn("Token {} has exceeded the maximum token length {}".format(token, _MAX_TOKEN_LENGTH, length))

def tokenize_lines(inp):
    """An iterator over lists of tokens, one for each line of the iterable
    input sequence inp.
    返回一个迭代器,对可迭代输入 inp 的每一行产生一个 token 列表。"""
    return (tokenize_line(line) for line in inp)

def count_tokens(inp):
    """Count the number of non-delimiter tokens in inp.
    统计 inp 中非分隔符 token 的数量。"""
    return len(list(chain(*tokenize_lines(inp))))

@main
def run(*args):
    import argparse
    parser = argparse.ArgumentParser(description='Count Scheme tokens.')
    parser.add_argument('file', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input file to be counted')
    args = parser.parse_args()
    print('counted', count_tokens(args.file), 'tokens')