# Mini-lisp

This document describes a small dialect of lisp, which we will call "mini-lisp".

## 1. Language terms

Language has 5 core types of terms:
* Number
* Symbol
* Nil
* Pair
* Environment
* Primtives

Terms can form lists: term is a list if it is Nil, or a pair of any term and list.

## 2. Syntax

### 2.1. Numbers

Numbers are written as a sequence of digits.

#### Examples:

```
0  4392  03059  203
```

### 2.2. Symbols

Symbols are any sequence of characters, except `(`, `)`, and whitespace. Symbols also cannot consist only of digits, and cannot be just `.`.

#### Examples:

```
abc  -5  can.contain:punctuation!
```

### 2.3. Nil

Nil is written as `()`. Whitespace between parentheses is allowed.

#### Examples:

```
()  ( )
```

### 2.4. Pairs

Pairs are written as `(a . b)`, where `a` and `b` are terms. There can be multiple terms before the dot, which is a syntaxic sugar for list-like construct:

```
(a b c . d)  ==>  (a . (b . (c . d)))
```

#### Examples:

```
(1 . 2)  (a . ())
```

### 2.5. Environments

Environments do not have a specific syntaxic representation for input. When displaying results environmets will be displayed as `<env>`.

### 2.6. Primitives

Primitives do not have a specific syntaxic representation for input. When displaying results primitives will be displayed as `<primitive {name}>` (e.g. `<primitive cons>`).

### 2.7. Lists

Lists are written as `(a b c)`, where `a`, `b`, and `c` are terms. Lists can be of any non-negative length. Note that list of length zero has the same syntaxic representation as Nil, making syntaxic sugar consistent.

#### Examples:

```
(a b-c () (1 . 2))  (1)
```

### 2.8. Additional syntaxic sugar

`'a` is parsed as `(quote a)` where a is a term.

#### Examples:

```
'(1 2 3)  ==>  (quote (1 2 3))
```

## 3. Evaluation

### 3.1. Evaluating terms

Evaluating a term in an environment proceeds as follows:

* If term is a number, it evaluates to itself.
* If term is Nil, it evaluates to itself.
* If term is a symbol, it evaluates to the value associated to that symbol in current environment.
* If term is a pair that is not a valid list, error is reported.
* If term is an environment, error is reported.
* If term is a primitive, error is reported.
* If term is a list, it is evaluated either as a special form, or as a function call.

### 3.2. Evaluating lists

If first item of a list is one of the listed symbols, list is evaluated as a special form.

Special forms: `quote`, `cond`, `eval`, `lambda`, `define`.

Otherwise first element ("callee") of the list is evaluated.

* If the result is a primitive, evaluate remaining list items, and evaluate primitive call.
* If the result is a list that meets the following requirements:
    * First element is symbol `lambda`.
    * Second element is argument list. Argument list is Nil, a symbol, or a pair of a symbol and an argument list.
    * Fourth element is an environment. This term is called "closure environment".
    Then remaining elements are evaluated, and then a function call is evaluated.
* Otherwise, an error is reported.

### 3.3. Evaluating Special forms

#### 3.3.1. Quote

Quote takes exactly one argument. It returns the argument unchanged.

```
(quote (1 a))  ==>  (1 a)
```

#### 3.3.2. Cond

Every argument to `cond` must be a list of two terms. It evaluates first item of each list in order until it evaluates to some non-Nil value. Then it returns the result of evaluating second element of that list. If no argument is matched, whole expression evaluates to Nil.

```
(cond (() 1) (2 2))  ==>  2
```

#### 3.3.3. Eval

Eval takes exactly one argument, and evaluates it twice in the current environment.

```
(eval ''a)  ==>  a
```

#### 3.3.4. Lambda

Lambda takes exactly two arguments, and constructs the following structure:

```
(lambda arg1 arg2 current-env)
```

where `arg1` and `arg2` are respectively first and second arguments, and `current-env` is current environment.

#### 3.3.5. Define

Define takes exactly two arguments, of which the first one must be a symbol. It evaluates second argument, and modifies the global environment by adding a mapping from the symbol to result value. Expression evaluates to the added value.

```
(define a '(1 2 3))
```

### 3.3.6. Evaluating primitive calls

Primitive functions take a list of arguments and give some result. Their behaviour is listed in the list below.

### 3.3.7. Evaluating lambda calls

First, an argument list is matched against given parameters:
* If parameter list is Nil, it matches empty parameter list.
* If parameter list is symbol, it matches parameter list.
* If parameter list is pair of symbol and parameter list:
    * Symbol matches car of parameter list, which must be nonempty.
    * Second element of the pair matches cdr of parameter list.

If there is a mismatch, an error is reported.

The environment stored in 4th element is extended with matches. If same symbol is matched multiple times, it must get the value from the right-most match.

Then the body is evaluated with this new extended environment, and returned as a result.

## 4. Built-in primitives

Initialy each primitive will be bound in the global env to its name, but user code can override the bindings.

| Name      | Arguments   | Description                                           |
| --------- | ----------- | ----------------------------------------------------- |
| `car`     | 1 (pair)    | Returns first element of the pair.                    |
| `cdr`     | 1 (pair)    | Returns second element of the pair.                   |
| `cons`    | 2           | Builds a pair from the given elements.                |
| `+`       | numbers     | Returns sum of arguments, 0 if no arguments given.    |
| `eq?`     | 2           | Returns symbol `t` if args are equal, Nil otherwise.  |
| `number?` | 1           | Returns symbol `t` if arg is number, Nil otherwise.   |
| `symbol?` | 1           | Returns symbol `t` if arg is symbol, Nil otherwise.   |
| `pair?`   | 1           | Returns symbol `t` if arg is pair, Nil otherwise.     |
| `nil?`    | 1           | Returns symbol `t` if arg is Nil, Nil otherwise.      |

## 5. Term equality

Two terms are equal iff any of the following:
* Both are numbers with equal values.
* Both are the same symbol.
* Both are Nil.
* Both are pairs, and corresponding elements are equal.
* Both are the same primitive.
