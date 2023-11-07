import discord
import os
from openai import OpenAI

apikey = youropenaiapikey
discord_apikey = yourdiscordapikey

def getImage(description):
    client = OpenAI(
    api_key = apikey,
    )
    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

def getDescription(url):
    client = OpenAI(
        api_key = apikey,
    )
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe the image in detail using as many proper names for each of the items as possible."},
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
                description = getDescription(url)
                await message.reply(description + "\n\nHere's my best effort in creating the image:  " + getImage(description))

client.run(yourdiscordapikey)
