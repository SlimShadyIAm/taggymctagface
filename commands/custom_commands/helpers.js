const { Command } = require("discord.js-commando");
var timediff = require("timediff");
var pingUsers = [];

module.exports = class HelpersCommand extends Command {
	constructor(client) {
		super(client, {
			name: "helpers",
			group: "custom commands",
			memberName: "helpers",
			description: "Ping @Helpers",
			guildOnly: true,
			examples: ['$helpers"']
		});
	}

	run(msg) {
		if (msg.channel.name !== "support") {
			msg.channel.send("This command is only usable in #support!");
			return;
		}

		var helpersRole = msg.guild.roles.cache.find(role => role.name === "Helpers");
		var pingCooldown = pingUsers.find(user => user.id === msg.author.id);

		if (pingCooldown) {
			var howLongAgoLastPing = timediff(
				pingCooldown.time,
				Date.now(),
				"H"
			).hours;
			if (howLongAgoLastPing > 12) {
				sendPing(msg, helpersRole);

				var index = pingUsers.indexOf(pingCooldown);
				pingUsers.splice(index, 1);
				pingUsers.push({ id: msg.author.id, time: Date.now() });
			} else {
				msg.channel.send(
					"Hey! You've pinged Helpers in the past 12 hours. Try again when the cooldown is over!"
				);
			}
		} else {
			pingUsers.push({ id: msg.author.id, time: Date.now() });
			sendPing(msg, helpersRole);
		}
	}
};
function sendPing(msg, helpersRole) {
	helpersRole.setMentionable(true, "Role needs to be pinged!").then(() => {
		msg.channel
			.send(`<@${msg.author.id}> pinged <@&${helpersRole.id}>`)
			.then(() => {
				helpersRole.setMentionable(
					false,
					"Role doesn't need to be pinged anymore!"
				);
			});
	});
}
