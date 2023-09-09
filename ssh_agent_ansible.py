import os
import subprocess
from subprocess import CalledProcessError, TimeoutExpired
import re

SSH_AUTH_SOCK = os.getenv("SSH_AUTH_SOCK")
ANSIBLE_SSH_KEY = os.getenv("ANSIBLE_SSH_KEY")
SSH_KEY_PASSPHRASE = os.getenv("SSH_KEY_PASSPHRASE")

def ssh_agent():
    try:
      agent_process = subprocess.run([f'eval $(ssh-agent -a {SSH_AUTH_SOCK})'], check=True, shell=True, capture_output=True, text=True)
      agent_output = agent_process.stdout 
      match = re.search(r"Agent pid (\d+)", agent_output)
      
      if match:
        agent_pid = match.group(1)
        print(agent_pid)
      else:
        print("Agent PID not found.")

      with open(os.path.expanduser("~/.ssh_askpass"), 'w') as pass_file:
         pass_file.write("#!/bin/bash\n")
         pass_file.write(f"echo \"{SSH_KEY_PASSPHRASE}\"")
      os.chmod(os.path.expanduser('~/.ssh_askpass'), 0o755)
      ANSIBLE_SSH_KEY.replace('\r', '')
      password = subprocess.run([os.path.expanduser("~/.ssh_askpass")], capture_output=True, text=True)
      env = {
         "DISPLAY": "None",
         "SSH_ASKPASS": f"{password.stdout}",
         "SSH_AGENT_PID": f"{agent_pid}" 
      }

      process = subprocess.run(["ssh-add", "-"], input=ANSIBLE_SSH_KEY, env={**env}, stdout=subprocess.DEVNULL, text=True, check=True)
         
    
    except CalledProcessError as e:
       print(f"Process failed non-zero code returned \n {e}")
       raise 
    except TimeoutExpired as e:
       print(f"Process Timed out \n {e}")


if __name__ == '__main__':

    if not all([SSH_AUTH_SOCK, SSH_KEY_PASSPHRASE, ANSIBLE_SSH_KEY]):
       print("Error: Some Credential is not set to a valid path")
    else:
       ssh_agent()




