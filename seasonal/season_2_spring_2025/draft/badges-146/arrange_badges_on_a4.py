from PIL import Image, ImageDraw
import os
import math
from pathlib import Path

# Параметры
badges_dir = "badges"    # Директория с индивидуальными бейджами
output_dir = "a4_sheets" # Директория для сохранения A4 листов
cut_line_color = (200, 200, 200)  # Светло-серый цвет для линий отреза
cut_line_width = 2  # Толщина линии отреза

# Размеры A4 при 300 DPI (в пикселях)
a4_width = 2480   # 210 мм при 300 DPI
a4_height = 3508  # 297 мм при 300 DPI

# Создаем выходную директорию
os.makedirs(output_dir, exist_ok=True)

def get_subdirectories(directory):
    """Получает все поддиректории в указанной директории"""
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

def get_badge_files(directory):
    """Получает все PNG файлы из указанной директории (не включая поддиректории)"""
    badge_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and file.lower().endswith('.png'):
            badge_files.append(file_path)
    return badge_files

def arrange_badges_on_a4(badge_files, output_prefix):
    """Размещает бейджи на листах A4 с линиями для отреза"""
    if not badge_files:
        print(f"Бейджи в {output_prefix} не найдены.")
        return
    
    # Загружаем первый бейдж для определения размеров
    sample_badge = Image.open(badge_files[0])
    badge_width, badge_height = sample_badge.size
    
    # Рассчитываем, сколько бейджей поместится на A4
    badges_per_row = math.floor(a4_width / badge_width)
    badges_per_column = math.floor(a4_height / badge_height)
    badges_per_sheet = badges_per_row * badges_per_column
    
    # Рассчитываем отступы для центрирования бейджей на листе
    h_margin = (a4_width - (badges_per_row * badge_width)) // 2
    v_margin = (a4_height - (badges_per_column * badge_height)) // 2
    
    # Обработка всех бейджей
    sheet_index = 1
    for i in range(0, len(badge_files), badges_per_sheet):
        # Создаем новый лист A4
        a4_sheet = Image.new("RGB", (a4_width, a4_height), "white")
        draw = ImageDraw.Draw(a4_sheet)
        
        # Размещаем бейджи на листе
        badges_on_this_sheet = badge_files[i:i+badges_per_sheet]
        for j, badge_file in enumerate(badges_on_this_sheet):
            try:
                # Определяем позицию текущего бейджа
                row = j // badges_per_row
                col = j % badges_per_row
                
                x_position = h_margin + (col * badge_width)
                y_position = v_margin + (row * badge_height)
                
                # Загружаем и вставляем бейдж
                badge = Image.open(badge_file)
                a4_sheet.paste(badge, (x_position, y_position))
                
                # Выводим информацию о прогрессе
                badge_name = os.path.basename(badge_file)
                print(f"Добавлен бейдж: {badge_name} на лист {output_prefix}_{sheet_index}")
            
            except Exception as e:
                print(f"Ошибка при добавлении бейджа {badge_file}: {e}")
        
        # Рисуем горизонтальные линии для отреза
        for row in range(1, badges_per_column):
            y = v_margin + (row * badge_height)
            draw.line([(0, y), (a4_width, y)], fill=cut_line_color, width=cut_line_width)
        
        # Рисуем вертикальные линии для отреза
        for col in range(1, badges_per_row):
            x = h_margin + (col * badge_width)
            draw.line([(x, 0), (x, a4_height)], fill=cut_line_color, width=cut_line_width)
        
        # Сохраняем лист
        output_subdir = os.path.join(output_dir, os.path.dirname(output_prefix))
        os.makedirs(output_subdir, exist_ok=True)
        output_file = os.path.join(output_dir, f"{output_prefix}_{sheet_index}.pdf")
        a4_sheet.save(output_file, "PDF", resolution=300)
        print(f"Создан лист {output_prefix}_{sheet_index}: {output_file}")
        
        sheet_index += 1

def process_directory(dir_path, output_prefix=""):
    """Рекурсивно обрабатывает директорию и все поддиректории"""
    # Получаем все файлы бейджей в текущей директории
    badge_files = get_badge_files(dir_path)
    
    # Если в директории есть бейджи, обрабатываем их
    if badge_files:
        print(f"Найдено {len(badge_files)} бейджей в {dir_path}.")
        current_prefix = output_prefix if output_prefix else os.path.basename(dir_path)
        arrange_badges_on_a4(badge_files, current_prefix)
    
    # Получаем все поддиректории
    subdirs = get_subdirectories(dir_path)
    
    # Обрабатываем каждую поддиректорию
    for subdir in subdirs:
        subdir_path = os.path.join(dir_path, subdir)
        new_prefix = f"{subdir}" if not output_prefix else f"{output_prefix}/{subdir}"
        process_directory(subdir_path, new_prefix)

def main():
    # Обрабатываем все города и статусы оплаты отдельно
    print("Начинаем обработку бейджей по директориям...")
    
    # Обработка основной директории бейджей
    process_directory(badges_dir)
    
    print("Готово!")

if __name__ == "__main__":
    main() 