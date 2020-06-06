const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");
const axios = require('axios').default;

const REQ_URL =
	"https://raw.githubusercontent.com/skylartaylor/cros-updates/master/src/data/cros-updates.json";

module.exports = class CrosServingCommand extends Command {
	constructor(client) {
		super(client, {
			name: "cros-serving",
			aliases: ["updates", "cros-updates"],
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
		axios
			.get(REQ_URL)
			.then((data) => {
				const deviceData = data.data;
				const ourBoard = deviceData.filter(item => item.Codename == board)[0];
				if (!ourBoard) {
					return sendErrorResponse(msg,`Board ${board} does not exist! Please use a valid board name.`);
				}
				var preparedData = {
					stable: {
						platform: ourBoard.Stable.split("<br>")[0],
						version: ourBoard.Stable.split("<br>")[1]
					},
					beta: {
						platform: ourBoard.Beta.split("<br>")[0],
						version: ourBoard.Beta.split("<br>")[1]
					},
					dev: {
						platform: ourBoard.Dev.split("<br>")[0],
						version: ourBoard.Dev.split("<br>")[1]
					},
					canary: {
						platform: ourBoard.Canary.split("<br>")[0],
						version: ourBoard.Canary.split("<br>")[1]
					}
				}
				return msg.channel.send(pushUpdate(preparedData));		 
			}).catch(() => {
				return sendErrorResponse(msg, "Some error occured! Maybe the feed is down. Contact SlimShadyIAm or Skylar.")
			  })
			  .finally(() => {
				msg.channel.stopTyping();
		});
		function sendErrorResponse(msg, text) {
			msg.channel.send(new MessageEmbed()
				.setColor(7506394)
				.setTitle("An error occured!")
				.setDescription(text));
		}
		function pushUpdate(boardData) {
			return new MessageEmbed()
				.setTitle(`Cros Serving Updates results for ${board}`)
				.addField("Stable Channel", `**Version**: ${boardData.stable.version}\n **Platform**: ${boardData.stable.platform}`, true)
				.addField("Beta Channel", `**Version**: ${boardData.beta.version}\n **Platform**: ${boardData. beta.platform}`, true)
				.addField("Dev Channel", `**Version**: ${boardData.dev.version}\n **Platform**: ${boardData.dev.platform}`, true)
				.addField("Canary Channel", `**Version**: ${boardData.canary.version}\n **Platform**: ${boardData.canary.platform}`, true)
				.setColor(7506394)
				.setFooter(
					"Powered by https://cros.tech/ (by Skylar)"
				);
		}
	}
};
