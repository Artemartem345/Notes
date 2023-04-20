import sys # обеспечивает высокоуровневое взаимодействие с операционной системой
from PyQt5 import QtCore, QtGui, QtWidgets
from main import send_email
class MainWindow(QtWidgets.QMainWindow):  # создаем собственный класс окна

                # создаем конструктор класса для доступа к переменным,
                # методам и др. из файла с дизайном
    def __init__(self, parent=None):
                QtWidgets.QWidget.__init__(self, parent)  #инициализируем класс
                self.ui = send_email()
                self.ui.setupUi(self)
                


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv) # Новый экземпляр QApplication (передаем аргументы командной строки)
    window = MainWindow()
    window.show()          #показываем окно
    sys.exit(app.exec_()) 


