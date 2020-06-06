const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const { StringStream } = require("scramjet");
const csv = require("csvtojson");
const request = require("request");
const csvUrl =
	"https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.csv";

module.exports = class Device2BoardCommand extends Command {
	constructor(client) {
		super(client, {
			name: "device2board",
			group: "custom commands",
			memberName: "device2board",
			description: "Find the board name for a device",
			guildOnly: true,
			examples: ["device2board Chromebook 14"],
			args: [
				{
					key: "device",
					prompt: "What is the device name?",
					type: "string"
				}
			]
		});
	}

	run(msg, { device }) {
		var test = RegExp("^[a-zA-Z0-9_()&,/ -]*$");

		if (!test.test(device)) {
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
							var boardArray = getKeyByValue(csvObj, device);

							if (boardArray.length == 0) {
								return sendErrorResponse(
									msg,
									`Sorry, we couldn't find any boards with device name ${device}!`
								);
							} else {
								const embed = new MessageEmbed()
									.setTitle(
										`Board(s) found with device name ${device}`
									)
									.setColor(7506394);

								var description = "";
								if (boardArray.length > 5) {
									description =
										"These results were limited to the first 5 found. Please use a more precise query.";
								}
								var i = 1;
								boardArray.forEach(board => {
									if (i < 6) {
										description += `\n\n**${i}. ${
											board[0]
										}** \n${parse(board[10])}`;
										i++;
									}
								});
								embed.setDescription(description);
								return msg.channel.send({ embed });
							}
						});
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
			return result;
		}

		function getKeyByValue(object, value) {
			var returnArray = [];
			object.forEach(device => {
				if (device[10].toLowerCase().includes(value.toLowerCase())) {
					returnArray.push(device);
				}
			});

			return returnArray;
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
