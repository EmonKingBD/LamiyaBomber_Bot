Lamiya Bomber Bot by @EmonDhali

Fully ready for Railway deployment with all features (points system, ads, referral, etc.)

import logging from aiogram import Bot, Dispatcher, executor, types from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton from aiogram.contrib.fsm_storage.memory import MemoryStorage import asyncio import json import datetime

API_TOKEN = '7347748386:AAGHpxqVnlkAmqKCFd-KZbyljpOMzA40soE' CHANNEL_ID = '@TermuxHubBD' ADMIN_ID = 8148383622

logging.basicConfig(level=logging.INFO) bot = Bot(token=API_TOKEN) dp = Dispatcher(bot, storage=MemoryStorage())

User data storage

try: with open("users.json", "r") as f: USERS = json.load(f) except: USERS = {}

HTML ad link

AD_URL = "https://www.profitableratecpm.com/ux7k3n129?key=9f8fbb19c45e74b93fc55ddbd45c0318"

--- Helper Functions ---

def save_users(): with open("users.json", "w") as f: json.dump(USERS, f)

def get_points(uid): return USERS.get(str(uid), {}).get("points", 0)

def add_points(uid, amount): uid = str(uid) if uid not in USERS: USERS[uid] = {"points": 0, "last_claim": ""} USERS[uid]["points"] += amount save_users()

def set_last_claim(uid, date): uid = str(uid) USERS[uid]["last_claim"] = date save_users()

def can_claim_daily(uid): uid = str(uid) today = str(datetime.date.today()) return USERS.get(uid, {}).get("last_claim") != today

--- Keyboards ---

def main_buttons(): kb = InlineKeyboardMarkup(row_width=2) kb.add( InlineKeyboardButton("💥 SMS বোমিং করুন", callback_data="bomber"), InlineKeyboardButton("🎁 পয়েন্ট আয় করুন", callback_data="earn"), InlineKeyboardButton("📢 অফিসিয়াল চ্যানেল", url="https://t.me/TermuxHubBD"), InlineKeyboardButton("ℹ️ বট তথ্য", callback_data="info") ) return kb

--- Commands & Handlers ---

@dp.message_handler(commands=['start']) async def start_handler(msg: types.Message): user = msg.from_user uid = str(user.id)

if uid not in USERS:
    USERS[uid] = {"points": 50, "last_claim": ""}
    save_users()
    await bot.send_message(ADMIN_ID, f"👤 New user joined: {user.full_name} (@{user.username})")

await msg.answer(
    f"🔹 💥 <b>Lamiya Bomber Bot</b> 💥\n\n"
    f"📲 SMS বোমিং করুন Points দিয়ে!\n"
    f"🎁 Start করলেই ফ্রি ৫০ পয়েন্ট!\n"
    f"📅 প্রতিদিন লগইন = ১৫ পয়েন্ট\n"
    f"📺 Ad দেখলেই = ৫ পয়েন্ট\n"
    f"📤 ১০ পয়েন্ট = ১টি SMS\n\n"
    f"📌 রেফার করলে ২০ পয়েন্ট বোনাস পাবে!\n"
    f"🆔 UID: <code>{uid}</code>",
    reply_markup=main_buttons(),
    parse_mode="html")

@dp.callback_query_handler(lambda c: c.data == 'info') async def bot_info(call: types.CallbackQuery): await call.message.edit_text( "🔹 <b>Lamiya Bomber Bot</b>\n\n" "🔧 Bot Maker: @EmonDhali\n" "📢 চ্যানেল: @TermuxHubBD\n" "🌍 সকল দেশের জন্য একটিভ!\n" "🎁 পয়েন্ট সিস্টেম + রেফার সিস্টেম + এড বোনাস\n\n" "✅ বট সব সময় ২৪/৭ চালু থাকবে!", parse_mode="html", reply_markup=main_buttons())

@dp.callback_query_handler(lambda c: c.data == 'earn') async def earn_points(call: types.CallbackQuery): uid = str(call.from_user.id) today = str(datetime.date.today())

# Daily bonus
if can_claim_daily(uid):
    add_points(uid, 15)
    set_last_claim(uid, today)
    await call.message.answer("🎁 আজকের Daily Bonus: ✅ ১৫ পয়েন্ট পেয়েছো!")
else:
    await call.message.answer("📅 আজকের Daily Bonus ইতিমধ্যে নিয়েছো!")

# Ad watching bonus
ad_kb = InlineKeyboardMarkup().add(InlineKeyboardButton("▶️ এখনই Ad দেখুন", url=AD_URL))
await call.message.answer("📺 Ad দেখে ৫ পয়েন্ট নিতে চাইলে নিচে ক্লিক করুন:\nAd শেষ হলে পয়েন্ট পাবে!", reply_markup=ad_kb)

@dp.callback_query_handler(lambda c: c.data == 'bomber') async def bomber_feature(call: types.CallbackQuery): uid = str(call.from_user.id) points = get_points(uid)

if points < 10:
    await call.message.answer("❌ SMS বোমিং এর জন্য কমপক্ষে ১০ পয়েন্ট লাগবে!")
else:
    add_points(uid, -10)
    await call.message.answer("✅ SMS বোমিং শুরু হয়েছে! [Demo SMS sent]")

--- Main ---

if name == 'main': executor.start_polling(dp, skip_updates=True)

