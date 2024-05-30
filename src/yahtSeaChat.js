const { execFile } = require('child_process');

function processChat(username) {
	const readline = require('readline');

	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout
	});

	rl.on('line', (input) => {
		const [action, target] = input.trim().toLowerCase().split(' ', 2);
		executeCall(username, action, target, (error, result) => {
			process.stdout.write(`${result.message}\n`);
		});
	});
}

function executeCall(username, action, target, callback) {
	execFile('python', ['dice_game.py', username, action, target], (error, stdout, stderr) => {

		const jsonStr = stdout.replace(/'/g, '"');
		callback(null, JSON.parse(jsonStr));
	});
}

module.exports = {
	processChat
};
