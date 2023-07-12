#Dependencias del proyecto - pip install -r requirements.txt para instalar las dependencias.
import random

# BillsCompartment class para generar el código de barras de las facturas
class BillsCompartment:
    @staticmethod
    def generate_code():
        return random.randint(100000000, 999999999)
