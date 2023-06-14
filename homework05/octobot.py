import json
import re
from datetime import datetime

import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore

bot = telebot.TeleBot("6070998338:AAFMfoDSqHvR1Eh2MVHOHA92SD7IuGMOeA4")


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    if divider != date[2]:
        return False
    try:
        if len(date) == 10:
            converted_date = datetime.strptime("/".join(date.split(divider)), "%d/%m/%Y")
        else:
            converted_date = datetime.strptime("/".join(date.split(divider)), "%d/%m/%y")
    except ValueError:
        return False
    if -1 <= (converted_date - datetime.today()).days < 365 and converted_date.date() >= datetime.today().date():
        return True
    return False


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    if "https://" not in url and "http://" not in url:
        url = "https://" + url
    try:
        if requests.get(url).status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    return datetime.strptime(date, "%d/%m/%y")


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    if is_valid_url(url):
        pattern = r"^https?://docs\.google\.com/spreadsheets/d/([a-zA-Z0-9-_]+)"
        match = re.match(pattern, url)
        if match:
            sheet_id = url.split("/")[url.split("/").index("d") + 1]  # sheet_id
            try:
                with open("tables.json") as json_file:
                    tables = json.load(json_file)
                title = len(tables) + 1
                tables[title] = {"url": url, "id": sheet_id}
            except FileNotFoundError:
                tables = {0: {"url": url, "id": sheet_id}}
            with open("tables.json", "w") as json_file:
                json.dump(tables, json_file)
            bot.send_message(message.chat.id, "Таблица подключена!")
            start(message)
        else:
            bot.send_message(message.chat.id, "Url должна указывать на Google-таблицу")
            start(message)
    else:
        bot.send_message(message.chat.id, "Некорректный url таблицы")
        start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    with open("tables.json") as json_file:
        tables = json.load(json_file)
    sheet_id = tables[max(tables)]["id"]
    gc = gspread.service_account(filename="credentials.json")
    sh = gc.open_by_key(sheet_id)
    worksheet = sh.sheet1
    # Преобразуем Google-таблицу в таблицу pandas
    df = pd.DataFrame(worksheet.get_all_records())
    return worksheet, tables[max(tables)]["url"], df


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        info = bot.send_message(message.chat.id, "Ссылка на Google-таблицу:")
        bot.register_next_step_handler(info, connect_table)

    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить предмет")
        start_markup.row("Изменить название и url предмета")
        start_markup.row("Удалить предмет")
        start_markup.row("Очистить таблицу")
        start_markup.row("Главное меню")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)

    elif message.text == "Редактировать дедлайны":
        deadline_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadline_markup.row("Добавить новый дедлайн")
        deadline_markup.row("Изменить дедлайн")
        deadline_markup.row("Удалить дедлайн")
        deadline_markup.row("Главное меню")
        info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=deadline_markup)
        bot.register_next_step_handler(info, choose_deadline_action)

    elif message.text == "Посмотреть дедлайны на этой неделе":
        show_deadlines(message)

    else:
        bot.send_message(message.chat.id, "Я Вас не понимаю...")
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    if message.text == "Удалить предмет":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        df = access_current_sheet()[2]

        try:
            for subject in df["Subject"]:
                start_markup.row(subject)
            start_markup.row("Главное меню")
            info = bot.send_message(message.chat.id, "Название предмета:", reply_markup=start_markup)
            bot.register_next_step_handler(info, delete_subject)

        except KeyError:
            bot.send_message(message.chat.id, "Таблица уже пуста!", reply_markup=start_markup)
            start(message)

    elif message.text == "Изменить название и url предмета":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        df = access_current_sheet()[2]

        try:
            for subject in df["Subject"]:
                start_markup.row(subject)
            start_markup.row("Главное меню")

            info = bot.send_message(message.chat.id, "Выберите предмет для изменения:", reply_markup=start_markup)
            bot.register_next_step_handler(info, update_subject)

        except KeyError:
            bot.send_message(message.chat.id, "Таблица пуста!", reply_markup=start_markup)
            start(message)

    elif message.text == "Добавить предмет":
        info = bot.send_message(message.chat.id, "Название нового предмета:")
        bot.register_next_step_handler(info, add_new_subject)

    elif message.text == "Очистить таблицу":
        choose_removal_option(message)

    elif message.text == "Главное меню":
        start(message)

    else:
        bot.send_message(message.chat.id, "Я Вас не понимаю...")
        start(message)


def show_deadlines(message):
    worksheet, _, df = access_current_sheet()
    post = []
    for index in range(df.shape[0]):
        header = f"#{index} Предмет: {df['Subject'][index]}\nСсылка: {df['Link'][index] if df['Link'][index] else '<none>'}\nДедлайны:"
        text_ = ""
        for i in range(1, df.loc[:, "1":"5"].shape[1] + 1):
            section = df.loc[:, "1":"5"][str(i)][index]
            if section:
                date = convert_date("/".join(section.split(section[2])))
                today = datetime.today()

                if (date - today).days <= 7 and date > today:
                    text_ += f"          {i} задание >> {section}           На этой неделе! \n"
                elif (date - today).days < 1:
                    text_ += f"          {i} задание >> {section}           !СЕГОДНЯ! \n"
                else:
                    text_ += f"          {i} задание >> {section}           Время еще есть! До дедлайна {(date - today).days} дн.\n"

        text = f"{header}\n{text_}" if text_ else header + " Дедлайнов нет! Можно жить спокойно..."
        post.append(text)
    if df.shape[0] == 0:
        bot.send_message(message.chat.id, "Таблица данных пуста!")
    else:
        bot.send_message(message.chat.id, "\n\n".join(post))
    start(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    if message.text == "Главное меню":
        return start(message)
    df = access_current_sheet()[2]
    if df.shape[0] == 0:
        bot.send_message(message.chat.id, "Таблица пуста! Сначaла добавьте предмет")
        start(message)

    else:
        if message.text == "Удалить дедлайн":
            info = bot.send_message(message.chat.id, "Название предмета, номер задания через запятую:")
            bot.register_next_step_handler(info, delete_deadline)

        elif message.text == "Изменить дедлайн":
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

            for subject in df["Subject"]:
                start_markup.row(subject)
            start_markup.row("Главное меню")

            info = bot.send_message(
                message.chat.id,
                "Выберите дедлайн:",
                reply_markup=start_markup,
            )
            bot.register_next_step_handler(info, choose_subject)

        elif message.text == "Добавить новый дедлайн":
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

            for subject in df["Subject"]:
                start_markup.row(subject)
            start_markup.row("Главное меню")

            info = bot.send_message(
                message.chat.id,
                "Название предмета:",
                reply_markup=start_markup,
            )
            bot.register_next_step_handler(info, choose_subject)

        else:
            bot.send_message(message.chat.id, "Я Вас не понимаю...")
            start(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Да")
    start_markup.row("Нет")
    warning = bot.send_message(
        message.chat.id, "Удалить таблицу? Данные о предметах будут утеряны: (Да/Нет)", reply_markup=start_markup
    )
    bot.register_next_step_handler(warning, clear_subject_list)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    message_ = message.text
    worksheet, _, df = access_current_sheet()

    if message_ == "Главное меню":
        return start(message)
    if not df["Subject"].isin([message_]).any():
        print(df["Subject"], message_)
        bot.send_message(message.chat.id, f"Предмет {message_} не был внесен в таблицу")
        return start(message)

    info = bot.send_message(message.chat.id, "Номер задания, новый дедлайн (dd/mm/yy):")
    bot.register_next_step_handler(info, update_subject_deadline, message.text)


def update_subject_deadline(msg, message_):
    """Обновляем дедлайн"""
    worksheet, _, df = access_current_sheet()
    try:
        n, date = [el.strip() for el in msg.text.split(",")]
        if not 1 <= int(n) <= 5:
            bot.send_message(msg.chat.id, "Номер задания: 1<=n<=5.")
            return start(msg)
        if is_valid_date(date, date[2]):
            worksheet.update_cell(
                worksheet.find(message_).row,
                int(n) + 2,
                convert_date("/".join(date.split(date[2]))).strftime("%d/%m/%y"),
            )
            bot.send_message(msg.chat.id, "Дата обновлена")
            start(msg)
        else:
            bot.send_message(
                msg.chat.id,
                "Ошибка ввода даты",
            )
            start(msg)
    except ValueError:
        bot.send_message(msg.chat.id, "Некорректный ввод! Номер задания, новый дедлайн (dd/mm/yy):")
        start(msg)


def delete_deadline(msg):
    """Вносим новое название предмета в Google-таблицу"""

    worksheet, _, df = access_current_sheet()
    try:
        subject_, n = [el.strip() for el in msg.text.split(",")]
        if not df["Subject"].isin([subject_]).any():
            bot.send_message(msg.chat.id, f"Предмет {subject_} не внесен в таблицу")
            return start(msg)

        if not 1 <= int(n) <= 5:
            bot.send_message(msg.chat.id, "Номер задания: 1<=n<=5")
            return start(msg)

        worksheet.update_cell(worksheet.find(subject_).row, int(n) + 2, "")
        bot.send_message(msg.chat.id, f"Дедлайн удален")
        start(msg)

    except ValueError:
        bot.send_message(msg.chat.id, "Некорректный ввод! Название предмета, номер задания через запятую:")
        start(msg)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    worksheet, _, df = access_current_sheet()
    try:
        if df["Subject"].isin([message.text.lower()]).any():
            bot.send_message(message.chat.id, f"Данные о предмете {message.text} уже есть в таблице")
            return start(message)
        else:
            worksheet.append_row([message.text])
            info = bot.send_message(
                message.chat.id,
                "Введите нужный url для предмета или любую комбинацию букв-не ссылку, если url не требуется",
            )
            bot.register_next_step_handler(info, add_new_subject_url)

    except KeyError:
        worksheet.append_row([message.text])
        info = bot.send_message(
            message.chat.id,
            "Введите нужный url для предмета или любую комбинацию букв-не ссылку, если url не требуется",
        )
        bot.register_next_step_handler(info, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    if is_valid_url(message.text):
        worksheet, _, df = access_current_sheet()
        index_row = df.shape[0] + 1
        worksheet.update_cell(index_row, 2, message.text)

        bot.send_message(message.chat.id, "Url внесена")
        return start(message)

    else:
        bot.send_message(
            message.chat.id, "Некорректный url! Вы всегда можете попробовать еще раз, или оставить предмет без ссылки"
        )
        return start(message)


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    message_ = message.text
    worksheet, _, df = access_current_sheet()

    if message_ == "Главное меню":
        return start(message)
    elif not df["Subject"].isin([message_]).any():
        bot.send_message(message.chat.id, f"Предмет {message_} не был внесен в таблицу")
        return start(message)

    def new_subject_and_url(msg):
        try:
            sub, url = [el.strip() for el in msg.text.split(",")]
            updated_subject_row = worksheet.find(message_).row
            worksheet.update_cell(updated_subject_row, 1, sub)
            if is_valid_url(url):
                worksheet.update_cell(updated_subject_row, 2, url)
                bot.send_message(msg.chat.id, "Информация о предмете и ссылка обновлена")
                start(msg)
            else:
                bot.send_message(msg.chat.id, "Неккоректный url, название обновлено")
                start(msg)
        except ValueError:
            bot.send_message(msg.chat.id, "Новая информация через запятую:")
            start(msg)

    info = bot.send_message(message.chat.id, "Новая информация через запятую: название, url")
    bot.register_next_step_handler(info, new_subject_and_url)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, _, df = access_current_sheet()
    if not df["Subject"].isin([message.text]).any():
        bot.send_message(message.chat.id, f"Предмет {message.text} не был внесен в таблицу")
        return start(message)
    worksheet.delete_row(worksheet.find(message.text).row)
    bot.send_message(message.chat.id, "Информация о предмете удалена")
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    if message.text.lower() == "да":
        worksheet = access_current_sheet()[0]
        worksheet.batch_clear(["A2:A", "B2:B", "C2:C", "D2:D", "E2:E", "F2:F", "G2:G"])
        bot.send_message(message.chat.id, "Таблица очищена")
        start(message)

    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id, "Вы отменили очищение таблицы")
        start(message)

    else:
        bot.send_message(
            message.chat.id, "Некорректный ввод! Выберите действие для очистки перед тем как продолжить: (Да/Нет)"
        )
        bot.register_next_step_handler(message, clear_subject_list)


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    try:
        access_current_sheet()
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайны")
        start_markup.row("Редактировать предметы")
    except ValueError:
        start_markup.row("Подключить Google-таблицу")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


with open("tables.json", "w") as f:
    json.dump({}, f)

# bot.infinity_polling()
