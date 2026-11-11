import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import wiener
from scipy.ndimage import minimum_filter, maximum_filter

class Lab6:
    def __init__(self, size=(128, 128), save_dir="lab6_images"):
        self.size = size
        self.save_dir = save_dir
        self.images = self._generate_dataset()
        self.filtered_data, self.errors = self._calculate_all()

    def _create_base_image(self):
        img = np.ones(self.size, dtype=np.uint8) * 127
        cv2.rectangle(img, (32, 32), (96, 96), 255, -1)
        cv2.circle(img, (64, 64), 22, 0, -1)
        return img

    def _generate_dataset(self):
        os.makedirs(self.save_dir, exist_ok=True)
        f0 = self._create_base_image()
        
        imgs = {
            0: f0,
            1: np.clip(f0 + np.random.normal(0, 10, f0.shape), 0, 255).astype(np.uint8),
            2: np.clip(f0 + np.random.normal(0, 20, f0.shape), 0, 255).astype(np.uint8),
            3: self._add_impulse(f0, 0.05),
            4: self._add_impulse(f0, 0.15),
            5: self._add_bright_noise(f0, 50),
            6: self._add_bright_noise(f0, 100),
            7: self._add_coord_noise(f0, 50),
            8: self._add_coord_noise(f0, 100),
        }
        for k, img in imgs.items():
            cv2.imwrite(os.path.join(self.save_dir, f"f{k}.bmp"), img)
        return imgs

    @staticmethod
    def _add_impulse(img, prob):
        res = np.copy(img)
        rnd = np.random.rand(*img.shape)
        res[rnd < prob / 2] = 0
        res[rnd > 1 - prob / 2] = 255
        return res

    @staticmethod
    def _add_bright_noise(img, scale):
        noise = np.random.normal(0, 1, img.shape) * (img / 255.0) * scale
        return np.clip(img + noise, 0, 255).astype(np.uint8)

    @staticmethod
    def _add_coord_noise(img, scale):
        rows, cols = img.shape
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))
        dist = np.sqrt((x - cols/2)**2 + (y - rows/2)**2) / (np.sqrt(cols**2 + rows**2)/2)
        noise = np.random.normal(0, 1, img.shape) * dist * scale
        return np.clip(img + noise, 0, 255).astype(np.uint8)

    def _apply_filters(self, img):
        with np.errstate(divide='ignore', invalid='ignore'):
            wiener_raw = wiener(img.astype(np.float64), (3, 3))
            wiener_clean = np.nan_to_num(wiener_raw, nan=0.0)
            wiener_img = np.clip(wiener_clean, 0, 255).astype(np.uint8)

        return {
            'Linear: Mean 3x3': cv2.blur(img, (3, 3)),
            'Linear: Mean 5x5': cv2.blur(img, (5, 5)),
            'Linear: Gaussian 3x3': cv2.GaussianBlur(img, (3, 3), 1.0),
            'Non-linear: Median 3x3': cv2.medianBlur(img, 3),
            'Non-linear: Median 5x5': cv2.medianBlur(img, 5),
            'Non-linear: Bilateral': cv2.bilateralFilter(img, 9, 75, 75),
            'Non-linear: Min 3x3': minimum_filter(img, size=3),
            'Non-linear: Max 3x3': maximum_filter(img, size=3),
            'Non-linear: Midpoint 3x3': np.clip(
                (minimum_filter(img, size=3).astype(np.float32) + 
                 maximum_filter(img, size=3).astype(np.float32)) / 2, 0, 255
            ).astype(np.uint8),
            'Non-linear: Wiener 3x3': wiener_img
        }

    @staticmethod
    def _calc_mse(g, f):
        return float(np.mean(np.square(g.astype(np.float64) - f.astype(np.float64))))

    def _calculate_all(self):
        filtered, errors = {}, {}
        for k, img in self.images.items():
            f_res = self._apply_filters(img)
            filtered[k] = f_res
            errors[k] = {fname: self._calc_mse(res, img) for fname, res in f_res.items()}
        return filtered, errors


    def show_all_test_images(self):
        """Відображення сітки 3х3 зі всіма зображеннями f0-f8"""
        titles = ["f0: Чисте", "f1: Адит. 1", "f2: Адит. 2", "f3: Імп. 1", "f4: Імп. 2", 
                  "f5: Нестац. яскр. 1", "f6: Нестац. яскр. 2", "f7: Нестац. коорд. 1", "f8: Нестац. коорд. 2"]
        fig, axes = plt.subplots(3, 3, figsize=(9, 9))
        fig.suptitle('Вхідний набір тестових зображень (f0 - f8)', fontsize=14)
        for i, ax in enumerate(axes.flat):
            ax.imshow(self.images[i], cmap='gray', vmin=0, vmax=255)
            ax.set_title(titles[i], fontsize=9)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    def print_summary_table(self):
        """Вивід підсумкової таблиці в консоль"""
        filter_names = list(self.errors[0].keys())
        print("\n" + "="*110)
        print(" " * 35 + "Підсумкова таблиця похибок ε²_AO")
        print("="*110)
        header = f"{'Назва фільтра':<25} | " + " | ".join([f"f{k:<5}" for k in range(9)])
        print(header)
        print("-" * len(header))
        for fname in filter_names:
            row = [f"{self.errors[k][fname]:<7.2f}" for k in range(9)]
            print(f"{fname:<25} | " + " | ".join(row))
        print("="*110 + "\n")

    def show_filtration_results(self, k: int):
        """Візуалізація фільтрації для конкретного зображення fk"""
        f0 = self.images[0]
        fk = self.images[k]
        f_results = self.filtered_data[k]
        
        fig, axes = plt.subplots(3, 4, figsize=(14, 10))
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
            axes[r, c].set_title(f"{fname}\nε² = {err:.2f}", fontsize=8)
            axes[r, c].axis('off')

        plt.tight_layout()
        plt.show()