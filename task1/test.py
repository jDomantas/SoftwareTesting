import itertools
from common import read_test, get_test_list, run_interpreter


def check_outputs(expected, got):
    if len(expected) != len(got):
        return ['Expected {} outputs, got {}'.format(len(expected), len(got))]
    errors = []
    for expected, got, index in zip(expected, got, itertools.count()):
        got = got.strip()
        if expected == 'Eval error: ...' and got.startswith('Eval error'):
            continue
        if expected != got:
            errors.append(
                'Mismatch in output #{}\nExpected: {}\nGot: {}'.format(
                    index + 1,
                    expected,
                    got))
    return errors

def run_and_report(test):
    print('test "{}" ... '.format(test), end = '')
    inputs, outputs = read_test(test)
    got = run_interpreter(inputs)
    if isinstance(got, str):
        print('FAIL')
        print(got)
        return False
    else:
        errors = check_outputs(outputs, got)
        if len(errors) == 0:
            print('ok')
            return True
        else:
            print('FAIL')
            for err in errors:
                print(err)
            return False

if __name__ == '__main__':
    success, fail = 0, 0
    for test in get_test_list():
        if run_and_report(test):
            success += 1
        else:
            fail += 1
    print('Tests passed: {}/{}'.format(success, success + fail))