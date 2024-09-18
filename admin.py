from telegram import Update
from telegram.ext import CallbackContext
from ftm import OWNER_ID, ADMINS

# Function to verify if the user is the owner
def is_owner(update: Update):
    return update.effective_user.id == OWNER_ID

# Function to check if the user is an admin
def is_admin(update: Update):
    return update.effective_user.id in ADMINS or is_owner(update)

# Command to add an admin (Owner only)
async def add_admin(update: Update, context: CallbackContext):
    if is_owner(update):
        try:
            admin_id = int(context.args[0])
            ADMIN_IDS.append(admin_id)
            await update.message.reply_text(f"Admin added successfully: {admin_id}")
        except Exception:
            await update.message.reply_text("Failed to add admin. Provide a valid Telegram ID.")
    else:
        await update.message.reply_text("Only the owner can add admins.")

# Command to remove an admin (Owner only)
async def remove_admin(update: Update, context: CallbackContext):
    if is_owner(update):
        try:
            admin_id = int(context.args[0])
            ADMIN_IDS.remove(admin_id)
            await update.message.reply_text(f"Admin removed successfully: {admin_id}")
        except Exception:
            await update.message.reply_text("Failed to remove admin. Provide a valid Telegram ID.")
    else:
        await update.message.reply_text("Only the owner can remove admins.")
