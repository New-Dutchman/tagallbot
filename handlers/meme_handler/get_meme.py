from bot import bot, conn
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from random import choice
from database import Meme


get_meme_router = Router()


@get_meme_router.message(Command(commands = 'meme'))
async def get_meme(message: Message) -> None:
    chat_id: int = message.chat.id

    command: list[str] = message.text.split(' ')

    match command:
        case (_, '-random', '-nocap'):
            if len(memes := conn.get_all_memes()) != 0:
                random_meme: Meme = choice(memes)

                await bot.send_photo(chat_id, random_meme.id)
            else:
                await bot.send_message(chat_id, 'В базе ещё нет мемов :(')

        case (_, '-random'):
            if len(memes := conn.get_all_memes()) != 0:
                random_meme: Meme = choice(memes)

                caption = 'Название: {:s}\nТеги: {:s}'.format(random_meme.name, random_meme.tags)

                await bot.send_photo(chat_id, random_meme.id, caption = caption)
            else:
                await bot.send_message(chat_id, 'В базе ещё нет мемов :(')

        case(_, '-nocap', *words):
            name: str = ' '.join(words)

            meme: Meme = conn.get_meme_by_name(name)

            if meme:
                await bot.send_photo(chat_id, meme.id)
            else:
                await message.reply('Я не нашёл такого мема :(')

        case (_, *words):
            name: str = ' '.join(words)

            meme: Meme = conn.get_meme_by_name(name)

            if meme:
                caption = 'Название: {:s}\nТеги: {:s}'.format(meme.name, meme.tags)

                await bot.send_photo(chat_id, meme.id, caption = caption)
            else:
                await message.reply('Я не нашёл такого мема :(')

        case _:
            await message.reply('Неправильно команду используешь')

@get_meme_router.message(Command(commands = 'random'))
async def get_random_meme(chat_id: int):
    # message = (await bot.get_random_meme())
    from_chat_id, message_id, photo_id = bot.__conn.get_random_meme()
    try:
        message = await bot.copy_message(chat_id, from_chat_id, message_id)
        return message
    except Exception as e:
        bot.__conn.delete_from_arxive(chat_id, message_id)
        return None    