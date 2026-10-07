from Bartkivskyi_Lab1_KGV import Lab1
from Bartkivskyi_Lab2_KGV import Lab2
from Bartkivskyi_Lab3_KGV import Lab3

class Program:
    def __init__(self):
        self.lab1 = Lab1()
        self.lab2 = Lab2()
        self.lab3 = Lab3()

    def run_lab1(self):
        while True:
            print("\n Меню лаб1")
            print("1 - Конвертація форматів зображень")
            print("2 - Конвертація розміру зображень")
            print("3 - Перетворення кольорів (заміна кольору з допуском)")
            print("4 - Корекція колірного балансу")
            print("0 - Повернутися у головне меню")

            choice = input("Оберіть дію (0-4): ").strip()

            if choice == '1':
                self.lab1.convert_formats()
            elif choice == '2':
                self.lab1.resize_images()
            elif choice == '3':
                self.lab1.replace_color()
            elif choice == '4':
                self.lab1.color_balance()
            elif choice == '0':
                break
            else:
                print("Обирайте значення від 0 до 4")

    def run_lab2(self):
        while True:
            print("\nМеню лаб2")
            print("1 - Зміна прозорості зображення")
            print("2 - Кадрування / Розбиття на частини")
            print("3 - Збільшення контрастності")
            print("0 - Повернутися у головне меню")

            choice = input("Оберіть дію (0-3): ").strip()

            if choice == '1':
                self.lab2.change_transparency()
            elif choice == '2':
                self.lab2.crop_and_split()
            elif choice == '3':
                self.lab2.enhance_contrast()
            elif choice == '0':
                break
            else:
                print("Обирайте значення від 0 до 3")

    def run_lab3(self):
        while True:
            print("\nМеню лаб3")
            print("1 - Об\'єднання зображень")
            print("2 - Водяний знак")
            print("3 - Слайд-шоу")
            print("0 - Повернутися у головне меню")

            choice = input("Оберіть дію (0-3): ").strip()

            if choice == '1':
                self.lab3.pics_merge()
            elif choice == '2':
                self.lab3.watermark()
            elif choice == '3':
                self.lab3.slideshow()
            elif choice == '0':
                break
            else:
                print("Обирайте значення від 0 до 3")

    def run(self):
        while True:
            print("\n")
            print("Меню")
            print("")
            print("1 - Лабораторна робота №1")
            print("2 - Лабораторна робота №2")
            print("3 - Лабораторна робота №3")
            print("0 - Вихід з програми")

            choice = input("Оберіть пункт меню (0-2): ").strip()

            if choice == '1':
                self.run_lab1()
            elif choice == '2':
                self.run_lab2()
            elif choice == '3':
                self.run_lab3()
            elif choice == '0':
                print("Завершення роботи програми.")
                break
            else:
                print("Обирайте значення від 0 до 2")


if __name__ == "__main__":
    app = Program()
    app.run()