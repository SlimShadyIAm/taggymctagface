const { Command } = require('discord.js-commando');
const { RichEmbed } = require('discord.js');
const SQLite = require("better-sqlite3");
const sql = SQLite('./commands.sqlite');

module.exports = class UnknownCommandCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'unknown-command',
            group: 'util',
            memberName: 'unknown-command',
            description: 'Displays help information for when an unknown command is used.',
            examples: ['unknown-command kickeverybodyever'],
            unknown: true,
            hidden: true,
            args:[
            {
                key: 'args',
                prompt: 'Args for the custom command',
                type: 'string',
                default: ''
            }
            ]
        });
    }

    run(msg, { args }) {
        var command = msg.content.split(' ')[0].slice(1);
        const checkExisting = sql.prepare(`SELECT * FROM commands WHERE command_name = ?`)
        const checkHasArgs = sql.prepare("SELECT * FROM commands WHERE command_name = ? AND args = ?")

        if (checkExisting.get(command)) {
            if (args !== '' && checkHasArgs.get(command, 'true')) {
                console.log('here1')
                return msg.say(checkHasArgs.response += args);
            } else {
                console.log(checkExisting.get(command).response);
                return msg.say(checkExisting.get(command).response);
            }
            
        }
    }
}