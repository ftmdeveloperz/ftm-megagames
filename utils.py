from telegram import Update
from telegram.ext import CallbackContext
from ftm import LOG_CHANNEL,

# Function to log user activity in the log channel
async def log_user_activity(update: Update, context: CallbackContext):
    user = update.effective_user
    message = f"User {user.username} ({user.id}) accessed the bot."
    await bot.send_message(chat_id=LOG_CHANNEL, text=message)
