const Discord = require("discord.js");
const Enmap = require("enmap");
const fs = require("fs");

const client = new Discord.Client();
const token = process.env.taggytoken;
var tagJson;

try {
	tagJson = require('./tagDb.json');
} catch (err) {
	console.error("You haven't created the tagDb.json file!");
	console.log(err);
	process.exit(1);
}

fs.readdir("./events/", (err, files) => {
	if (err) return console.error(err);
	files.forEach(file => {
		const event = require(`./events/${file}`);
		let eventName = file.split(".")[0];
		client.on(eventName, event.bind(null, client));
	});
});

client.commands = new Enmap();

fs.readdir("./commands/", (err, files) => {
	if (err) return console.error(err);
	files.forEach(file => {
	  if (!file.endsWith(".js")) return;
	  let props = require(`./commands/${file}`);
	  let commandName = file.split(".")[0];
	  console.log(`Attempting to load command ${commandName}`);
	  client.commands.set(commandName, props);
	});
  });

client.on("ready", () => {
	if (tagJson[0] == null) {
		console.log("here")
	}
});

client.login(token);