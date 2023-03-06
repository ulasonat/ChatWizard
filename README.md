# ChatWizard
Discord bot to encourage positiveness within a server by analyzing and scoring each member's behavior.


![](https://img.shields.io/github/license/ulasonat/prime-video-plus?color=blue&label=License)
![](https://img.shields.io/github/issues/ulasonat/ChatWizard)


## Prerequisites 

To execute the program, you will need to have:
- Python 3 installed
- An OpenAI API key
- A Discord API key
- The following packages imported:
  - `discord`
  - `openai`
  - `faker`
  - `coverage`


To execute the Discord bot:
<code>python3 main.py</code>

## Test & Coverage

<code>make test</code>
<code>make coverage</code>

| Filename      | Coverage |
| ----------- | ----------- |
| *discord_bot.py*       | 68%       |
| *openai_handler.py*   | 89%        |
| **TOTAL COVERAGE**  | 80.4%        |



## Overview
The bot will assess members based on factors such as helpfulness and language use to encourage and reward positive contributions. Whether you're looking to improve the overall tone of your server or simply incentivize positive behavior, ChatWizard can help create a more welcoming and supportive environment for everyone!

## How will it work?
Our bot will leverage the OpenAI API to analyze members' text and assign them scores based on various categories. For example, if a member writes something like <em>"Sure, let me know if you have any questions."</em>, this will increase their helpfulness score and the bot may assign them a <em>Helper</em> role if they continue to exhibit helpful behavior. With our bot, users can be recognized and rewarded for their contributions, while also helping to create a more positive and supportive community within the server.

## Which technologies?
The main programming language for the project is Python, while the main APIs will be the OpenAI and Discord.
