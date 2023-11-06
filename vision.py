import discord
import os
from openai import OpenAI

openai.api_key = youropenaiapikey
discord_apikey = yourdiscordapikey

def getDescription(url):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": url,
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return(response.choices[0].message.content)

intents = discord.Intents.all()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if len(message.attachments) > 0:
        for attachment in message.attachments:
            if attachment.filename.endswith('.jpg') or attachment.filename.endswith('.png'):
                url = message.attachments[0].url
                await message.reply(getDescription(url))
client.run(yourdiscordapikey)
