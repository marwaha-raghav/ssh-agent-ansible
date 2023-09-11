[![Pipeline for Testing ansible infrastructure with SSH-AGENT Automation](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-workflow.yml/badge.svg)](https://github.com/marwaha-raghav/ssh-agent-ansible/actions/workflows/test-workflow.yml)

# ssh-agent-ansible

This tool has been built for automating ssh-add for key with/without passphrase.

Runs ssh-agent, generates a file with passphrase for ssh_ask_pass and adds key and passphrase with ssh-add.

## Todo:
    - Add functionality to differentiate between keys with and without passphrase.
    - Upload and Publish as a Github Action on the Marketplace.

## Attributes:
    - SSH_AUTH_SOCK (str): Path to the ssh AUTH socket file.
    - ANSIBLE_SSH_KEY (str): Github Actions Secret saved SSH private Key (PEM).
    - SSH_KEY_PASSPHRASE (str): Github Actions Secret saved SSH private key passphrase.
## Functions:
    - ssh_agent: Runs SSH agent and Adds Key and passphrase to SSH-AGENT.
     
## Note:
    This is only works with private keys in the PEM format. If used with OpenSSH format keys it will error out.