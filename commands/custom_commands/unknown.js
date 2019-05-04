const { Command } = require('discord.js-commando');
const { RichEmbed } = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class UnknownCommandCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'unknown',
            group: 'custom commands',
            memberName: 'unknown',
            description: 'This command outputs the actual custom commnands',
            guildOnly: true,
            examples: [''],
            unknown: true,
            args: [
            {
                key: 'command',
                prompt: 'The command to invoke',
                type: 'string'
            },
            {
                key: 'args',
                prompt: 'Args for the custom command',
                type: 'string',
                default: ''
            }
            ]
        });
    }

    run(msg, { command, args }) {
        console.log('here')
        const checkExisting = sql.prepare(`SELECT * FROM commands WHERE command_name = ?`)
        const checkHasArgs = sql.prepare("SELECT * FROM commands WHERE command_name = ? AND args = ?")

        if (checkExisting.get(command)) {
            const response = "";
            if (args !== '' && checkHasArgs.get(command, 'true')) {
                response += checkHasArgs.response += args;
            } else {
                response += checkExisting.response;
            }
            msg.channel.say(response);
        }
    }
}