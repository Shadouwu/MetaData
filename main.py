import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ExifTags
import piexif
import os
import json
import math
import threading
import time
from datetime import datetime
import struct

# ═══════════════════════════════════════════════════════════
#                    ПЕРЕКЛАД МЕТАДАНИХ
# ═══════════════════════════════════════════════════════════

TRANSLATIONS = {
    # Основна інформація про файл
    "File Name": "Назва файлу",
    "File Size": "Розмір файлу",
    "File Type": "Тип файлу",
    "MIME Type": "MIME тип",
    "File Permissions": "Дозволи файлу",
    "File Modification Date/Time": "Дата зміни файлу",
    "File Creation Date/Time": "Дата створення файлу",
    "File Access Date/Time": "Дата доступу до файлу",

    # Камера та пристрій
    "Make": "Виробник камери",
    "Camera Model Name": "Модель камери",
    "Model": "Модель пристрою",
    "Software": "Програмне забезпечення",
    "Xiaomi Model": "Модель Xiaomi",

    # Зображення
    "Image Width": "Ширина зображення",
    "Image Height": "Висота зображення",
    "Image Size": "Розмір зображення",
    "Exif Image Width": "Ширина (EXIF)",
    "Exif Image Height": "Висота (EXIF)",
    "Megapixels": "Мегапікселі",
    "Orientation": "Орієнтація",
    "Image Description": "Опис зображення",
    "Color Space": "Кольоровий простір",
    "Color Components": "Кількість каналів",
    "Bits Per Sample": "Бітів на канал",
    "Encoding Process": "Процес кодування",
    "Compression": "Стиснення",
    "Y Cb Cr Sub Sampling": "Субдискретизація YCbCr",
    "Y Cb Cr Positioning": "Позиціонування YCbCr",
    "X Resolution": "Горизонтальна роздільність",
    "Y Resolution": "Вертикальна роздільність",
    "Resolution Unit": "Одиниця роздільності",

    # Час та дата
    "Date/Time Original": "Дата та час зйомки",
    "Create Date": "Дата створення",
    "Modify Date": "Дата редагування",
    "Datetime": "Дата та час",

    # Налаштування зйомки
    "Exposure Time": "Витримка",
    "Shutter Speed": "Швидкість затвора",
    "Shutter Speed Value": "Значення затвора",
    "F Number": "Діафрагма (F-число)",
    "Aperture": "Значення діафрагми",
    "Max Aperture Value": "Максимальна діафрагма",
    "ISO": "Чутливість ISO",
    "Recommended Exposure Index": "Рекомендований індекс експозиції",
    "Sensitivity Type": "Тип чутливості",
    "Exposure Program": "Програма експозиції",
    "Exposure Mode": "Режим експозиції",
    "Exposure Compensation": "Корекція експозиції",
    "Brightness Value": "Значення яскравості",
    "Light Value": "Значення світла",
    "Light Source": "Джерело світла",
    "White Balance": "Баланс білого",
    "Flash": "Спалах",
    "Focal Length": "Фокусна відстань",
    "Focal Length In 35mm Format": "Фокусна відстань (35мм екв.)",
    "Focal Length 35mm Equiv": "Еквівалент 35мм",
    "Digital Zoom Ratio": "Цифровий зум",
    "Zoom Multiple": "Кратність зуму",
    "Metering Mode": "Режим замірювання",
    "Scene Capture Type": "Тип сцени",
    "Mirror": "Дзеркало",
    "Sensor Type": "Тип сенсора",
    "Hdr": "HDR",
    "Filter Id": "Ідентифікатор фільтру",
    "AI Scene": "Сцена ШІ",
    "Op Mode": "Режим роботи",
    "Small Picture": "Мале зображення",

    # GPS
    "GPS Latitude": "Широта GPS",
    "GPS Longitude": "Довгота GPS",
    "GPS Altitude": "Висота GPS",
    "GPS Speed": "Швидкість GPS",
    "GPS Date Stamp": "Дата GPS",
    "GPS Time Stamp": "Час GPS",
    "GPS Position": "Позиція GPS",

    # EXIF технічне
    "Exif Version": "Версія EXIF",
    "Flashpix Version": "Версія Flashpix",
    "Exif Byte Order": "Порядок байтів EXIF",
    "Components Configuration": "Конфігурація компонентів",
    "Sub Sec Time": "Субсекундний час",
    "Sub Sec Time Original": "Субсекундний час (оригінал)",
    "Sub Sec Time Digitized": "Субсекундний час (оцифрований)",
    "Interoperability Index": "Індекс сумісності",
    "Interoperability Version": "Версія сумісності",
    "Thumbnail Offset": "Зміщення мініатюри",
    "Thumbnail Length": "Розмір мініатюри",
    "Thumbnail Image": "Мініатюра зображення",
    "Zone Identifier": "Ідентифікатор зони",
}

UNIT_TRANSLATIONS = {
    "inches": "дюйми",
    "cm": "сантиметри",
    "pixels": "пікселі",
    "Unknown": "Невідомо",
    "Standard": "Стандартна",
    "Auto": "Автоматично",
    "Manual": "Вручну",
    "Not Defined": "Не визначено",
    "Off, Did not fire": "Вимкнений, не спрацював",
    "On": "Увімкнений",
    "Off": "Вимкнений",
    "Other": "Інше",
    "Center-weighted average": "Центральнозважений",
    "Spot": "Точковий",
    "Matrix": "Матричний",
    "true": "Так",
    "false": "Ні",
    "rear": "Задня",
    "front": "Передня",
    "off": "Вимкнений",
    "on": "Увімкнений",
    "Little-endian (Intel, II)": "Малий порядок байтів (Intel)",
    "Big-endian (Motorola, MM)": "Великий порядок байтів (Motorola)",
    "Baseline DCT, Huffman coding": "Базовий DCT, кодування Хаффмана",
    "JPEG (old-style)": "JPEG (старий стиль)",
    "Co-sited": "Суміщений",
    "Centered": "По центру",
    "sRGB": "sRGB",
    "Adobe RGB": "Adobe RGB",
}


def translate_key(key):
    return TRANSLATIONS.get(key, key)


def translate_value(value):
    str_val = str(value)
    return UNIT_TRANSLATIONS.get(str_val, str_val)


# ═══════════════════════════════════════════════════════════
#                  ЧИТАННЯ МЕТАДАНИХ
# ═══════════════════════════════════════════════════════════

def get_file_info(filepath):
    """Отримує базову інформацію про файл"""
    info = {}
    try:
        stat = os.stat(filepath)
        size_bytes = stat.st_size

        # Форматування розміру
        if size_bytes < 1024:
            size_str = f"{size_bytes} Б"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} КБ"
        elif size_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.1f} МБ"
        else:
            size_str = f"{size_bytes / (1024 * 1024 * 1024):.1f} ГБ"

        info["Назва файлу"] = os.path.basename(filepath)
        info["Розмір файлу"] = size_str
        info["Шлях до файлу"] = os.path.dirname(filepath)
        info["Дата зміни файлу"] = datetime.fromtimestamp(stat.st_mtime).strftime("%Y:%m:%d %H:%M:%S")
        info["Дата створення файлу"] = datetime.fromtimestamp(stat.st_ctime).strftime("%Y:%m:%d %H:%M:%S")

        # Тип файлу
        ext = os.path.splitext(filepath)[1].upper()
        ext_map = {
            ".JPG": "JPEG", ".JPEG": "JPEG",
            ".PNG": "PNG", ".TIFF": "TIFF",
            ".TIF": "TIFF", ".HEIC": "HEIC",
            ".HEIF": "HEIF", ".WEBP": "WebP",
            ".BMP": "BMP", ".GIF": "GIF",
        }
        info["Тип файлу"] = ext_map.get(ext, ext.strip("."))
        info["Розширення"] = ext.strip(".").lower()

        mime_map = {
            ".JPG": "image/jpeg", ".JPEG": "image/jpeg",
            ".PNG": "image/png", ".TIFF": "image/tiff",
            ".HEIC": "image/heic", ".WEBP": "image/webp",
            ".BMP": "image/bmp", ".GIF": "image/gif",
        }
        info["MIME тип"] = mime_map.get(ext, "image/unknown")

    except Exception as e:
        info["Помилка"] = str(e)

    return info


def parse_exif_value(tag_name, value):
    """Парсить та форматує значення EXIF"""
    try:
        if isinstance(value, bytes):
            try:
                return value.decode('utf-8', errors='ignore').strip('\x00')
            except:
                return str(value)

        if isinstance(value, tuple) and len(value) == 2:
            num, den = value
            if den == 0:
                return "0"

            if tag_name in ["ExposureTime", "ShutterSpeedValue"]:
                if num < den:
                    return f"1/{den // num} с"
                else:
                    return f"{num / den:.4f} с"

            elif tag_name in ["FNumber", "ApertureValue", "MaxApertureValue"]:
                result = num / den
                return f"f/{result:.1f}"

            elif tag_name in ["FocalLength", "FocalLengthIn35mmFilm"]:
                result = num / den
                return f"{result:.1f} мм"

            elif tag_name in ["XResolution", "YResolution"]:
                return f"{num // den} dpi"

            elif tag_name in ["DigitalZoomRatio", "BrightnessValue",
                               "ExposureBiasValue", "CompressedBitsPerPixel"]:
                result = num / den
                return f"{result:.2f}"

            elif tag_name == "GPSAltitude":
                result = num / den
                return f"{result:.1f} м"

            else:
                if den == 1:
                    return str(num)
                result = num / den
                return f"{result:.4f}".rstrip('0').rstrip('.')

        return str(value)

    except Exception:
        return str(value)


def get_orientation_text(val):
    orientations = {
        1: "Горизонтально (нормальна)",
        2: "Дзеркально горизонтально",
        3: "Повернуто на 180°",
        4: "Дзеркально вертикально",
        5: "Дзеркально та повернуто на 270° за годинниковою",
        6: "Повернуто на 90° за годинниковою",
        7: "Дзеркально та повернуто на 90° за годинниковою",
        8: "Повернуто на 270° за годинниковою",
    }
    return orientations.get(val, f"Невідомо ({val})")


def get_metering_mode_text(val):
    modes = {
        0: "Невідомий", 1: "Середній", 2: "Центральнозважений",
        3: "Точковий", 4: "Мультиточковий", 5: "Матричний",
        6: "Частковий", 255: "Інший",
    }
    return modes.get(val, str(val))


def get_flash_text(val):
    if val == 0:
        return "Вимкнений, не спрацював"
    elif val & 1:
        return "Спрацював"
    else:
        return "Не спрацював"


def get_exposure_program_text(val):
    programs = {
        0: "Не визначено", 1: "Ручний", 2: "Нормальна програма",
        3: "Пріоритет діафрагми", 4: "Пріоритет витримки",
        5: "Творчий", 6: "Динамічний", 7: "Портретний",
        8: "Пейзажний",
    }
    return programs.get(val, str(val))


def get_white_balance_text(val):
    return "Автоматичний" if val == 0 else "Ручний"


def get_light_source_text(val):
    sources = {
        0: "Невідомо", 1: "Денне світло", 2: "Флуоресцентне",
        3: "Вольфрамове (лампа розжарювання)", 4: "Спалах",
        9: "Гарна погода", 10: "Похмура погода",
        11: "Тінь", 12: "Денне флуоресцентне",
        13: "Денне біле флуоресцентне", 14: "Холодне біле флуоресцентне",
        15: "Біле флуоресцентне", 255: "Інше",
    }
    return sources.get(val, str(val))


def get_color_space_text(val):
    if val == 1:
        return "sRGB"
    elif val == 65535:
        return "Некалібрований"
    return str(val)


def get_scene_capture_text(val):
    scenes = {0: "Стандартна", 1: "Пейзаж", 2: "Портрет", 3: "Нічна сцена"}
    return scenes.get(val, str(val))


def extract_metadata(filepath):
    """Повне вилучення метаданих з фото"""
    all_metadata = {}

    # 1. Базова інформація про файл
    all_metadata["📁 Інформація про файл"] = get_file_info(filepath)

    # 2. EXIF через Pillow
    try:
        img = Image.open(filepath)

        # Розміри зображення
        width, height = img.size
        img_info = {
            "Ширина зображення": f"{width} пікс.",
            "Висота зображення": f"{height} пікс.",
            "Розмір зображення": f"{width}x{height} пікс.",
            "Мегапікселі": f"{(width * height) / 1_000_000:.1f} Мп",
            "Режим кольору": img.mode,
        }
        all_metadata["🖼️ Параметри зображення"] = img_info

        # EXIF дані
        exif_data = img._getexif()
        if exif_data:
            camera_info = {}
            shooting_info = {}
            datetime_info = {}
            technical_info = {}
            gps_info = {}

            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, f"Tag_{tag_id}")

                # Пропускаємо бінарні дані мініатюри
                if tag_name in ["MakerNote", "UserComment", "JPEGThumbnail",
                                 "ThumbnailImage", "PrintIM"]:
                    continue

                if isinstance(value, bytes) and len(value) > 100:
                    continue

                # GPS окремо
                if tag_name == "GPSInfo":
                    try:
                        for gps_tag_id, gps_value in value.items():
                            gps_tag = ExifTags.GPSTAGS.get(gps_tag_id, f"GPS_{gps_tag_id}")
                            if isinstance(gps_value, tuple) and len(gps_value) > 0:
                                if gps_tag == "GPSLatitude":
                                    deg = gps_value[0][0] / gps_value[0][1]
                                    min_ = gps_value[1][0] / gps_value[1][1]
                                    sec = gps_value[2][0] / gps_value[2][1]
                                    gps_info["Широта"] = f"{deg:.0f}° {min_:.0f}' {sec:.2f}\""
                                elif gps_tag == "GPSLongitude":
                                    deg = gps_value[0][0] / gps_value[0][1]
                                    min_ = gps_value[1][0] / gps_value[1][1]
                                    sec = gps_value[2][0] / gps_value[2][1]
                                    gps_info["Довгота"] = f"{deg:.0f}° {min_:.0f}' {sec:.2f}\""
                                elif gps_tag == "GPSAltitude":
                                    alt = gps_value[0] / gps_value[1]
                                    gps_info["Висота над рівнем моря"] = f"{alt:.1f} м"
                                elif gps_tag == "GPSSpeed":
                                    speed = gps_value[0] / gps_value[1]
                                    gps_info["Швидкість"] = f"{speed:.1f} км/год"
                            else:
                                gps_info[gps_tag] = str(gps_value)
                    except Exception:
                        pass
                    continue

                # Форматування значень
                formatted_value = parse_exif_value(tag_name, value)

                # Спеціальна обробка
                if tag_name == "Orientation":
                    formatted_value = get_orientation_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "MeteringMode":
                    formatted_value = get_metering_mode_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "Flash":
                    formatted_value = get_flash_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "ExposureProgram":
                    formatted_value = get_exposure_program_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "WhiteBalance":
                    formatted_value = get_white_balance_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "LightSource":
                    formatted_value = get_light_source_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "ColorSpace":
                    formatted_value = get_color_space_text(value) if isinstance(value, int) else formatted_value
                elif tag_name == "SceneCaptureType":
                    formatted_value = get_scene_capture_text(value) if isinstance(value, int) else formatted_value

                # Отримуємо переклад ключа
                uk_name = TRANSLATIONS.get(tag_name, tag_name)

                # Розподіл по категоріях
                camera_tags = {"Make", "Model", "Software", "XiaomiModel",
                               "LensMake", "LensModel"}
                datetime_tags = {"DateTime", "DateTimeOriginal",
                                 "DateTimeDigitized", "SubSecTime",
                                 "SubSecTimeOriginal", "SubSecTimeDigitized",
                                 "OffsetTime", "OffsetTimeOriginal"}
                shooting_tags = {"ExposureTime", "FNumber", "ISOSpeedRatings",
                                 "ShutterSpeedValue", "ApertureValue",
                                 "BrightnessValue", "ExposureBiasValue",
                                 "MaxApertureValue", "MeteringMode",
                                 "Flash", "FocalLength", "ExposureProgram",
                                 "ExposureMode", "WhiteBalance", "LightSource",
                                 "DigitalZoomRatio", "FocalLengthIn35mmFilm",
                                 "SceneCaptureType", "SensingMethod"}

                if tag_name in camera_tags:
                    camera_info[uk_name] = formatted_value
                elif tag_name in datetime_tags:
                    datetime_info[uk_name] = formatted_value
                elif tag_name in shooting_tags:
                    shooting_info[uk_name] = formatted_value
                else:
                    technical_info[uk_name] = formatted_value

            if camera_info:
                all_metadata["📷 Камера та пристрій"] = camera_info
            if datetime_info:
                all_metadata["📅 Дата та час"] = datetime_info
            if shooting_info:
                all_metadata["⚙️ Налаштування зйомки"] = shooting_info
            if gps_info:
                all_metadata["📍 GPS координати"] = gps_info
            if technical_info:
                all_metadata["🔧 Технічні дані"] = technical_info

    except Exception as e:
        all_metadata["❌ Помилка читання EXIF"] = {"Помилка": str(e)}

    return all_metadata


def save_metadata_to_file(metadata, filepath):
    """Зберігає метадані у текстовий файл"""
    lines = []
    lines.append("=" * 70)
    lines.append("          МЕТАДАНІ ЗОБРАЖЕННЯ - ANONYMOUS METADATA VIEWER")
    lines.append("=" * 70)
    lines.append(f"Згенеровано: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")

    for section, data in metadata.items():
        lines.append(f"\n{section}")
        lines.append("─" * 50)
        if isinstance(data, dict):
            for key, value in data.items():
                key_padded = key.ljust(35)
                lines.append(f"  {key_padded}: {value}")
        lines.append("")

    lines.append("=" * 70)
    lines.append("        © Anonymous Metadata Viewer | Автор: @shadouwu (Telegram)")
    lines.append("=" * 70)

    content = "\n".join(lines)

    # Вибір куди зберегти
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[
            ("Текстовий файл", "*.txt"),
            ("Всі файли", "*.*")
        ],
        initialfile=f"metadata_{os.path.basename(filepath)}.txt",
        title="Зберегти метадані"
    )

    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return save_path
    return None


# ═══════════════════════════════════════════════════════════
#                    ГОЛОВНЕ ВІКНО
# ═══════════════════════════════════════════════════════════

class SplashScreen:
    """Екран завантаження з анімацією"""

    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.canvas = None
        self.animation_running = True
        self.angle = 0
        self.particles = []
        self.alpha = 0
        self.setup()

    def setup(self):
        self.root.title("")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        self.root.configure(bg="#000000")

        # Центрування вікна
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 800) // 2
        y = (sh - 500) // 2
        self.root.geometry(f"800x500+{x}+{y}")
        self.root.overrideredirect(True)

        # Canvas для анімації
        self.canvas = tk.Canvas(
            self.root,
            width=800, height=500,
            bg="#000000",
            highlightthickness=0
        )
        self.canvas.pack()

        # Ініціалізація частинок
        import random
        for _ in range(40):
            self.particles.append({
                "x": random.randint(0, 800),
                "y": random.randint(0, 500),
                "size": random.uniform(1, 3),
                "speed": random.uniform(0.2, 1.0),
                "alpha": random.randint(50, 200),
                "dx": random.uniform(-0.5, 0.5),
            })

        self.draw_frame()

    def draw_frame(self):
        if not self.animation_running:
            return

        c = self.canvas
        c.delete("all")

        # Фон - градієнт
        for i in range(0, 500, 3):
            r = int(0 + (i / 500) * 5)
            g = int(0 + (i / 500) * 5)
            b = int(20 + (i / 500) * 10)
            color = f"#{r:02x}{g:02x}{b:02x}"
            c.create_rectangle(0, i, 800, i + 3, fill=color, outline="")

        # Матричний дощ (символи)
        import random
        matrix_chars = "01アイウエオカキクケコ∂∫∑∏∆"
        for i in range(0, 800, 25):
            for j in range(0, 500, 18):
                if random.random() > 0.85:
                    alpha_v = random.randint(30, 120)
                    char = random.choice(matrix_chars)
                    green_val = int(alpha_v)
                    color = f"#00{min(green_val, 255):02x}00"
                    size = random.choice([8, 9, 10])
                    c.create_text(i, j, text=char, fill=color,
                                  font=("Courier", size))

        # Частинки
        for p in self.particles:
            p["x"] += p["dx"]
            p["y"] -= p["speed"]
            if p["y"] < -5:
                p["y"] = 505
                p["x"] = random.randint(0, 800)
            if p["x"] < 0 or p["x"] > 800:
                p["dx"] *= -1

            brightness = p["alpha"]
            color = f"#00{min(brightness, 255):02x}{min(brightness // 2, 255):02x}"
            size = p["size"]
            c.create_oval(
                p["x"] - size, p["y"] - size,
                p["x"] + size, p["y"] + size,
                fill=color, outline=""
            )

        # Рамка з ліній
        c.create_rectangle(15, 15, 785, 485,
                            outline="#00ff41", width=1)
        c.create_rectangle(20, 20, 780, 480,
                            outline="#00aa20", width=1)

        # Кутові акценти
        corners = [(15, 15), (785, 15), (15, 485), (785, 485)]
        offsets = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        for (cx, cy), (ox, oy) in zip(corners, offsets):
            c.create_line(cx, cy, cx + ox * 30, cy, fill="#00ff41", width=2)
            c.create_line(cx, cy, cx, cy + oy * 30, fill="#00ff41", width=2)

        # Рядок що рухається
        line_y = 250 + 100 * math.sin(math.radians(self.angle * 0.5))
        c.create_line(30, line_y, 770, line_y,
                      fill="#003300", width=1, dash=(4, 4))

        # Велике лого ANONYMOUS
        c.create_text(400, 140,
                      text="ANONYMOUS",
                      font=("Courier", 52, "bold"),
                      fill="#00ff41")

        # Тінь логотипу
        c.create_text(402, 142,
                      text="ANONYMOUS",
                      font=("Courier", 52, "bold"),
                      fill="#003300")
        c.create_text(400, 140,
                      text="ANONYMOUS",
                      font=("Courier", 52, "bold"),
                      fill="#00ff41")

        # Підзаголовок
        c.create_text(400, 200,
                      text="[ METADATA VIEWER @shadouwu ]",
                      font=("Courier", 20),
                      fill="#00cc33")

        # Декоративна лінія
        c.create_line(150, 225, 650, 225, fill="#005500", width=1)

        # Рядки інформації
        c.create_text(400, 260,
                      text="Аналіз метаданих зображень",
                      font=("Courier", 13),
                      fill="#00aa20")

        c.create_text(400, 285,
                      text="Перегляд • Аналіз • Збереження",
                      font=("Courier", 11),
                      fill="#007710")

        # Анімована крапки завантаження
        dots = "●" * (int(self.angle / 15) % 4 + 1)
        c.create_text(400, 330,
                      text=f"Ініціалізація {dots}",
                      font=("Courier", 12),
                      fill="#00ff41")

        # Прогрес бар
        progress = min(self.angle / 360, 1.0)
        bar_width = int(500 * progress)
        c.create_rectangle(150, 360, 650, 375,
                            outline="#005500", fill="#001100")
        if bar_width > 0:
            c.create_rectangle(150, 360, 150 + bar_width, 375,
                                fill="#00ff41", outline="")

        c.create_text(400, 380,
                      text=f"{int(progress * 100)}%",
                      font=("Courier", 10),
                      fill="#00cc33")

        # Нижній рядок
        c.create_text(400, 460,
              text="[ We are Anonymous • We are Legion • Автор проекту: @shadouwu ]",
                      font=("Courier", 8),
                      fill="#003300")

        # Оновлення кута
        self.angle += 2

        if self.angle >= 360:
            self.animation_running = False
            self.root.after(300, self.callback)
        else:
            self.root.after(16, self.draw_frame)


# ═══════════════════════════════════════════════════════════
#                 ВІКНО МЕТАДАНИХ
# ═══════════════════════════════════════════════════════════

class MetadataWindow:
    """Вікно відображення метаданих конкретного фото"""

    def __init__(self, parent, filepath, metadata):
        self.filepath = filepath
        self.metadata = metadata

        self.window = ctk.CTkToplevel(parent)
        self.window.title(f"Метадані — {os.path.basename(filepath)}")
        self.window.geometry("950x700")
        self.window.configure(fg_color="#050505")

        # Центрування
        self.window.update_idletasks()
        sw = self.window.winfo_screenwidth()
        sh = self.window.winfo_screenheight()
        x = (sw - 950) // 2
        y = (sh - 700) // 2
        self.window.geometry(f"950x700+{x}+{y}")

        self.setup_ui()
        self.window.grab_set()

    def setup_ui(self):
        # Заголовок
        header = ctk.CTkFrame(self.window, fg_color="#050505", height=80)
        header.pack(fill="x", padx=15, pady=(15, 0))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="[ METADATA VIEWER ]",
            font=ctk.CTkFont("Courier", 22, "bold"),
            text_color="#00ff41"
        ).pack(side="left", padx=15)

        filename = os.path.basename(self.filepath)
        if len(filename) > 35:
            filename = filename[:32] + "..."

        ctk.CTkLabel(
            header,
            text=f"📄 {filename}",
            font=ctk.CTkFont("Courier", 13),
            text_color="#00cc33"
        ).pack(side="left", padx=20)

        # Кнопка збереження
        save_btn = ctk.CTkButton(
            header,
            text="💾 ЗАВАНТАЖИТИ",
            font=ctk.CTkFont("Courier", 13, "bold"),
            fg_color="#003300",
            hover_color="#005500",
            border_color="#00ff41",
            border_width=1,
            text_color="#00ff41",
            width=160,
            height=40,
            corner_radius=4,
            command=self.save_metadata
        )
        save_btn.pack(side="right", padx=15)

        # Роздільник
        ctk.CTkFrame(self.window, height=1, fg_color="#003300").pack(
            fill="x", padx=15, pady=8)

        # Основний контент
        content_frame = ctk.CTkFrame(self.window, fg_color="#050505")
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        content_frame.rowconfigure(0, weight=1)

        # Ліва панель - прев'ю + секції
        left_panel = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="#080808",
            scrollbar_button_color="#003300",
            scrollbar_button_hover_color="#005500",
            width=230
        )
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Прев'ю зображення
        try:
            img = Image.open(self.filepath)
            img.thumbnail((200, 160), Image.LANCZOS)
            self.thumb = ctk.CTkImage(light_image=img, size=img.size)

            preview_frame = ctk.CTkFrame(left_panel, fg_color="#0a0a0a",
                                         border_color="#003300", border_width=1)
            preview_frame.pack(fill="x", pady=(5, 10), padx=5)

            ctk.CTkLabel(
                preview_frame,
                image=self.thumb,
                text=""
            ).pack(pady=8)

        except Exception:
            pass

        # Кнопки секцій
        ctk.CTkLabel(
            left_panel,
            text="РОЗДІЛИ",
            font=ctk.CTkFont("Courier", 10, "bold"),
            text_color="#005500"
        ).pack(pady=(5, 5))

        self.section_buttons = {}
        for section in self.metadata.keys():
            btn = ctk.CTkButton(
                left_panel,
                text=section,
                font=ctk.CTkFont("Courier", 10),
                fg_color="#0a0a0a",
                hover_color="#002200",
                border_color="#003300",
                border_width=1,
                text_color="#00aa20",
                anchor="w",
                height=32,
                corner_radius=3,
                command=lambda s=section: self.scroll_to_section(s)
            )
            btn.pack(fill="x", padx=5, pady=2)
            self.section_buttons[section] = btn

        # Права панель - метадані
        self.right_panel = ctk.CTkScrollableFrame(
            content_frame,
            fg_color="#050505",
            scrollbar_button_color="#003300",
            scrollbar_button_hover_color="#005500",
        )
        self.right_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        self.section_frames = {}
        self.render_metadata()

    def render_metadata(self):
        """Відображення всіх метаданих"""
        for section, data in self.metadata.items():
            # Заголовок секції
            section_label = ctk.CTkLabel(
                self.right_panel,
                text=f"  {section}",
                font=ctk.CTkFont("Courier", 14, "bold"),
                text_color="#00ff41",
                anchor="w",
                fg_color="#0a1a0a"
            )
            section_label.pack(fill="x", pady=(15, 3), padx=5)
            self.section_frames[section] = section_label

            # Роздільник
            ctk.CTkFrame(
                self.right_panel, height=1, fg_color="#003300"
            ).pack(fill="x", padx=10, pady=2)

            if not isinstance(data, dict):
                continue

            # Рядки даних
            for i, (key, value) in enumerate(data.items()):
                row_color = "#080808" if i % 2 == 0 else "#050505"

                row = ctk.CTkFrame(
                    self.right_panel,
                    fg_color=row_color,
                    corner_radius=3
                )
                row.pack(fill="x", padx=10, pady=1)
                row.columnconfigure(1, weight=1)

                # Ключ
                key_label = ctk.CTkLabel(
                    row,
                    text=f"  {key}",
                    font=ctk.CTkFont("Courier", 11),
                    text_color="#00aa20",
                    anchor="w",
                    width=220
                )
                key_label.grid(row=0, column=0, sticky="w",
                                padx=(5, 10), pady=4)

                # Розділювач
                ctk.CTkLabel(
                    row, text="│",
                    font=ctk.CTkFont("Courier", 11),
                    text_color="#003300"
                ).grid(row=0, column=1, padx=2)

                # Значення
                value_str = str(value) if value else "—"
                val_label = ctk.CTkLabel(
                    row,
                    text=f"  {value_str}",
                    font=ctk.CTkFont("Courier", 11),
                    text_color="#00ff41",
                    anchor="w",
                    wraplength=450,
                    justify="left"
                )
                val_label.grid(row=0, column=2, sticky="w",
                                padx=(5, 10), pady=4)

    def scroll_to_section(self, section):
        """Прокрутка до секції"""
        if section in self.section_frames:
            widget = self.section_frames[section]
            self.right_panel._parent_canvas.yview_moveto(
                widget.winfo_y() / max(self.right_panel.winfo_height(), 1)
            )

    def save_metadata(self):
        """Збереження метаданих у файл"""
        path = save_metadata_to_file(self.metadata, self.filepath)
        if path:
            messagebox.showinfo(
                "Успішно збережено",
                f"✅ Метадані збережено у файл:\n{path}",
                parent=self.window
            )


# ═══════════════════════════════════════════════════════════
#                   ГОЛОВНЕ МЕНЮ
# ═══════════════════════════════════════════════════════════

class MainApp:
    """Головне вікно застосунку"""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = ctk.CTk()
        self.photos = []  # Список доданих фото: (path, metadata)

        # Показуємо splash screen
        self.show_splash()

    def show_splash(self):
        """Показ splash screen"""
        splash_win = tk.Tk()
        splash_win.configure(bg="#000000")
        SplashScreen(splash_win, lambda: self.on_splash_done(splash_win))
        splash_win.mainloop()

    def on_splash_done(self, splash_win):
        """Після splash screen показуємо головне меню"""
        splash_win.destroy()
        self.setup_main_window()
        self.root.mainloop()

    def setup_main_window(self):
        """Налаштування головного вікна"""
        self.root.title("Anonymous Metadata Viewer")
        self.root.geometry("1100x720")
        self.root.configure(fg_color="#050505")

        # Центрування
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - 1100) // 2
        y = (sh - 720) // 2
        self.root.geometry(f"1100x720+{x}+{y}")

        self.build_ui()

    def build_ui(self):
        """Побудова інтерфейсу"""
        # ── Ліва панель ──────────────────────────────────────────
        left_panel = ctk.CTkFrame(
            self.root,
            width=280,
            fg_color="#050505",
            border_color="#002200",
            border_width=1
        )
        left_panel.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left_panel.pack_propagate(False)

        # Логотип
        logo_frame = ctk.CTkFrame(left_panel, fg_color="#050505")
        logo_frame.pack(fill="x", pady=(20, 10))

        ctk.CTkLabel(
            logo_frame,
            text="ANON",
            font=ctk.CTkFont("Courier", 32, "bold"),
            text_color="#00ff41"
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="METADATA",
            font=ctk.CTkFont("Courier", 14, "bold"),
            text_color="#00cc33"
        ).pack()

        ctk.CTkLabel(
            logo_frame,
            text="VIEWER",
            font=ctk.CTkFont("Courier", 14),
            text_color="#007710"
        ).pack()

        # Декоративна лінія
        ctk.CTkFrame(left_panel, height=1,
                     fg_color="#003300").pack(fill="x", padx=15, pady=10)

        # Статистика
        self.stats_frame = ctk.CTkFrame(
            left_panel,
            fg_color="#0a0a0a",
            border_color="#002200",
            border_width=1,
            corner_radius=5
        )
        self.stats_frame.pack(fill="x", padx=15, pady=5)

        ctk.CTkLabel(
            self.stats_frame,
            text="СТАТИСТИКА",
            font=ctk.CTkFont("Courier", 9, "bold"),
            text_color="#005500"
        ).pack(pady=(8, 3))

        self.photos_count_label = ctk.CTkLabel(
            self.stats_frame,
            text="Фотографій: 0",
            font=ctk.CTkFont("Courier", 11),
            text_color="#00aa20"
        )
        self.photos_count_label.pack(pady=2)

        ctk.CTkFrame(left_panel, height=1,
                     fg_color="#003300").pack(fill="x", padx=15, pady=10)

        # Кнопки управління
        ctk.CTkLabel(
            left_panel,
            text="ДІЇ",
            font=ctk.CTkFont("Courier", 9, "bold"),
            text_color="#005500"
        ).pack(pady=(0, 5))

        add_btn = ctk.CTkButton(
            left_panel,
            text="＋  ДОДАТИ ФОТО",
            font=ctk.CTkFont("Courier", 13, "bold"),
            fg_color="#003300",
            hover_color="#005500",
            border_color="#00ff41",
            border_width=1,
            text_color="#00ff41",
            height=45,
            corner_radius=5,
            command=self.add_photos
        )
        add_btn.pack(fill="x", padx=15, pady=4)

        clear_btn = ctk.CTkButton(
            left_panel,
            text="🗑  ОЧИСТИТИ ВСЕ",
            font=ctk.CTkFont("Courier", 11),
            fg_color="#0a0a0a",
            hover_color="#1a0000",
            border_color="#330000",
            border_width=1,
            text_color="#aa2020",
            height=38,
            corner_radius=5,
            command=self.clear_all
        )
        clear_btn.pack(fill="x", padx=15, pady=4)

        # Декоративний текст знизу
        ctk.CTkFrame(left_panel, height=1,
                     fg_color="#002200").pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(
    left_panel,
    text="We are Anonymous\nАвтор: @shadouwu",
            font=ctk.CTkFont("Courier", 9),
            text_color="#003300"
        ).pack(pady=5)

        # ── Права панель ──────────────────────────────────────────
        right_panel = ctk.CTkFrame(
            self.root,
            fg_color="#050505"
        )
        right_panel.pack(side="right", fill="both",
                         expand=True, padx=(5, 10), pady=10)

        # Заголовок правої панелі
        header = ctk.CTkFrame(right_panel, fg_color="#050505", height=60)
        header.pack(fill="x", pady=(0, 5))
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="[ ГАЛЕРЕЯ ФОТОГРАФІЙ ]",
            font=ctk.CTkFont("Courier", 18, "bold"),
            text_color="#00ff41"
        ).pack(side="left", padx=10, pady=15)

        ctk.CTkLabel(
            header,
            text="Натисніть на фото для перегляду метаданих",
            font=ctk.CTkFont("Courier", 10),
            text_color="#005500"
        ).pack(side="right", padx=10, pady=15)

        ctk.CTkFrame(right_panel, height=1,
                     fg_color="#003300").pack(fill="x", padx=5)

        # Scrollable галерея
        self.gallery_frame = ctk.CTkScrollableFrame(
            right_panel,
            fg_color="#050505",
            scrollbar_button_color="#003300",
            scrollbar_button_hover_color="#005500",
        )
        self.gallery_frame.pack(fill="both", expand=True, pady=(5, 0))

        # Порожній стан
        self.empty_label = ctk.CTkLabel(
            self.gallery_frame,
            text="[ Фотографій не додано ]\n\nНатисніть '+ ДОДАТИ ФОТО'\nщоб розпочати аналіз",
            font=ctk.CTkFont("Courier", 16),
            text_color="#003300"
        )
        self.empty_label.pack(expand=True, pady=200)

    def add_photos(self):
        """Додавання фотографій"""
        filepaths = filedialog.askopenfilenames(
            title="Оберіть фотографії",
            filetypes=[
                ("Зображення", "*.jpg *.jpeg *.png *.tiff *.tif "
                               "*.heic *.heif *.webp *.bmp"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("Всі файли", "*.*"),
            ]
        )

        if not filepaths:
            return

        # Видаляємо порожній label
        if self.empty_label and self.empty_label.winfo_exists():
            self.empty_label.pack_forget()

        # Завантаження з прогресом
        loading = ctk.CTkLabel(
            self.gallery_frame,
            text="⏳ Читання метаданих...",
            font=ctk.CTkFont("Courier", 14),
            text_color="#00aa20"
        )
        loading.pack(pady=20)
        self.root.update()

        for filepath in filepaths:
            # Перевірка чи вже є
            if any(p[0] == filepath for p in self.photos):
                continue

            metadata = extract_metadata(filepath)
            self.photos.append((filepath, metadata))

        loading.pack_forget()

        self.render_gallery()
        self.update_stats()

    def render_gallery(self):
        """Відображення галереї"""
        # Очищення
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()

        if not self.photos:
            self.empty_label = ctk.CTkLabel(
                self.gallery_frame,
                text="[ Фотографій не додано ]\n\nНатисніть '+ ДОДАТИ ФОТО'\nщоб розпочати аналіз",
                font=ctk.CTkFont("Courier", 16),
                text_color="#003300"
            )
            self.empty_label.pack(expand=True, pady=200)
            return

        # Сітка карток
        columns = 3
        row_frame = None

        for idx, (filepath, metadata) in enumerate(self.photos):
            if idx % columns == 0:
                row_frame = ctk.CTkFrame(
                    self.gallery_frame, fg_color="#050505"
                )
                row_frame.pack(fill="x", padx=5, pady=3)

            self.create_photo_card(row_frame, filepath, metadata, idx)

    def create_photo_card(self, parent, filepath, metadata, idx):
        """Створення картки фото"""
        card = ctk.CTkFrame(
            parent,
            fg_color="#0a0a0a",
            border_color="#003300",
            border_width=1,
            corner_radius=6,
            width=230,
            height=200
        )
        card.pack(side="left", padx=5, pady=5)
        card.pack_propagate(False)

        # Прев'ю
        try:
            img = Image.open(filepath)
            img.thumbnail((190, 130), Image.LANCZOS)
            photo_img = ctk.CTkImage(light_image=img, size=img.size)

            img_label = ctk.CTkLabel(
                card, image=photo_img, text="",
                cursor="hand2"
            )
            img_label.image = photo_img
            img_label.pack(pady=(8, 4))

        except Exception:
            ctk.CTkLabel(
                card,
                text="[ Помилка\nзавантаження ]",
                font=ctk.CTkFont("Courier", 10),
                text_color="#550000"
            ).pack(pady=20)

        # Назва файлу
        filename = os.path.basename(filepath)
        if len(filename) > 22:
            filename = filename[:19] + "..."

        name_label = ctk.CTkLabel(
            card,
            text=filename,
            font=ctk.CTkFont("Courier", 10, "bold"),
            text_color="#00cc33",
            cursor="hand2"
        )
        name_label.pack()

        # Розмір з метаданих
        size_str = ""
        file_info = metadata.get("📁 Інформація про файл", {})
        if file_info:
            size_str = file_info.get("Розмір файлу", "")

        if size_str:
            ctk.CTkLabel(
                card,
                text=size_str,
                font=ctk.CTkFont("Courier", 9),
                text_color="#005500"
            ).pack()

        # Кнопка видалення
        del_btn = ctk.CTkButton(
            card,
            text="✕",
            width=20, height=20,
            fg_color="#0a0a0a",
            hover_color="#1a0000",
            text_color="#550000",
            border_width=0,
            font=ctk.CTkFont("Courier", 10),
            corner_radius=3,
            command=lambda i=idx: self.remove_photo(i)
        )
        del_btn.place(relx=1.0, rely=0.0, x=-5, y=5, anchor="ne")

        # Клік для відкриття метаданих
        def open_meta(event=None, fp=filepath, md=metadata):
            self.open_metadata_window(fp, md)

        card.bind("<Button-1>", open_meta)
        for child in card.winfo_children():
            child.bind("<Button-1>", open_meta)

        # Hover ефект
        def on_enter(e, c=card):
            c.configure(border_color="#00ff41")

        def on_leave(e, c=card):
            c.configure(border_color="#003300")

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    def open_metadata_window(self, filepath, metadata):
        """Відкриття вікна метаданих"""
        MetadataWindow(self.root, filepath, metadata)

    def remove_photo(self, idx):
        """Видалення фото"""
        if 0 <= idx < len(self.photos):
            self.photos.pop(idx)
            self.render_gallery()
            self.update_stats()

    def clear_all(self):
        """Очищення всіх фото"""
        if self.photos:
            if messagebox.askyesno(
                "Підтвердження",
                "Видалити всі додані фотографії?",
                parent=self.root
            ):
                self.photos.clear()
                self.render_gallery()
                self.update_stats()

    def update_stats(self):
        """Оновлення статистики"""
        self.photos_count_label.configure(
            text=f"Фотографій: {len(self.photos)}"
        )


# ═══════════════════════════════════════════════════════════
#                      ЗАПУСК
# ═══════════════════════════════════════════════════════════

if __name__ == "__main__":
    app = MainApp()