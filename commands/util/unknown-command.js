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
                key: 'cmd',
                prompt: 'Args for the custom command',
                type: 'string'
            }
            ]
        });
    }

    run(msg, { cmd }) {
        var args = msg.content.split(" ")[1];
        var argsFlag = 'false';
        if (args) {
            argsFlag = 'true';
        }
        const getCommandFromDb = sql.prepare("SELECT * FROM commands WHERE command_name = ? AND args = ? AND server_id = ?")
        const incrementUseCounter = sql.prepare ("UPDATE commands SET no_of_uses = ? WHERE command_name = ? AND args = ? AND server_id = ?")
        // console.log(cmd+ args)
        if (getCommandFromDb.get(cmd, argsFlag, msg.guild.id)) {
            var useCounter = getCommandFromDb.get(cmd, argsFlag, msg.guild.id).no_of_uses + 1;
            incrementUseCounter.run(useCounter, cmd, argsFlag, msg.guild.id);
            console.log(useCounter)
            if (argsFlag === 'true' && getCommandFromDb.get(cmd, 'true', msg.guild.id)) {
                return msg.say(getCommandFromDb.get(cmd, argsFlag, msg.guild.id).response += args);
            } else {
                return msg.say(getCommandFromDb.get(cmd, argsFlag, msg.guild.id).response);
            }
            
        }
    }
}