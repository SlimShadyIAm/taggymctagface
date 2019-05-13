const {
    Command
} = require('discord.js-commando');
const {
    MessageEmbed
} = require('discord.js');
const {
    StringStream
} = require("scramjet");
const request = require("request");
const csv = require('csvtojson');
const csvUrl = "http://cros-updates-serving.appspot.com/csv";

module.exports = class CrosServingCommand extends Command {
    constructor(client) {
        super(client, {
            name: 'cros-serving',
            group: 'custom commands',
            memberName: 'cros-serving',
            description: 'Fetch details from the Cros-Serving website',
            guildOnly: true,
            examples: ['cros-serving (board)'],
            args: [{
                key: 'board',
                prompt: "Enter a board name",
                type: 'string',
                default: ''
            }]
        });
    }

    run(msg, { board }) {
        var data;
        var tempCsv;
        var embed = new MessageEmbed();        
        if (board !== '') {
            msg.channel.startTyping();
            parseCsv(embed, csvUrl, board)
            msg.channel.stopTyping();
            return;
        } else {
           return msg.channel.send("http://cros-updates-serving.appspot.com/")
        }

        function parseCsv(embed, url, board) { // this function parses the actual remote CSV file
            tempCsv = {}
            request.get(url)
                .pipe(new StringStream())
                .consume(object => tempCsv += object)
                .then(() => {
                    csv({
                            noheader: true,
                            output: "csv"
                        })
                        .fromString(tempCsv)
                        .then((csvData) => {
                            for (var i = 0; i < csvData.length; i++) {
                                if (csvData[i][0] === board) {
                                    msg.channel.send(pushUpdate(board, embed, csvData[i]));
                                }
                            }
                           
                            
                        })
                });
            // our output (csvRow) looks something like this...
            // [
            //     [1, 2, 3],
            //     [4, 5, 6],
            //     [7, 8, 9]
            // ]
            // we then want to compare the new copy of data
            // to the old copy of the data, to see if we have
            // new updates available
        }

        function pushUpdate(board, embed, csvRow) {
            return embed
                .setTitle(`Cros Serving Updates results for ${board}`)
                .addField("Stable Channel", csvRow[2], true)
                .addField("Beta Channel", csvRow[32], true)
                .addField("Dev Channel", csvRow[34], true)
                .addField("Canary Channel", csvRow[36], true)
                .setColor(7506394)
                .setFooter("Powered by http://cros-updates-serving.appspot.com/");
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