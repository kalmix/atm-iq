# Descripción : Clase que representa a un usuario
class User:
    # Constructor de la clase User que recibe como parámetros el nombre de usuario y el pin
    def __init__(self, username, pin):
        self.username = username
        self.pin = pin
        self.balance_file = "balance/{}.txt".format(username)
        self.balance = self.load_balance()

    # Método para cargar el balance del usuario
    def load_balance(self):
        try:
            with open(self.balance_file, "r") as file:
                balance = float(file.read())
        except FileNotFoundError:
            balance = 0.0
        return balance

    # Método para guardar el balance del usuario en el archivo correspondiente a su nombre de usuario
    def save_balance(self):
        with open(self.balance_file, "w") as file:
            file.write(str(self.balance))


    # Método para retirar dinero del balance del usuario
    def withdraw(self, amount):
        self.balance -= amount
        self.save_balance()

    # Método para depositar dinero al balance del usuario
    def deposit(self, amount):
        self.balance += amount
        self.save_balance()
    
    # Método para verificar el balance del usuario
    def check_balance(self):
        return self.balance
    
    # Método para comprar recarga
    def buy_recharge(self, amount):
        self.balance -= amount
        self.save_balance()

