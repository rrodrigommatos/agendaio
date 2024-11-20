import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

class LoginApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Agenda.io - Login')
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.label = QLabel("Acessar seu negócio")
        self.sub_label = QLabel("Organize suas demandas com Agenda.io")
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Qual o CPF do dono do negócio ou CNPJ da empresa?")

        self.button = QPushButton("Avançar", self)
        self.button.clicked.connect(self.verificar_cpf_cnpj)

        layout.addWidget(self.label)
        layout.addWidget(self.sub_label)
        layout.addWidget(self.input_field)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def verificar_cpf_cnpj(self):
        cpf_cnpj = self.input_field.text()
        if not cpf_cnpj:
            QMessageBox.warning(self, "Erro", "Por favor, insira o CPF/CNPJ.")
            return

        # Realiza a requisição para verificar se o CPF/CNPJ está cadastrado
        try:
            response = requests.post("http://127.0.0.1:5000/verificar_cpf_cnpj", json={"cpf_cnpj": cpf_cnpj})
            data = response.json()
            if data["existe"]:
                QMessageBox.information(self, "Usuário encontrado", "Redirecionando para a tela de senha.")
                # Aqui você poderia chamar a próxima tela de senha
            else:
                QMessageBox.information(self, "Usuário não encontrado", "Redirecionando para a tela de cadastro.")
                # Aqui você poderia chamar a tela de cadastro
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Erro", f"Erro de conexão com o servidor: {e}")

def main():
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
