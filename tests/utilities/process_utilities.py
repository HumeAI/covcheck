from subprocess import Popen, PIPE

from typing import List


class CommandOutput:
    def __init__(self, stdout: str, stderr: str):
        self.stdout = stdout
        self.stderr = stderr


def run_command(command: List[str]) -> CommandOutput:
    with Popen(command, stdout=PIPE, stderr=PIPE) as process:
        stdout_pipe, stderr_pipe = process.communicate()
        out_message = stdout_pipe.strip().decode('utf-8')
        err_message = stderr_pipe.strip().decode('utf-8')
        return CommandOutput(out_message, err_message)
