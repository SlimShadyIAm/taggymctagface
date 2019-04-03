exports.run = (client, message, args) => {
    if (args[0] === "add") {
        console.log("We got a tag add")
        tag = {
            id: 0,
            tag: args[1],
            args: "", 
            val: args[2],
            count: 0,
            adder: message.author.id
        }
        g_c = {
            guild_id: message.guild.id,
            tagarg_id: 0,
            tagarg: args[1]
        }
        client.addtag(tag);
        client.updaterel(g_c);
        
        console.log("We got a tag added")
    }
    if (args[0] === "list") {

    }
}

