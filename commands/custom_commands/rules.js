const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");

module.exports = class RulesCommand extends Command {
	constructor(client) {
		super(client, {
			name: "rules",
			group: "custom commands",
			memberName: "rules",
			description:
				"Remove accepted-rules role from person, 5m cooldown to be able to accept again. For discipline.",
			guildOnly: true,
			examples: ["$rules @SlimShadyIAm"],
			userPermissions: ["MANAGE_MESSAGES"],
			args: [
				{
					key: "member",
					prompt: "Who do you want to discipline?",
					type: "member"
				}
			]
		});
	}

	run(msg, { member }) {
		let acceptedRole = msg.guild.roles.find(
			role => role.name === "accepted-rules"
		);
		let rulesRole = msg.guild.roles.find(role => role.name === "rules");

		member.roles.remove(acceptedRole);
		member.roles.add(rulesRole).then(() => {
			const embed = new MessageEmbed()
				.setTitle(`Done!`)
				.setDescription(
					`Removed <@${member.id}>'s accepted role. We'll let them know they need to read the rules.`
				)
				.setColor(7506394);

			const dmEmbed = new MessageEmbed()
				.setTitle(`Punished!`)
				.setDescription(
					`Moderator ${msg.author.username}#${msg.author.discriminator} thinks you need to re-read the rules. **You are on a 5 minute cooldown**. Please use this time to read the rules and then re-accept the rules in #verify!`
				)
				.setColor(12663868);

			member.send(dmEmbed);
			msg.channel.send({
				embed
			});
			setTimeout(() => {
				member.roles.remove(rulesRole);
			}, 30000);
		});

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
