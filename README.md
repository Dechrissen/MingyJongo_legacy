# MingyJongo
 A chatbot for my personal Twitch channel
 
 ## Chat commands
- `!commands`
     - Displays a list of all commands
- `!addcommand <!command_name> <command_text>` (moderator)
     - Adds a basic text command to commands.txt
- `!deletecommand <!command_name>` (channel owner)
     - Deletes a command from commands.txt
- `!quote [number]`
     - Displays a quote from quotes.txt
- `!addquote <quote_text>` (moderator)
     - Adds a quote to quotes.txt
- `!followage [username]`
     - Displays the followage for a user
- `!uptime`
     - Displays the stream uptime
- `!quit` (channel owner)
     - Kill the bot program
 
 ### Croissant Game commands
- `!daily`
    - Receive a daily bonus of 1 - 10 croissants
- `!slots`
    - Play the slots for a chance to win (10-min cooldown)
- `!gamble <wager>`
    - Put croissants on the line for a 50% chance to double your wager or lose it (10-min cooldown)
- `!croissants [username]`
    - Displays the amount of croissants a user has
- `!top3`
    - Displays the top 3 users on the croissant leaderboard
- `!award <username> <amount>` (channel owner)
    - Give a user some amount of points
- `!raffle` (channel owner)
    - Start a raffle
- `!enter`
    - Enter the current raffle
