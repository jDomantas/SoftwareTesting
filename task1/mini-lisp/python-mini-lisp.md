# Python mini-lisp interpreter

This is a simple interpreter for (mini-lisp)[spec.md], written in python. This interpreter provides a simple REPL. If you run it, you will be given a prompt where you can enter mini-lisp terms, as described in the specification. Interpreter will evaluate those terms and print the resulting terms. All evaluations share the same global environment, so you can define symbols and use them later.

If `--no-prompt` argument is supplied, interpreter will not print `> ` before reading input.
