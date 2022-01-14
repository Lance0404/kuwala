"""
build_cli.sh:

cd ../..
pip3 install virtualenv
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r kuwala/core/cli/requirements.txt
pip install -e .
"""

import subprocess
import os
from threading import Thread

def run_command(command: [str], exit_keyword=None):
    process = subprocess.Popen(
        command,
        bufsize=1,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True
    )
    thread_result = dict(hit_exit_keyword=False)

    def print_std(std, result):
        while True:
            line = std.readline()

            if len(line.strip()) > 0:
                print(line if 'Stage' not in line and '%' not in line else line.strip(), end='\r')

            if exit_keyword is not None and exit_keyword in line:
                result['hit_exit_keyword'] = True

                break

            return_code = process.poll()

            if return_code is not None:
                if return_code != 0:
                    return RuntimeError()

                break

    stdout_thread = Thread(target=print_std, args=(process.stdout, thread_result,), daemon=True)
    stderr_thread = Thread(target=print_std, args=(process.stderr, thread_result,), daemon=True)

    stdout_thread.start()
    stderr_thread.start()

    while stdout_thread.is_alive() and stderr_thread.is_alive():
        pass

    if thread_result['hit_exit_keyword']:
        return process

script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(os.path.join(script_dir,'../..'))
run_command(['pip3 install virtualenv'])
run_command(['virtualenv -p python3 venv'])
run_command(['source ./venv/bin/activate'])
run_command(['pip install -r kuwala/core/cli/requirements.txt'])
run_command(['pip install -e .'])