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
        var argsArray= msg.content.split(" ");
        var args = "";
        for (var i = 1; i<argsArray.length; i++) {
            args += argsArray[i] + " ";
        }
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
            if (argsFlag === 'true' && getCommandFromDb.get(cmd, 'true', msg.guild.id)) {
                var response = getCommandFromDb.get(cmd, argsFlag, msg.guild.id).response;
                if (isUrl(response)) {
                    for (var i = 1; i<argsArray.length; i++) {
                        response += argsArray[i];
                        if (i != argsArray.length -1) {
                            response += "%20";
                        }
                    }
                } else {
                    response += " "
                    for (var i = 1; i<argsArray.length; i++) {
                        response += argsArray[i] + " ";
                    }
                }
                return msg.say(response);
            } else {
                return msg.say(getCommandFromDb.get(cmd, argsFlag, msg.guild.id).response);
            }
            
        }
        function isUrl(s) {
            var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/
            return regexp.test(s);
         }
    }
}