const { Command } = require("discord.js-commando");
var timediff = require("timediff");
var pingUsers = [];

module.exports = class HelpersCommand extends Command {
    constructor(client) {
        super(client, {
            name: "helpers",
            group: "custom commands",
            memberName: "helpers",
            description: "Ping @Helpers",
            guildOnly: true,
            examples: ['$helpers"']
        });
    }

    run(msg) {
        if (msg.channel.name !== "support") {
            msg.channel.send("This command is only usable in #support!");
            return;
        }

        var helpersRole = msg.guild.roles.find(role => role.name === "Helpers");
        var pingCooldown = pingUsers.find(user => user.id === msg.author.id);

        if (pingCooldown) {
            var howLongAgoLastPing = timediff(
                pingCooldown.time,
                Date.now(),
                "H"
            ).hours;
            if (howLongAgoLastPing > 3) {
                sendPing(msg, helpersRole);

                var index = pingUsers.indexOf(pingCooldown);
                pingUsers.splice(index, 1);
                pingUsers.push({ id: msg.author.id, time: Date.now() });
            } else {
                msg.channel.send(
                    "Hey! You've pinged Helpers in the past 12 hours. Try again when the cooldown is over!"
                );
            }
        } else {
            sendPing(msg, helpersRole);
        }

        pingUsers.push({ id: msg.author.id, time: Date.now() });
        pingUsers.push({ id: msg.author.id, time: Date.now() });
    }
};
function sendPing(msg, helpersRole) {
    helpersRole.setMentionable(true, "Role needs to be pinged!");
    msg.channel.send(`<@${msg.author.id}> pinged <@&${helpersRole.id}>`);
    helpersRole.setMentionable(
        false,
        "Role doesn't need to be pinged anymore!"
    );
}
