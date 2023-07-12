# Dependencias del proyecto - pip install -r requirements.txt para instalar las dependencias.
from screen import Screen
from keyboard import Keyboard
from bills_compartment import BillsCompartment
from user import User
from database import Database
import inquirer


# Clase ATM
class ATM:
    # Constructor
    def __init__(self):
        self.screen = Screen()
        self.keyboard = Keyboard()
        self.bills_compartment = BillsCompartment()
        self.user_file = "usuarios.txt"
        self.database = Database(self.user_file)
        self.users = {}

    # Método start para iniciar el cajero
    def start(self):
        self.load_users()
        username = self.login()
        if username:
            self.menu(username)

    # Método para cargar los usuarios
    def load_users(self):
        self.database.load_users()
        for username, pin in self.database.users.items():
            self.users[username] = User(username, pin)

    # Método para iniciar sesión (Preguntar por usuario y pin y validar credenciales)
    def login(self):
        questions = [
            inquirer.Text('username', message='[👤] Ingrese su usuario'),
            inquirer.Password('pin', message='[🔢] Ingrese su PIN')
        ]
        # While True para que se repita el proceso de inicio de sesión hasta que se ingrese un usuario y pin correctos
        while True:
            answers = self.keyboard.prompt(questions)
            username = answers['username']
            pin = answers['pin']
            # Validar credenciales con el método validate_credentials de la clase Database
            if self.database.validate_credentials(username, pin):
                self.screen.print_message("[✅] Inicio de sesión exitoso")
                return username
            # Login fallido
            else:
                self.screen.print_error("[❌] Credenciales incorrectas. Intente nuevamente.")

    # Menú principal del cajero
    def menu(self, username):
        # Mensaje de bienvenida
        self.screen.print_message("[👋] Bienvenido, {}".format(username))
        # While True para que se repita el menú hasta que se seleccione la opción de salir
        while True:
            # Opciones del menú
            options = [
                inquirer.List('option',
                              message='Seleccione una opción',
                              choices=[
                                  '[💵] Retirar efectivo',
                                  '[💳] Consultar saldo',
                                  '[📥] Depositar saldo',
                                  '[📞] Comprar recarga',
                                  '[❌] Salir'
                              ]
                              )
            ]
            # Respuesta del usuario
            response = self.keyboard.prompt(options)['option']

            #Dispatch Table para ejecutar la función correspondiente a la opción seleccionada
            menu_functions = {
                '[💵] Retirar efectivo': self.withdraw_cash,
                '[💳] Consultar saldo': self.check_balance,
                '[📥] Depositar saldo': self.deposit_cash,
                '[📞] Comprar recarga': self.buy_top_up,
                '[❌] Salir': self.exit
            }

            if response in menu_functions:
                menu_functions[response](username)
            
            # Opción inválida
            else:
                self.screen.print_error("Opción inválida")

    # Método para retirar efectivo
    def withdraw_cash(self, username):
        user = self.users[username]
        questions = [
            inquirer.Text('amount', message='Ingrese el monto a retirar')
        ]
        amount = float(self.keyboard.prompt(questions)['amount'])
        # Validar que el monto sea mayor y diferente a 0
        if amount <= 0:
            self.screen.print_error("[❌] La cantidad ingresada es inválida. Por favor, ingrese un monto válido.")
        # Validar que el usuario tenga suficiente saldo
        elif amount > user.balance:
            self.screen.print_error("[❌] No tiene suficiente saldo para retirar esa cantidad.")
        else:
            #Llamar al método withdraw de la clase User
            user.withdraw(amount)
            self.screen.wait_for_cash()
            self.screen.print_message("[💵] Nuevo saldo: ${}".format(user.balance), "green")
            trasaction_code = self.bills_compartment.generate_code()
            self.screen.print_message("[📜] Su código de factura es: #{}".format(trasaction_code), "green")
            self.screen.print_qr_code(trasaction_code)
            user.save_balance()

    # Función para verificar el saldo
    def check_balance(self, username):
        user = self.users[username]
        # Llamar al método check_balance de la clase User y al método print_message de la clase Screen para mostrar el saldo
        self.screen.print_message("Su saldo es: ${}".format(user.check_balance()), "green")

    # Funcion para depositar saldo
    def deposit_cash(self, username):
        user = self.users[username]
        questions = [
            inquirer.Text('amount', message='Ingrese el monto a depositar')
        ]
        amount = float(self.keyboard.prompt(questions)['amount'])
        # Validar que el monto sea mayor y diferente a 0
        if amount <= 0:
            self.screen.print_error("[❌] La cantidad ingresada es inválida. Por favor, ingrese un monto válido.")
        else:
            # Llamar al método deposit de la clase User y al método print_message de la clase Screen para mostrar el saldo
            user.deposit(amount)
            self.screen.print_message("Depósito exitoso. Nuevo saldo: ${}".format(user.balance), "green")
            user.save_balance()

    def buy_top_up(self, username):
        companies = ["[⬛] Altice", "[🔴] Claro", "[🟢] Viva"]
        user = self.users[username]
        questions = [
            inquirer.Text('amount', message='Ingrese el monto de la recarga')
        ]
        amount = float(self.keyboard.prompt(questions)['amount'])

        # Validar que el monto no sea mayor al saldo del usuario
        if amount > user.balance:
            self.screen.print_error("[❌] No tiene suficiente saldo para comprar esa recarga")
        
        # Validar que el monto sea mayor y diferente a 0
        elif amount <= 0:
            self.screen.print_error("[❌] La cantidad ingresada es inválida. Por favor, ingrese un monto válido.")

        # Compra de recarga exitosa
        else:
            questions = [
                inquirer.List('company',
                              message='Seleccione la compañía',
                              choices=companies
                              )]
            company = self.keyboard.prompt(questions)['company']
            code = self.bills_compartment.generate_code()
            self.screen.print_message("Su código de recarga es: {}".format(code), "green")
            # Llamar al método buy_recharge de la clase User
            user.buy_recharge(amount)
            # Llamar al método print_message de la clase Screen para mostrar el saldo, la compañía y el monto.
            self.screen.print_message("[✅] Compra de recarga exitosa.")
            self.screen.print_message("Compañía: {}".format(company))
            self.screen.print_message("Monto: ${}".format(amount), "green")
            self.screen.print_qr_code(code)
            # Llamar al método save_balance de la clase User
            user.save_balance()

    # Función para salir del cajero
    def exit(self, username):
        # Llamar al método clear de la clase Screen para limpiar la pantalla
        self.screen.clear()
        self.screen.print_message("[👋] Gracias por usar el cajero bancario")
        self.start()


# Función principal para iniciar el programa
def main():
    atm = ATM()
    atm.start()

# Verificar si el archivo se está ejecutando directamente y no siendo importado
if __name__ == "__main__":
    main()
