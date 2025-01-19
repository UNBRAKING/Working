import json
import os
import subprocess
from pathlib import Path
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
from pyrogram.errors import MessageIdInvalid
# Importing configurations
from info import Config, Txt
# Define OWNER and SUDO properly
OWNER = Config.OWNER  # Ensure Config has OWNER defined
SUDO = Config.SUDO    # Ensure Config has SUDO defined
AUTHORIZED_USERS = [OWNER] + SUDO
# Path to the config file
config_path = Path("config.json")
async def Report_Function(No):
    list_of_choices = [
        'Report for child abuse', 'Report for copyrighted content', 'Report for impersonation',
        'Report an irrelevant geogroup', 'Report an illegal drug', 'Report for Violence',
        'Report for offensive person detail', 'Reason for Pornography', 'Report for spam'
    ]
    message = list_of_choices[int(No) - 1]
    # Run a shell command and capture its output
    process = subprocess.Popen(
        ["python", "report.py", message],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()
    return_code = process.wait()
    if return_code == 0:
        output = stdout.decode('utf-8')
        return [output, True]
    else:
        error_output = stderr.decode('utf-8')
        return f"<b>Something Went Wrong! Check your Inputs!</b>\n\n
<code>{error_output}</code>\n ERROR"
async def CHOICE_OPTION(bot, msg, number):
    if not config_path.exists():
        return await msg.reply_text(
            text="**You don't have any config. Create it first to report**\n\n Use /make_config",
            reply_to_message_id=msg.id,
            reply_markup=ReplyKeyboardRemove()
        )
    with open(config_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    if Path('report.txt').exists():
        return await msg.reply_text(
            text="**A process is already running. Please wait until it finishes ⏳ **",
            reply_to_message_id=msg.id
        )
    try:
        no_of_reports = await bot.ask(
            text=Txt.SEND_NO_OF_REPORT_MSG.format(config['Target']),
            chat_id=msg.chat.id,
            filters=filters.text,
            timeout=30,
            reply_markup=ReplyKeyboardRemove()
        )
    except:
        await bot.send_message(msg.from_user.id, "Error!!\n\nRequest
timed out.\nRestart by using /report")
        return
    ms = await bot.send_message(
        chat_id=msg.chat.id,
        text=f"**Please wait**\n\n Have patience ⏳  ",
        reply_to_message_id=msg.id,
        reply_markup=ReplyKeyboardRemove()
    )
    if no_of_reports.text.isnumeric():
        try:
            for _ in range(int(no_of_reports.text)):
                result = await Report_Function(number)
                if result[1]:
                    output_string = result[0].replace('\r\n', '\n')
                    with open('report.txt', 'a+', encoding='utf-8') as file:
                        file.write(output_string)
                else:
                    await bot.send_message(chat_id=msg.chat.id, text=f"{result}", reply_to_message_id=msg.id)
        except Exception as e:
            return await msg.reply_text(text=f"**{e}**\n\n ERROR!")
    else:
        await msg.reply_text(text="**Enter a valid integer number!**\n\nTry again: /report")
        return
    await ms.delete()
    await msg.reply_text(text=f"Successfully reported @{config['Target']} ✅  \n\n{no_of_reports.text} times")
    with open('report.txt', 'a', encoding='utf-8') as file:
        file.write(f"\n\n@{config['Target']} was reported {no_of_reports.text} times ✅ ")
    await bot.send_document(chat_id=msg.chat.id, document='report.txt', reply_to_message_id=msg.id)
    os.remove('report.txt')
@Client.on_message(filters.private & filters.user(AUTHORIZED_USERS) & filters.command('report'))
async def handle_report(bot: Client, cmd: Message):
    CHOICE = [
        [("1"), ("2")], [("3"), ("4")], [("5"), ("6")], [("7"), ("8")], [("9")]
    ]
    await bot.send_message(
        chat_id=cmd.from_user.id,
        text=Txt.REPORT_CHOICE,
        reply_to_message_id=cmd.id,
        reply_markup=ReplyKeyboardMarkup(CHOICE, resize_keyboard=True)
    )
@Client.on_message(filters.regex("1"))
async def one(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 1)
@Client.on_message(filters.regex("2"))
async def two(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 2)
@Client.on_message(filters.regex("3"))
async def three(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 3)
@Client.on_message(filters.regex("4"))
async def four(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 4)
@Client.on_message(filters.regex("5"))
async def five(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 5)
@Client.on_message(filters.regex("6"))
async def six(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 6)
@Client.on_message(filters.regex("7"))
async def seven(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 7)
@Client.on_message(filters.regex("8"))
async def eight(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 8)
@Client.on_message(filters.regex("9"))
async def nine(bot: Client, msg: Message):
    await CHOICE_OPTION(bot, msg, 9)