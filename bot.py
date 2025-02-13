from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# Твой API-токен
TOKEN = "8083534238:AAFWBxn8kRXRd_Dc9HCFyDMsNZMKSEP-dH8"

# ID закрытого канала (замени на свой)
CHANNEL_ID = "-1002323991792"

# Этапы диалога
ROLE_SELECTION, SECOND_QUESTION = range(2)

# Главное меню выбора роли
role_keyboard = [
    ["💅 Я мастер – работаю в салоне или на себя."],
    ["✨ Делаю маникюр себе – хочу ухаживать за ногтями дома."],
    ["👀 Просто интересуюсь – хочу узнать больше про пилочный маникюр."],
    ["📚 Я мастер и хочу повышать квалификацию – ищу обучение и полезные советы."]
]
markup_role = ReplyKeyboardMarkup(role_keyboard, one_time_keyboard=True, resize_keyboard=True)

# Варианты опыта работы для мастеров
experience_keyboard = [
    ["🆕 Только начинаю (до 1 года)."],
    ["✂️ 1-3 года."],
    ["🎨 3-5 лет."],
    ["🏆 Более 5 лет."]
]
markup_experience = ReplyKeyboardMarkup(experience_keyboard, one_time_keyboard=True, resize_keyboard=True)

# Варианты частоты маникюра для пользователей
personal_care_keyboard = [
    ["💅 Редко, раз в несколько месяцев."],
    ["🖌️ Регулярно, но без особых техник."],
    ["🎨 Освоила пилочный маникюр и делаю его себе."],
    ["💎 Люблю сложные техники и эксперименты."]
]
markup_personal_care = ReplyKeyboardMarkup(personal_care_keyboard, one_time_keyboard=True, resize_keyboard=True)

# Варианты интересов для новичков
curious_keyboard = [
    ["📖 Хочу понять, что такое пилочный маникюр."],
    ["👀 Люблю смотреть видео про маникюр."],
    ["🛠 Интересно, как делают мастера."],
    ["❓ Пока просто читаю, без цели."]
]
markup_curious = ReplyKeyboardMarkup(curious_keyboard, one_time_keyboard=True, resize_keyboard=True)

# Обработчик команды /start
async def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    await update.message.reply_text(
        f"📌 Привет, {user.first_name}! Чтобы вступить в закрытый канал **Pilim Shura**, ответь на пару вопросов.",
        reply_markup=markup_role
    )
    return ROLE_SELECTION

# Обработка выбора роли и переход ко второму вопросу
async def role_selection(update: Update, context: CallbackContext) -> int:
    user_response = update.message.text
    context.user_data["role"] = user_response

    if "Я мастер" in user_response or "Я мастер и хочу повышать квалификацию" in user_response:
        await update.message.reply_text("✅ Какой у тебя опыт работы?", reply_markup=markup_experience)
    elif "Делаю маникюр себе" in user_response:
        await update.message.reply_text("✅ Как часто ты делаешь маникюр?", reply_markup=markup_personal_care)
    elif "Просто интересуюсь" in user_response:
        await update.message.reply_text("✅ Что тебе больше всего интересно?", reply_markup=markup_curious)
    
    return SECOND_QUESTION

# Финальный ответ, сохранение данных в файл и отправка ссылки
async def second_question(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_id = user.id
    username = user.username or "Без имени"
    first_name = user.first_name or "Без имени"
    role = context.user_data.get("role", "Не указан")
    second_answer = update.message.text

    # Логируем в консоли (чтобы видеть в терминале)
    print(f"Пользователь: {first_name} (@{username}) | ID: {user_id}")
    print(f"Роль: {role}")
    print(f"Доп. ответ: {second_answer}")
    print("-" * 30)

    # Сохраняем данные в файл
    with open("users_data.txt", "a", encoding="utf-8") as file:
        file.write(f"Пользователь: {first_name} (@{username}) | ID: {user_id}\n")
        file.write(f"Роль: {role}\n")
        file.write(f"Доп. ответ: {second_answer}\n")
        file.write("-" * 30 + "\n")

    await update.message.reply_text("✅ Спасибо за ответы! Теперь бот перенаправит вас в канал.")
    await update.message.reply_text(f"🔗 [Вступить в канал](t.me/PilimShura)", parse_mode="Markdown")

    return ConversationHandler.END

# Функция запуска бота
def main():
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ROLE_SELECTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, role_selection)],
            SECOND_QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_question)]
        },
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()