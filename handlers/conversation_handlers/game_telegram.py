from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler
from handlers.base_handler import BaseHandler
STARTGAME, ISLAND, WAY, LIFE, DANGER, HELP, HOME = range(7)
class SecondConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('startgame', cls.startgame)],
        states={

            STARTGAME: [MessageHandler(filters.Regex('^(Готланд|Манілайд)$'), cls.startgame)],
            ISLAND: [MessageHandler(filters.Regex('^(Готланд|Манілайд)$'), cls.island)],
            WAY: [MessageHandler(filters.Regex('^(Право|Ліво)$'), cls.way)],
            LIFE: [MessageHandler(filters.Regex('^(1|2)$'), cls.life)],
            DANGER: [MessageHandler(filters.Regex('^(1|2)$'), cls.danger)],
            HELP:[MessageHandler(filters.Regex('^(Ні|Так)$'), cls.Help)],
            HOME:[MessageHandler(filters.Regex('^(Ні|Так)$'), cls.home)]
,
        },
        fallbacks=[CommandHandler('exit', cls.exit)]
    )

        app.add_handler(conversation_handler)


    @staticmethod
    async def startgame(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Готланд'), KeyboardButton('Манілайд')],
            [KeyboardButton('/exit'), KeyboardButton('/startgame')]
        ]

        reply_text = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True)
        await update.message.reply_text(
            f'Привіт {update.effective_user.first_name}! На який острів ви хочете потрапити?',
            reply_markup=reply_text)

        return ISLAND

    @staticmethod
    async def island(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Манілайд":
            await update.message.reply_text(f"Ви обрали цей острів. Він виявився весь отруїний. Ви програли, гру закінчено")
            return ConversationHandler.END

        if answer == "Готланд":
            keyboard = [
                [KeyboardButton('Право'), KeyboardButton('Ліво')],

            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(f"Ви обрали цей острів. З першого погляду він виявився безпечним. Ви бачите дві стежки куди підете?", reply_markup=reply_text)
            return WAY





    @staticmethod
    async def way(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Право":
            await update.message.reply_text(f"Ви обрали праву стежку, ви портрапили на диких звірів. Ви програли, гру закінчено")
            return ConversationHandler.END
        elif answer == "Ліво":
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(f"Ви обрали цю стежку. Там було багато різноманітних і смачних фруктів.ви пообідали і ви побачили перед собою ще 2 шляхи. Куди підете?", reply_markup=reply_text)
            return LIFE

    @staticmethod
    async def life(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "1":
            await update.message.reply_text(f"Ви обрали 1 і ви загинули тому що на вас напали крокодили")
            return ConversationHandler.END
        elif answer == "2":
            keyboard = [
                [KeyboardButton('1'), KeyboardButton('2')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(f"Ви вибрали шлях 2 і перед вами з'явилися дві прірву. Яку виберете",reply_markup=reply_text,)
            return DANGER

    @staticmethod
    async def danger(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "1":
            await update.message.reply_text(f"Якщо ви обралу прірву 1 ви загинули, тому що вона виявилася занадто високою і ви її не дали раду перестрибнути, під нею було болото де жили багато отруйних змій. Ви загинули")
            return ConversationHandler.END
        elif answer == "2":
            keyboard = [
                [KeyboardButton('Так'), KeyboardButton('Ні')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

            await update.message.reply_text(f"Якщо ви вибрали прірву 2 то вона була невелика ви її перестрибнули тому що вона була невелика. Ви побачили гору підете на неї?",reply_markup=reply_text)
        return HELP


    @staticmethod
    async def Help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Ні":
            await update.message.reply_text(
                f"Це була помилка. Ви не пішли на гору і потрапили в сипучий пісок. Ви загинули")
            return ConversationHandler.END

        elif answer == "Так":
            keyboard = [
                [KeyboardButton('Так'), KeyboardButton('Ні')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            await update.message.reply_text(f"Ви побачили що летить літак, ви подали сигнал допомоги, Пілот вас побачив і вас врятували. Коли ви летіли додому ви побачили в океані людину на іншому острові. Підберете?",)
            return HOME

    @staticmethod
    async def home(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == "Так":
            await update.message.reply_text(
                f"Ця людина виявилася маньяком він вас убив. Ви загинули")
            return ConversationHandler.END
        elif answer == "Ні":
            await update.message.reply_text(f"Ви спокійно і нормально долетіли додому Вітаю! ВИ ПЕРЕМОГЛИ!!!  ", )
            return ConversationHandler.END

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END