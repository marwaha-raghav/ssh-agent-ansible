const { execSync } = require('child_process');

function runCommand(command) {
    try {
        // Execute the command
        let output = execSync(command, { stdio: 'inherit' });
        console.log(output);
    } catch (error) {
        console.error(`Error executing command: ${command}\n${error}`);
        process.exit(1);
    }
}

function main() {
    // Install ncc if it's not installed
    console.log("Installing ncc...");
    runCommand('npm install @vercel/ncc');

    // Compile the action's code using ncc
    console.log("Building with ncc...");
    runCommand('npx ncc build index.js -o dist');

    console.log("Build complete!");
}

main();
