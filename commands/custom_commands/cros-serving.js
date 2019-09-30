const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const board2device = require("../../boardnamedevices.json");
const crosServingObj = require("../../crosserving.json");

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
		var embed = new MessageEmbed();
		var test = RegExp("^[a-zA-Z]*$");
		if (board !== "" && !test.test(board)) {
			return sendErrorResponse(
				msg,
				"Your board name contained illegal characters! Make sure you only use alphabetical lettters."
			);
		}

		if (board !== "") {
			if (board in board2device) {
				findBoardData(embed, board);
				return;
			} else {
				return sendErrorResponse(
					msg,
					`Board ${board} does not exist! Please use a valid board name.`
				);
			}
		} else {
			return msg.channel.send("http://cros-updates-serving.appspot.com/");
		}

		function findBoardData(embed, board) {
			// use the locally cached version data from cros-serving to get cros-serving info
			// for the inputted device
			for (var i = 0; i < crosServingObj.length; i++) {
				if (crosServingObj[i][0] === board) {
					msg.channel.send(pushUpdate(board, embed, crosServingObj[i]));
				}
			}
		}

		function pushUpdate(board, embed, csvRow) {
			// \n is being escaped in the string for each row. Fix this.
			// Also add "Version:" and "Platform:" in relevant locations in string
			for (var i = 5; i < 9; i++) {
				csvRow[i] = csvRow[i]
					.replace(/^/, "**Platform**:  ")
					.replace("\\n", "\r\n**Version**: ");
			}
			return embed
				.setTitle(`Cros Serving Updates results for ${board}`)
				.addField("Stable Channel", csvRow[5], true)
				.addField("Beta Channel", csvRow[6], true)
				.addField("Dev Channel", csvRow[7], true)
				.addField("Canary Channel", csvRow[8], true)
				.setColor(7506394)
				.setFooter("Powered by https://cros-updates.netlify.com/ (by Skylar)");
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
