import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


class Lab5:
    def kirsch_edge_detection(self, Y_matrix):
        """Реалізація виділення меж методом Кірша для 2D-матриці яскравості Y."""
        height, width = Y_matrix.shape
        output_matrix = np.zeros((height, width), dtype=np.uint8)

        Y = Y_matrix.astype(np.float32)

        for y in range(1, height - 1):
            for x in range(1, width - 1):
                # 8 пікселів навколо центрального
                A = [
                    Y[y - 1, x - 1],
                    Y[y - 1, x],
                    Y[y - 1, x + 1],
                    Y[y, x + 1],
                    Y[y + 1, x + 1],
                    Y[y + 1, x],
                    Y[y + 1, x - 1],
                    Y[y, x - 1],
                ]

                max_grad = 0.0

                # Обчислюємо S_i та T_i для 8 напрямків
                for i in range(8):
                    S_i = A[i] + A[(i + 1) % 8] + A[(i + 2) % 8]
                    T_i = (
                        A[(i + 3) % 8]
                        + A[(i + 4) % 8]
                        + A[(i + 5) % 8]
                        + A[(i + 6) % 8]
                        + A[(i + 7) % 8]
                    )

                    val = abs(5 * S_i - 3 * T_i)
                    if val > max_grad:
                        max_grad = val

                output_matrix[y, x] = min(255, int(max_grad))

        return output_matrix

    def process_image(self):
        path = (input("Уведіть назву зображення: ").strip().strip("\"'"))

        if not os.path.exists(path):
            print("Файл не знайдено.")
            return

        try:
            img = Image.open(path).convert("RGB")
            img_array = np.array(img)

            R = img_array[:, :, 0]
            G = img_array[:, :, 1]
            B = img_array[:, :, 2]

            Y = (0.299 * R + 0.587 * G + 0.114 * B).astype(np.uint8)

            print("Обробка зображення методом Кірша...")
            kirsch_edges = self.kirsch_edge_detection(Y)

            plt.figure(figsize=(10, 5))

            plt.subplot(1, 2, 1)
            plt.imshow(img)
            plt.title("Оригінальне зображення")
            plt.axis("off")

            plt.subplot(1, 2, 2)
            plt.imshow(kirsch_edges, cmap="gray")
            plt.title("Виділення меж (метод Кірша)")
            plt.axis("off")

            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"Помилка під час обробки: {e}")