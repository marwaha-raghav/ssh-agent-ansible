[![Pipeline for Testing ansible infrastructure with SSH-AGENT Automation](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-workflow.yml/badge.svg)](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-workflow.yml)
[![Pipeline for Testing Action for ansible infrastructure with SSH-AGENT Automation](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-action.yml/badge.svg)](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-action.yml)

# ssh-agent-ansible (Python Code) 

This tool has been built for automating ssh-add for key with/without passphrase.

Runs ssh-agent, generates a file with passphrase for ssh_ask_pass and adds key and passphrase with ssh-add.

## Why was this built?

When running a GitHub Action workflow for running ansible playbooks or roles for you Infrastructure as Code (IaC) projects, you will need to use SSH secrets (SSH Pvt Key, and passphrase (if applicable)) in a non-interactive way with the shell, this can become a bit cumbersome using toools like ssh-agent, ssh-add with direct shell commands.

Any Private Key with a passphrase requires the passphrase to be added interactively for every host specified in the ansible inventory So, in order to make this process non-interactive at the shell level and easy to use IaC CI pipelines through Github Actions, This tool/action runs ssh-agent, generates a file with specified passphrase for ssh_ask_pass and then adds the key and passphrase with ssh-add to the ssh-agent non-interactively.

## Attributes (py):
    - SSH_AUTH_SOCK (str): Path to the ssh AUTH socket file.
    - ANSIBLE_SSH_KEY (str): Github Actions Secret saved SSH private Key (PEM).
    - SSH_KEY_PASSPHRASE (str): Github Actions Secret saved SSH private key passphrase.
## Functions:
    - ssh_agent: Runs SSH agent and Adds Key and passphrase to SSH-AGENT.
## Todo:
    - Add functionality to differentiate between keys with and without passphrase.
    - Upload and Publish as a Github Action on the Marketplace.     
## Note:
    - This is only works with private keys in the PEM format. If used with OpenSSH format keys it will error out.
    - The action unsets SSH_AUTH_SOCK, kills the ssh-agent process and removes the SSH_AUTH_SOCK file before every run to remove any lingering or already running instances. 

---
# Action: Related Details

## How to Use the Action in a Workflow
```
      - name: 'Remove old SSH_AUTH_SOCKET and SSH-AGENT Instance'
        run: |
            rm /tmp/ssh_agent.sock
            unset SSH_AUTH_SOCK
            pkill ssh-agent
        continue-on-error: true
        shell: bash


      - name: Execute Key & passphrase Storage with SSH-AGENT
        uses: marwaha-raghav/ssh-agent-ansible@v0.1.0
        with:
          SSH_AUTH_SOCK: "/tmp/ssh_agent.sock"
          SSH_KEY_PASSPHRASE: ${{secrets.SSH_KEY_PASSPHRASE}}
          ANSIBLE_SSH_KEY: ${{secrets.ANSIBLE_SSH_KEY}}


```
## Inputs
  - SSH_AUTH_SOCK (str): Path to the ssh AUTH socket file.
  - ANSIBLE_SSH_KEY (str): Github Actions Secret saved SSH private Key (PEM).
  - SSH_KEY_PASSPHRASE (str): Github Actions Secret saved SSH private key passphrase.

# Limitations
## Works for the Current Job Only
Each job on Github Actions runs in a fresh instance of the VM, the SSH key will only be available in the job where this action has been referenced. THus this action will have to be called each time for a new Job. 

## SSH Private Key Format
If the private key is not in the PEM format, you will see an Error loading key "(stdin)": invalid format message.

Use ssh-keygen -p -f path/to/your/key -m pem to convert your key file to PEM, (Create a backup of your key, since this changes the original)

**Note: Examples for workflows are in the test dir. 
