const {
    Command
} = require('discord.js-commando');
const {
    RichEmbed
} = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class DeleteCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'delete',
            group: 'custom commands',
            memberName: 'delete',
            description: 'Delete a custom command',
            guildOnly: true,
            userPermissions: ['MANAGE_MESSAGES'],
            examples: ['delete <id>"'],
            args: [{
                    key: 'id',
                    prompt: 'What is the ID of the command?',
                    type: 'string'
                }
            ]
        });
    }

    run(msg, { id }) {
        const checkExisting = sql.prepare(`SELECT * FROM commands WHERE server_id = '${msg.guild.id}' AND command_id = ?;`)
        const deleteCommand = sql.prepare(`DELETE FROM commands WHERE server_id = '${msg.guild.id}' AND command_id = ?`)

        if (checkExisting.get(id)) {
            var command = "$" + checkExisting.get(id).command_name;
            var author = checkExisting.get(id).user_who_added;
            var noOfUses = checkExisting.get(id).no_of_uses;

            deleteCommand.run(id);

            sendSuccessResponse(id, command, author, noOfUses);
        } else {
            sendErrorResponse(msg, `Command with ID ${id} doesn't exist!`)
        }

        function sendSuccessResponse(id, command, author, noOfUses) {
            msg.channel.send({
                embed: {
                    color: 4159791,
                    title: `Successfully deleted command!`,
                    fields: [{
                            "name": "Command",
                            "value": command,
                            "inline": true
                        },
                        {
                            "name": "Creator",
                            "value": `<@${author}>`,
                            "inline": true
                        },
                        {
                            "name": "Number of uses",
                            "value": noOfUses,
                            "inline": true
                        },
                        {
                            "name": "ID",
                            "value": id,
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