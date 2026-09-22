import builtins

from pair import *

class SchemeError(Exception):
    """Exception indicating an error in a Scheme program.
    表示 Scheme 程序出错的异常。"""

################
# Environments #
################
# 环境

class Frame:
    """An environment frame binds Scheme symbols to Scheme values.
    环境帧把 Scheme 符号绑定到 Scheme 值。"""

    def __init__(self, parent):
        """An empty frame with parent frame PARENT (which may be None).
        一个空帧,其父帧为 PARENT(可以为 None)。"""
        self.bindings = {}
        self.parent = parent

    def __repr__(self):
        if self.parent is None:
            return '<Global Frame>'
        s = sorted(['{0}: {1}'.format(k, v) for k, v in self.bindings.items()])
        return '<{{{0}}} -> {1}>'.format(', '.join(s), repr(self.parent))

    def define(self, symbol, value):
        """Define Scheme SYMBOL to have VALUE.
        在本帧中把 Scheme 符号 SYMBOL 定义为 VALUE。"""
        # BEGIN PROBLEM 1
        self.bindings[symbol] = value
        # END PROBLEM 1

    def lookup(self, symbol):
        """Return the value bound to SYMBOL. Errors if SYMBOL is not found.
        返回绑定到 SYMBOL 的值。若找不到 SYMBOL 则报错。"""
        # BEGIN PROBLEM 1
        p = self
        while p != None:
            if symbol in p.bindings:
                return p.bindings[symbol]
            else:
                p = p.parent
        # END PROBLEM 1
        raise SchemeError('unknown identifier: {0}'.format(symbol))


    def make_child_frame(self, formals, vals):
        """Return a new local frame whose parent is SELF, in which the symbols
        in a Scheme list of formal parameters FORMALS are bound to the Scheme
        values in the Scheme list VALS. Both FORMALS and VALS are represented
        as Pairs. Raise an error if too many or too few vals are given.
        返回一个以 SELF 为父帧的新局部帧,其中把 Scheme 列表 FORMALS 中的形参符号
        依次绑定到 Scheme 列表 VALS 中的值。FORMALS 和 VALS 都以 Pair 表示。
        若给的值过多或过少则报错。

        >>> env = create_global_frame()
        >>> formals, expressions = read_line('(a b c)'), read_line('(1 2 3)')
        >>> env.make_child_frame(formals, expressions)
        <{a: 1, b: 2, c: 3} -> <Global Frame>>
        """
        if len(formals) != len(vals):
            raise SchemeError('Incorrect number of arguments to function call')
        # BEGIN PROBLEM 8
        frame = Frame(self)
        while formals != nil:
            frame.define(formals.first, vals.first)
            formals, vals = formals.rest, vals.rest
        return frame
        # END PROBLEM 8

##############
# Procedures #
##############
# 过程

class Procedure:
    """The the base class for all Procedure classes.
    所有过程类的基类。"""

class BuiltinProcedure(Procedure):
    """A Scheme procedure defined as a Python function.
    用 Python 函数定义的 Scheme 过程(内置过程)。"""

    def __init__(self, py_func, need_env=False, name='builtin'):
        self.name = name
        self.py_func = py_func
        self.need_env = need_env

    def __str__(self):
        return '#[{0}]'.format(self.name)

class LambdaProcedure(Procedure):
    """A procedure defined by a lambda expression or a define form.
    由 lambda 表达式或 define 形式定义的过程。"""

    def __init__(self, formals, body, env):
        """A procedure with formal parameter list FORMALS (a Scheme list),
        whose body is the Scheme list BODY, and whose parent environment
        starts with Frame ENV.
        一个过程:形参列表为 FORMALS(Scheme 列表),函数体为 Scheme 列表 BODY,
        其父环境从帧 ENV 开始。"""
        assert isinstance(env, Frame), "env must be of type Frame"

        from scheme_utils import validate_type, scheme_listp
        validate_type(formals, scheme_listp, 0, 'LambdaProcedure')
        validate_type(body, scheme_listp, 1, 'LambdaProcedure')
        self.formals = formals
        self.body = body
        self.env = env

    def __str__(self):
        return str(Pair('lambda', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'LambdaProcedure({0}, {1}, {2})'.format(
            repr(self.formals), repr(self.body), repr(self.env))

class MuProcedure(Procedure):
    """A procedure defined by a mu expression, which has dynamic scope.
    由 mu 表达式定义的过程,采用动态作用域。
     _________________
    < Scheme is cool! >
     -----------------
            \   ^__^
             \  (oo)\_______
                (__)\       )\/\
                    ||----w |
                    ||     ||
    """

    def __init__(self, formals, body):
        """A procedure with formal parameter list FORMALS (a Scheme list) and
        Scheme list BODY as its definition.
        一个过程:形参列表为 FORMALS(Scheme 列表),定义体为 Scheme 列表 BODY。"""
        self.formals = formals
        self.body = body

    def __str__(self):
        return str(Pair('mu', Pair(self.formals, self.body)))

    def __repr__(self):
        return 'MuProcedure({0}, {1})'.format(
            repr(self.formals), repr(self.body))
