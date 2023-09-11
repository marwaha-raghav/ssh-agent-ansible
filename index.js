const core = require('@actions/core');
const exec = require('@actions/exec');

async function run() {
  try {

    // Call your Python script
    await exec.exec(`python3 ssh_agent.py`);
    
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
