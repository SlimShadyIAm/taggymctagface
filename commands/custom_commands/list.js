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
            .setDescription("You look cute today by the way :)");


        for (const command in allCommandsFromServer) {
            embed.addField("Command", allCommandsFromServer[command].command_name, true);
            embed.addField("Response", allCommandsFromServer[command].response, true);
            embed.addBlankField();
        }
        return msg.channel.send({
            embed
        });

        function sendSuccessResponse(msg, commandName, args, response) {
            msg.channel.send({
                embed: {
                    color: 4159791,
                    title: `Successfully added command to the leaderboard!`,
                    fields: [{
                            "name": "Command",
                            "value": commandName,
                            "inline": true
                        },
                        {
                            "name": "Creator",
                            "value": `<@${msg.author.id}>`,
                            "inline": true
                        },
                        {
                            "name": "Response",
                            "value": response,
                            "inline": true
                        },
                        {
                            "name": "Arguments supported?",
                            "value": args,
                            "inline": true
                        }
                    ]
                }
            })
        }

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