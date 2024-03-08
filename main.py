import disnake
from disnake.ext import commands
import aiocron
import pytz
import ast
import os

bot = commands.InteractionBot()


async def send_scheduled_message(ping=False, time=5):
    with open("settings.txt", "r", encoding="UTF8") as f:
        d = ast.literal_eval(f.read())
        for i in d["channel"]:
            channel = bot.get_channel(d["channel"][i])
            if ping is False:
                await channel.send(f"Chest Raid in {time} minutes")
            elif ping is True:
                await channel.send(f"@everyone Chest Raid in {time} minutes")
            else:
                 await channel.send("Error")


@bot.slash_command(description="test notification")
async def ping(inter, time=5):
    await send_scheduled_message(False, time)
    await inter.response.send_message(".")


@bot.slash_command(description="select channel to notifications")
async def save_channel(inter):
    with open("settings.txt", "r", encoding="UTF8") as f:
        d = ast.literal_eval(f.read())
    with open("settings.txt", "w", encoding="UTF8") as f:
        d["channel"].update({str(inter.channel.guild): inter.channel.id})
        f.writelines(str(d))
    await inter.response.send_message("Successful saving")


@bot.slash_command(description="off notifications")
async def delete_channel(inter):
    with open("settings.txt", "r", encoding="UTF8") as f:
        d = ast.literal_eval(f.read())
    with open("settings.txt", "w", encoding="UTF8") as f:
        d["channel"].pop(str(inter.channel.guild))
        f.writelines(str(d))
    await inter.response.send_message("Successful deleting")


@aiocron.crontab('55 6 * * *', tz=pytz.timezone("Europe/Moscow"))
async def scheduled_message():
    await send_scheduled_message(True)


@aiocron.crontab('55 20 * * *', tz=pytz.timezone("Europe/Moscow"))
async def scheduled_message():
    await send_scheduled_message(True)

# starting
if __name__ == "__main__":
    file_path = "settings.txt"
    if not os.path.isfile(file_path):  # creating settings file, if it is not exist
        with open(file_path, 'w', encoding="UTF8") as file:
            wr = {'token': input("Token: "), "channel": {}}
            file.write(str(wr))
    with open("settings.txt", "r", encoding="UTF8") as f:
        d = ast.literal_eval(f.read())
        bot.run(d["token"])