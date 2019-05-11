//const Discord = require('discord.js');
const { CommandoClient } = require('discord.js-commando');
const SQLite = require("better-sqlite3");
const sql = new SQLite('./commands.sqlite');
const path = require('path');

const token = process.env.taggyToken;
const client = new CommandoClient({
    commandPrefix: '$',
    owner: '109705860275539968',
    disableEveryone: true,
    unknownCommandResponse: true
})

client.registry
    .registerDefaultTypes()
    .registerGroups([
        ['custom commands', 'Custom commands, used for invoking resources and helpful links']
	])
	.registerDefaultGroups()
	.registerDefaultCommands({
		unknownCommand: false
	  })
    .registerCommandsIn(path.join(__dirname, 'commands'));
client.on('ready', () => {
    const table = sql.prepare("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='commands';").get();
    if (!table['count(*)']) {
        // no table exists, create one and setup the database properly
        sql.prepare("CREATE TABLE commands (command_id INTEGER PRIMARY KEY, server_id TEXT, user_who_added TEXT, command_name TEXT, no_of_uses INTEGER, response TEXT, args TEXT);").run();
        sql.prepare("CREATE UNIQUE INDEX idx_command_id ON commands (command_id);").run();
        sql.pragma("synchronous = 1");
        sql.pragma("journal_mode = wal");
    }

    console.log("Logged in!");
})

client.on('error', console.error);

client.login(token);
