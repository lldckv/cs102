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


def match_case_calc_2(num_1: float, num_2: float, command: str)\
        -> tp.Union[float, str]:  # type: ignore
    match command:
        case "/" if num_2 != 0:
            return num_1 / num_2
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
    print("Выберите тип операции:", "Справка : 0",
          "Двуместная : 1", "Одноместная : 2", "Выход : 3", sep=("\n"))
    c = input("\n")
    match c:
        case "1":
            print("Выберите тип операции:", "Одно действие : 0",
                  "Более одного действия : 1", sep=("\n"))
            c2 = input("\n")
            match c2:
                case "0":
                    string = input("Введите выражение:"
                                   " символы через пробел, затем нажмите Enter: ")
                    if check(string):
                        n1, d, n2 = string.split(" ")
                        print(string, "=", match_case_calc_2(float(n1), float(n2), d))
                        T = False
                    else:
                        print(f"Некорректный ввод: {string!r}.")
                case "1":
                    pass
                case _:
                    pass
        case "2":
            print("Выберите тип операции:", "Одно действие : 0",
                  "Более одного действия : 1", sep=("\n"))
            c1 = input("\n")
            match c1:
                case "0":
                    string = input("Введите выражение, затем нажмите Enter: ")
                    if check(string):
                        d, n1 = string.split("(")
                        d = d.strip(")")
                        n1 = n1.strip(")")
                        print(string, "=", match_case_calc_1(float(n1), d))
                        T = False
                    else:
                        print(f"Некорректный ввод: {string!r}.")
                case "1":
                    pass
                case _:
                    pass
        case "0":
            print("Калькулятор поддерживает : ", "\n")
            print(
                "Двуместные операции : ",
                "Сложение, ввод: a + b",
                "Вычитание, ввод: a - b",
                "Деление, ввод: a / b",
                "Умножение, ввод: a * b",
                "Возведение в степень, ввод: a ** b",
                "Перевод десятичного числа в систему счисления"
                " с основанием [2,9], ввод: a to b",
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
