#Clase para la base de datos de usuarios y sus credenciales.
class Database:
    # Constructor de la clase Database que recibe como parámetro el archivo de usuarios
    def __init__(self, user_file):
        self.user_file = user_file
        self.users = {}

    # Método para cargar los usuarios del archivo de usuarios.txt
    def load_users(self):
        with open(self.user_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                username, pin = line.strip().split(",")
                self.users[username] = pin

    # Método para validar credenciales de usuario y pin
    def validate_credentials(self, username, pin):
        if username in self.users and self.users[username] == pin:
            return True
        return False
