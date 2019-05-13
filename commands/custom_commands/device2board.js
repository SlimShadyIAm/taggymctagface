const {
    Command
} = require('discord.js-commando');
const {
    MessageEmbed
} = require('discord.js');
const board2device = require("../../boardnamedevices.json")

module.exports = class Device2BoardCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'device2board',
            group: 'custom commands',
            memberName: 'device2board',
            description: 'Find the board name for a device',
            guildOnly: true,
            examples: ['device2board Chromebook 14'],
            args: [{
                    key: 'device',
                    prompt: 'What is the device name?',
                    type: 'string'
                }
            ]
        });
    }

    run(msg, { device }) {
        var test = RegExp('^[a-zA-Z0-9_\(\)&,/ -]*$');

        if(!test.test(device)) {
            return sendErrorResponse(msg, "Hey! Looks like you had some illegal characters in there!")
        }

        var boardArray = getKeyByValue(board2device, device);

        if (boardArray.length == 0) {
            return sendErrorResponse(msg, `Sorry, we couldn't find any boards with device name ${device}!`)
        } else {
            var i = 1;
            const embed = new MessageEmbed()
                .setTitle(`Board(s) found with device name ${device}`)
                .setColor(7506394)

            for (const board in boardArray) {
                
                if (i > 5) {
                    embed.setDescription("These results were limited to the first 5 found. Please use a more precise query.")
                    break;
                } else {
                    embed.addField(`${i}. ${boardArray[i-1]}`, `${board2device[boardArray[i-1]]}`, true);
                }
                i++;
                
            }
            
            return msg.channel.send({ embed })
        }

        function getKeyByValue(object, value) {
            var returnArray = []
            for (const line in object) {
                if (object[line].toLowerCase().includes(value.toLowerCase())) {
                    returnArray.push(line)
                }
            }
            return returnArray;
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