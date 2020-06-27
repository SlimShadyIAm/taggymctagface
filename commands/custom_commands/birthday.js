const { Command } = require("discord.js-commando");
const { MessageEmbed } = require("discord.js");

module.exports = class VerifyCommand extends Command {
	constructor(client) {
		super(client, {
			name: "birthday",
			group: "custom commands",
			memberName: "birthday",
			description: "Toggle user birthday role",
			guildOnly: true,
			examples: ["$birthday"],
			userPermissions: ["MANAGE_MESSAGES"],
			args: [
				{
					key: "member",
					prompt: "Who do you want to toggle the birthday role for?",
					type: "member"
				}
			]
		});
	}

	run(msg, { member }) {
		let birthdayRole = msg.guild.roles.cache.find(role => role.name === "birthday boi")

		member.roles.add(birthdayRole).then(() => {
			const embed = new MessageEmbed()
				.setTitle(`Done!`)
				.setDescription(
					`Gave <@${member.id}> the birthday role. We will remove it in 24 hours.`
				)
				.setColor(7506394);

			const dmEmbed = new MessageEmbed()
				.setTitle(`Happy birthday!`)
				.setDescription(
					`Moderator ${msg.author.username}#${msg.author.discriminator} gave you the birthday role. Happy birthday! (role is removed in 24 hours)`
				)
				.setColor(7506394);

			member.send(dmEmbed);
			msg.channel.send(embed);

			setTimeout(() => {
				member.roles.remove(birthdayRole).then(() => {
					const embed = new MessageEmbed()
						.setTitle(`Birthday role expired!`)
						.setDescription(
							`Removed ${member.user.username}#${member.user.discriminator}'s birthday role. We will remove it in 24 hours.`
						)
						.setColor(7506394);

					const dmEmbed = new MessageEmbed()
						.setTitle(`Birthday role expired!`)
						.setDescription(
							`Your birthday role has expired! We've removed it.`
						)
						.setColor(7506394);
					member.send(dmEmbed);
					msg.author.send(embed);
				});
			}, 86400000);
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
