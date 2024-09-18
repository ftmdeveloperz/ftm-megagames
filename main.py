from telegram.ext import Application, CommandHandler, MessageHandler, filters
from ftm import TOKEN
from admin import add_admin, remove_admin
from premium import check_premium, add_premium, remove_premium
from utils import log_user_activity

# Initialize the bot application
application = Application.builder().token(TOKEN).build()

# Handler setup for admin functions
application.add_handler(CommandHandler("add_admin", add_admin))
application.add_handler(CommandHandler("remove_admin", remove_admin))

# Handler setup for premium functions
application.add_handler(CommandHandler("check_premium", check_premium))
application.add_handler(CommandHandler("add_premium", add_premium))
application.add_handler(CommandHandler("remove_premium", remove_premium))

# Log user activity on any command
application.add_handler(MessageHandler(filters.COMMAND, log_user_activity))

# Run the bot
if __name__ == "__main__":
    application.run_polling()
