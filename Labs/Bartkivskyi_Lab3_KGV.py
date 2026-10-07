from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import time
import os

class Lab3:
    def pics_merge(self):
        path1 = input("Уведіть назву першого зображення: ").strip().strip('"\'')
        path2 = input("Уведіть назву другого зображення: ").strip().strip('"\'')

        print("Напрямок об'єднання: ")
        print("1 - Горизонтально\n2 - Вертикально")
        direction = input("Ваш вибір (1, 2): ")

        if direction in ('1', '2'):
            try:
                with Image.open(path1) as img1, Image.open(path2) as img2:
                    img1 = img1.convert("RGBA")
                    img2 = img2.convert("RGBA")

                    w1, h1 = img1.size
                    w2, h2 = img2.size
                    
                    if direction == '1':
                        if h1 != h2:
                            new_w2 = int(w2 * (h1 / h2))
                            img2 = img2.resize((new_w2, h1), Image.Resampling.LANCZOS)
                            w2 = new_w2

                        new_width = w1 + w2
                        new_height = h1
                        canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
                        canvas.paste(img1, (0, 0))
                        canvas.paste(img2, (w1, 0))

                        d = "horizontal"

                    elif direction == '2':
                        if w1 != w2:
                            new_h2 = int(h2 * (w1 / w2))
                            img2 = img2.resize((w1, new_h2), Image.Resampling.LANCZOS)
                            h2 = new_h2

                        new_width = w1
                        new_height = h1 + h2
                        canvas = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
                        canvas.paste(img1, (0, 0))
                        canvas.paste(img2, (0, h1))

                        d = "vertical"

                    new_path = f"combined_image_{d}.png"
                    canvas.save(new_path)
                    print(f"Зображення збережено як {new_path}")

            except Exception as e:
                print(f"Помилка під час об'єднання зображень: {e}")
        else:
            print("Обирайте число 1 або 2")
            return

    def watermark(self):
        path = input("Уведіть назву зображення: ").strip().strip('"\'')
        text = input("Уведіть текст водяного знаку: ")

        try:
            opacity_percent = int(input("Прозорість тексту (0-100, 100 - непрозорий): "))
            font_size = int(input("Розмір шрифту (наприклад, 36): "))

            start_input = input("Координати розміщення XxY (наприклад, 50x50): ").strip()
            tokens = start_input.replace(',', ' ').replace('x', ' ').replace('X', ' ').split()
            if len(tokens) != 2:
                print("Некоректний формат координат.")
                return
            x, y = int(tokens[0]), int(tokens[1])

            alpha_val = int((opacity_percent / 100.0) * 255)

            text_colour_input = input("Уведіть колір тексту (r = red, g = green, b = blue): ").strip().lower()

            if text_colour_input == 'r':
                colour_rgb = (255, 0, 0, alpha_val)
            elif text_colour_input == 'g':
                colour_rgb = (0, 255, 0, alpha_val)
            elif text_colour_input == 'b':
                colour_rgb = (0, 0, 255, alpha_val)
            else:
                print("Уводьте r, g або b")
                return

            with Image.open(path) as img:
                base_img = img.convert("RGBA")

                watermark_layer = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
                draw = ImageDraw.Draw(watermark_layer)

                # Спроба завантажити системний шрифт Arial, або стандартний якщо відсутній
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except IOError:
                    font = ImageFont.load_default()

                draw.text((x, y), text, fill=colour_rgb, font=font)

                result_img = Image.alpha_composite(base_img, watermark_layer)

                base_name, _ = os.path.splitext(path)
                new_path = f"{base_name}_watermarked.png"
                result_img.save(new_path)
                print(f"Зображення збережено як {new_path}")

        except Exception as e:
            print(f"Помилка при додаванні водяного знаку: {e}")

    def slideshow(self):
        paths_input = input("Уведіть назви файлів або шляхи через пробіл: ").strip()
        raw_paths = paths_input.split()
    
        # Фільтруємо існуючі файли
        file_list = [p.strip('"\'') for p in raw_paths if os.path.exists(p.strip('"\''))]

        if not file_list:
            print("Не знайдено жодного дійсного файлу.")
            return

        try:
            delay = float(input("Уведіть затримку між слайдами в секундах (наприклад, 2): "))
        except ValueError:
            delay = 2.0

        # Створюємо вікно заданого розміру (ширина x висота в дюймах)
        plt.figure(figsize=(6, 6))

        for path in file_list:
            try:
                img = Image.open(path)
            
                plt.clf()  # Очищаємо вікно перед виводом нового кадру
                plt.imshow(img)
                plt.axis('off')  # Приховуємо рамки та осі з координатами
                plt.title(f"Файл: {os.path.basename(path)}")
            
                plt.draw()
                plt.pause(delay)  # Затримка замість time.sleep(), яка оновлює інтерфейс matplotlib

            except Exception as e:
                print(f"Не вдалося відкрити {path}: {e}")
                
        plt.close()