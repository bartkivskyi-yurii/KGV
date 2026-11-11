import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import wiener
from scipy.ndimage import minimum_filter, maximum_filter

class Lab6:
    def __init__(self, input_image_path="input.jpg", save_dir="lab6_images"):
        self.save_dir = save_dir
        self.input_image_path = input_image_path
        self.images = self._generate_dataset()
        self.filtered_data, self.errors = self._calculate_all()

    def _load_base_image(self):
        """Зчитує вхідне зображення з ПК по назві файлу та перетворює у 128х128 в градаціях сірого."""
        if os.path.exists(self.input_image_path):
            img = cv2.imread(self.input_image_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                return cv2.resize(img, (128, 128))
        
        raise FileNotFoundError(
            f"Помилка: Файл '{self.input_image_path}' не знайдено в папці проекту! "
            f"Будь ласка, помістіть фото в папку або вкажіть точну назву."
        )

    def _generate_dataset(self):
        """Генерує 9 зашумлених зображень (f0-f8)"""
        os.makedirs(self.save_dir, exist_ok=True)
        f0 = self._load_base_image()
        
        imgs = {
            0: f0, # f0: Вхідне чисте зображення
            # f1, f2: Адитивний шум різної дисперсії (Гауссівський N(0, σ^2))
            1: np.clip(f0 + np.random.normal(0, 10, f0.shape), 0, 255).astype(np.uint8),
            2: np.clip(f0 + np.random.normal(0, 20, f0.shape), 0, 255).astype(np.uint8),
            # f3, f4: Імпульсний шум ("Сіль і перець") з ймовірністю p
            3: self._add_impulse(f0, 0.05),
            4: self._add_impulse(f0, 0.15),
            # f5, f6: Просторово-нестаціонарний адитивний шум, залежний від яскравості σ^2(I) = α*I
            5: self._add_bright_noise(f0, 50),
            6: self._add_bright_noise(f0, 100),
            # f7, f8: Просторово-нестаціонарний адитивний шум, залежний від координат σ^2(x, y)
            7: self._add_coord_noise(f0, 50),
            8: self._add_coord_noise(f0, 100),
        }
        
        for k, img in imgs.items():
            cv2.imwrite(os.path.join(self.save_dir, f"f{k}.bmp"), img)
        return imgs

    @staticmethod
    def _add_impulse(img, prob):
        """Імпульсний шум ('Сіль і перець')."""
        res = np.copy(img)
        rnd = np.random.rand(*img.shape)
        res[rnd < prob / 2] = 0        # Перець (чорні пікселі)
        res[rnd > 1 - prob / 2] = 255  # Сіль (білі пікселі)
        return res

    @staticmethod
    def _add_bright_noise(img, scale):
        """Просторово-нестаціонарний шум за рівнем яскравості пікселів."""
        noise = np.random.normal(0, 1, img.shape) * (img / 255.0) * scale
        return np.clip(img + noise, 0, 255).astype(np.uint8)

    @staticmethod
    def _add_coord_noise(img, scale):
        """Просторово-нестаціонарний шум за просторовими координатами."""
        rows, cols = img.shape
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))
        dist = np.sqrt((x - cols/2)**2 + (y - rows/2)**2) / (np.sqrt(cols**2 + rows**2)/2)
        noise = np.random.normal(0, 1, img.shape) * dist * scale
        return np.clip(img + noise, 0, 255).astype(np.uint8)

    def _apply_filters(self, img):
        # Адаптивний фільтр Вінера
        with np.errstate(divide='ignore', invalid='ignore'):
            wiener_raw = wiener(img.astype(np.float64), (3, 3))
            wiener_clean = np.nan_to_num(wiener_raw, nan=0.0)
            wiener_img = np.clip(wiener_clean, 0, 255).astype(np.uint8)

        min_f = minimum_filter(img, size=3).astype(np.float32)
        max_f = maximum_filter(img, size=3).astype(np.float32)
        midpoint_img = np.clip((min_f + max_f) / 2, 0, 255).astype(np.uint8)

        return {
            # Лінійні фільтри
            'Лінійний: Усереднювальний 3x3': cv2.blur(img, (3, 3)),
            'Лінійний: Усереднювальний 5x5': cv2.blur(img, (5, 5)),
            'Лінійний: Гаусса 3x3': cv2.GaussianBlur(img, (3, 3), 1.0),
            
            # Нелінійні та Адаптивні фільтри
            'Нелінійний: Медіанний 3x3': cv2.medianBlur(img, 3),
            'Нелінійний: Медіанний 5x5': cv2.medianBlur(img, 5),
            'Нелінійний: Білатеральний': cv2.bilateralFilter(img, 9, 75, 75),
            'Нелінійний: Мінімальний 3x3': minimum_filter(img, size=3),
            'Нелінійний: Максимальний 3x3': maximum_filter(img, size=3),
            'Нелінійний: Серединної точки 3x3': midpoint_img,
            'Адаптивний: Вінера 3x3': wiener_img
        }

    @staticmethod
    def _calc_mse(g, f):
        """Обчислення середньоквадратичної похибки (MSE)."""
        return float(np.mean(np.square(g.astype(np.float64) - f.astype(np.float64))))

    def _calculate_all(self):
        filtered, errors = {}, {}
        for k, img in self.images.items():
            f_res = self._apply_filters(img)
            filtered[k] = f_res
            errors[k] = {fname: self._calc_mse(res, img) for fname, res in f_res.items()}
        return filtered, errors

    # Вивід
    def show_all_test_images(self):
        titles = [
            "f0: Оригінал (без шуму)",
            "f1: Адитивний шум (σ^2=100)",
            "f2: Адитивний шум (σ^2=400)",
            "f3: Імпульсний шум (p=0.05)",
            "f4: Імпульсний шум (p=0.15)",
            "f5: Нестац. яскравість (s=50)",
            "f6: Нестац. яскравість (s=100)",
            "f7: Нестац. координати (s=50)",
            "f8: Нестац. координати (s=100)"
        ]
        fig, axes = plt.subplots(3, 3, figsize=(10, 10))
        fig.suptitle('Вхідний набір зображень (f0 - f8)', fontsize=14, fontweight='bold')
        for i, ax in enumerate(axes.flat):
            ax.imshow(self.images[i], cmap='gray', vmin=0, vmax=255)
            ax.set_title(titles[i], fontsize=8)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    def print_summary_table(self):
        """Форматований вивід таблиці ε^2_AO в консоль."""
        filter_names = list(self.errors[0].keys())
        print("\n" + "-"*125)
        print(" " * 42 + "Підсумкова таблиця похибок ε^2_AO")
        print("-"*125)
        header = f"{'Назва фільтра':<35} | " + " | ".join([f"f{k:<5}" for k in range(9)])
        print(header)
        print("-" * len(header))
        for fname in filter_names:
            row = [f"{self.errors[k][fname]:<7.2f}" for k in range(9)]
            print(f"{fname:<35} | " + " | ".join(row))
        print("-"*125 + "\n")

    def show_filtration_results(self, k: int):
        """Графічне порівняння відфільтрованих результатів для зображення fk."""
        f0 = self.images[0]
        fk = self.images[k]
        f_results = self.filtered_data[k]
        
        fig, axes = plt.subplots(3, 4, figsize=(15, 10))
        fig.suptitle(f"Результати фільтрації для зображення f{k}", fontsize=14, fontweight='bold')

        axes[0, 0].imshow(f0, cmap='gray', vmin=0, vmax=255)
        axes[0, 0].set_title("Еталон (f0)", fontweight='bold')
        axes[0, 0].axis('off')

        axes[0, 1].imshow(fk, cmap='gray', vmin=0, vmax=255)
        axes[0, 1].set_title(f"Оброблюване (f{k})", fontweight='bold')
        axes[0, 1].axis('off')

        indices = [(0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3)]
        for (fname, res_img), (r, c) in zip(f_results.items(), indices):
            err = self.errors[k][fname]
            axes[r, c].imshow(res_img, cmap='gray', vmin=0, vmax=255)
            axes[r, c].set_title(f"{fname}\nε^2 = {err:.2f}", fontsize=8)
            axes[r, c].axis('off')

        plt.tight_layout()
        plt.show()