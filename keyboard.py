#Dependencias del proyecto - pip install -r requirements.txt para instalar las dependencias.
import inquirer
from inquirer.themes import GreenPassion


class Keyboard:
    #static method para que no sea necesario instanciar la clase
    @staticmethod
    #Función para mostrar las preguntas y obtener las respuestas
    def prompt(questions):
        return inquirer.prompt(questions, theme=GreenPassion())
    
