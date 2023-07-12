#Dependencias del proyecto - pip install -r requirements.txt para instalar las dependencias.
import os
import pyfiglet
from termcolor import colored
import qrcode
import time

# Clase para la pantalla
class Screen:
    def __init__(self):
        self.clear()
        self.print_banner()

    @staticmethod
    # Método para limpiar la pantalla
    def clear():
        os.system('cls')

    @staticmethod
    # Método para imprimir el banner
    def print_banner():
        
        ascii_banner = pyfiglet.figlet_format("ATMIQ", font="broadway")
        print(colored(ascii_banner, "green"))

    @staticmethod
    # Método para imprimir un mensaje
    def print_message(message, color="green"):
        print(colored(message, color), '\n')

    @staticmethod
    # Método para imprimir un mensaje de error
    def print_error(message, color="red"):
        print(colored(message, color))

    @staticmethod
    # Método para imprimir un QR
    def print_qr_code(data):
        qr = qrcode.QRCode()
        qr.add_data(data)
        qr.make()
        qr.print_ascii()

    @staticmethod
    # Método para imprimir un mensaje de espera
    def wait_for_cash():
        # Mensaje de espera
        print(colored("Espere mientras se procesa su transacción...", "green"))
        time.sleep(1)
        
        # Animación de espera
        animation = "|/-\\"
        for i in range(10):
            time.sleep(0.2)
            print("\r" + colored("Retirando dinero " + animation[i % len(animation)], "green"), end="")
            print("\r" + colored("Retirando dinero ", "green"), end="")
            time.sleep(0.2)

        # Limpiar pantalla
        os.system('cls')
        print("\n" + colored("[📤] Retire su dinero del compartimiento.", "green"))