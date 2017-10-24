# 1. Įvadas

Darbo tikslas yra ištestuoti mini-lisp programavimo kalbos interpretatorių. Šiame dokumente yra aprašytas testavimo procesas ir pateikti testavimo rezultatai.

Testuojamas interpretatorius yra trumpai aprašytas [python-mini-lisp.md](mini-lisp/python-mini-lisp.md), mini-lisp specifikacija: [spec.md](mini-lisp/spec.md).

Interpretatorius bus testuojamas juodos dėžės principu. Jam bus pateikiami mini-lisp termai, ir išvedami termai bus lyginami su specifikacijos nusakomu rezultatu. Kadangi interpretatoriaus vartotojo sąsaja yra labai praprasta, testai yra automatizuoti. Testas yra aprašomas paprastu formatu kaip sąrašas įvesčių ir norimų rezultatų. Testams paleisti naudojama trumpa Python programėlė kuri nuskaito testus, paleidžia interpretatorių, suveda testo įvestis, palygina išvestis, ir praneša rezultatus.

Siekiant sumažinti darbo apimtį, testuojamas tik programų vykdymas (specifikacijos skyrius `3. Evaluation`). Testavimo tikslams likusi specifikacijos dalis (sintaksė ir esamos primityvios operacijos) yra laikoma realizuota teisingai.

# 2. Interpretatoriaus testavimas

## 2.1. Reikalavimai

Interpretatorius yra testuojamas pagal specifikaciją, neišrašant atskirai detalių reikalavimų. Testavimo atvejai yra parašyti pagal specifikacijos punktus.

## 2.2. Atsekamumo matrica

Pateikiama lentelė nurodo kuriuos specifikacijos skyrius atitinka kurie testai.

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

## 2.3. Testavimo atvejai ir rezultatai

Testavimo atvejo id sudarytas pagal testuojamą kalbos elementą.

<< testavimo atvejų lentelės >>

## 2.4. Defektų sąrašas

Defekto ID sudaromas pagal taisyklę D+XX, kur XX - defekto numeris.

Pagal poveikį interpretatoriaus naudojimui defektai suskirstyti į:
* Kritinis - defektas neleidžia naudotis esminėmis interpretatoriaus funkcijomis.
* Svarbus - defektas įtakoja esmines funkcijas, bet juo naudotis iš esmės galima.
* Nesvarbus - defektas turi mažai įtakos interpretatoriaus naudojimui.

<< defektų lentelės >>

## 3. Rezultatai ir išvados

???

## 4. Priedai

Trumpas interpretatoriaus aprašymas: [python-mini-lisp.md](mini-lisp/python-mini-lisp.md).

Mini-lisp specifikacija: [spec.md](mini-lisp/spec.md).
