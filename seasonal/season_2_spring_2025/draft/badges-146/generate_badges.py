import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

# Пути к файлам
csv_path = "Регистрации.csv"           # Замените на путь к вашему CSV-файлу
logo_path = "logo_146_1.jpg"            # Логотип школы
output_dir = "badges"                   # Папка для сохранения бейджей

# Размер бейджа в пикселях (7.5 x 5.5 см при 300 DPI)
badge_width = 885
badge_height = 650

# Шрифты
try:
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    name_font = ImageFont.truetype(font_path, 70)
    class_font = ImageFont.truetype(font_path, 40)  # Меньший размер для класса
except:
    name_font = ImageFont.load_default()
    class_font = ImageFont.load_default()

# Загрузка данных
df = pd.read_csv(csv_path)
df.columns = [col.strip() for col in df.columns]
name_col = "ФИО"
tg_col = "Telegram Username"
year_col = "Год выпуска"  # Колонка с годом выпуска
class_col = "Класс"  # Колонка с информацией о классе
city_col = "Город участия во встрече"
paid_col = "Статус оплаты"

# Загрузка логотипа
logo = Image.open(logo_path).convert("RGBA")

# Подготовка папки
os.makedirs(output_dir, exist_ok=True)

# Генерация бейджей
for _, row in df.iterrows():
    name = str(row[name_col]).strip()
    username = str(row[tg_col]).strip()
    city = str(row[city_col]).strip()
    paid = str(row[paid_col]).strip()
    
    # Разделяем ФИО на фамилию и имя+отчество (если есть)
    name_parts = name.split()
    if len(name_parts) >= 2:
        surname = name_parts[0]
        first_name = " ".join(name_parts[1:])
    else:
        surname = name
        first_name = ""
    
    # Получаем год выпуска и класс
    year_info = ""
    class_info = ""
    
    if year_col in df.columns:
        year_info = str(row[year_col]).strip()
        if year_info.lower() == "nan":
            year_info = ""
            
    if class_col in df.columns:
        class_info = str(row[class_col]).strip()
        if class_info.lower() == "nan":
            class_info = ""
    
    # Формируем строку "Выпуск [год], [класс]"
    graduation_info = ""
    if str(year_info) == "0":
        #this is a teacher
        graduation_info = "Учитель"
    elif year_info and class_info:
        graduation_info = f"Выпуск {year_info}, 11 {class_info}"
    elif year_info:
        graduation_info = f"Выпуск {year_info}"
    elif class_info:
        graduation_info = class_info

    # Новый бейдж
    badge = Image.new("RGB", (badge_width, badge_height), "white")
    draw = ImageDraw.Draw(badge)

    # Логотип - справа вверху
    logo_resized = logo.resize((200, 200))
    logo_x = badge_width - 220  # Отступ от правого края
    badge.paste(logo_resized, (logo_x, 20), logo_resized)

    # Фамилия - слева
    text_x = 50  # Отступ от левого края
    draw.text((text_x, 100), surname, fill="black", font=name_font)
    
    # Имя (и отчество) - слева под фамилией
    if first_name:
        draw.text((text_x, 180), first_name, fill="black", font=name_font)

    # Информация о выпуске (если есть) - слева под именем
    y_pos = 260  # Начальная позиция для информации о выпуске
    if graduation_info:
        draw.text((text_x, y_pos), graduation_info, fill="black", font=class_font)

    # QR-код (если есть username) - справа внизу
    if username and username.lower() != "nan":
        qr_link = f"https://t.me/{username}"
        qr_img = qrcode.make(qr_link).resize((200, 200))
        qr_x = badge_width - 220  # Тот же отступ, что и для логотипа
        badge.paste(qr_img, (qr_x, badge_height - 220))  # Размещаем внизу справа

    # Сохранение
    filename = f"{city}/{paid}/{name.replace(' ', '_')}.png"
    os.makedirs(os.path.join(output_dir, city, paid), exist_ok=True)
    badge.save(os.path.join(output_dir, filename))