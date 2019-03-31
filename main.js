const Discord = require("discord.js");
const Enmap = require("enmap");
const fs = require("fs");

const client = new Discord.Client();
const token = process.env.taggytoken;

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
 
const SQLite = require("better-sqlite3");
const sql = new SQLite('./db');

client.on("ready", () => {
	// Check if the table "points" exists.
	const table = sql.prepare("SELECT count(*) FROM sqlite_master WHERE type='table' AND name = 'Guilds';").get();
	if (!table['count(*)']) {
		// If the table isn't there, create it and setup the database correctly.
		sql.prepare("CREATE TABLE Guilds (guild_id TEXT PRIMARY KEY);").run();
		sql.prepare(`CREATE TABLE Guilds_Commands 
						(guild_id TEXT NOT NULL, 
						tag_id INTEGER NOT NULL, 
						tag TEXT, 
						FOREIGN KEY (guild_id) 
							REFERENCES Guilds (guild_id), 
						FOREIGN KEY (tag_id) 
							REFERENCES Tags (tag_id)
					);`)
			.run();
			
		sql.prepare(`CREATE TABLE Commands 
						(tag_id INTEGER PRIMARY KEY NOT NULL, 
						tag TEXT, 
						args TEXT,
						val TEXT,
						count INTEGER,
						adder TEXT
					);`)
			.run();

		// Ensure that the "id" row is always unique and indexed.
		sql.prepare("CREATE UNIQUE INDEX tag_id ON Commands (tag_id);").run();
		sql.pragma("synchronous = 1");
		sql.pragma("journal_mode = wal");
		sql.pragma("foreign_keys = ON")
	}

	// And then we have two prepared statements to get and set the score data.
	// client.getScore = sql.prepare("SELECT * FROM scores WHERE user = ? AND guild = ?");
	// client.setScore = sql.prepare("INSERT OR REPLACE INTO scores (id, user, guild, points, level) VALUES (@id, @user, @guild, @points, @level);");
});
client.login(token);