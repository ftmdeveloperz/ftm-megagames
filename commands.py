from telegram import Update
from telegram.ext import CallbackContext
from ftm import PLANS, premium_users

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
