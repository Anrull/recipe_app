# подключаем библиотеку для считывания из БД
import sqlite3
# подключаем систему к программе
import sys

# импорт из библиотеки PyQt5 метод для поключения ui файла
from PyQt5 import uic, QtWidgets
# импортируем виджеты
from PyQt5.QtWidgets import *
# для обработки нажатий клавиши
from PyQt5.QtCore import Qt
# Для вывода изображений
from PyQt5.QtGui import QPixmap
# Для вывода БД
from PyQt5.QtSql import *
# для парсинга изображений
import requests
from bs4 import BeautifulSoup

global_background = "Системный"


class AutorisationDialog(QDialog):
    def __init__(self):
        """
        Происходит инициация диалогового окна, которое предназначено для выбора режима
        """
        super().__init__()

        self.show_for_table = None
        self.for_new_elem = None
        self.castom = None
        self.infor = None
        self.MainFile = None
        self.MainApp = None

        uic.loadUi('for_ui/dialog1.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.setFixedSize(228, 303)

        self.initUi()

    def initUi(self):
        """
        Основная функция для подключения функций
        """
        self.setWindowTitle('Меню выбора')
        self.customization.setFlat(True)
        self.information.setFlat(True)

        self.pushButton_app.clicked.connect(self.app)
        self.pushButton_file.clicked.connect(self.file)
        self.pushButton_change.clicked.connect(self.change)
        self.pushButton_show.clicked.connect(self.showw)
        self.information.clicked.connect(self.info)
        self.customization.clicked.connect(self.setting)

    def app(self):
        """
        Открытие приложения для работы внутри него
        """
        self.hide()
        self.MainApp = MainWindowApplication()
        self.MainApp.show()

    def file(self):
        """
        Открытие приложения для работы через файлы
        """
        self.hide()
        self.MainFile = MainWindowForFile()
        self.MainFile.show()

    def info(self):
        self.hide()
        self.infor = Information()
        self.infor.show()

    def setting(self):
        self.hide()
        self.castom = Customization()
        self.castom.show()

    def change(self):
        self.hide()
        self.for_new_elem = AddDateBase()
        self.for_new_elem.show()

    def showw(self):
        self.hide()
        self.show_for_table = ShowMenu()
        self.show_for_table.show()


class MainWindowApplication(QMainWindow):
    """
    Основное окно приложения
    """

    def __init__(self):
        """
        Инициализация
        """
        super().__init__()

        self.pixmap = None
        self.autorisation = None
        self.name_for_db = None

        uic.loadUi('for_ui/main1.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#MainWindow{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#MainWindow{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#MainWindow{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#MainWindow{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#MainWindow{border-image:url("
                               "for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp.jpg)}")

        self.setFixedSize(374, 600)

        self.initUi()

    def initUi(self):
        """
        Основная настройка приложения
        """
        self.setWindowTitle('Блюда и рецепты')
        self.setGeometry(0, 0, 374, 600)

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.app_result_text.hide()
        self.label_for_image.hide()

        self.ok_button.clicked.connect(self.OK_button)
        self.delete_button.clicked.connect(self.DELETE_button)
        self.app_result.clicked.connect(self.for_db)
        self.escape.clicked.connect(self.esc)

    def OK_button(self):
        """
        Сохранение line_name при нажатии на кнопку ok
        """
        self.name_for_db = self.line_name.text()

    def DELETE_button(self):
        """
        Удаление текста со строки line_name
        """
        self.line_name.setText("")
        self.label_for_image.hide()
        self.app_result_text.hide()

    def for_db(self):
        """
        Импортирование из базы данных, а так-же вывод внутри приложения рецепта.
        """
        con = sqlite3.connect("for_db/components_ru.db")
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("""SELECT * FROM id
                             WHERE name = ?""",
                             (self.name_for_db,)).fetchall()
        # закрываем БД для экономии памяти и не перегружания его открытыми БД
        con.close()

        if not result:
            # сообщаем пользователю если не нашлось ничего по его запросу
            self.statusBar().showMessage('Ничего не нашлось')
        else:
            # сообщаем пользователю о том, что все нормально работает
            self.statusBar().showMessage(f"Нашлась запись с именем: {self.name_for_db}")

            # показываем поле для вывода текста
            self.app_result_text.show()
            # обнуляем запрос
            self.app_result_text.setPlainText(f"")

            # создание нового списка
            new_result = []

            # распаковка старого, неудобного списка
            for i in result:
                for j in i:
                    new_result.append(j)

            # выводим результат
            self.app_result_text.setPlainText(f"Номер блюда: {new_result[0]}\n"
                                              f"Название: {new_result[1]}\n"
                                              f"Количество компонентов: {new_result[2]}\n"
                                              f"Компоненты:")

            # выводим компоненты блюда
            for i in new_result[3].split(", "):
                self.app_result_text.append(f"                      ●{i.capitalize()}")

            # выводим время, требуемое для приготовления блюда
            self.app_result_text.append(f"Время, нужное на приготовление блюда: {new_result[4]}")

            self.label_for_image.show()

            def get_url():
                """
                Парсер изображения блюда по названию через интернет с помощью библиотеки bs4
                """
                name_for_parsing = new_result[1] + " картинка блюда"

                url = 'https://www.google.com/search?q={0}&tbm=isch'.format(name_for_parsing)
                content = requests.get(url).content
                soup = BeautifulSoup(content, features="html5lib")
                images = soup.findAll('img')

                for image in images[1: 2]:
                    print(image.get('src'))

                url = [image.get("src") for image in images][1]

                return requests.get(url)

            def show_image(response):
                """
                Для вывода изображения
                """
                if response.status_code == 200:
                    with open("for_time_image/image.jpg", "wb") as f:
                        f.write(response.content)
                    print("Изображение успешно сохранено.")

                    self.pixmap = QPixmap('for_time_image/image.jpg')

                    self.label_for_image.resize(331, 111)

                    self.label_for_image.setPixmap(self.pixmap)
                else:
                    print("Не удалось загрузить изображение. Код статуса:", response.status_code)

            # получаем адрес на изображение, а затем сохраняем его в папку, откуда потом выводим изображение
            show_image(get_url())

    def esc(self):
        """
        Назад, на экран выбора
        """
        self.autorisation = AutorisationDialog()
        self.autorisation.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.autorisation = AutorisationDialog()
            self.autorisation.show()
            self.hide()


class MainWindowForFile(QMainWindow):
    def __init__(self):
        """
        Инициализация
        """
        super().__init__()

        self.autorisation = None
        self.rule = None
        self.read_file_name = None

        uic.loadUi('for_ui/main2.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#MainWindow{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#MainWindow{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#MainWindow{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#MainWindow{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#MainWindow{border-image:url("
                               "for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp.jpg)}")

        self.setFixedSize(353, 303)

        self.initUi()

    def initUi(self):
        self.setWindowTitle('Блюда и рецепты edit file')

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # ⟱ (270, 60) 71 51
        # ⟰ (270, 120) 71 51
        self.button_fdf.clicked.connect(self.for_read_file)
        self.button_fwf.clicked.connect(self.for_write_file)
        self.rules_btn.clicked.connect(self.rules)
        self.escape.clicked.connect(self.esc)

    def for_read_file(self):
        """
        Считывание с файла название блюда
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt)", options=options)
        # сообщаем пользователю о находке, параллельно созраняя название блюда
        if fileName:
            self.statusBar().showMessage(f"Нашлась запись с именем: {fileName}")
            with open(fileName, "r", encoding="UTF-8") as read_file:
                read_f = read_file.readlines()
                self.read_file_name = None
                for i in read_f:
                    self.read_file_name = i
        else:
            # если ничего не нашлось
            self.statusBar().showMessage('Ничего не нашлось')

    def for_write_file(self):
        """
        Запись в файл
        """
        # поиск пользователя в проводнике файла
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # есть возможность добавить только txt файл
        NewfileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                     "All Files (*.txt)", options=options)
        # если нашелся файл
        if NewfileName:
            self.statusBar().showMessage(f"Нашлась запись с именем: {NewfileName}")

            # подключение БД
            con = sqlite3.connect("for_db/components_ru.db")
            cur = con.cursor()
            # Получили результат запроса, который ввели в текстовое поле

            result = cur.execute("""SELECT * FROM id
                                    WHERE name = ?""",
                                 (self.read_file_name,)).fetchall()

            # закрываем БД
            con.close()

            # если пользователь не нашел файл
            if not result:
                self.statusBar().showMessage('Ничего не нашлось')
            else:
                self.statusBar().showMessage(f"Нашлась запись с именем: {self.read_file_name}")

                # создание нового списка
                new_result = []

                # Смотри выше
                for i in result:
                    for j in i:
                        new_result.append(j)

                def get_url():
                    """
                    Парсер изображения блюда по названию через интернет с помощью библиотеки bs4
                    """
                    name_for_parsing = new_result[1] + " картинка блюда"

                    url = 'https://www.google.com/search?q={0}&tbm=isch'.format(name_for_parsing)
                    content = requests.get(url).content
                    soup = BeautifulSoup(content, features="html5lib")
                    images = soup.findAll('img')

                    for image in images[1: 2]:
                        print(image.get('src'))

                    url1 = [image.get("src") for image in images][1]

                    return url1

                # получаем адрес на изображение, а затем сохраняем его в папку, откуда потом выводим изображение
                url = get_url()

                # записываем в файл
                with open(NewfileName, "w", encoding="UTF-8") as write_file:
                    write_file.write(f"Изображение можно посмотреть по ссылке:\n{url}\n")
                    write_file.write(f"Номер блюда: {new_result[0]}\n")
                    write_file.write(f"Название: {new_result[1]}\n")
                    write_file.write(f"Количество компонентов: {new_result[2]}\n")
                    write_file.write(f"Компоненты:\n")

                    for i in new_result[3].split(", "):
                        write_file.write(f"                      ●{i.capitalize()}\n")

                    write_file.write(f"Время, нужное на приготовление блюда: {new_result[4]}")
        else:
            # если ничего не нашлось
            self.statusBar().showMessage('Ничего не нашлось')

    def rules(self):
        """
        Открывает пользователю диалоговое окно с правилами
        """
        self.rule = Rules()
        self.rule.show()
        self.hide()

    def esc(self):
        """
        Возвращение к истокам
        """
        self.hide()
        self.autorisation = AutorisationDialog()
        self.autorisation.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Возвращение к истокам
            """
            self.hide()
            self.autorisation = AutorisationDialog()
            self.autorisation.show()


class Rules(QDialog):
    def __init__(self):
        """
        Класс для показа диалогового окна с правилами
        """
        super().__init__()
        self.main_file = None
        uic.loadUi('for_ui/dialog2.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.setFixedSize(400, 280)

        self.initUi()

    def initUi(self):
        self.setWindowTitle('Правила')

        self.textEdit.setText("Для нормального функционирования"
                              "программы требуется правильно вводить файл.\n"
                              "Он должен иметь вид одной"
                              "текстовой строки содержащей только название блюда.")
        self.warning_ok.clicked.connect(self.rules_ok)

    def rules_ok(self):
        """
        Возвращаемся к истокам https://tsitaty.ru/images/dobro-pozhalovat-v-nash-dermovyij-mir-obratno.jpg
        """
        self.main_file = MainWindowForFile()
        self.main_file.show()
        self.hide()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_O:
            """
            Возвращаемся к истокам
            """
            self.main_file = MainWindowForFile()
            self.main_file.show()
            self.hide()

        if event.key() == Qt.Key_Escape:
            """
            Возвращаемся к истокам
            """
            self.main_file = MainWindowForFile()
            self.main_file.show()
            self.hide()


class Information(QDialog):
    def __init__(self):
        """
        Инициализация класса информирующего пользователя о приложении
        """
        super().__init__()

        self.autorisation = None
        uic.loadUi('for_ui/dialog3.ui', self)

        self.setFixedSize(400, 300)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.initUi()

    def initUi(self):
        self.setWindowTitle('Информация')

        self.textEdit.setText(f"Это приложение предназначено для быстрого поиска рецептов "
                              f"по названию. Оно выводит информацию по блюду, такую как позиция в списке блюд, "
                              f"название самого блюда, кол-во компонентов, сами компоненты и требуемое время.\n"
                              f"Само приложение имеет два режима работы:\n"
                              f"1) Работа в приложении. Требуется ввод блюда, а информацию о нем оно выводит ниже.\n"
                              f"2) Работа в приложеии через файлы. Требуется выбрать два файла: считываемый и тот, "
                              f"куда будут записывать информацию")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.autorisation = AutorisationDialog()
            self.autorisation.show()
            self.hide()


class Customization(QDialog):
    def __init__(self):
        """
        Инициализация класса для настройки темы приложения
        """
        super().__init__()

        self.autorisation = None
        self.setting = None
        uic.loadUi('for_ui/dialog4.ui', self)

        self.setFixedSize(400, 302)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
            self.system.setChecked(True)
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
            self.green.setChecked(True)
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
            self.red.setChecked(True)
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
            self.blue.setChecked(True)
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")
            self.image.setChecked(True)

        self.initUi()

    def initUi(self):
        try:
            self.setting = QButtonGroup(self)
            self.setting.addButton(self.system)
            self.setting.addButton(self.blue)
            self.setting.addButton(self.red)
            self.setting.addButton(self.green)
            self.setting.addButton(self.image)

            self.save.clicked.connect(self.ssave)
            self.escape.clicked.connect(self.esc)
        except Exception:
            pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.autorisation = AutorisationDialog()
            self.autorisation.show()
            self.hide()

    def esc(self):
        """
        Назад, на экран выбора
        """
        self.autorisation = AutorisationDialog()
        self.autorisation.show()
        self.hide()

    def ssave(self):
        global global_background
        sett = self.setting.checkedButton().text()
        global_background = sett
        if sett == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif sett == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif sett == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif sett == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif sett == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")


class ShowMenu(QMainWindow):
    def __init__(self):
        """
        Инициализация, класса для показа всей БД
        """
        super().__init__()

        self.autorisation = None
        self.setWindowTitle('Database Viewer')

        if global_background == "Системный":
            self.setStyleSheet("#MainWindow{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#MainWindow{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#MainWindow{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#MainWindow{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#MainWindow{border-image:url("
                               "for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp.jpg)}")

        self.resize(800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout()

        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('for_db/components_ru.db')
        db.open()

        view = QTableView()
        model = QSqlQueryModel()

        query = QSqlQuery("SELECT * FROM id")
        model.setQuery(query)
        view.setModel(model)

        layout.addWidget(view)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.autorisation = AutorisationDialog()
            self.autorisation.show()
            self.hide()


class AddDateBase(QMainWindow):
    def __init__(self):
        """
        Инициализация окна, для добваления данных
        """
        super().__init__()

        self.edit_button = None
        self.delete_button = None
        self.time = None
        self.add_user_button = None
        self.query = None
        self.model = None
        self.view = None
        self.db = None
        self.layout = None
        self.central_widget = None
        self.autorisation = None

        self.setWindowTitle('Database Viewer')

        if global_background == "Системный":
            self.setStyleSheet("#MainWindow{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#MainWindow{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#MainWindow{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#MainWindow{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#MainWindow{border-image:url("
                               "for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp.jpg)}")

        self.resize(800, 600)

        self.initUi()

    def initUi(self):
        """
        Основное окно для добавление
        """
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('for_db/components_ru.db')
        self.db.open()

        self.view = QTableView()
        self.model = QSqlQueryModel()

        self.query = QSqlQuery("SELECT * FROM id")
        self.model.setQuery(self.query)
        self.view.setModel(self.model)

        self.layout.addWidget(self.view)
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

        self.add_user_button = QPushButton('Добавить в меню')
        self.delete_button = QPushButton("Удалить значения")
        self.edit_button = QPushButton("Изменить значения")

        self.delete_button.clicked.connect(self.DeleteElem)
        self.edit_button.clicked.connect(self.EditElem)
        self.add_user_button.clicked.connect(self.AddElems)

        self.layout.addWidget(self.add_user_button)
        self.layout.addWidget(self.edit_button)
        self.layout.addWidget(self.delete_button)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.autorisation = AutorisationDialog()
            self.autorisation.show()
            self.hide()

    def AddElems(self):
        """
        Открываем диалоговое окно, для добавления новых элементов
        """
        self.time = ForAddItem()
        self.time.show()
        self.hide()

    def DeleteElem(self):
        self.time = DeleteElement()
        self.time.show()
        self.hide()

    def EditElem(self):
        self.time = EditElement()
        self.time.show()
        self.hide()


class ForAddItem(QDialog):
    def __init__(self):
        """
        Для диалогового окна, добавляющего новые позиции в БД
        """
        super().__init__()

        self.mainAdd = None

        uic.loadUi('for_ui/dialog5.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.ok.clicked.connect(self.Add)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.mainAdd = AddDateBase()
            self.mainAdd.show()
            self.hide()

    def Add(self):
        """
        Для добавления в БД
        """
        connection = sqlite3.connect('for_db/components_ru.db')
        cursor = connection.cursor()

        # Добавляем новые значения
        cursor.execute('INSERT INTO id (id, name, count_components, components, time) VALUES (?, ?, ?, ?, ?)',
                       (self.id.text(), self.Name.text(), self.count.text(),
                        self.components.text(), self.time.text()))

        # Сохраняем изменения и зак рываем соединение
        connection.commit()
        connection.close()

        self.mainAdd = AddDateBase()
        self.mainAdd.show()
        self.hide()


class DeleteElement(QDialog):
    def __init__(self):
        super().__init__()

        uic.loadUi('for_ui/dialog6.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.app_result.clicked.connect(self.showw)
        self.delete_2.clicked.connect(self.delete)

    def showw(self):
        """
        Импортирование из базы данных, а так-же вывод внутри приложения рецепта.
        """
        con = sqlite3.connect("for_db/components_ru.db")
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("""SELECT * FROM id
                                     WHERE name = ?""",
                             (self.Name.text(),)).fetchall()
        # закрываем БД для экономии памяти и не перегружания его открытыми БД
        con.close()

        if not result:
            print("Ничего не нашлось")
        else:
            # показываем поле для вывода текста
            self.app_result_text.show()
            # обнуляем запрос
            self.app_result_text.setPlainText(f"")

            # создание нового списка
            new_result = []

            # распаковка старого, неудобного списка
            for i in result:
                for j in i:
                    new_result.append(j)

            # выводим результат
            self.app_result_text.setPlainText(f"Номер блюда: {new_result[0]}\n"
                                              f"Название: {new_result[1]}\n"
                                              f"Количество компонентов: {new_result[2]}\n"
                                              f"Компоненты:")

            # выводим компоненты блюда
            for i in new_result[3].split(", "):
                self.app_result_text.append(f"                      ●{i.capitalize()}")

            # выводим время, требуемое для приготовления блюда
            self.app_result_text.append(f"Время, нужное на приготовление блюда: {new_result[4]}")

            self.label_for_image.show()

            def get_url():
                """
                Парсер изображения блюда по названию через интернет с помощью библиотеки bs4
                """
                name_for_parsing = new_result[1] + " картинка блюда"

                url = 'https://www.google.com/search?q={0}&tbm=isch'.format(name_for_parsing)
                content = requests.get(url).content
                soup = BeautifulSoup(content, features="html5lib")
                images = soup.findAll('img')

                for image in images[1: 2]:
                    print(image.get('src'))

                url = [image.get("src") for image in images][1]

                return requests.get(url)

            def show_image(response):
                """
                Для вывода изображения
                """
                if response.status_code == 200:
                    with open("for_time_image/image.jpg", "wb") as f:
                        f.write(response.content)
                    print("Изображение успешно сохранено.")

                    self.pixmap = QPixmap('for_time_image/image.jpg')

                    self.label_for_image.resize(331, 111)

                    self.label_for_image.setPixmap(self.pixmap)
                else:
                    print("Не удалось загрузить изображение. Код статуса:", response.status_code)

            # получаем адрес на изображение, а затем сохраняем его в папку, откуда потом выводим изображение
            show_image(get_url())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.mainAdd = AddDateBase()
            self.mainAdd.show()
            self.hide()

    def delete(self):
        con = sqlite3.connect("for_db/components_ru.db")
        cur = con.cursor()

        valid = QMessageBox.question(
            self, '', "Действительно удалить элемент с названием " + self.Name.text(),
            QMessageBox.Yes, QMessageBox.No)
        # Если пользователь ответил утвердительно, удаляем элементы.
        # Не забываем зафиксировать изменения
        if valid == QMessageBox.Yes:
            cur.execute("""DELETE FROM id WHERE name=?""", (self.Name.text(),))
            con.commit()
            con.close()


class EditElement(QDialog):
    def __init__(self):
        super().__init__()

        self.mainAdd = None

        uic.loadUi('for_ui/dialog7.ui', self)

        if global_background == "Системный":
            self.setStyleSheet("#Dialog{background-color:white}")
        elif global_background == "Зеленый":
            self.setStyleSheet("#Dialog{background-color:green}")
        elif global_background == "Красный":
            self.setStyleSheet("#Dialog{background-color:red}")
        elif global_background == "Синий":
            self.setStyleSheet("#Dialog{background-color:blue}")
        elif global_background == "Космический":
            self.setStyleSheet("#Dialog{border-image:url(for_image/54232_C8waTyKw81_2297_sci_fi_sci_fi_planets_wallp"
                               ".jpg)}")

        self.id.hide()
        self.name.hide()
        self.count.hide()
        self.components.hide()
        self.time.hide()
        self.ok.hide()
        self.image.hide()

        self.label_2.hide()
        self.label_3.hide()
        self.label_4.hide()
        self.label_5.hide()
        self.label_6.hide()

        self.start.clicked.connect(self.Start)
        self.ok.clicked.connect(self.Ok)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            """
            Назад, на экран выбора
            """
            self.mainAdd = AddDateBase()
            self.mainAdd.show()
            self.hide()

    def Start(self):
        self.id.show()
        self.name.show()
        self.count.show()
        self.components.show()
        self.time.show()
        self.ok.show()
        self.image.show()

        self.label_2.show()
        self.label_3.show()
        self.label_4.show()
        self.label_5.show()
        self.label_6.show()

        con = sqlite3.connect("for_db/components_ru.db")
        cur = con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("""SELECT * FROM id
                                             WHERE name = ?""",
                             (self.Name.text(),)).fetchall()
        # закрываем БД для экономии памяти и не перегружания его открытыми БД
        con.close()

        new_result = []

        # распаковка старого, неудобного списка
        for i in result:
            for j in i:
                new_result.append(j)

        self.id.setText(f"{new_result[0]}")
        self.name.setText(f"{new_result[1]}")
        self.count.setText(f"{new_result[2]}")

        # выводим компоненты блюда
        for i in new_result[3].split(", "):
            if i != new_result[3].split(", ")[0]:
                self.components.append(f"{i.capitalize()}")
            else:
                self.components.setText(f"{i.capitalize()}")

        # выводим время, требуемое для приготовления блюда
        self.time.setText(f"{new_result[4]}")

        self.image.show()

        def get_url():
            """
            Парсер изображения блюда по названию через интернет с помощью библиотеки bs4
            """
            name_for_parsing = new_result[1] + " картинка блюда"

            url = 'https://www.google.com/search?q={0}&tbm=isch'.format(name_for_parsing)
            content = requests.get(url).content
            soup = BeautifulSoup(content, features="html5lib")
            images = soup.findAll('img')

            for image in images[1: 2]:
                print(image.get('src'))

            url = [image.get("src") for image in images][1]

            return requests.get(url)

        def show_image(response):
            """
            Для вывода изображения
            """
            if response.status_code == 200:
                with open("for_time_image/image.jpg", "wb") as f:
                    f.write(response.content)
                print("Изображение успешно сохранено.")

                self.pixmap = QPixmap('for_time_image/image.jpg')

                self.image.setPixmap(self.pixmap)
            else:
                print("Не удалось загрузить изображение. Код статуса:", response.status_code)

        # получаем адрес на изображение, а затем сохраняем его в папку, откуда потом выводим изображение
        show_image(get_url())

    def Ok(self):
        con = sqlite3.connect("for_db/components_ru.db")
        cur = con.cursor()

        comp = str(", ".join(self.components.toPlainText().split("\n")))

        # Получили результат запроса, который ввели в текстовое поле
        cur.execute("""UPDATE id SET id=?, name=?, count_components=?, components=?, time=? WHERE name = ?""",
                    (self.id.text(), self.name.text(), self.count.text(),
                     comp, self.time.text(), self.name.text()))

        con.commit()
        con.close()

        self.mainAdd = AddDateBase()
        self.mainAdd.show()
        self.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    autorisationDialog = AutorisationDialog()
    autorisationDialog.show()
    sys.exit(app.exec())
