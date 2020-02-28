const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const { StringStream } = require("scramjet");
const csv = require("csvtojson");
const request = require("request");
const csvUrl =
	"https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.csv";

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
		var test = RegExp("^[a-zA-Z]*$");
		if (!test.test(board)) {
			return sendErrorResponse(
				msg,
				"Hey! Looks like you had some illegal characters in there!"
			);
		}
		msg.channel.startTyping();
		parseCsv(csvUrl);
		msg.channel.stopTyping();

		function parseCsv(url) {
			// this function parses the actual remote CSV file
			var tempCsv = {};
			request
				.get(url)
				.pipe(new StringStream())
				.consume(object => (tempCsv += object))
				.then(() => {
					csv({
						noheader: true,
						output: "csv"
					})
						.fromString(tempCsv)
						.then(csvObj => {
							var found = false;
							csvObj.forEach(device => {
								if (device[0] == board) {
									const embed = new MessageEmbed()
										.setColor(7506394)
										.setDescription(
											`Board **${board}** belongs to the following device(s):\n\n ${parse(
												device[10]
											)}`
										);
									found = true;
									return msg.channel.send({ embed });
								}
							});
							if (!found) {
								return sendErrorResponse(
									msg,
									`Board **${board}** does not exist! Please enter a valid board name`
								);
							}
						});
				});
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

		function parse(str) {
			let result = "",
				item = "",
				depth = 0;

			function push() {
				if (item) result += ` - ${item}\n`;
				item = "";
			}

			for (let i = 0, c; (c = str[i]), i < str.length; i++) {
				if (!depth && c === ",") push();
				else {
					item += c;
					if (c === "(") depth++;
					if (c === ")") depth--;
				}
			}

			push();
			console.log(result);
			return result;
		}
	}
};
