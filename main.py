from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QComboBox, QWidget, QMessageBox
from PySide6.QtGui import QIcon
from db import SessionLocal, Item, Category

class ShoppingListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список покупок")
        self.setWindowIcon(QIcon("/home/KHPK.RU/student/Рабочий стол/asd/shopping_icon.png"))
        self.setGeometry(100, 100, 600, 400)

        # Настройка интерфейса
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Поля ввода
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Название товара")
        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Категория")

        # Кнопки
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_item)
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_item)

        # Список товаров
        self.item_list = QListWidget()

        # Фильтр категорий
        self.category_filter = QComboBox()
        self.category_filter.addItem("Все категории")
        self.category_filter.currentTextChanged.connect(self.filter_items)

        # Размещение виджетов
        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.category_input)
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)
        self.layout.addWidget(self.category_filter)
        self.layout.addWidget(self.item_list)

        # Загрузка данных из базы
        self.session = SessionLocal()
        self.load_categories()
        self.load_items()

    def load_categories(self):
        # Загружает категории в фильтр
        self.category_filter.clear()
        self.category_filter.addItem("Все категории")
        categories = self.session.query(Category).all()
        for category in categories:
            self.category_filter.addItem(category.name)

    def load_items(self, category_name=None):
        # Загружает товары в список
        self.item_list.clear()
        if category_name and category_name != "Все категории":
            category = self.session.query(Category).filter_by(name=category_name).first()
            if category:
                items = self.session.query(Item).filter_by(category_id=category.id).all()
            else:
                items = []
        else:
            items = self.session.query(Item).all()

        for item in items:
            category = self.session.query(Category).get(item.category_id)
            self.item_list.addItem(f"{item.name} ({category.name})")

    def add_item(self):
        # Добавляет новый товар в базу данных
        name = self.name_input.text().strip()
        category_name = self.category_input.text().strip()

        if not name or not category_name:
            QMessageBox.warning(self, "Ошибка", "Введите название и категорию!")
            return

        # Добавляем или находим категорию
        category = self.session.query(Category).filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            self.session.add(category)
            self.session.commit()

        # Добавляем товар
        item = Item(name=name, category_id=category.id)
        self.session.add(item)
        self.session.commit()

        # Обновляем интерфейс
        self.load_items()
        self.load_categories()

        # Очищаем поля
        self.name_input.clear()
        self.category_input.clear()

    def delete_item(self):
        # Удаляет выбранный товар из базы данных
        selected_item = self.item_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления!")
            return

        item_text = selected_item.text()
        item_name = item_text.split(" (")[0]

        # Удаление товара
        item = self.session.query(Item).filter_by(name=item_name).first()
        if item:
            self.session.delete(item)
            self.session.commit()

        # Обновляем интерфейс
        self.load_items()

    def filter_items(self):
        # Фильтрует товары по выбранной категории
        category_name = self.category_filter.currentText()
        self.load_items(category_name)

if __name__ == "__main__":
    app = QApplication([])
    window = ShoppingListApp()
    window.show()
    app.exec()
