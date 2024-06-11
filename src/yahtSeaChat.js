const { execFile } = require('child_process');

function processChat(message, username) {
	const [action, target] = message.trim().toLowerCase().split(' ', 2);

	//disable this to test, by providing the term "play" in chat.
	if (action === 'play') {
		return;
	}

	executeCall(username, action, target, (error, result) => {
		process.stdout.write(`${result.message}\n`);
	});
}

function processCommand(m) {
	const readline = require('readline');

	const rl = readline.createInterface({
		input: process.stdin,
		output: process.stdout
	});

	rl.on('line', (input) => {
		const message = input.trim();
		if (message === 'launch') {
			launchPyGame();
		}

		const regex = /^play (.*)$/;
		const match = message.match(regex);
		if (match) {
			play(match[1])
		}

		if (message === 'help') {
			help();
		}
	});
}

function executeCall(username, action, target, callback) {
	if (action === 'hold') {
		if (target !== undefined) {
			target = target.replace(/,| /g, '');
			if (/^\d+$/.test(target) === false) {
				return;
			}

			const uniqueNumbers = Array.from(new Set(target));
			target = uniqueNumbers.join(',');
		} else {
			target  = '';
		}
	}

	if (
		(action === 'play' && target === undefined) ||
		(action === 'hold') ||
		(action === 'roll' && target === undefined) ||
		(action === 'end_round' && target === undefined) ||
		(action === 'leaderboard' && target === undefined) ||
		(action === 'resume' && target === undefined)
	) {
		execFile('python', ['dice_game.py', username, action, target], (error, stdout, stderr) => {
			const jsonStr = stdout.replace(/'/g, '"');
			const response = JSON.parse(jsonStr);
			callback(null, response);

			if (response.message !== '') {
				settings.twitchapi.postMessage(`${response.message}\n`);
			}

			if (action === 'play' && response.data.remainingRolls === 0) {
				settings.twitchapi.postMessage(`A game of YahtSea was redeemed by ${username}!`);
			}
		});
	}
}

function launchPyGame() {
	execFile('python', ['yahtsea_pygame.py'], (error, stdout, stderr) => {
		//nothing to do here
	});
}

function play(username) {
	execFile('python', ['dice_game.py', username, 'play'], (error, stdout, stderr) => {
		//nothing to do here
	});
}

function help() {
	process.stdout.write(
	`launch - Launches YahtSeaPyGame application.
	reset [username] - Resets the game for the specified user.\n
	play [username] - Resets the game for the specified user.\n`
	);
}

var settings;
function init(s) {
	settings = s;
}

module.exports = {
	init,
	processChat,
	processCommand
};
