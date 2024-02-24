import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWebEngineView

class WebViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl("https://www.example.com")  # Substitua pelo URL desejado

        self.setCentralWidget(self.browser)
        self.setWindowTitle("PyQtWebEngine Example")
        self.setGeometry(100, 100, 800, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebViewWindow()
    window.show()
    sys.exit(app.exec_())

