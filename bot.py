import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (ApplicationBuilder, ContextTypes, CommandHandler,
                          InlineQueryHandler)

from shikimori_requests import (get_user, search_animes,
                                check_anime_entry_in_user_list)
from utils import (get_environment_variable, NotFoundError, UnauthorizedError,
                   ForbiddenError, TooManyRequestsError)

TOKEN = get_environment_variable('TOKEN')
BOT_USERNAME = get_environment_variable('BOT_USERNAME')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logging.basicConfig(level=logging.DEBUG)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with common usage info."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(f'Hello! Tag me in any chat to check if user have a'
              f' certain anime in their shikimori.one list.\n\n'
              f'*Usage:*\n'
              f'``` @{BOT_USERNAME} Nickname::Anime title```'
              f'While typing the title select one from list.'
              f' On a side note: Nickname must be written'
              f' exactly as it is in user profile url.'),
        disable_web_page_preview=True,
        parse_mode='Markdown'
    )


async def inline_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline command to check if user have certain anime in their list."""
    query = update.inline_query.query
    if '::' not in query:
        return
    nickname, title = query.split('::', 1)
    nickname = nickname.strip()
    title = title.strip()
    if not title:
        return
    try:
        user = get_user(nickname)
        search_results = search_animes(title)
    except NotFoundError as e:
        logging.info(f'{e}, {query=}')
        return
    except (UnauthorizedError, ForbiddenError, TooManyRequestsError) as e:
        logging.error(f'{e}, {query=}')
        return
    results = [
        InlineQueryResultArticle(
            id=anime['id'],
            title=anime['name'],
            input_message_content=InputTextMessageContent(
                check_anime_entry_in_user_list(user, anime),
                disable_web_page_preview=True,
                parse_mode='Markdown'
            )
        )
        for anime in search_results
    ]
    await context.bot.answer_inline_query(update.inline_query.id, results)


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    inline_check_handler = InlineQueryHandler(inline_check)

    application.add_handler(start_handler)
    application.add_handler(inline_check_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
