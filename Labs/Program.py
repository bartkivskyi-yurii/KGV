from Bartkivskyi_Lab1_KGV import Lab1
from Bartkivskyi_Lab2_KGV import Lab2
from Bartkivskyi_Lab3_KGV import Lab3
from Bartkivskyi_Lab4_KGV import Lab4
from Bartkivskyi_Lab5_KGV import Lab5
from Bartkivskyi_Lab6_KGV import Lab6

class Program:
    def __init__(self):
        self.lab1 = Lab1()
        self.lab2 = Lab2()
        self.lab3 = Lab3()
        self.lab4 = Lab4()
        self.lab5 = Lab5()
        self.lab6 = Lab6()

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

    def run_lab4(self):
        while True:
            print("\nЗавдання лаб4")
            print("1 - Виведення первиного зображення")
            print("2 - Виведення матриці значень яскравості зображення")
            print("3 - Побудова гістограми яскравості кольорового зображення")
            print("4 - Зміна кольоровості")
            print("0 - Повернутися у головне меню")

            choice = input("Щоб виконати завдання натисніть 1 або 0 для виходу: ").strip()

            if choice == '1':
                self.lab4.process_image()
            elif choice == '0':
                break
            else:
                print("Обирайте значення від 0 до 1")

    def run_lab5(self):
        while True:
            print("\nЗавдання лаб5")
            print("1 - Виділення меж: метод Кірша")
            print("0 - Повернутися у головне меню")

            choice = input("Щоб виконати завдання натисніть 1 або 0 для виходу: ").strip()

            if choice == '1':
                self.lab5.process_image()
            elif choice == '0':
                break
            else:
                print("Обирайте значення від 0 до 1")

    def run_lab6(self):
        while True:
            print("\nЗавдання лаб6")
            print("1 - Показати всі 9 початкових тестових зображень (f0-f8)")
            print("2 - Вивести підсумкову таблицю похибок ε²_AO")
            print("3 - Візуалізація фільтрації для обраного зображення (0-8)")
            print("0 - Повернутися у головне меню")

            choice = input("Оберіть дію (0-3): ").strip()

            if choice == '1':
                self.lab6.show_all_test_images()
            elif choice == '2':
                self.lab6.print_summary_table()
            elif choice == '3':
                num = input("Введіть номер зображення (0 - f0, 1 - f1, ..., 8 - f8): ").strip()
                if num.isdigit() and 0 <= int(num) <= 8:
                    self.lab6.show_filtration_results(int(num))
                else:
                    print("Уводьте число від 0 до 8")
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
            print("4 - Лабораторна робота №4")
            print("5 - Лабораторна робота №5")
            print("6 - Лабораторна робота №6")
            print("0 - Вихід з програми")

            choice = input("Оберіть пункт меню (0-6): ").strip()

            if choice == '1':
                self.run_lab1()
            elif choice == '2':
                self.run_lab2()
            elif choice == '3':
                self.run_lab3()
            elif choice == '4':
                self.run_lab4()
            elif choice == '5':
                self.run_lab5()
            elif choice == '6':
                self.run_lab6()
            elif choice == '0':
                print("Завершення роботи програми.")
                break
            else:
                print("Обирайте значення від 0 до 6")


if __name__ == "__main__":
    app = Program()
    app.run()