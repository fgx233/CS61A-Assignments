from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################
# 特殊形式

# Each of the following do_xxx_form functions takes the cdr of a special form as
# its first argument---a Scheme list representing a special form without the
# initial identifying symbol (if, lambda, quote, ...). Its second argument is
# the environment in which the form is to be evaluated.
# 下面每个 do_xxx_form 函数的第一个参数都是特殊形式的 cdr——即去掉开头标识符号
# (if、lambda、quote 等)之后、表示该特殊形式的 Scheme 列表。第二个参数是
# 求值该形式时所在的环境。

def do_define_form(expressions, env):
    """Evaluate a define form.
    求值 define 形式。
    >>> env = create_global_frame()
    >>> do_define_form(read_line("(x 2)"), env) # evaluating / 相当于求值 (define x 2)
    'x'
    >>> scheme_eval("x", env)
    2
    >>> do_define_form(read_line("(x (+ 2 8))"), env) # evaluating / 相当于求值 (define x (+ 2 8))
    'x'
    >>> scheme_eval("x", env)
    10
    >>> # problem 10(问题 10)
    >>> env = create_global_frame()
    >>> do_define_form(read_line("((f x) (+ x 2))"), env) # evaluating / 相当于求值 (define (f x) (+ x 8))
    'f'
    >>> scheme_eval(read_line("(f 3)"), env)
    5
    """
    validate_form(expressions, 2) # Checks that expressions is a list of length at least 2(检查 expressions 是长度至少为 2 的列表)
    signature = expressions.first
    if scheme_symbolp(signature):
        # assigning a name to a value e.g. (define x (+ 1 2))
        # 把一个名字绑定到一个值,例如 (define x (+ 1 2))
        validate_form(expressions, 2, 2) # Checks that expressions is a list of length exactly 2(检查 expressions 是长度恰好为 2 的列表)
        # BEGIN PROBLEM 4
        env.define(signature, scheme_eval(expressions.rest.first, env))
        return signature
        # END PROBLEM 4
    elif isinstance(signature, Pair) and scheme_symbolp(signature.first):
        # defining a named procedure e.g. (define (f x y) (+ x y))
        # 定义一个具名过程,例如 (define (f x y) (+ x y))
        # BEGIN PROBLEM 10
        env.define(signature.first, do_lambda_form(Pair(signature.rest, expressions.rest), env))
        return signature.first
        # END PROBLEM 10
    else:
        bad_signature = signature.first if isinstance(signature, Pair) else signature
        raise SchemeError('non-symbol: {0}'.format(bad_signature))

def do_quote_form(expressions, env):
    """Evaluate a quote form.
    求值 quote 形式。

    >>> env = create_global_frame()
    >>> do_quote_form(read_line("((+ x 2))"), env) # evaluating / 相当于求值 (quote (+ x 2))
    Pair('+', Pair('x', Pair(2, nil)))
    """
    validate_form(expressions, 1, 1)
    # BEGIN PROBLEM 5
    return expressions.first
    # END PROBLEM 5

def do_begin_form(expressions, env):
    """Evaluate a begin form.
    求值 begin 形式。

    >>> env = create_global_frame()
    >>> x = do_begin_form(read_line("((print 2) 3)"), env) # evaluating / 相当于求值 (begin (print 2) 3)
    2
    >>> x
    3
    """
    validate_form(expressions, 1)
    return eval_all(expressions, env)

def do_lambda_form(expressions, env):
    """Evaluate a lambda form.
    求值 lambda 形式。

    >>> env = create_global_frame()
    >>> do_lambda_form(read_line("((x) (+ x 2))"), env) # evaluating / 相当于求值 (lambda (x) (+ x 2))
    LambdaProcedure(Pair('x', nil), Pair(Pair('+', Pair('x', Pair(2, nil))), nil), <Global Frame>)
    """
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 7
    return LambdaProcedure(expressions.first, expressions.rest, env)
    # END PROBLEM 7

def do_if_form(expressions, env):
    """Evaluate an if form.
    求值 if 形式。

    >>> env = create_global_frame()
    >>> do_if_form(read_line("(#t (print 2) (print 3))"), env) # evaluating / 相当于求值 (if #t (print 2) (print 3))
    2
    >>> do_if_form(read_line("(#f (print 2) (print 3))"), env) # evaluating / 相当于求值 (if #f (print 2) (print 3))
    3
    """
    validate_form(expressions, 2, 3)
    if is_scheme_true(scheme_eval(expressions.first, env)):
        return scheme_eval(expressions.rest.first, env)
    elif len(expressions) == 3:
        return scheme_eval(expressions.rest.rest.first, env)

def do_and_form(expressions, env):
    """Evaluate a (short-circuited) and form.
    求值(短路的)and 形式。

    >>> env = create_global_frame()
    >>> do_and_form(read_line("(#f (print 1))"), env) # evaluating / 相当于求值 (and #f (print 1))
    False
    >>> # evaluating / 相当于求值 (and (print 1) (print 2) (print 4) 3 #f)
    >>> do_and_form(read_line("((print 1) (print 2) (print 3) (print 4) 3 #f)"), env)
    1
    2
    3
    4
    False
    """
    # BEGIN PROBLEM 12
    if expressions == nil:
        return True

    p = expressions
    while p != nil:
        ret = scheme_eval(p.first, env)
        if is_scheme_false(ret):
            return ret
        p = p.rest
    return ret
    # END PROBLEM 12

def do_or_form(expressions, env):
    """Evaluate a (short-circuited) or form.
    求值(短路的)or 形式。

    >>> env = create_global_frame()
    >>> do_or_form(read_line("(10 (print 1))"), env) # evaluating / 相当于求值 (or 10 (print 1))
    10
    >>> do_or_form(read_line("(#f 2 3 #t #f)"), env) # evaluating / 相当于求值 (or #f 2 3 #t #f)
    2
    >>> # evaluating / 相当于求值 (or (begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))
    >>> do_or_form(read_line("((begin (print 1) #f) (begin (print 2) #f) 6 (begin (print 3) 7))"), env)
    1
    2
    6
    """
    # BEGIN PROBLEM 12
    if expressions == nil:
            return False
    
    p = expressions
    while p != nil:
        ret = scheme_eval(p.first, env)
        if is_scheme_true(ret):
            return ret
        p = p.rest
    return ret
    # END PROBLEM 12

def do_cond_form(expressions, env):
    """Evaluate a cond form.
    求值 cond 形式。

    >>> do_cond_form(read_line("((#f (print 2)) (#t 3))"), create_global_frame())
    3
    """
    while expressions is not nil:
        clause = expressions.first
        validate_form(clause, 1)
        if clause.first == 'else':
            test = True
            if expressions.rest != nil:
                raise SchemeError('else must be last')
        else:
            test = scheme_eval(clause.first, env)
        if is_scheme_true(test):
            # BEGIN PROBLEM 13
            if clause.rest == nil:
                return test
            return eval_all(clause.rest, env)
            # END PROBLEM 13
        expressions = expressions.rest
    # return None

def do_let_form(expressions, env):
    """Evaluate a let form.
    求值 let 形式。

    >>> env = create_global_frame()
    >>> do_let_form(read_line("(((x 2) (y 3)) (+ x y))"), env)
    5
    """
    validate_form(expressions, 2)
    let_env = make_let_frame(expressions.first, env)
    return eval_all(expressions.rest, let_env)

def make_let_frame(bindings, env):
    """Create a child frame of Frame ENV that contains the definitions given in
    BINDINGS. The Scheme list BINDINGS must have the form of a proper bindings
    list in a let expression: each item must be a list containing a symbol
    and a Scheme expression.
    创建帧 ENV 的一个子帧,其中包含 BINDINGS 给出的定义。Scheme 列表 BINDINGS
    必须符合 let 表达式中绑定列表的格式:每一项都是一个包含一个符号和
    一个 Scheme 表达式的列表。"""
    if not scheme_listp(bindings):
        raise SchemeError('bad bindings list in let form')
    names = vals = nil
    # BEGIN PROBLEM 14
    while bindings != nil:
        expr = bindings.first
        validate_form(expr, 2, 2)
        names = Pair(expr.first, names)
        vals = Pair(scheme_eval(expr.rest.first, env), vals)
        bindings = bindings.rest
    validate_formals(names)
    
    # END PROBLEM 14
    return env.make_child_frame(names, vals)



def do_quasiquote_form(expressions, env):
    """Evaluate a quasiquote form with parameters EXPRESSIONS in
    Frame ENV.
    在帧 ENV 中求值参数为 EXPRESSIONS 的 quasiquote 形式。"""
    def quasiquote_item(val, env, level):
        """Evaluate Scheme expression VAL that is nested at depth LEVEL in
        a quasiquote form in Frame ENV.
        在帧 ENV 中求值 Scheme 表达式 VAL,VAL 位于 quasiquote 形式中
        嵌套深度为 LEVEL 的位置。"""
        if not scheme_pairp(val):
            return val
        if val.first == 'unquote':
            level -= 1
            if level == 0:
                expressions = val.rest
                validate_form(expressions, 1, 1)
                return scheme_eval(expressions.first, env)
        elif val.first == 'quasiquote':
            level += 1

        return val.map(lambda elem: quasiquote_item(elem, env, level))

    validate_form(expressions, 1, 1)
    return quasiquote_item(expressions.first, env, 1)

def do_unquote(expressions, env):
    raise SchemeError('unquote outside of quasiquote')


#################
# Dynamic Scope #
#################
# 动态作用域

def do_mu_form(expressions, env):
    """Evaluate a mu form.
    求值 mu 形式。"""
    validate_form(expressions, 2)
    formals = expressions.first
    validate_formals(formals)
    # BEGIN PROBLEM 11
    return MuProcedure(formals, expressions.rest)
    # END PROBLEM 11



SPECIAL_FORMS = {
    'and': do_and_form,
    'begin': do_begin_form,
    'cond': do_cond_form,
    'define': do_define_form,
    'if': do_if_form,
    'lambda': do_lambda_form,
    'let': do_let_form,
    'or': do_or_form,
    'quote': do_quote_form,
    'quasiquote': do_quasiquote_form,
    'unquote': do_unquote,
    'mu': do_mu_form,
}