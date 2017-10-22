# Compiler testing

## About compiler bugs

* Compilers are programs just like everything else.
* Its certainly possible for them to have bugs.
* Compiler bugs are usually pretty rare.


## Compiler bug kinds

* Crash (internal compilation error - ICE).
* Disallowing valid programs.
* Miscompilation - programs behave not as they should. Also compiler might allow through invalid programs.


## Why are the bugs rare?

* There are a lot of people who use compilers day to day.
* Compiler bugs are quite high priority - for example, a compiler that generates bad code is pretty much useless.
* Problem is well specified and stuff is pretty well researched.
* They usually have a shitton of tests.
* Usually people solve normal problems by writing normal code that doesn't do anything funny.


## When can I encounter them?

* Pick a compiler that barely anyone uses.
* Pick a compiler that was not tested.
* Pick a compiler that was not well researched before.
* Try to do something funny.


## A scary example

```c++
#include <iostream>

void f(bool x = !(std::cout << "hi\n")) {}

int main() {
	f();
}
```


## A scary example

TODO: check with more recent g++ version.

```
$ g++ --version
g++.exe (GCC) 4.8.1
Copyright (C) 2013 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

$ g++ example.cpp -o example && ./example
hi
hi
```


## Testing strategies

* How are compilers tested in practice?
* Let's take a look at some real-world projects.


## Rust

[BIGASS RUST LOGO]


## Rust

`src/test/` contains ~7500 programs, with most interesting being:
* ~2500 under `src/test/compile-fail` - programs that must fail to compile.
* ~3000 under `src/test/run-pass/` - programs that must compile and not crash when run.


## Rust - `compile-fail` test

```rust
fn main () {
    loop {
        break 'a;
        //~^ ERROR E0426
        //~| NOTE undeclared label `'a`
    }
}
```


## Rust - `run-pass` test

```rust
fn test<F>(f: F) -> usize where F: FnOnce(usize) -> usize {
    return f(22);
}

pub fn main() {
    let y = test(|x| 4 * x);
    assert_eq!(y, 88);
}
```


## Roslyn

They don't have a logo :(


## Roslyn

* .NET compiler platform - compilers and code analysis APIs for C# and Visual Basic .NET.
* 70000 tests :O
* Most tests are:
    * Feed a program into the API,
    * Check that the results it spits out are correct.


## CompCert

`test/` contains 117 tests:
* 24 small programs,
* 3 bigger programs,
* 90 regression tests.


## CompCert

* CompCert compiler is written in Coq (and a bit of OCaml).
* Instead of tests, compiler correctness is verified by formal machine checked proofs.


## Java bug (?)

```java
class Unsound {
    static class Constrain<A, B extends A> {}
    static class Bind<A> {
        <B extends A>
        A upcast(Constrain<A, B> constrain, B b) {
            return b;
        }
    }
    static <T, U> U coerce(T t) {
        Constrain<U, ? super T> constrain = null;
        Bind<U> bind = new Bind<U>();
        return bind.upcast(constrain, t);
    }
    public static void main(String[] args) {
        String zero = Unsound.<Integer, String>coerce(0);
    }
}
```
