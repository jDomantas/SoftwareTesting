# Įvadas

Darbo tikslas yra ištestuoti mini-lisp programavimo kalbos interpretatorių. Šiame dokumente aprašomi pagal specifikaciją sudaryti testavimo atvejai, testų vykdymo rezultatai, ir aprašomi testavimo metu rasti defektai.

Testuojamas interpretatorius yra trumpai aprašytas [python-mini-lisp.md](mini-lisp/python-mini-lisp.md), mini-lisp specifikacija: [spec.md](mini-lisp/spec.md).

Interpretatorius bus testuojamas juodos dėžės principu. Jam bus pateikiami mini-lisp termai, ir išvedami termai bus lyginami su specifikacijos nusakomu rezultatu. Kadangi interpretatoriaus vartotojo sąsaja yra labai praprasta, testai yra automatizuoti. Testas yra aprašomas paprastu formatu kaip sąrašas įvesčių ir norimų rezultatų. Testams paleisti naudojama trumpa Python programėlė kuri nuskaito testus, paleidžia interpretatorių, suveda testo įvestis, palygina išvestis, ir praneša rezultatus.

Šiame darbe testuojamas tik programų vykdymas (trečias specifikacijos skyrius - "Evaluation"). Testavimo tikslams likusi specifikacijos dalis (sintaksė ir primityvios operacijos) yra laikoma realizuota teisingai.

# 1. Interpretatoriaus testavimas

## 1.1. Reikalavimai

Interpretatorius yra testuojamas pagal specifikaciją, neišrašant atskirai detalių reikalavimų. Testavimo atvejai yra parašyti pagal specifikacijos punktus. Testavimo atvejuose kuriuose tikimasi kad interpretatorius praneš klaidą, koks yra konkretus klaidos pranešimas nėra tikrinama - kai tikimasi klaidos pranešimo, išvestis bus laikoma teisinga jei interpretatorius praneš bet kokią klaidą.

## 1.2. Atsekamumo matrica

Pateikiama lentelė nurodo kurie testai atitinka kuriuos specifikacijos skyrius.

| Testas                 | 3.1. | 3.2. | 3.3.1. | 3.3.2. | 3.3.3. | 3.3.4. | 3.3.5. | 3.3.6. |
| ---------------------- |:----:|:----:|:------:|:------:|:------:|:------:|:------:|:------:|
| `eval-bad-cond`        |      | X    |        | X      |        |        |        |        |
| `eval-bad-eval`        |      | X    |        |        | X      |        |        |        |
| `eval-bad-lambda-call` |      | X    |        |        |        |        |        | X      |
| `eval-bad-lambda`      |      | X    |        |        |        | X      |        |        |
| `eval-bad-quote`       |      | X    | X      |        |        |        |        |        |
| `eval-cond`            |      | X    |        | X      |        |        |        |        |
| `eval-define`          |      | X    |        |        |        |        | X      |        |
| `eval-environment`     | X    |      |        |        |        |        |        |        |
| `eval-eval`            |      | X    |        |        | X      |        |        |        |
| `eval-lambda-call`     |      | X    |        |        |        |        |        | X      |
| `eval-lambda`          |      | X    |        |        |        | X      |        |        |
| `eval-nil`             | X    |      |        |        |        |        |        |        |
| `eval-non-list`        | X    |      |        |        |        |        |        |        |
| `eval-number`          | X    |      |        |        |        |        |        |        |
| `eval-primitive`       | X    |      |        |        |        |        |        |        |
| `eval-quote`           |      | X    | X      |        |        |        |        |        |
| `eval-symbol`          | X    |      |        |        |        |        |        |        |

## 1.3. Testavimo atvejai ir rezultatai

Testavimo atvejo id sudarytas pagal testuojamą kalbos elementą.

|   |   |
| - | - |
| Testas | eval-bad-cond |
| Įvestis | <code>(cond (1 . 2))<br/>(cond (1 2) (3 . 4))<br/>(cond (1 2) a b c)</code> |
| Laukiami rezultatai | <code>Eval error: ...<br/>Eval error: ...<br/>Eval error: ...</code> |
| Rezultatai | <code>Eval error: cond has bad branch<br/>2<br/>2</code> |
| Būsena | Išvestis bloga, fiksuojamas defektas `D-01` |

|   |   |
| - | - |
| Testas | eval-bad-eval |
| Įvestis | <code>(eval)<br/>(eval 1 2)</code> |
| Laukiami rezultatai | <code>Eval error: ...<br/>Eval error: ...</code> |
| Rezultatai | <code>Eval error: eval got 0 args<br/>Eval error: eval got 2 args</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-bad-lambda-call |
| Įvestis | <code>((lambda (x) x) 1 2 3)<br/>((lambda (x) x))<br/>((lambda (x . y) x))</code> |
| Laukiami rezultatai | <code>Eval error: ...<br/>Eval error: ...<br/>Eval error: ...</code> |
| Rezultatai | <code>Eval error: too many arguments<br/>Eval error: too few arguments<br/>Eval error: too few arguments</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-bad-lambda |
| Įvestis | <code>(lambda)<br/>(lambda x)<br/>(lambda x y z)</code> |
| Laukiami rezultatai | <code>Eval error: ...<br/>Eval error: ...<br/>Eval error: ...</code> |
| Rezultatai | <code>Eval error: lambda got 0 args<br/>Eval error: lambda got 1 args<br/>Eval error: lambda got 3 args</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-bad-quote |
| Įvestis | <code>(quote)<br/>(quote 1 2)</code> |
| Laukiami rezultatai | <code>Eval error: ...<br/>Eval error: ...</code> |
| Rezultatai | <code>Eval error: quote got 0 args<br/>Eval error: quote got 2 args</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-cond |
| Įvestis | <code>(cond)<br/>(cond (1 2))<br/>(cond ((cdr '(1)) 1) (() 2) ('symbol 3))</code> |
| Laukiami rezultatai | <code>()<br/>2<br/>3</code> |
| Rezultatai | <code>()<br/>2<br/>3</code> |
| Būsena | ??? |

|   |   |
| - | - |
| Testas | eval-define |
| Įvestis | <code>(define previously-undefined-symbol 3)<br/>previously-undefined-symbol</code> |
| Laukiami rezultatai | <code>3<br/>3</code> |
| Rezultatai | <code>()<br/>3</code> |
| Būsena | Išvestis neteisinga, fiksuojamas defektas `D-02` |

|   |   |
| - | - |
| Testas | eval-environment |
| Įvestis | <code>(eval (car (cdr (cdr (cdr (lambda () ()))))))</code> |
| Laukiami rezultatai | <code>Eval error: ...</code> |
| Rezultatai | Interpretatorius nulūžo (išeities kodas: 1) |
| Būsena | Interpretatorius nulūžo, fiksuojamas defektas `D-03` |

|   |   |
| - | - |
| Testas | eval-eval |
| Įvestis | <code>(eval 1)<br/>(eval '''a)</code> |
| Laukiami rezultatai | <code>1<br/>(quote a)</code> |
| Rezultatai | <code>1<br/>(quote a)</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-lambda-call |
| Įvestis | <code>((lambda (x) x) 1)<br/>((lambda (x y) y) 1 2)<br/>((lambda (x . y) y) 1 2 3)<br/>((lambda x x) 1 2 3)<br/>(((lambda (x) (lambda () x)) 1))</code> |
| Laukiami rezultatai | <code>1<br/>2<br/>(2 3)<br/>(1 2 3)<br/>1</code> |
| Rezultatai | <code>1<br/>2<br/>(2 3)<br/>(1 2 3)<br/>1</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-lambda |
| Įvestis | <code>(lambda (x) x)<br/>(lambda (x . y) (cdr (+ x y)))</code> |
| Laukiami rezultatai | <code>(lambda (x) x \<env>)<br/>(lambda (x . y) (cdr (+ x y)) \<env>)</code> |
| Rezultatai | <code>(lambda (x) x \<env>)<br/>(lambda (x . y) (cdr (+ x y)) \<env>)</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-nil |
| Įvestis | <code>()</code> |
| Laukiami rezultatai | <code>()</code> |
| Rezultatai | <code>()</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-non-list |
| Įvestis | <code>(1 . 2)</code> |
| Laukiami rezultatai | <code>Eval error: ...</code> |
| Rezultatai | <code>Eval error: bad list</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-number |
| Įvestis | <code>123<br/>0<br/>12869281642198634812764389</code> |
| Laukiami rezultatai | <code>123<br/>0<br/>12869281642198634812764389</code> |
| Rezultatai | <code>123<br/>0<br/>12869281642198634812764389</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-primitive |
| Įvestis | <code>(eval +)</code> |
| Laukiami rezultatai | <code>Eval error: ...</code> |
| Rezultatai | Interpretatorius nulūžo (išeities kodas: 1) |
| Būsena | Interpretatorius nulūžo, fiksuojamas defektas `D-04` |

|   |   |
| - | - |
| Testas | eval-quote |
| Įvestis | <code>(quote (1 2 3))<br/>(quote a)<br/>(quote (quote (quote quote)))</code> |
| Laukiami rezultatai | <code>(1 2 3)<br/>a<br/>(quote (quote quote))</code> |
| Rezultatai | <code>(1 2 3)<br/>a<br/>(quote (quote quote))</code> |
| Būsena | Išvestis teisinga |

|   |   |
| - | - |
| Testas | eval-symbol |
| Įvestis | <code>+<br/>eq?</code> |
| Laukiami rezultatai | <code><builtin +><br/><builtin eq?></code> |
| Rezultatai | <code><builtin +><br/><builtin eq?></code> |
| Būsena | Išvestis teisinga |

## 1.4. Defektų sąrašas

Defekto ID sudaromas pagal taisyklę D+XX, kur XX - defekto numeris.

Pagal poveikį interpretatoriaus naudojimui defektai suskirstyti į:
* Kritinis - defektas neleidžia naudotis esminėmis interpretatoriaus funkcijomis.
* Svarbus - defektas įtakoja esmines funkcijas, bet juo naudotis iš esmės galima.
* Nesvarbus - defektas turi mažai įtakos interpretatoriaus naudojimui.

| Defekto ID | Aprašymas | Testas | Defekto svarba |
| ---------- | --------- | ------ | -------------- |
| `D-01`     | Interpretatorius nepraneša klaidos kai vykdoma bloga `cond` išraiška. | eval-bad-cond | Kritinis |

| Defekto ID | Aprašymas | Testas | Defekto svarba |
| ---------- | --------- | ------ | -------------- |
| `D-02`     | Grąžinamas neteisingas rezultatas vykdant `define` išraišką. | eval-define | Kritinis |

| Defekto ID | Aprašymas | Testas | Defekto svarba |
| ---------- | --------- | ------ | -------------- |
| `D-03`     | Interpretatorius nulūžta bandant įvykdyti "environment" termą, vietoj to kad būtų išspausdintas klaidos pranešimas. | eval-env | Svarbus |

| Defekto ID | Aprašymas | Testas | Defekto svarba |
| ---------- | --------- | ------ | -------------- |
| `D-04`     | Interpretatorius nulūžta bandant įvykdyti "primitive" termą, vietoj to kad būtų išspausdintas klaidos pranešimas. | eval-primitive | Svarbus |

## 2. Rezultatai ir išvados

Pagal specifikaciją buvo sudaryti ir atlikti 17 testavimo atvejų. Rasti du kritiniai defektai `D-01` ir `D-02`, bei du svarbūs defektai - `D-03` ir `D-04`.

Testuotas interpretatorių sunku naudoti kol nebus ištaisyti du kritiniai defektai, nes interpretatoriaus gaunami rezultatai neatitinka specifikacijos reikalavimų. Likę defektai `D-03` ir `D-04` nėra kritiniai, su jais susidūrus jie tikrai bus pastebėti.

## 3. Priedai

Trumpas interpretatoriaus aprašymas: [python-mini-lisp.md](mini-lisp/python-mini-lisp.md).

Mini-lisp specifikacija: [spec.md](mini-lisp/spec.md).
