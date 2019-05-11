const {
    Command
} = require('discord.js-commando');
const { MessageEmbed } = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class ListCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'ls',
            group: 'custom commands',
            memberName: 'ls',
            description: 'List all custom commands',
            guildOnly: true,
            examples: ['$ls']
        });
    }

    run(msg) {
        const allCommandsFromServer = sql.prepare(`SELECT * FROM commands WHERE server_id = '${msg.guild.id}'`).all();
         const embed = new MessageEmbed()
            .setTitle(`All commands for guild ${msg.guild.name}`)
            .setDescription("You look cute today by the way :)")
            .setColor(7506394);

        if (allCommandsFromServer.length == 0) {
            return sendErrorResponse(msg, "There are no commands added for this server! Please add some using the `$add` command. See `$help `for more information.")
        }

        for (const command in allCommandsFromServer) {
            var thisCommand = allCommandsFromServer[command];
            var commandName = thisCommand.command_name;
            var acceptsArgs = thisCommand.args;
            var response = thisCommand.response;
            var noOfUses = thisCommand.no_of_uses;
            var userId = thisCommand.user_who_added;
            var inline = true;
            var commandId = thisCommand.command_id;

            if (response.length > 200) {
                response = response.substring(0, 200)
                response += "..."
                inline = false;
            }
            if (acceptsArgs === 'true') {
                response += "<arg>"
            }
            embed.addField(`$${commandName}`, `**Accepts arguments**: ${acceptsArgs}\n**Response**: ${response}\n**Number of times invoked**: ${noOfUses}\n **Creator of command**: <@${userId}>\n **ID:** ${commandId}`, inline)
        }
        return msg.channel.send({
            embed
        });

        function sendErrorResponse(msg, text) {
            msg.channel.send({
                embed: {
                    color: 12663868,
                    title: "An error occured!",
                    description: text
                }
            })
        }
    }
}