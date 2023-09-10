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
      match = re.search("Agent pid (\d+)", agent_output.strip())
      print(agent_output.strip())
      
      if match:
        agent_pid = match.group(1)
        print(agent_pid.strip())
      else:
        print("Agent PID not found.")

      with open(os.path.expanduser("~/.ssh_askpass"), 'w') as pass_file:
         pass_file.write("#!/bin/bash\n")
         pass_file.write(f"echo \"$SSH_KEY_PASSPHRASE\"")
      os.chmod(os.path.expanduser('~/.ssh_askpass'), 0o755)
      ANSIBLE_SSH_KEY.replace('\r', '')
      password = subprocess.run([os.path.expanduser("~/.ssh_askpass")], capture_output=True, text=True)
      #print(password.stdout)
      env = {
         "DISPLAY": "None",
         "SSH_ASKPASS": os.path.expanduser("~/.ssh_askpass"),
         "SSH_AGENT_PID": f"{agent_pid}",
         "SSH_AUTH_SOCK": f"{SSH_AUTH_SOCK}", 
         "ANSIBLE_SSH_KEY": f"{ANSIBLE_SSH_KEY}"
      }

      process = subprocess.Popen(["ssh-add", "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env={**env}, text=True)
      stdout, stderr = process.communicate(input=ANSIBLE_SSH_KEY.strip())
      print(stdout)
      print(stderr)   
    
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




