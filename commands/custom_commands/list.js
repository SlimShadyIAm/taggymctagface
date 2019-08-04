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
        const allCommandsFromServer = sql.prepare(`SELECT * FROM commands WHERE server_id = '${msg.guild.id}' ORDER BY command_name`).all();
         var embed = new MessageEmbed()
            .setTitle(`All commands for guild ${msg.guild.name}`)
            .setDescription("You look cute today by the way :)")
            .setColor(7506394);

        if (allCommandsFromServer.length == 0) {
            return sendErrorResponse(msg, "There are no commands added for this server! Please add some using the `$add` command. See `$help `for more information.")
        }

        var commandCounter = 1;
        for (const command in allCommandsFromServer) {
            if (commandCounter % 10 == 0) {
                msg.channel.send({
                    embed
                });
                embed = new MessageEmbed()
                    .setTitle(`Commands (continued)`)
                    .setColor(7506394);
            }
            var thisCommand = allCommandsFromServer[command];
            var commandName = thisCommand.command_name;
            var acceptsArgs = thisCommand.args;
            var inline = true;
            var commandId = thisCommand.command_id;

            embed.addField(`$${commandName}`, `**Accepts arguments**: ${acceptsArgs}\n**ID:** ${commandId}`, inline)

            commandCounter++;
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