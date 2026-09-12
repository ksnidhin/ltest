import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, LOG_CHAT_ID
from ai import generate_response

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Compile regex to detect question words or question marks
# Looks for "how", "why", "what", "where", "when", "who" as standalone words, or a "?" anywhere
QUESTION_PATTERN = re.compile(r'\b(how|why|what|where|when|who|can|could|would)\b|\?', re.IGNORECASE)

def is_question(text: str) -> bool:
    """Checks if the text looks like a question."""
    if not text:
        return False
    return bool(QUESTION_PATTERN.search(text))

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Answers the /start command with a friendly greeting."""
    greeting = "Hello! 👋 I'm your friendly AI assistant. Feel free to ask me anything!"
    await update.message.reply_text(greeting)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Analyzes incoming messages. If it's a question, it generates an AI response.
    """
    text = update.message.text
    
    # Check if the message is a question or directed at the bot
    if is_question(text) or (update.message.chat.type == "private"):
        # In private chats, answer everything. In groups, answer only questions.
        
        # Send typing action
        await update.message.chat.send_action(action="typing")
        
        # Get AI response
        answer = await generate_response(text)
        
        # Reply to the user
        await update.message.reply_text(answer)
        
        # Log the interaction if a log chat is configured
        if LOG_CHAT_ID:
            chat_type = update.message.chat.type
            username = update.message.from_user.username or update.message.from_user.first_name
            log_msg = (
                f"🤖 **AI Replied**\n"
                f"👤 User: {username}\n"
                f"🗣 Chat: {chat_type}\n"
                f"❓ Question: `{text}`\n"
                f"💬 Answer: `{answer}`"
            )
            try:
                await context.bot.send_message(chat_id=LOG_CHAT_ID, text=log_msg)
            except Exception as e:
                logger.error(f"Failed to send to log chat: {e}")

def main():
    """Starts the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))

    # Add message handler (filters out commands)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("AI Bot is running...")
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
