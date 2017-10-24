import os
import os.path
import subprocess


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

def get_test_list():
    def is_file(name):
        path = os.path.join(TEST_DIR, name)
        return os.path.isfile(path)
    return sorted(f for f in os.listdir(TEST_DIR) if is_file(f))

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
