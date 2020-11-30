const { execSync } = require('child_process');

const runner = (ID, category, description, lang) => {
    var pyCommand = '(python python_section/communicator.py' + ' --ID=' + ID + ' --cat=' + category + ' --lang=' + lang + ' --desc=\"' + description + '\")';
    console.log('Waiting for resource...');
    execSync(pyCommand);

    return Date.now();
};

module.exports.runner = runner;