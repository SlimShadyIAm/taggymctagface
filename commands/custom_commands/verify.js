const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");

module.exports = class VerifyCommand extends Command {
	constructor(client) {
		super(client, {
			name: "verify",
			group: "custom commands",
			memberName: "verify",
			description: "Verify user",
			guildOnly: true,
			examples: ["$verify"],
			userPermissions: ["MANAGE_MESSAGES"],
			args: [
				{
					key: "member",
					prompt: "Who do you want to verify?",
					type: "member"
				}
			]
		});
	}

	run(msg, { member }) {
		let acceptedRole = msg.guild.roles.find(
			role => role.name === "accepted-rules"
		);

		member.roles
			.add(acceptedRole)
			.then(() => {
				const embed = new MessageEmbed()
					.setTitle(`Done!`)
					.setDescription(
						`Verified <@${member.id}>. We will also let them know you manually gave them the role.`
					)
					.setColor(7506394);

				const dmEmbed = new MessageEmbed()
					.setTitle(`Approved!`)
					.setDescription(
						`Moderator ${msg.author.username}#${msg.author.discriminator} manually gave you the role to accept the rules, so you can now talk in the server. Enjoy!`
					)
					.setColor(7506394);

				member.send(dmEmbed);
				return msg.channel.send({
					embed
				});
			})
			.catch(() => {
				sendErrorResponse("An error occurred while adding the role!");
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
