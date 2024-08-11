import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


class FilmSearcher:
    def search_by_keyword(self, keyword, limit=10):

        return [{"title": "Example Movie", "release_year": "2023", "description": "An example movie description."}]


film_searcher = FilmSearcher()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Поиск по ключевому слову", callback_data='keyword')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text('Привет! Я бот для поиска фильмов. Выберите опцию:', reply_markup=reply_markup)
    else:
        logger.error("Update.message is None")


def get_return_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Назад в главное меню", callback_data='main_menu')],
        [InlineKeyboardButton("Назад", callback_data='back')]
    ])


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = context.user_data.get('action')

    if query.data == 'main_menu':
        await start(update, context)
    elif query.data == 'back':
        if action == 'keyword':
            await query.edit_message_text(text="Введите ключевое слово:", reply_markup=get_return_keyboard())
        else:
            await query.edit_message_text(text="Не удалось вернуться к предыдущему шагу.",
                                          reply_markup=get_return_keyboard())
    else:
        if query.data == 'keyword':
            await query.edit_message_text(text="Введите ключевое слово:", reply_markup=get_return_keyboard())
            context.user_data['action'] = 'keyword'
        else:
            await query.edit_message_text(text="Неизвестное действие.", reply_markup=get_return_keyboard())


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    action = context.user_data.get('action')

    if action == 'keyword':
        keyword = update.message.text
        results = film_searcher.search_by_keyword(keyword, limit=10)
        response = "\n\n".join(
            [f"Название: {res['title']}\nГод: {res['release_year']}\nОписание: {res['description']}" for res in
             results])
        await update.message.reply_text(response if response else "Ничего не найдено.",
                                        reply_markup=get_return_keyboard())
    else:
        await update.message.reply_text("Неизвестное действие. Пожалуйста, начните сначала.",
                                        reply_markup=get_return_keyboard())

    context.user_data['action'] = None


if __name__ == '__main__':
    app = ApplicationBuilder().token('').build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    app.run_polling()
