import logging, asyncio, random, re
from telegram import (
    Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, CallbackQueryHandler, filters
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from db import SessionLocal, User, Bet, Lottery, Request, create_db
from config import BOT_TOKEN, ADMIN_IDS, MIN_BET, MAX_BET, CUSTOMER_SERVICE_GROUP_IDS
from chart import draw_history_chart

scheduler = AsyncIOScheduler()
lottery_lock = asyncio.Lock()
session = SessionLocal()
current_period = 1

def get_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("我的")]], resize_keyboard=True)
def get_my_inline_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('充值', callback_data='show_recharge')],
        [InlineKeyboardButton(💸提现', callback_data='show_withdraw')],
        [InlineKeyboardButton('盈亏', callback_data='show_profit')],
        [InlineKeyboardButton('投注历史', callback_data='show_history')]
    ])
def get_recharge_withdraw_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('充值', callback_data='show_recharge'),
         InlineKeyboardButton('提现', callback_data='show_withdraw')]
    ])
def is_admin(user_id): return user_id in ADMIN_IDS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = session.query(User).filter_by(tg_id=user_id).first()
    if not user:
        user = User(tg_id=user_id, name=update.effective_user.full_name)
        session.add(user)
        session.commit()
    if user.banned:
        await update.message.reply_text("你已被封禁，无法使用本机器人。")
        return
    msg = "欢迎来到欢乐骰子机器人！"
    if update.message.chat.type == 'private':
        await update.message.reply_text(msg, reply_markup=get_keyboard())
    else:
        await update.message.reply_text(msg)

async def handle_menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == "private":
        if update.message.text.strip() == "我的":
            await update.message.reply_text("请选择操作：", reply_markup=get_my_inline_keyboard())

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    user = session.query(User).filter_by(tg_id=user_id).first()
    if not user or user.banned:
        await query.answer("你已被封禁，无法使用本机器人。", show_alert=True)
        return
    data = query.data
    if data == 'show_recharge':
        await query.answer()
        await query.edit_message_text("请输入充值金额并发送，人工客服会联系您。")
        for gid in CUSTOMER_SERVICE_GROUP_IDS:
            await context.bot.send_message(
                chat_id=gid,
                text=f"【充值申请】用户:{user.name or user.tg_id}（ID:{user.tg_id}）正在申请充值。请人工跟进。"
            )
    elif data == 'show_withdraw':
        await query.answer()
        await query.edit_message_text("请输入提现金额并发送，人工客服会联系您。")
        for gid in CUSTOMER_SERVICE_GROUP_IDS:
            await context.bot.send_message(
                chat_id=gid,
                text=f"【提现申请】用户:{user.name or user.tg_id}（ID:{user.tg_id}）正在申请提现。请人工跟进。"
            )
    elif data == 'show_profit':
        await query.answer()
        await query.edit_message_text(f"您的盈亏情况：{user.profit} 元")
    elif data == 'show_history':
        await query.answer()
        bets = session.query(Bet).filter_by(user_id=user.id).order_by(Bet.id.desc()).limit(10).all()
        if not bets:
            await query.edit_message_text("暂无投注历史")
        else:
            lines = [f"期{b.period} {b.bet_type} {b.amount} 状态:{b.status}" for b in bets]
            await query.edit_message_text("您的投注历史：\n" + "\n".join(lines))

if __name__ == "__main__":
    create_db()
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_menu_button))
    app.add_handler(CallbackQueryHandler(callback_query_handler))
    scheduler.start()
    app.run_polling()
