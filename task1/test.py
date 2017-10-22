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

def run_test(inputs, outputs):
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
    output = proc.stdout.read().decode('UTF-8').splitlines()
    if len(output) != len(outputs):
        return 'Expected {} outputs, got {}'.format(len(outputs), len(output))
    for expected, got, index in zip(outputs, output, itertools.count()):
        got = got.strip()
        if expected == 'Eval error: ...' and got.startswith('Eval error'):
            continue
        if expected != got:
            return (index + 1, expected, got)
    return None

def get_test_list():
    def is_file(name):
        path = os.path.join(TEST_DIR, name)
        return os.path.isfile(path)
    return sorted(f for f in os.listdir(TEST_DIR) if is_file(f))

def run_and_report(test):
    print('test "{}" ... '.format(test), end = '')
    inputs, outputs = read_test(test)
    result = run_test(inputs, outputs)
    if result is None:
        print('ok')
        return True
    elif isinstance(result, str):
        print('FAIL')
        print(result)
        return False
    else:
        index, expected, got = result
        print('FAIL')
        print('Mismatch in output #{}'.format(index))
        print('Expected: {}'.format(expected))
        print('Got: {}'.format(got))
        return False

if __name__ == '__main__':
    success, fail = 0, 0
    for test in get_test_list():
        if run_and_report(test):
            success += 1
        else:
            fail += 1
    print('Tests passed: {}/{}'.format(success, success + fail))