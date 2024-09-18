from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackContext
from ftm import TOKEN, OWNER_ID, ADMIN_IDS, LOG_CHANNEL, premium_users, PLANS
import logging
import os
from commands import my_plan, available_plans, about, get_id, youtube

# Logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global variables
subscribed_users = set()

# Start command handler
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    subscribed_users.add(user_id)
    
    # Log user access to log channel
    await context.bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"User {user.username} with ID {user_id} started the bot."
    )
    
    # Reply to the user
    await update.message.reply_text(
        f"Hello {user.username}, welcome to the bot! Type /help for commands."
    )

# Admin only - Broadcast messages
async def broadcast(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id == OWNER_ID or user.id in ADMINS:
        message = " ".join(context.args)
        if message:
            for user_id in subscribed_users:
                try:
                    await context.bot.send_message(chat_id=user_id, text=message)
                except Exception as e:
                    logger.error(f"Failed to send message to {user_id}: {str(e)}")
            await update.message.reply_text("Message broadcasted to all users.")
        else:
            await update.message.reply_text("Please provide a message to broadcast.")
    else:
        await update.message.reply_text("You are not authorized to use this command.")

# Admin only - Add premium users
async def add_premium(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id == OWNER_ID:
        try:
            premium_id = int(context.args[0])
            plan = context.args[1] if len(context.args) > 1 else 'basic'
            if plan in PLANS:
                premium_users[premium_id] = plan
                await update.message.reply_text(f"User {premium_id} added to the {plan.capitalize()} plan.")
            else:
                await update.message.reply_text("Invalid plan. Available plans are: free, basic, premium.")
        except (IndexError, ValueError):
            await update.message.reply_text("Please provide a valid Telegram ID and plan.")
    else:
        await update.message.reply_text("Only the owner can add premium users.")

# Admin only - Remove premium users
async def remove_premium(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id == OWNER_ID:
        try:
            premium_id = int(context.args[0])
            premium_users.pop(premium_id, None)
            await update.message.reply_text(f"User {premium_id} removed from premium users.")
        except (IndexError, ValueError):
            await update.message.reply_text("Please provide a valid Telegram ID.")
    else:
        await update.message.reply_text("Only the owner can remove premium users.")

# Check premium status
async def premium_status(update: Update, context: CallbackContext):
    user = update.effective_user
    if user.id in premium_users:
        await update.message.reply_text("You are a premium user!")
    else:
        await update.message.reply_text(f"You are not a premium user. To subscribe, send payment to UPI ID: {UPI_ID}")

# Check subscription plans
async def my_plan(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id
    plan = premium_users.get(user_id, 'free')
    plan_description = PLANS.get(plan, 'Free Plan: Basic access to bot features.')
    await update.message.reply_text(f"Your current plan: {plan_description}")

# Display available plans
async def available_plans(update: Update, context: CallbackContext):
    plans_text = "Available Plans:\n\n"
    for plan, description in PLANS.items():
        plans_text += f"{plan.capitalize()}: {description}\n"
    await update.message.reply_text(plans_text)

# About command
async def about(update: Update, context: CallbackContext):
    about_text = """
    **About this Bot:**
    - **Name:** MegaBot
    - **Version:** 1.0
    - **Features:** Tic Tac Toe, Tetris, Rock Paper Scissors, YouTube Video Downloader, Subscription Management, and more.
    - **Developer:** Shivam Kumar
    - **Initiative of:** FUN TOONS MULTIMEDIA Pvt. Ltd.
    - **Contact:** Join us on Telegram [here](https://t.me/ftmbotzsupport) or email at funtoonsmultimedia@gmail.com
    """
    await update.message.reply_text(about_text, parse_mode='Markdown')

# Get user ID
async def get_id(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    await update.message.reply_text(f"Your Telegram ID is: {user_id}")

# YouTube video downloader
async def youtube(update: Update, context: CallbackContext):
    url = " ".join(context.args)
    if url:
        # Implement YouTube video download logic here
        await update.message.reply_text(f"Downloading video from URL: {url}")
    else:
        await update.message.reply_text("Please provide a YouTube URL.")

# Tic Tac Toe game command
async def tic_tac_toe(update: Update, context: CallbackContext):
    # Implement Tic Tac Toe game logic here
    await update.message.reply_text("Tic Tac Toe game started!")

# Tetris game command
async def tetris(update: Update, context: CallbackContext):
    # Implement Tetris game logic here
    await update.message.reply_text("Tetris game started!")

# Rock Paper Scissors game command
async def rock_paper_scissors(update: Update, context: CallbackContext):
    # Implement Rock Paper Scissors game logic here
    await update.message.reply_text("Rock Paper Scissors game started!")

# Main function
async def main():
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ftmcast", broadcast))
    application.add_handler(CommandHandler("add_premium", add_premium))
    application.add_handler(CommandHandler("remove_premium", remove_premium))
    application.add_handler(CommandHandler("premium_status", premium_status))
    application.add_handler(CommandHandler("myplan", my_plan))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("id", get_id))
    application.add_handler(CommandHandler("youtube", youtube))
    application.add_handler(CommandHandler("plans", available_plans))
    application.add_handler(CommandHandler("tic_tac_toe", tic_tac_toe))
    application.add_handler(CommandHandler("tetris", tetris))
    application.add_handler(CommandHandler("rock_paper_scissors", rock_paper_scissors))

    # Start the bot
    await application.start_polling()
    await application.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
