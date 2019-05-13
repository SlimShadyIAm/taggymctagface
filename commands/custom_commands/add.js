const {
    Command
} = require('discord.js-commando');
const {
    RichEmbed
} = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class AddCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'add',
            group: 'custom commands',
            memberName: 'add',
            description: 'Add a custom command',
            guildOnly: true,
            userPermissions: ['MANAGE_MESSAGES'],
            examples: ['add commandname true "response"'],
            args: [{
                    key: 'commandName',
                    prompt: 'What is the name of the command?',
                    type: 'string'
                },
                {
                    key: 'args',
                    prompt: 'Is this a command with args?',
                    type: 'string',
                    default: 'false'
                },
                {
                    key: 'response',
                    prompt: 'What is the output you want?',
                    type: 'string'
                }
            ]
        });
    }

    run(msg, { commandName, args, response }) {
        const checkExisting = sql.prepare(`SELECT * FROM commands WHERE command_name = ? AND args = ?;`)
        const addNewCommand = sql.prepare("INSERT OR REPLACE INTO commands (command_id, server_id, user_who_added, command_name, no_of_uses, response, args) VALUES (@command_id, @server_id, @user_who_added, @command_name, @no_of_uses, @response, @args)")
        var test = RegExp('^[a-zA-Z0-9_-]*$');

        if (!test.test(commandName)) {
            return sendErrorResponse(msg, "Your command name has illegal characters! Please make sure it contains only the following: `A-Z, a-z, 0-9, _, -`")
        }

        if (args !== 'true' && args !== 'false') {
            return sendErrorResponse(msg, "Please specify whether you want arguments or not! See `$help` for the command usage.")
        }

        if (!checkExisting.get(commandName, args)) {
            const leaderboard = {
                command_id: generateCommandID(100000),
                server_id: msg.guild.id,
                user_who_added: msg.author.id,
                command_name: commandName,
                no_of_uses: 0,
                response: response,
                args: args
            }
            addNewCommand.run(leaderboard);

            response = response.slice(0, 1000) + "...";
            sendSuccessResponse(msg, commandName, args, response);
        } else {
            sendErrorResponse(msg, `Command with name ${commandName} already exists!`)
        }
        function generateCommandID(max) {
            return Math.floor(Math.random() * Math.floor(max));
        }

        function sendSuccessResponse(msg, commandName, args, response) {
            msg.channel.send({
                embed: {
                    color: 1558399,
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