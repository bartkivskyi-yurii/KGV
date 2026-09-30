import os
import math
from PIL import Image, ImageEnhance

class Lab2:
    def change_transparency(self):
        path = input("Уведіть назву зображення: ").strip().strip('"\'')

        try:
            opacity_percent = float(input("Введіть рівень прозорості (0-100, де 100 - непрозоре): "))
            if not (0 <= opacity_percent <= 100):
                print("Помилка: значення має бути від 0 до 100.")
                return

            # Перетворення відсотків у коефіцієнт (від 0.0 до 1.0)
            alpha_factor = opacity_percent / 100.0

            with Image.open(path) as img:
                img = img.convert("RGBA")
                r, g, b, alpha = img.split()
                alpha = alpha.point(lambda p: int(p * alpha_factor))    # Зміна значення прозорості кожного пікселя на коефіцієнт

                result_img = Image.merge("RGBA", (r, g, b, alpha))

                base_name, _ = os.path.splitext(path)
                new_path = f"{base_name}_transparent.png"
                result_img.save(new_path)
                print(f"Прозорість змінено, збережено як {new_path}")
        except Exception as e:
            print(f"Помилка при зміні прозорості: {e}")

    def crop_and_split(self):
        path = input("Уведіть назву зображення: ").strip().strip('"\'')

        print("Оберіть режим кадрування:")
        print("1 - Розбити зображення на сітку частин")
        print("2 - Вирізати конкретну область за координатами")
        choice = input("Ваш вибір (1-2): ").strip()

        try:
            with Image.open(path) as img:
                width, height = img.size
                base_name, ext = os.path.splitext(path)

                # Розбиття на частини
                if choice == '1':
                    rows = int(input("Введіть кількість рядків: "))
                    cols = int(input("Введіть кількість стовпчиків: "))

                    if rows <= 0 or cols <= 0:
                        print("Кількість частин має бути більше 0")
                        return

                    # Розрахунок ширини та висоти одного шматочка
                    part_w = width // cols
                    part_h = height // rows

                    # Поодинці вирізаємо та зберігаємо кожен фрагмент сітки
                    for r in range(rows):
                        for c in range(cols):
                            left = c * part_w
                            top = r * part_h
                            right = (c + 1) * part_w if c < cols - 1 else width
                            bottom = (r + 1) * part_h if r < rows - 1 else height

                            cropped = img.crop((left, top, right, bottom))
                            cropped.save(f"{base_name}_part_{r+1}x{c+1}{ext}")

                    print(f"Зображення розбито на {rows}x{cols} частин")

                # вирізання області по координатам
                elif choice == '2':
                    print(f"Оригінальний розмір зображення: {width}x{height} px")
                    
                    start_input = input("Введіть початкові координати (ліва x верхня, наприклад 0x0): ").strip()
                    end_input = input(f"Введіть кінцеві координати (права x нижня, наприклад {width}x{height}): ").strip()

                    start_tokens = start_input.replace(',', ' ').replace('x', ' ').replace('X', ' ').split()
                    end_tokens = end_input.replace(',', ' ').replace('x', ' ').replace('X', ' ').split()

                    if len(start_tokens) != 2 or len(end_tokens) != 2:
                        print("Координати мають бути у форматі XxY (наприклад, 100x100)")
                        return

                    left, top = int(start_tokens[0]), int(start_tokens[1])
                    right, bottom = int(end_tokens[0]), int(end_tokens[1])

                    # Перевірка правильності меж
                    if left >= right or top >= bottom or right > width or bottom > height or left < 0 or top < 0:
                        print("Невірні межі кадрування або координати виходять за рамки зображення.")
                        return

                    # Вирізання обраної ділянки
                    cropped = img.crop((left, top, right, bottom))
                    new_path = f"{base_name}_cropped{ext}"
                    cropped.save(new_path)
                    print(f"Область успішно вирізано та збережено як {new_path}")
                else:
                    print("Невірний вибір.")
        except ValueError:
            print("Введено некоректні числові координати")
        except Exception as e:
            print(f"Помилка при кадруванні: {e}")

    def enhance_contrast(self):
        path = input("Уведіть назву зображення: ").strip().strip('"\'')

        try:
            factor = float(input("Уведіть коефіцієнт контрастності (наприклад, 1.5 для збільшення на 50%): "))

            with Image.open(path) as img:
                if img.mode == 'RGBA':
                    img = img.convert('RGB')

                # Зміна контрасності
                enhancer = ImageEnhance.Contrast(img)
                result_img = enhancer.enhance(factor)

                base_name, ext = os.path.splitext(path)
                new_path = f"{base_name}_contrast{ext}"
                result_img.save(new_path)
                print(f"Контрастність скориговано, збережено як {new_path}")
        except Exception as e:
            print(f"Помилка при зміні контрастності: {e}")