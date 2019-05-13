const {
    Command
} = require('discord.js-commando');
const {
    MessageEmbed
} = require('discord.js');
const board2device = require("../../boardnamedevices.json")

module.exports = class Board2DeviceCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'board2device',
            group: 'custom commands',
            memberName: 'board2device',
            description: 'Find the device name for a board',
            guildOnly: true,
            examples: ['board2device coral'],
            args: [{
                    key: 'board',
                    prompt: 'What is the board name?',
                    type: 'string'
                }
            ]
        });
    }

    run(msg, { board }) {
        var test = RegExp('^[a-zA-Z]*$');

        if(!test.test(board)) {
            return sendErrorResponse(msg, "Hey! Looks like you had some illegal characters in there!")
        }
        board = board.toLowerCase();
        
        if (board in board2device) {
            const embed = new MessageEmbed()
                .setColor(7506394)
                .setDescription(`Board **${board}** belongs to the following device(s): **${board2device[board]}**`);
            return msg.channel.send({ embed });
        } else {
            return sendErrorResponse(msg, `Board **${board}** does not exist! Please enter a valid board name`)
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