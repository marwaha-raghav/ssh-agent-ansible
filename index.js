const core = require('@actions/core');
const exec = require('@actions/exec');

async function run() {
  try {
    
    // Retrieve the action's inputs
    const ANSIBLE_SSH_KEY = core.getInput('ANSIBLE_SSH_KEY');
    const SSH_KEY_PASSPHRASE = core.getInput('SSH_KEY_PASSPHRASE');
    const SSH_AUTH_SOCK = core.getInput('SSH_AUTH_SOCK');

    // Set environment variables for the exec command
    const env = {
      ANSIBLE_SSH_KEY: ANSIBLE_SSH_KEY,
      SSH_KEY_PASSPHRASE: SSH_KEY_PASSPHRASE,
      SSH_AUTH_SOCK: SSH_AUTH_SOCK
    };

    // Python script with the environment variables
    await exec.exec(`python3 ../py_scripts/ssh_agent_ansible.py`, [], { env: env });
    
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();