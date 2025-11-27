## About
A python rewrite of the original dozer-discord-bot.
Much of this project is powered by the blue alliance at https://www.thebluealliance.com/

## Setup
1. To run the bot, create a file called ".env" in the project root.
2. Add your token to the file in this form: 
    ```
    token=YourTokenHere
    ```
3. Add the id of the guild the bot will be run on to the dotenv.
    This provides instant syncing to the guild and is required for this bot.
     ```
    guild_id=YourGuildIdHere
    ```
4. Run main.py

Requires the discord.py and dotenv libraries