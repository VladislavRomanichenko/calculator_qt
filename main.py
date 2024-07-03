import sys
from typing import Union, Optional
from operator import add, sub, mul, truediv, mod
from PySide6.QtWidgets import QApplication, QMainWindow
from design import Ui_MainWindow

ERROR_ZERO_DIV = 'Division by zero'
ERROR_UNDEFINED = 'Result is undefined'

DEFAULT_FONT_SIZE = 16
DEFAULT_ENTRY_FONT_SIZE = 40

BUTTONS_TO_DISABLE = [
    'btn_calc', 'btn_plus', 'btn_sub',
    'btn_mul', 'btn_div', 'btn_neg',
    'btn_point', 'btn_div_x', 'btn_moddiv',
    'btn_sqare', 'btn_sqrt'
]

operations = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '%': mod,
}

class Calculator(QMainWindow):
    def __init__(self):
        super(Calculator, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.entry_max_len = self.ui.le_entry.maxLength()

        #Digits
        self.ui.btn_0.clicked.connect(lambda: self.add_digit('0'))
        self.ui.btn_1.clicked.connect(lambda: self.add_digit('1'))
        self.ui.btn_2.clicked.connect(lambda: self.add_digit('2'))
        self.ui.btn_3.clicked.connect(lambda: self.add_digit('3'))
        self.ui.btn_4.clicked.connect(lambda: self.add_digit('4'))
        self.ui.btn_5.clicked.connect(lambda: self.add_digit('5'))
        self.ui.btn_6.clicked.connect(lambda: self.add_digit('6'))
        self.ui.btn_7.clicked.connect(lambda: self.add_digit('7'))
        self.ui.btn_8.clicked.connect(lambda: self.add_digit('8'))
        self.ui.btn_9.clicked.connect(lambda: self.add_digit('9'))

        #Action button
        self.ui.btn_clear.clicked.connect(self.clear_all)
        self.ui.btn_ce.clicked.connect(self.clear_entry)
        self.ui.btn_point.clicked.connect(self.add_point)
        self.ui.btn_sub.clicked.connect(self.negate)
        self.ui.btn_backspace.clicked.connect(self.backspace)

        #Math operation
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_plus.clicked.connect(lambda: self.math_operation('+'))
        self.ui.btn_div.clicked.connect(lambda: self.math_operation('/'))
        self.ui.btn_neg.clicked.connect(lambda: self.math_operation('-'))
        self.ui.btn_mul.clicked.connect(lambda: self.math_operation('*'))
        self.ui.btn_moddiv.clicked.connect(lambda: self.math_operation('%'))
        self.ui.btn_div_x.clicked.connect(self.div_x)
        self.ui.btn_sqare.clicked.connect(self.sqare)
        self.ui.btn_sqrt.clicked.connect(self.sqrt)

    def add_digit(self, btn_text: str) -> None:
        self.remove_error()
        # Если в поле ноль, то заменяем нажатой цифрой, иначе добавляем нажатую цифру к строке
        self.clear_temp_equal()
        if self.ui.le_entry.text() == '0':
            self.ui.le_entry.setText(btn_text)
            self.adjust_entry_font_size()
        else:
            self.ui.le_entry.setText(self.ui.le_entry.text() + btn_text)
            self.adjust_entry_font_size()

    def add_point(self) ->None:
        self.clear_temp_equal()
        #Если в поле ввода нету точки, то добавляем её
        if "." not in self.ui.le_entry.text():
            self.ui.le_entry.setText(self.ui.le_entry.text() + '.')
            self.adjust_entry_font_size()

    def negate(self):
        self.clear_temp_equal()
        entry = self.ui.le_entry.text()
        if '-' not in entry:
            if entry != 0:
                entry = '-' + entry
        else:
            entry = entry[1:]

        if len(entry) == self.entry_max_len + 1 and '-' in entry:
            self.ui.le_entry.setMaxLength(self.entry_max_len + 1)
        else:
            self.ui.le_entry.setMaxLength(self.entry_max_len)

        self.ui.le_entry.setText(entry)
        self.adjust_entry_font_size()

    def backspace(self) -> None:
        self.remove_error()
        self.clear_temp_equal()
        #Обработка нажатия backspace с обычными числами и с негативными
        entry = self.ui.le_entry.text()
        if len(entry) != 1:
            if len(entry) == 2 and '-' in entry:
                self.ui.le_entry.setText('0')
            else:
                self.ui.le_entry.setText(entry[:-1])
        else:
            self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()

    def clear_temp_equal(self) -> None:
        if self.get_sign() == '=':
            self.ui.lbl_temp.clear()

    @staticmethod
    def remove_zeros(num: str) -> str:
        n = str(float(num))
        return n[:-2] if n[-2:] == '.0' else n

    def add_temp(self, math_sign: str):
        if not self.ui.lbl_temp.text() or self.get_sign() == '=':
            self.ui.lbl_temp.setText(self.remove_zeros(self.ui.le_entry.text()) + f' {math_sign} ')
            self.clear_entry()

    def get_entry_num(self) -> Union[int, float]:
        #Получаем число и поля ввода
        entry = self.ui.le_entry.text().strip('.')
        return float(entry) if '.' in entry else int(entry)

    def get_temp_num(self) -> Union[int, float, None]:
        #Получаем число из временного поля
        temp = self.ui.lbl_temp.text().strip('.').split()[0]
        return float(temp) if '.' in temp else int(temp)

    def get_sign(self) -> Optional[str]:
        #Получаем знак из временного поля
        if self.ui.lbl_temp.text():
            return self.ui.lbl_temp.text().strip('.').split()[-1]

    def sqare(self):
        #Возведение в квадрат поля ввода
        if self.ui.le_entry.text() != 0:
            result = self.remove_zeros(self.get_entry_num() ** 2)
            self.ui.le_entry.setText(result)
            self.adjust_entry_font_size()

    def sqrt(self):
        #Квадратный корень поля ввода
        if self.ui.le_entry.text() != 0:
            result = self.remove_zeros(self.get_entry_num() ** 0.5)
            self.ui.le_entry.setText(result)
            self.adjust_entry_font_size()

    def div_x(self):
        #Деление единицы на число из нашего поля ввода
        if self.ui.le_entry.text() != 0:
            self.ui.le_entry.setText(self.remove_zeros(1 / self.get_entry_num()))
            self.adjust_entry_font_size()

    def calculate(self):
        entry = self.ui.le_entry.text()
        temp = self.ui.lbl_temp.text()
        sign = self.get_sign()

        if temp:
            try:
                result = self.remove_zeros(str(operations[self.get_sign()](self.get_temp_num(), self.get_entry_num())))
                self.ui.lbl_temp.setText(temp + self.remove_zeros(entry) + " =")
                self.ui.le_entry.setText(result)
                self.adjust_entry_font_size()
                return result
            except KeyError:
                pass
            except ZeroDivisionError:
                if self.get_temp_num() == 0:
                    self.show_error(ERROR_UNDEFINED)
                else:
                    self.show_error(ERROR_ZERO_DIV)

    def math_operation(self, math_sign: str):
        temp = self.ui.lbl_temp.text()

        try:
            if not temp:
                self.add_temp(math_sign)
            else:
                if self.get_sign() != math_sign:
                    if self.get_sign() == '=':
                        self.add_temp(math_sign)
                    else:
                        self.ui.lbl_temp.setText(temp[:-2] + f' {math_sign} ')
                else:
                    self.ui.lbl_temp.setText(self.calculate() + f' {math_sign} ')
        except TypeError:
            pass
        self.adjust_entry_font_size()

    def clear_all(self) -> None:
        #Полная очистка(поле ввода и временное выражение)
        self.remove_error()
        self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()
        self.ui.lbl_temp.clear()

    def clear_entry(self) -> None:
        #Очистка, не трогая поле временного выражения
        self.remove_error()
        self.clear_temp_equal()
        self.ui.le_entry.setText('0')
        self.adjust_entry_font_size()

    def disable_buttons(self, disable: bool) -> None:
        for btn in BUTTONS_TO_DISABLE:
            getattr(self.ui, btn).setDisabled(disable)

        color = 'color: #888;' if disable else 'color: white;'
        self.change_buttons_color(color)

    def change_buttons_color(self, css_color: str) -> None:
        for btn in BUTTONS_TO_DISABLE:
            getattr(self.ui, btn).setStyleSheet(css_color)

    def show_error(self, text: str) -> None:
        self.ui.le_entry.setMaxLength(len(text))
        self.ui.le_entry.setText(text)
        self.adjust_entry_font_size()
        self.disable_buttons(True)

    def remove_error(self) -> None:
        if self.ui.le_entry.text() in (ERROR_UNDEFINED, ERROR_ZERO_DIV):
            self.ui.le_entry.setMaxLength(self.entry_max_len)
            self.ui.le_entry.setText('0')
            self.adjust_entry_font_size()
            self.disable_buttons(False)

    def get_entry_text_width(self) -> int:
        return self.ui.le_entry.fontMetrics().boundingRect(self.ui.le_entry.text()).width()

    def get_temp_text_width(self) -> int:
        return self.ui.lbl_temp.fontMetrics().boundingRect(self.ui.lbl_temp.text()).width()

    def adjust_entry_font_size(self) -> None:
        font_size = DEFAULT_ENTRY_FONT_SIZE
        while self.get_entry_text_width() > self.ui.le_entry.width() - 15:
            font_size -= 1
            self.ui.le_entry.setStyleSheet(f'font-size: {font_size}pt; border: none;')

        font_size = 1
        while self.get_entry_text_width() < self.ui.le_entry.width() - 60:
            font_size += 1

            if font_size > DEFAULT_ENTRY_FONT_SIZE:
                break

            self.ui.le_entry.setStyleSheet(f'font-size: {font_size}pt; border: none;')


    def adjust_temp_font_size(self) -> None:
        font_size = DEFAULT_FONT_SIZE
        while self.get_temp_text_width() > self.ui.lbl_temp.width() - 10:
            font_size -= 1
            self.ui.lbl_temp.setStyleSheet(f'font-size: {font_size}pt; color: #888;')

        font_size = 1
        while self.get_temp_text_width() < self.ui.lbl_temp.width() - 60:
            font_size += 1

            if font_size > DEFAULT_FONT_SIZE:
                break

            self.ui.lbl_temp.setStyleSheet(f'font-size: {font_size}pt; color: #888;')

    def resizeEvent(self, event) -> None:
        self.adjust_entry_font_size()
        self.adjust_temp_font_size()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())