import os
from common import read_test, get_test_list, run_interpreter


def format_code(code):
    result = '<code>'
    first = True
    for line in code:
        if not first:
            result += '<br/>'
        first = False
        result += line
    return result + '</code>'

def make_table(test_name):
    name = os.path.splitext(test_name)[0]
    inputs, expected = read_test(test_name)
    outputs = run_interpreter(inputs)
    result = '|   |   |\n| - | - |\n'
    result += '| Testas | ' + name + ' |\n'
    result += '| Įvestis | ' + format_code(inputs) + ' |\n'
    result += '| Laukiami rezultatai | ' + format_code(expected) + ' |\n'
    if isinstance(outputs, str):
        result += '| Rezultatai | ' + outputs + ' |\n'
    else:
        result += '| Rezultatai | ' + format_code(outputs) + ' |\n'
    result += '| Būsena | ??? |\n'
    return result

if __name__ == '__main__':
    with open('tables.md', 'w', encoding='UTF-8') as f:
        for test in get_test_list():
            f.write(make_table(test))
            f.write('\n')
