import itertools
import subprocess
import os
import os.path

TEST_DIR = './tests'

def read_test(filename):
    inputs, outputs = [], []
    with open(os.path.join(TEST_DIR, filename)) as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('# '):
                continue
            elif line.startswith('> '):
                inputs.append(line[2:])
            else:
                outputs.append(line)
    return inputs, outputs

def run_interpreter(inputs):
    proc = subprocess.Popen(
        ['python', 'mini-lisp/lisp.py', '--no-prompt'],
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE,
        stderr = subprocess.DEVNULL)
    for i in inputs:
        encoded = (i + '\n').encode('UTF-8')
        proc.stdin.write(encoded)
    proc.stdin.close()
    exit_code = proc.wait()
    if exit_code != 0:
        return 'Interpreter exited with code {}'.format(exit_code)
    return proc.stdout.read().decode('UTF-8').splitlines()

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

def get_test_list():
    def is_file(name):
        path = os.path.join(TEST_DIR, name)
        return os.path.isfile(path)
    return sorted(f for f in os.listdir(TEST_DIR) if is_file(f))

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