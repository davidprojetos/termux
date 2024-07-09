import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class GeradorSorteio(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Sorteio - Ariely")
        self.setGeometry(100, 100, 300, 200)

        self.resultado_label = QLabel("Número Sorteado: ", self)
        self.sortear_button = QPushButton("Sortear", self)
        self.sortear_button.clicked.connect(self.sortear_numero)

        layout = QVBoxLayout()
        layout.addWidget(self.resultado_label)
        layout.addWidget(self.sortear_button)

        self.setLayout(layout)

    def sortear_numero(self):
        numero_sorteado = random.randint(1, 1000)
        self.resultado_label.setText(f"Número Sorteado: {numero_sorteado}")

def main():
    app = QApplication(sys.argv)
    gerador_sorteio = GeradorSorteio()
    gerador_sorteio.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

