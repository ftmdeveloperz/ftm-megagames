from telegram import Update
from telegram.ext import CallbackContext
from ftm import OWNER_ID, PREMIUM_USERS

# Function to verify if the user is the owner
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

# Function to check if a user is a premium user
def is_premium(user_id: int):
    return user_id in PREMIUM_USERS

# Command to check premium status
async def check_premium(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if is_premium(user_id):
        await update.message.reply_text("You are a premium user!")
    else:
        await update.message.reply_text("You are not a premium user. Send your payment receipt to @ftmdeveloper.")

# Command to add a premium user (Owner only)
async def add_premium(update: Update, context: CallbackContext):
    if is_owner(update):
        try:
            user_id = int(context.args[0])
            PREMIUM_USERS.append(user_id)
            await update.message.reply_text(f"User {user_id} added as premium user.")
        except Exception:
            await update.message.reply_text("Failed to add premium user. Provide a valid Telegram ID.")
    else:
        await update.message.reply_text("Only the owner can add premium users.")

# Command to remove a premium user (Owner only)
async def remove_premium(update: Update, context: CallbackContext):
    if is_owner(update):
        try:
            user_id = int(context.args[0])
            PREMIUM_USERS.remove(user_id)
            await update.message.reply_text(f"User {user_id} removed from premium users.")
        except Exception:
            await update.message.reply_text("Failed to remove premium user. Provide a valid Telegram ID.")
    else:
        await update.message.reply_text("Only the owner can remove premium users.")
