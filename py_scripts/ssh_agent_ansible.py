"""Module for automating ssh-add for key with/without passphrase.

Runs ssh-agent, generates a file with passphrase for ssh_ask_pass and 
adds key and passphrase with ssh-add.

Todo:
    - Add functionality to differentiate between keys with and without passphrase

Attributes:
    - SSH_AUTH_SOCK (str): Path to the ssh AUTH socket file.
    - ANSIBLE_SSH_KEY (str): Github Actions Secret saved SSH private Key (PEM).
    - SSH_KEY_PASSPHRASE (str): Github Actions Secret saved SSH private key passphrase.
Functions:
    - ssh_agent: Runs SSH agent and Adds Key and passphrase to SSH-AGENT
     
Note:
    This is only works with private keys in the PEM format. 
    If used with OpenSSH format keys it will error out.

"""

import os
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
import re

# Environment Variables that need to be set
SSH_AUTH_SOCK = os.getenv("SSH_AUTH_SOCK")
# Github Actions Secrets
ANSIBLE_SSH_KEY = os.getenv("ANSIBLE_SSH_KEY")
SSH_KEY_PASSPHRASE = os.getenv("SSH_KEY_PASSPHRASE")


# ssh_agent() Function that
# Runs SSH agent
# -> Creates a file with SSH_PASSPHRASE for SSH_ASKPASS
# -> Addes Key and passphrase to SSH-AGENT
def ssh_agent():
    """Function to Add Pvt. Key and Passphrase to ssh-agent.

    Runs ssh-agent, generates a file with passphrase for ssh_ask_pass and 
    adds key and passphrase with ssh-add.

    Args:
        None

    Returns:
        None

    Raises:
        CalledProcessError: If subprocess returns a non-zero code
        TimeoutExpired: if subprocess times out
    """

    try:
        # Runs the ssh-agent and capture the PID using regex
        agent_process = subprocess.run(
            [f"eval $(ssh-agent -a {SSH_AUTH_SOCK})"],
            check=True,
            shell=True,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )
        agent_output = agent_process.stdout
        match = re.search(r"Agent pid (\d+)", agent_output.strip())
        print(agent_output.strip())
        # If PID successfull found strip any whitespace and extract to agent_pid
        if match:
            agent_pid = match.group(1)
            print(agent_pid.strip())
        else:
            print("Agent PID not found.")
        # Writing the passphrase env variable to a file: ~/.ssh_askpass
        with open(os.path.expanduser("~/.ssh_askpass"), "w", encoding="utf-8") as pass_file:
            pass_file.write("#!/bin/bash\n")
            pass_file.write('echo "$SSH_KEY_PASSPHRASE"')
        # Give rwx to user, r-x to group and user
        os.chmod(os.path.expanduser("~/.ssh_askpass"), 0o755)
        # Replace any '\r' in the private key
        ANSIBLE_SSH_KEY.replace("\r", "")
        # Copy the env vars for the parent process
        envi = os.environ.copy()
        # Appending vars needed by ssh-add
        envi.update(
            {
                "DISPLAY": "None",
                "SSH_ASKPASS": os.path.expanduser("~/.ssh_askpass"),
                "SSH_AGENT_PID": f"{agent_pid}",
                "SSH_AUTH_SOCK": SSH_AUTH_SOCK,
                "ANSIBLE_SSH_KEY": ANSIBLE_SSH_KEY,
            }
        )
        # Adding the key using ssh-add, Display=None no prompt is generated.
        process = subprocess.run(
            ["ssh-add", "-"],
            input=envi["ANSIBLE_SSH_KEY"].strip(),
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            env=envi,
            check=True,
            text=True,
        )
        print(f" STDOUT: {process.stdout}")
        print(f"STDERR: {process.stderr}")

    # Exception caught & raised if any subprocess fails
    # Key might not be of the correct Type (PEM)
    # ssh-add fails to connect to agent
    # ssh-add -> passphrase might not be correct
    except CalledProcessError as exception:
        print(f"Process failed non-zero code returned \n {exception}")
        raise
    # Exception for timeout caught & raise
    except TimeoutExpired as exception:
        print(f"Process Timed out \n {exception}")
        raise


if __name__ == "__main__":
    # Only executed if all default env vars are defined
    if not all([SSH_AUTH_SOCK, SSH_KEY_PASSPHRASE, ANSIBLE_SSH_KEY]):
        print("Error: Some Credential is not set to a valid path")
    else:
        ssh_agent()
