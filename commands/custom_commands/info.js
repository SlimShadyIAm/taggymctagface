const {
    Command
} = require('discord.js-commando');
const { MessageEmbed } = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class ListCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'info',
            group: 'custom commands',
            memberName: 'info',
            description: 'Information about a specific command',
            guildOnly: true,
            examples: ['$info aue'],
            args: [{
                key: 'id',
                prompt: 'What is the ID of the command?',
                type: 'string'
            }]
        });
    }

    run(msg, { id }) {
        const commandPreparedStatement = sql.prepare(`SELECT * FROM commands WHERE server_id = ? AND command_id = ?`);
        const commandFromDb = commandPreparedStatement.get(msg.guild.id, id);
        
        if (!commandFromDb) {
            return sendErrorResponse(msg, `There is no command with that ID! Please add some using the \`$add\` command. See \`$help \`for more information.`)
        }
        
        var commandName = commandFromDb.command_name;
        var acceptsArgs = commandFromDb.args;
        var response = commandFromDb.response;
        var noOfUses = commandFromDb.no_of_uses;
        var userId = commandFromDb.user_who_added;
        var inline = true;
        var commandId = commandFromDb.command_id;

        const embed = new MessageEmbed()
            .setTitle(`$${commandName}`)
            .setDescription("You look cute today by the way :)")
            .setColor(7506394);

        embed.addField(`Info`, `**Accepts arguments**: ${acceptsArgs}\n**Response**: ${response}\n**Number of times invoked**: ${noOfUses}\n **Creator of command**: <@${userId}>\n **ID:** ${commandId}`, inline)
 
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