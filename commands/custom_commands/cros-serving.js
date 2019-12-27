const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const { StringStream } = require("scramjet");
const csv = require("csvtojson");
const request = require("request");
const csvUrl =
	"https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.csv";

module.exports = class CrosServingCommand extends Command {
	constructor(client) {
		super(client, {
			name: "cros-serving",
			group: "custom commands",
			memberName: "cros-serving",
			description: "Fetch details from the Cros-Serving website",
			guildOnly: true,
			examples: ["cros-serving (board)"],
			args: [
				{
					key: "board",
					prompt: "Enter a board name",
					type: "string",
					default: ""
				}
			]
		});
	}

	run(msg, { board }) {
		msg.channel.startTyping();
		var embed = new MessageEmbed();
		var crosServingObj;
		parseCsv(csvUrl);
		msg.channel.stopTyping();
		function findBoardData(embed, board) {
			// use the locally cached version data from cros-serving to get cros-serving info
			// for the inputted device
			var found = false;
			for (var i = 0; i < crosServingObj.length; i++) {
				if (crosServingObj[i][0] === board) {
					found = true;
					msg.channel.send(
						pushUpdate(board, embed, crosServingObj[i])
					);
				}
			}

			if (!found) {
				sendErrorResponse(
					msg,
					`Board ${board} does not exist! Please use a valid board name.`
				);
			}
		}

		function pushUpdate(board, embed, csvRow) {
			// \n is being escaped in the string for each row. Fix this.
			// Also add "Version:" and "Platform:" in relevant locations in string
			var tempCsv = csvRow;
			for (var i = 5; i < 9; i++) {
				tempCsv[i] = tempCsv[i]
					.replace(/^/, "**Platform**:  ")
					.replace("\\n", "\r\n**Version**: ");
			}
			return embed
				.setTitle(`Cros Serving Updates results for ${board}`)
				.addField("Stable Channel", tempCsv[5], true)
				.addField("Beta Channel", tempCsv[6], true)
				.addField("Dev Channel", tempCsv[7], true)
				.addField("Canary Channel", tempCsv[8], true)
				.setColor(7506394)
				.setFooter(
					"Powered by https://cros-updates.netlify.com/ (by Skylar)"
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
						.then(csv => {
							crosServingObj = csv;
							var test = RegExp("^[a-zA-Z]*$");
							if (board !== "" && !test.test(board)) {
								return sendErrorResponse(
									msg,
									"Your board name contained illegal characters! Make sure you only use alphabetical lettters."
								);
							}

							if (board !== "") {
								findBoardData(embed, board);
								return;
							} else {
								return msg.channel.send(
									"http://cros-updates-serving.appspot.com/"
								);
							}
						});
				});
			// our output (csvRow) looks something like this...
			// [
			//     [1, 2, 3],
			//     [4, 5, 6],
			//     [7, 8, 9]
			// ]
			// we then want to compare the new copy of data
			// to the old copy of the data, to see if we have
			// new updates available
		}
	}
};
