import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

class Lab4:
    def process_image(self):
        path = input("Уведіть назву зображення: ").strip().strip('"\'')
        
        if not os.path.exists(path):
            print("Файл не знайдено.")
            return

        try:
            # 1. Завантаження первинного зображення
            img = Image.open(path).convert("RGB")
            img_array = np.array(img)
            
            # Розділення на канали R, G, B
            R = img_array[:, :, 0]
            G = img_array[:, :, 1]
            B = img_array[:, :, 2]

            # 2. Обчислення матриці значень яскравості
            Y = 0.299 * R + 0.587 * G + 0.114 * B
            Y = Y.astype(np.uint8)

            print(f"Матриця значень яскравості (роздільна здатність {Y.shape[1]}x{Y.shape[0]}):")
            print(Y)

            plt.figure(figsize=(12, 8))

            # Виведення оригіналу
            plt.subplot(2, 3, 1)
            plt.imshow(img)
            plt.title("Оригінальне зображення")
            plt.axis('off')

            # 3. Побудова гістограми кольорового зображення (RGB)
            plt.subplot(2, 3, 2)
            colors = ('red', 'green', 'blue')
            for i, col in enumerate(colors):
                hist, bins = np.histogram(img_array[:, :, i], bins=256, range=(0, 256))
                plt.plot(hist, color=col, alpha=0.7)
            plt.title("Гістограма RGB")
            plt.xlim([0, 256])

            # 4. Зміна кольоровості: Відтінки сірого
            gray_img = Image.fromarray(Y, mode='L')
            plt.subplot(2, 3, 4)
            plt.imshow(gray_img, cmap='gray')
            plt.title("Відтінки сірого")
            plt.axis('off')

            # 4. Зміна кольоровості: Бінаризація
            try:
                threshold = int(input("Уведіть поріг для бінаризації (0-255, зазвичай 127): "))
            except ValueError:
                threshold = 127
                
            binary_array = np.where(Y > threshold, 255, 0).astype(np.uint8)
            plt.subplot(2, 3, 5)
            plt.imshow(binary_array, cmap='gray')
            plt.title(f"Бінаризація (поріг {threshold})")
            plt.axis('off')

            # 4. Зміна кольоровості: Негатив
            negative_array = 255 - Y
            plt.subplot(2, 3, 6)
            plt.imshow(negative_array, cmap='gray')
            plt.title("Негатив")
            plt.axis('off')

            # 4. Побудова гістограми зображення в градаціях сірого
            plt.subplot(2, 3, 3)
            gray_hist, _ = np.histogram(Y, bins=256, range=(0, 256))
            plt.plot(gray_hist, color='black')
            plt.fill_between(range(256), gray_hist, color='gray', alpha=0.5)
            plt.title("Гістограма сірого")
            plt.xlim([0, 256])

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Помилка під час обробки зображення: {e}")