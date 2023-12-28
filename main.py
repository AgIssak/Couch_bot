import telebot
from telebot import types
import sqlite3
import os
import random
import time
import schedule


bot = telebot.TeleBot("6487829037:AAEjsPmRFt-h4bhkkP5JbxIzF1QJ99S0aqY")
bench = ""
upper_bench = ""
cross = ""
butterfly = ""
muscle_group = ("Грудак, Спина, Ноги, Руки")

def reminder(message):
    bot.send_message(message.chat.id, "Приветик качказавр!Хотел напомнить тебе, что у тебя сегодня тренька:3)")
schedule.every().monday.at("00:07").do(reminder)
# while True:
#     schedule.run_pending()
#     time.sleep(1)

@bot.message_handler(commands = ["start"])
def main(message):
    bot.send_message(message.from_user.id, f"Привет, {message.from_user.first_name}")
    video = open("mem/welcome.mp4", "rb")
    bot.send_video(message.chat.id, video, timeout=120)
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Gym songs", url='https://t.me/gym_song_by_coach')
    button2 = types.InlineKeyboardButton("Посчитать норму калорий в день", callback_data="calories")
    button4 = types.InlineKeyboardButton("Поднять мотивацию!", callback_data="motivation")
    button5 = types.InlineKeyboardButton("Мой результаты!", callback_data="get_pr")
    button6 = types.InlineKeyboardButton("Написать о результатах", callback_data="set_pr")
    markup.add(button1)
    markup.add(button2)
    markup.add(button5,button6)
    markup.add(button4)
    bot.send_message(message.chat.id, "Йо, что хочешь сделать?".format(message.from_user), reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == "set_pr":
        bot.send_message(callback.message.chat.id,f"Результаты какой группы мышц ты хочешь записать Buddyboy? {muscle_group}\n")
    elif callback.data == "get_pr":
        conn = sqlite3.connect("pr_sql.db")
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM chest")
        chest = cur.fetchall()

        info = ""
        for i in chest:
            info += f"День №{i[0]}, Жим лежа: {i[1]} , Верхний жим: {i[2]} , Кросс: {i[3]} , Бабочка: {i[4]}\n"

        cur.close()
        conn.close()

        bot.send_message(callback.message.chat.id, "Щяяяс, дайкс чекну записи!")
        bot.send_message(callback.message.chat.id, info)
        bot.send_message(callback.message.chat.id, "Напиши /start и чекни другие функции, я не только такое умею😏")
    elif callback.data == "motivation":
        bot.send_message(callback.message.chat.id, "Маааатииивааациию наадааа подняяяяять)")
        photo = open("mem/m.png", "rb")
        bot.send_photo(callback.message.chat.id, photo)
        bot.send_message(callback.message.chat.id, "Подожди минутку найду видос под твою безмотивационную рожу")
        video = open("motivation/"+random.choice(os.listdir("motivation")), "rb")
        bot.send_video(callback.message.chat.id, video, timeout=120)
    elif callback.data =="calories":
        bot.send_message(callback.message.chat.id,"Масл монстр напомни свой пол?(их два кстати не надо мне тут чудить(P.S. Пиши: Мужчина или Женщина))")

@bot.message_handler(content_types=["text"])
def calories(message):
    if message.text == "Мужчина":
        bot.send_message(message.chat.id, "Сколько ты там весишь?")
        bot.register_next_step_handler(message, men_process_weight)
    elif message.text == "Женщина":
        bot.send_message(message.chat.id, "Сколько ты там весишь?")
        bot.register_next_step_handler(message, women_process_weight)

    elif message.text == "Грудак":
        conn = sqlite3.connect("pr_sql.db")
        cur = conn.cursor()
        cur.execute(f"CREATE TABLE IF NOT EXISTS chest(days int auto_increment, bench int(4), upper int(4), cross int(4), butterfly int(4))")
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, "Грудные значит щя запишем")
        bot.send_message(message.chat.id, "Скок жмешь в жиме? Хоть 100-ка есть?")
        bot.register_next_step_handler(message, process_bench)
    elif message.text == "Спина":
        bot.send_message(message.chat.id, "Сорри пока что она на разработке")
        sticker = open("mem/nan.webp","rb")
        bot.send_sticker(message.chat.id, sticker)
    elif message.text == "Ноги":
        bot.send_message(message.chat.id, "Сорри пока что она на разработке")
        sticker = open("mem/nan.webp","rb")
        bot.send_sticker(message.chat.id, sticker)
    elif message.text == "Руки":
        bot.send_message(message.chat.id, "Сорри пока что она на разработке")
        sticker = open("mem/nan.webp","rb")
        bot.send_sticker(message.chat.id, sticker)
    else:
        bot.send_message(message.chat.id, "Не понял тебя. Прочитай внимательно инструкцию")
        bot.send_message(message.chat.id, "Если нифига не понял просто жмяни на --> /start")
        sticker = open("mem/ag.webp","rb")
        bot.send_sticker(message.chat.id, sticker)
def men_process_weight(message):
    global men_weight
    men_weight = int(message.text.strip())
    bot.send_message(message.chat.id, "А рост какой?(P.S.Пиши в сантиметрах)")
    bot.register_next_step_handler(message, men_process_height)
def men_process_height(message):
    global men_height
    men_height = int(message.text.strip())
    bot.send_message(message.chat.id, "Подожди а скок те лет?")
    bot.register_next_step_handler(message, men_process_age)
def men_process_age(message):
    global men_age
    men_age = int(message.text.strip())
    bot.send_message(message.chat.id, "Я бы дал меньше😏. Все последний вопрос, твой уровень физической активности в течение недели?")
    bot.register_next_step_handler(message, men_process_exercise)
def men_process_exercise(message):
    info = 0
    exercise = int(message.text.strip())
    if exercise == "0":
        men_factor = 1.2
    elif exercise == "1" or "2" or "3":
        men_factor = 1.375
    elif exercise == "4" or "5":
        men_factor = 1.55
    elif exercise == "6" or "7":
        men_factor = 1.725
    else:
        men_factor = 1.9
    info = (88.362 + (13.397 * men_weight) + (4.799 * men_height) - (5.677 * men_age)) * men_factor
    bot.send_message(message.chat.id, f"{info} ккал/день надо употреблять для сохранение веса и нормального состояния")
    bot.send_message(message.chat.id, "Напиши /start и чекни другие функции, я не только такое умею😏")

def women_process_weight(message):
    global women_weight
    women_weight = int(message.text.strip())
    bot.send_message(message.chat.id, "А рост какой?(P.S.Пиши в сантиметрах)")
    bot.register_next_step_handler(message, women_process_height)
def women_process_height(message):
    global women_height
    women_height = int(message.text.strip())
    bot.send_message(message.chat.id, "Подожди а скок те лет?")
    bot.register_next_step_handler(message, women_process_age)
def women_process_age(message):
    global women_age
    women_age = int(message.text.strip())
    bot.send_message(message.chat.id, "Я бы дал меньше😏. Все последний вопрос, твой уровень физической активности в течение недели?")
    bot.register_next_step_handler(message, women_process_exercise)
def women_process_exercise(message):
    info = 0
    exercise = int(message.text.strip())
    if exercise == "0":
        women_factor = 1.2
    elif exercise == "1" or "2" or "3":
        women_factor = 1.375
    elif exercise == "4" or "5":
        women_factor = 1.55
    elif exercise == "6" or "7":
        women_factor = 1.725
    else:
        women_factor = 1.9
    info = (447.593 + (9.247 * women_weight) + (3.098 * women_height) - (4.33 * women_age)) * women_factor
    # посмотреть можно ли впихнуть int(info)
    bot.send_message(message.chat.id, f"{info} ккал/день надо употреблять для сохранение веса и нормального состояния")
    bot.send_message(message.chat.id, "Напиши /start и чекни другие функции, я не только такое умею😏")



        

# @bot.message_handler(content_types=["text"])
# def chest(message):
    #  if message.text == "Грудак":
    #     conn = sqlite3.connect("pr_sql.db")
    #     cur = conn.cursor()
    #     cur.execute("CREATE TABLE IF NOT EXISTS chest(days int auto_increment primary key, bench int(4), upper int(4), cross int(4), butterfly int(4))")
    #     conn.commit()
    #     cur.close()
    #     conn.close()
    #     bot.send_message(message.chat.id, "Грудные значит щя запишем")
    #     bot.send_message(message.chat.id, "Скок жмешь в жиме? Хоть 100-ка есть?")
    #     bot.register_next_step_handler(message, bench)
def process_bench(message):
    global bench
    bench = message.text.strip()
    bot.send_message(message.chat.id, "Нормально, но я больше жму:3 Лан на верхний грудь?")
    bot.register_next_step_handler(message, process_upper_bench)

def process_upper_bench(message):
    global upper_bench
    upper_bench = message.text.strip()
    bot.send_message(message.chat.id, "WOW! А как насчет Кросса?")
    bot.register_next_step_handler(message, process_cross)

def process_cross(message):
    global cross
    cross = message.text.strip()
    bot.send_message(message.chat.id, "Надо по работать еще! И наконец скок на бабочке, монстр?")
    bot.register_next_step_handler(message, process_butterfly)

def process_butterfly(message):
    butterfly = message.text.strip()
    conn = sqlite3.connect("pr_sql.db")
    cur = conn.cursor()
    cur.execute(f"INSERT INTO chest(bench, upper, cross, butterfly) VALUES('%s', '%s', '%s', '%s') " %(bench, upper_bench, cross, butterfly))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Прнял все записал.Хорошо постарался жду новых результатов!")
    bot.send_message(message.chat.id, "Напиши /start и чекни другие функции, я не только такое умею😏")


bot.polling(none_stop = True)

def reminder(message):
    bot.send_message(message.from_user.id, "Приветик качказавр!Хотел напомнить тебе, что у тебя сегодня тренька:3)")

schedule.every().monday.at("00:15").do(reminder)

while True:
    schedule.run_pending()
    time.sleep(1)