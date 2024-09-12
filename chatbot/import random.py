import random
import asyncio 
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = '7316688548:AAEWCvoj3gzUyaLrPyR1BzgEe5rTT55syXc'
BOT_USERNAME: Final = '@chatchatsbot'


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(1)  
    await update.message.reply_text("Hello! I'm your AI assistant. How can I assist you today?")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(1) 
    await update.message.reply_text("You can ask me anything or tell me how I can assist.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await asyncio.sleep(1)
    await update.message.reply_text("Custom command recognized! What else would you like to try?")

RESPONSE_DICT = {
    'hello': ['Hmm, hello there!', 'Hey! How can I assist you today?', 'Greetings! How can I help?'],
    'hi': ['Hi! What’s on your mind?', 'Hello! Ready to assist you.', 'Hi there! Need something?'],
    'how are you': ['I’m functioning at 100%! How about you?', 'I’m here and ready to help. How are you doing?', 'All good here! How can I assist you today?'],
    "what's your name": ["You can call me Chatchats, your virtual assistant.", "I go by Chatchats, how can I help today?"],
    "thank you": ["You're welcome! Always happy to help.", "No problem at all! I'm here if you need me.", "Anytime! 😊"],
    'bye': ['Goodbye! Feel free to return anytime.', 'See you later! Stay safe.', 'Take care! Looking forward to chatting again.'],
    'help me': ['Of course! I’m thinking… What do you need assistance with?', 'I’m analyzing… Tell me more about what you need help with.'],
    'assist me': ['Absolutely! What can I do for you today?', 'Sure! Just tell me what you need, and I’ll help you out.'],
    'what can you do': ["I'm equipped to chat, assist with tasks, answer your questions, and much more. What do you need help with?", "I can do many things! Want to explore some options together?"],
    'sing a song': ["Let me think… hmm, I can hum a tune! 🎶", "I’m not the best singer, but I can give it a try! 🎵"],
    'what’s the weather': ["I can’t directly check the weather, but maybe a weather app would help?", "Hmm, I don’t have weather capabilities, but it’s always a good time to stay positive!"],
    'tell me a joke': ["Let me think… Why don’t scientists trust atoms? Because they make up everything! 😄", "Thinking… Okay, here’s one: Why did the computer go to the doctor? It had a virus! 😆"],
    'how old are you': ["I’m ageless, but I’m always learning new things!", "I was created not long ago, but I feel as wise as ever."],
    'what’s the meaning of life': ["Deep question! Some say it's 42, others say it’s all about the journey.", "Hmm… The meaning of life is something you define for yourself."],
    'life advice': ["Stay curious, be kind, and always keep learning. That’s my advice!", "Let me think… You can control how you respond to things—choose positivity!"],
    "do you believe in aliens": ["It’s a big universe out there… anything’s possible!", "I’m open to the possibility! What do you think?"],
}

async def handle_response(text: str) -> str:
    processed = text.lower().strip()
    
    for key in RESPONSE_DICT:
        if key in processed:
            return random.choice(RESPONSE_DICT[key])
        return "Hmm, I don't have any idea of what are you saying, but I’m always learning. Can you tell me more?"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group' and BOT_USERNAME in text:
        new_text = text.replace(BOT_USERNAME, "").strip()
        response = await handle_response(new_text)
    else:
        response = await handle_response(text)
    
    await asyncio.sleep(random.uniform(0.5, 1.5)) 
    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")
    await context.bot.send_message(chat_id=update.message.chat.id, text="Sorry, something went wrong! Please try again.")

if __name__ == '_main_':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).connect_timeout(20).read_timeout(20).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=1)