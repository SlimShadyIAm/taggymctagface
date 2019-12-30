const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const request = require("request");
const cheerio = require("cheerio");

module.exports = class Board2DeviceCommand extends Command {
	constructor(client) {
		super(client, {
			name: "board2device",
			group: "custom commands",
			memberName: "board2device",
			description: "Find the device name for a board",
			guildOnly: true,
			examples: ["board2device coral"],
			args: [
				{
					key: "board",
					prompt: "What is the board name?",
					type: "string"
				}
			]
		});
	}

	run(msg, { board }) {
		var board2device;
		var test = RegExp("^[a-zA-Z]*$");
		if (!test.test(board)) {
			return sendErrorResponse(
				msg,
				"Hey! Looks like you had some illegal characters in there!"
			);
		}
		msg.channel.startTyping();
		updateLocalBoardInfo();
		msg.channel.stopTyping();

		function updateLocalBoardInfo() {
			request(
				"https://dark-nova.me/chromeos/boardnamedevices-2.json",
				function(error, response, html) {
					if (!error && response.statusCode == 200) {
						var $ = cheerio.load(html);
						var obj = JSON.parse($.text());
						board2device = obj;

						board = board.toLowerCase();
						console.log(board2device);
						if (board in board2device) {
							const embed = new MessageEmbed()
								.setColor(7506394)
								.setDescription(
									`Board **${board}** belongs to the following device(s): **${board2device[board]}**`
								);
							return msg.channel.send({ embed });
						} else {
							return sendErrorResponse(
								msg,
								`Board **${board}** does not exist! Please enter a valid board name`
							);
						}
					} else {
						return sendErrorResponse(
							msg,
							"Problem reaching feed :("
						);
					}
				}
			);
		}

		function sendErrorResponse(msg, text) {
			msg.channel.send({
				embed: {
					color: 12663868,
					title: "An error occured!",
					description: text
				}
			});
		}
	}
};
