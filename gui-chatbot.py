import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton
from PyQt5.QtGui import QTextCursor, QColor, QPalette, QFont
from PyQt5.QtCore import Qt
import threading
import asyncio
from rasa.core.agent import Agent
from rasa.shared.nlu.constants import ACTION_NAME

class ChatInterface(QMainWindow):
    def __init__(self, agent):
        super().__init__()
        self.setWindowTitle("Eichhörnchen Tissot")
        self.setGeometry(100, 100, 800, 600)
        self.setFixedSize(800, 600)

        self.chat_window = QTextEdit(self)
        self.chat_window.setReadOnly(True)
        self.chat_window.setGeometry(10, 10, 780, 500)
        self.chat_window.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.user_input_entry = QLineEdit(self)
        self.user_input_entry.setGeometry(10, 520, 600, 30)
        self.user_input_entry.returnPressed.connect(self.send_message)

        self.send_button = QPushButton("Enviar", self)
        self.send_button.setGeometry(620, 520, 170, 30)
        self.send_button.clicked.connect(self.send_message)

        self.agent = agent

        self.chat_window.append("¡Bienvenido! Por favor, introduce tu saludo al chatbot.")

    def send_message(self):
        user_message = self.user_input_entry.text()
        self.user_input_entry.clear()
        self.display_message(user_message, "Usuario")

        threading.Thread(target=self.process_message, args=(user_message,)).start()

    def process_message(self, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def handle_message():
            responses = await self.agent.handle_text(message)
            for response in responses:
                if 'form' in response:
                    # El bot ha solicitado información del formulario
                    form_name = response['form']
                    self.display_message(f"Por favor, completa el formulario: {form_name}", "Chatbot")
                else:
                    bot_action = response.get('next_action', ACTION_NAME)
                    if bot_action.startswith('validate_asignatura_tipo_dato_form'):
                        custom_action_name = bot_action.replace('validate_asignatura_tipo_dato_form', '')
                        self.handle_custom_action(custom_action_name)
                    else:
                        bot_message = response['text']
                        self.display_message(bot_message, "Chatbot")

        loop.run_until_complete(handle_message())

    def display_message(self, message, sender):
        if sender == "Usuario":
            self.chat_window.append(f"Tú: {message}")
        else:
            messages = message.split('\n')
            for msg in messages:
                self.chat_window.append(f"Chatbot: {msg}")

        self.chat_window.moveCursor(QTextCursor.End)
        self.chat_window.ensureCursorVisible()

        # Estilos de texto
        if sender == "Usuario":
            color = QColor("black")
        else:
            color = QColor("red")

        text_cursor = self.chat_window.textCursor()
        text_cursor.movePosition(QTextCursor.End)
        text_cursor.select(QTextCursor.LineUnderCursor)
        text_format = text_cursor.charFormat()
        text_format.setForeground(color)
        text_format.setFontWeight(QFont.Bold)
        text_cursor.mergeCharFormat(text_format)

        self.chat_window.mergeCurrentCharFormat(text_format)

    def handle_custom_action(self, custom_action_name):
        # Lógica para llamar a la acción personalizada definida en actions.py
        # Importar las clases o funciones necesarias desde actions.py
        from actions import CustomActionClass

        # Crear una instancia de la acción personalizada
        custom_action = CustomActionClass()

        # Ejecutar la acción personalizada
        response = custom_action.run()
        
        # Mostrar la respuesta de la acción personalizada en el chat
        bot_message = response['text']
        self.display_message(bot_message, "Chatbot")

if __name__ == "__main__":
    # Cargar y configurar el agente de Rasa
    agent = Agent.load("models/20230707-094657-laminated-gable.tar.gz")

    # Crear la aplicación y la ventana principal
    app = QApplication(sys.argv)
    window = ChatInterface(agent)
    window.show()

    # Ejecutar la aplicación
    sys.exit(app.exec_())
