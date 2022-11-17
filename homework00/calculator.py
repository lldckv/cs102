import typing as tp
from math import cos, log, log10, sin, tan


def check(string: str):
    if string.isalnum() or len(string) < 5 or string.count("(") != string.count(")"):
        return False
    return True


def match_case_calc_1(num: float, command: str):
    match command:
        case "sin":
            return sin(num)
        case "tan":
            return tan(num)
        case "cos":
            return cos(num)
        case "ln":
            if num > 0:
                return log(num)
            return f"Некорректный ввод аргумента: {num!r}."
        case "lg":
            if num > 0:
                return log10(num)
            return f"Некорректный ввод аргумента: {num!r}."
        case _:
            return f"Неизвестный оператор: {command!r}."


def match_case_calc_2(num_1: float, num_2: float, command: str) -> tp.Union[float, str]:  # type: ignore
    match command:
        case "/":
            if num_2 != 0:
                return num_1 / num_2
            return "Невозможно поделить на ноль"
        case "-":
            return num_1 - num_2
        case "+":
            return num_1 + num_2
        case "*":
            return num_1 * num_2
        case "**":
            return pow(num_1, num_2)
        case "to" if 1 < num_2 < 10 and num_1 >= 0:
            return change(int(num_1), int(num_2))
        case _:
            return f"Неизвестный оператор: {command!r}."


def change(num1: int, num2: int):
    result = ""
    while num1:
        result = result + str(num1 % num2)
        num1 = num1 // num2
    result = result[::-1]
    if result:
        return int(result)
    return 0


T = True
while T:
    print("Выберите тип операции:\nСправка : 0")
    print("Двуместная : 1\nОдноместная : 2\nВыход : 3")
    c = input("\n")
    while c != "3":
        match c:
            case "1":
                print("Выберите тип операции:\nОдно действие : 0")
                print("Отмена : 1\n")
                c2 = input("\n")
                match c2:
                    case "0":
                        string = input("Введите выражение: символы через пробел + Enter: ")
                        if check(string):
                            n1, d, n2 = string.split(" ")
                            try:
                                if not (n1.isalnum() or n2.isalnum()):
                                    print(string, "=", match_case_calc_2(float(n1), float(n2), d), "\n")
                                    T = False
                                else:
                                    print(f"Некорректный ввод: {string!r}.")
                            except ValueError:
                                print(f"Некорректный ввод: {string!r}.")
                        else:
                            print(f"Некорректный ввод: {string!r}.")
                    case "1":
                        pass
                    case _:
                        print(f"Неизвестный оператор: {c2!r}.")
            case "2":
                print("Выберите тип операции:\nОдно действие : 0")
                print("Отмена : 1\n")
                c1 = input("\n")
                match c1:
                    case "0":
                        string = input("Введите выражение + Enter: ")
                        if check(string):
                            d, n1 = string.split("(")
                            d = d.strip(")")
                            n1 = n1.strip(")")
                            print(string, "=", match_case_calc_1(float(n1), d), "\n")
                            T = False
                        else:
                            print(f"Некорректный ввод: {string!r}.")
                    case "1":
                        pass
                    case _:
                        print(f"Неизвестный оператор: {c1!r}.")
            case "0":
                print("Калькулятор поддерживает : ", "\n")
                print(
                    "Двуместные операции : ",
                    "Сложение, ввод: a + b",
                    "Вычитание, ввод: a - b",
                    "Деление, ввод: a / b",
                    "Умножение, ввод: a * b",
                    "Возведение в степень, ввод: a ** b",
                    "Перевод десятичного числа в систему счисления, ввод: a to b",
                    sep=("\n"),
                )
                print("\n")
                print(
                    "Одноместные операции :\n Вычисление синуса, ввод: sin(a),\n "
                    "Вычисление косинуса, ввод: cos(a),\nВычисление тангенса, ввод: tan(a),"
                    "\nНатуральный логарифм, ввод: ln(a),\nДесятичный логарифм, ввод: lg(a)\n"
                )
                print("\n")
            case "3":
                break
            case _:
                print(f"Неизвестный оператор: {c!r}.")
        print("Выберите тип операции:\nСправка : 0")
        print("Двуместная : 1\nОдноместная : 2\nВыход : 3")
        c = input("\n")
