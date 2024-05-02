from handlers.base_handler import BaseHandler
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler


STATE_FIRST_NAME, STATE_LAST_NAME, STATE_PHONE_NUMBER = range(3)


class UserRegisterConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('user_register', cls.user_register)],
            states={
                STATE_FIRST_NAME: [MessageHandler(filters.TEXT, cls.state_first_name)],
                STATE_LAST_NAME: [MessageHandler(filters.TEXT, cls.state_last_name)],
                STATE_PHONE_NUMBER: [
                    MessageHandler(filters.CONTACT, cls.state_phone_number),
                    MessageHandler(filters.TEXT & filters.TEXT & filters.COMMAND, cls.state_phone_number)],
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def user_register(update: Update, context: ContextTypes.DEFAULT_TYPE):

        await update.message.reply_text(f'Hello {update.effective_user.first_name}! Введіть своє імя')
        return STATE_FIRST_NAME

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Exit from conversation')

        return ConversationHandler.END

    @staticmethod
    async def state_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        first_name = update.message.text
        context.user_data["first_name"] = first_name
        await update.message.reply_text(f'Your welcome {first_name}! Зараз введіть своє прізвище')

        return STATE_LAST_NAME


    @staticmethod
    async def state_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
        last_name = update.message.text
        context.user_data["last_name"] = last_name
        contact_keyboard = KeyboardButton(text="send_contact", request_contact=True)
        keyboard = [
            [contact_keyboard],
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Поділіться своїм контактом або введіть вручну", reply_markup=reply_markup)

        return STATE_PHONE_NUMBER


    @staticmethod
    async def state_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.contact:
            phone_number = update.message.contact.phone_number
        else:
            phone_number = update.message.text
        context.user_data["phone_number"] = phone_number

        first_name = context.user_data["first_name"]
        last_name = context.user_data["last_name"]



        await update.message.reply_text(
            f"Ви зареєстровані: "
            f"{context.user_data['first_name']} \n"
            f"{context.user_data['last_name']} \n "
            f"{context.user_data['phone_number']}"
        )


        return ConversationHandler.END