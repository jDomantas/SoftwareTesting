import sys


class ParseError(Exception):
    def __init__(self, message):
        super(ParseError, self).__init__(message)


class Parser:
    def __init__(self, source):
        self.tokens = (source
            .replace('(', ' ( ')
            .replace(')', ' ) ')
            .replace('.', ' . ')
            .replace("'", " ' ")
            .split())
        self.pos = 0

    def peek(self):
        if self.is_at_end():
            return None
        else:
            return self.tokens[self.pos]

    def advance(self):
        self.pos += 1

    def consume(self):
        tok = self.peek()
        self.advance()
        return tok
        
    def is_at_end(self):
        return self.pos >= len(self.tokens)

    def parse_term(self):
        tok = self.consume()
        if tok is None:
            raise ParseError('expected term, got eof')
        if tok == '(':
            return self.finish_list()
        elif tok == '.':
            raise ParseError('unexpected "."')
        elif tok == "'":
            term = self.parse_term()
            return ('quote', (term, None))
        else:
            try:
                return int(tok)
            except ValueError:
                return tok

    def finish_list(self):
        if self.peek() == '.':
            self.advance()
            cdr = self.parse_term()
            if self.consume() != ')':
                raise ParseError('expected ")" after cdr')
            return cdr
        elif self.peek() == ')':
            self.advance()
            return None
        else:
            term = self.parse_term()
            rest = self.finish_list()
            return (term, rest)


class UnboundSymbol(Exception):
    def __init__(self, symbol):
        message = 'unbound symbol: {}'.format(symbol)
        super(UnboundSymbol, self).__init__(message)


class Env:
    def __init__(self, parent=None):
        self.parent = parent
        if parent is None:
            self.globals = self
        else:
            self.globals = self.parent.globals
        self.env = dict()

    def lookup(self, symbol):
        if symbol in self.env:
            return self.env[symbol]
        elif self.parent is None:
            raise UnboundSymbol(symbol)
        else:
            return self.parent.lookup(symbol)

    def add(self, symbol, value):
        self.env[symbol] = value
        
    def add_builtin(self, builtin):
        self.env[builtin.name] = builtin


def stringify(value):
    def finish_list(value):
        if value is None:
            return ')'
        elif isinstance(value, tuple):
            return ' ' + stringify(value[0]) + finish_list(value[1])
        else:
            return ' . ' + stringify(value) + ')'
    if value is None:
        return '()'
    if isinstance(value, int):
        return str(value)
    elif isinstance(value, str):
        return value
    elif isinstance(value, tuple):
        return '(' + stringify(value[0]) + finish_list(value[1])
    elif isinstance(value, Env):
        return '<env>'
    elif isinstance(value, Builtin):
        return '<builtin {}>'.format(value.name)
    else:
        raise Exception('bad value: ' + str(value))


def read(s):
    parser = Parser(s)
    term = parser.parse_term()
    if parser.is_at_end():
        return term
    else:
        raise ParseError('too much input')


class Builtin:
    def __init__(self, name, arg_count, args_type, fn):
        self.name = name
        self.fn = fn
        if arg_count is not None:
            def wrapping(args):
                if len(args) != arg_count:
                    raise EvalError('{} got {} args'.format(name, len(args)))
                return fn(args)
            self.fn = wrapping
        if args_type is not None:
            def wrapping(args):
                for arg in args:
                    if type(arg) != args_type:
                        raise EvalError('{} got bad arg'.format(name))
                return fn(args)
            self.fn = wrapping


class EvalError(Exception):
    def __init__(self, message):
        super(EvalError, self).__init__(message)

        
def eval_cond(cases, env):
    for case in cases:
        if not isinstance(case, tuple) or not isinstance(case[1], tuple) or case[1][1] is not None:
            raise EvalError('cond has bad branch')
        cond = eval(case[0], env)
        if cond is not None:
            return eval(case[1][0], env)


def eval_list(lst, env, start_from=0):
    if start_from >= len(lst):
        return None
    value = eval(lst[start_from], env)
    rest = eval_list(lst, env, start_from + 1)
    return (value, rest)	


def to_python_list(value):
    result = []
    while value is not None:
        if isinstance(value, tuple):
            result.append(value[0])
            value = value[1]
        else:
            raise EvalError('bad list')
    return result


def to_lisp_list(lst):
    result = None
    for item in range(0, len(lst)):
        result = (lst[len(lst) - item - 1], result)
    return result


def define_list(params, values, env):
    if params is None:
        if values is not None:
            raise EvalError('too many arguments')
    elif isinstance(params, str):
        env.add(params, values)
    elif isinstance(params, tuple):
        if values is None:
            raise EvalError('too few arguments')
        if isinstance(params[0], str):
            env.add(params[0], values[0])
            define_list(params[1], values[1], env)
        else:
            raise EvalError('defining non-symbol')
    else:
        raise EvalError('defining non-symbol')


def apply(f, args, parent_env):
    if isinstance(f, Builtin):
        args = eval_list(args, parent_env)
        return f.fn(to_python_list(args))
    elif isinstance(f, tuple) and f[0] == 'lambda':
        args = eval_list(args, parent_env)
        f = to_python_list(f)
        if len(f) != 4:
            raise EvalError('malformed closure')
        env = Env(f[3])
        define_list(f[1], args, env)
        return eval(f[2], env)
    elif isinstance(f, tuple) and f[0] == 'macro':
        f = to_python_list(f)
        if len(f) != 4:
            raise EvalError('malformed macro closure')
        env = Env(f[3])
        define_list(f[1], to_lisp_list(args), env)
        result = eval(f[2], env)
        return eval(result, parent_env)
    else:
        raise EvalError('calling non-function: {}'.format(f))


def eval(expr, env):
    if expr is None:
        return None
    elif isinstance(expr, int):
        return expr
    elif isinstance(expr, str):
        return env.lookup(expr)
    elif isinstance(expr, tuple):
        args = to_python_list(expr[1])
        if expr[0] == 'quote':
            if len(args) != 1:
                raise EvalError('quote got {} args'.format(len(args)))
            return args[0]
        elif expr[0] == 'cond':
            return eval_cond(args, env)
        elif expr[0] == 'lambda':
            if len(args) != 2:
                raise EvalError('lambda got {} args'.format(len(args)))
            return ('lambda', (args[0], (args[1], (env, None))))
        elif expr[0] == 'macro':
            if len(args) != 2:
                raise EvalError('macro got {} args'.format(len(args)))
            return ('macro', (args[0], (args[1], (env, None))))
        elif expr[0] == 'eval':
            if len(args) != 1:
                raise EvalError('eval got {} args'.format(len(args)))
            return eval(eval(args[0], env), env)
        elif expr[0] == 'define':
            if len(args) != 2:
                raise EvalError('define got {} args'.format(len(args)))
            if not isinstance(args[0], str):
                raise EvalError('defines first arg is ' + stringify(args[0]))
            value = eval(args[1], env)
            env.globals.add(args[0], value)
        else:
            return apply(eval(expr[0], env), args, env)
    else:
        raise Exception('cannot eval value: ' + stringify(expr))

        
def error(args):
    raise EvalError(args[0])


def compare_terms(args):
    [a, b] = args
    if isinstance(a, int) and isinstance(b, int):
        return 't' if a == b else None
    elif isinstance(a, str) and isinstance(b, str):
        return 't' if a == b else None
    elif a is None and b is None:
        return 't'
    elif isinstance(a, tuple) and isinstance(b, tuple):
        if compare_terms(a[0], b[0]) is not None:
            return 't'
        return compare_terms(a[1], b[1])
    elif isinstance(a, Builtin) and isinstance(b, Builtin):
        return 't' if a.name == b.name else None
    else:
        return None


def make_env():
    env = Env()
    def run(source):
        code = read(source)
        eval(code, env)
    env.add_builtin(Builtin('cons', 2, None, lambda x: tuple(x)))
    env.add_builtin(Builtin('car', 1, tuple, lambda x: x[0][0]))
    env.add_builtin(Builtin('cdr', 1, tuple, lambda x: x[0][1]))
    env.add_builtin(Builtin('+', None, int, sum))
    env.add_builtin(Builtin('number?', 1, None, lambda x: 't' if isinstance(x[0], int) else None))
    env.add_builtin(Builtin('symbol?', 1, None, lambda x: 't' if isinstance(x[0], str) else None))
    env.add_builtin(Builtin('pair?', 1, None, lambda x: 't' if isinstance(x[0], tuple) else None))
    env.add_builtin(Builtin('nil?', 1, None, lambda x: 't' if x[0] is None else None))
    env.add_builtin(Builtin('eq?', 2, None, compare_terms))
    return env


def run_repl(print_prompt):
    env = make_env()
    while True:
        if print_prompt:
            print('> ', end='')
        try:
            source = input()
        except EOFError:
            break
        try:
            code = read(source)
        except ParseError as e:
            print('Parse error:', str(e))
            continue
        try:
            result = eval(code, env)
        except (EvalError, UnboundSymbol) as e:
            print('Eval error:', str(e))
            continue
        print(stringify(result))


if __name__ == '__main__':
    print_prompt = all(a != '--no-prompt' for a in sys.argv)
    run_repl(print_prompt)
