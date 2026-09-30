import os
import math
from PIL import Image, ImageEnhance


class Lab1:
    def convert_formats():
        paths_input = input("Уведіть назву зображень через кому (наприклад, image.jpg, image2.jpg): ")
        paths = [p.strip().strip('"\'') for p in paths_input.split(',')]

        target_format = input("Уведіть вихідний формат (Наприклад, png, jpeg, bmp): ").lower()
        save_dir = input("Уведіть шлях до папки для збереження (натисніть ENTER для поточної папки): ").strip().strip('"\'')

        if save_dir and not os.path.exists(save_dir):   # Якщо папку вказано і вона ще не існує у системі — програма створює її
            os.makedirs(save_dir)

        for path in paths:
            try:
                old_size = os.path.getsize(path)
                with Image.open(path) as img:   # Файл зображення відкривається, і автоматично закриється після виходу з блоку with
                    base_name = os.path.splitext(os.path.basename(path))[0] # З повного шляху витягується лише ім'я файлу без розширення
                    new_filename = f"{base_name}.{target_format}"
                    new_path = os.path.join(save_dir, new_filename) if save_dir else new_filename

                    if target_format in ['jpg', 'jpeg'] and img.mode == 'RGBA':
                        img = img.convert('RGB')    # Конвертація в RGB, бо jpg і jpeg не мають прозорості

                    img.save(new_path, format=target_format.upper())

                new_size = os.path.getsize(new_path)
                print(f"{base_name} збережено як {new_path}")
                print(f"  Розмір до: {old_size / 1024:.2f} KB | Розмір після: {new_size / 1024:.2f} KB")
            except Exception as e:
                print(f"Помилка при обробці {path}: {e}")

    def resize_images():
        paths_input = input("Введіть назву зображень через кому: ")
        paths = [p.strip().strip('"\'') for p in paths_input.split(',')]

        pixel_input = input("Уведіть кількість пікселів: ").strip()
    
        tokens = pixel_input.replace(',', ' ').replace('x', ' ').split()    # Введене значення очищається від ком та символу 'x', щоб виділити конкретне число

        if len(tokens) != 1:
            print("Потрібно уводити лише одне число.")
            return
        try:
            target_pixels = int(tokens[0])
            if target_pixels <= 0:
                print("Кількість пікселів має бути більше 0")
                return
        except ValueError:
            print("Уведене значення має бути цілим числом")
            return

        save_dir = input("Папка для збереження (натисніть Enter для поточної): ").strip().strip('"\'')
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for path in paths:
            try:
                with Image.open(path) as img:
                    orig_w, orig_h = img.size

                    # Визначається орієнтація (альбомна чи портретна) для правильного пропорційного зменшення
                    if orig_w >= orig_h:
                        w = target_pixels
                        h = int(orig_h * (target_pixels / orig_w))
                    else:
                        h = target_pixels
                        w = int(orig_w * (target_pixels / orig_h))
                    resized_img = img.resize((w, h), Image.Resampling.LANCZOS)  # використовується алгоритм LANCZOS для високої якості

                    base_name = os.path.splitext(os.path.basename(path))[0]
                    ext = os.path.splitext(path)[1]
                    new_path = os.path.join(save_dir, f"{base_name}_resized{ext}") if save_dir else f"{base_name}_resized{ext}"
                
                    resized_img.save(new_path)
                    print(f"{base_name} Успішно змінено з {orig_w}x{orig_h} px на {w}x{h} px")
            except Exception as e:
                print(f"Помилка при обробці {path}: {e}")

    def replace_colour():
        path = input("Уведіть назву зображення: ")

        print("Уведіть RGB колір, який потрібно замінити (Наприклад, 255 255 255): ")
        target_r, target_g, target_b = map(int, input().split())    # Рядок розбивається по пробілах, і кожен елемент перетворюється на ціле число
    
        print("Уведіть новий RGB колір (Наприклад, 0 0 0): ")
        new_r, new_g, new_b = map(int, input().split())

        tolerance = int(input("Уведіть похибку кольору (Наприклад, 30 для схожих відтінків, 0 для точного збігу): "))

        try:
            with Image.open(path) as img:
                img = img.convert("RGBA")   # Зображення переводиться у режим RGBA, щоб кожен піксель мав 4 значення
                data = img.getdata()    # Завантажується масив усіх пікселів зображення у пам'ять

                new_data = []
                for item in data:
                    # Вираховується математична відстань між кольором поточного пікселя та цільовим кольором (формула Евкліда в 3D просторі)
                    distance = math.sqrt((item[0] - target_r)**2 + (item[1] - target_g)**2 + (item[2] - target_b)**2)   

                    # Якщо піксель достатньо схожий на колір, який шукаємо (У межах похибки), тоді замінюємо його
                    if distance <= tolerance:
                        new_data.append((new_r, new_g, new_b, item[3]))    # item[3] це прозорість
                    else:
                        new_data.append(item)

                img.putdata(new_data)
                base_name, _ = os.path.splitext(path)
                new_path = f"{base_name}_color_replaced.png"
                img.save(new_path)
                print(f"Колір та його відтінки замінено, збережено як {new_path}")
        except Exception as e:
            print(f"Помилка: {e}")

    def color_balance():
        path = input("Уведіть назву зображення: ").strip().strip('"\'')

        print("Оберіть тип корекції:")
        print("1. Збільшити/зменшити Червоний (Red)")
        print("2. Збільшити/зменшити Зелений (Green)")
        print("3. Збільшити/зменшити Синій (Blue)")
        print("4. Загальна корекція яскравості")
        choice = input("Ваш вибір: ")

        factor = float(input("Уведіть коефіцієнт (Наприклад, 1.5 для збільшення на 50%, 0.8 для зменшення): "))
    
        try:
            with Image.open(path) as img:   # Якщо зображення не в RGB, воно примусово стає кольоровим
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Створюється об'єкт для зміни яскравості і застосовується коефіцієнт
                if choice == '4':
                    enhancer = ImageEnhance.Brightness(img)
                    result_img = enhancer.enhance(factor)
                elif choice in ['1', '2', '3']:
                    r, g, b = img.split()   # Зображення розщеплюється на 3 окремі картинки
                    if choice == '1':
                        r = r.point(lambda p: p * factor)
                    elif choice == '2':
                        g = g.point(lambda p: p * factor)
                    elif choice == '3':
                        b = b.point(lambda p: p * factor)
                    result_img = Image.merge('RGB', (r, g, b))  # Три канали зливаються назад в одне кольоре зображення RGB
                else:
                    print("Невірний вибір.")
                    return

                base_name, ext = os.path.splitext(path)
                new_path = f"{base_name}_balanced{ext}"
                result_img.save(new_path)
                print(f"Колірний баланс скориговано, збережено як {new_path}")
        except Exception as e:
            print(f"Помилка: {e}")