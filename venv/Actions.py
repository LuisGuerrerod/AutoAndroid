from Scripts import AndroidDevice
from MakeCall import llamada
import time

DELAY = 10

def is_valid_number(number):
    if number[0] == '+' or number[0] == '*':
        return number[1:].isdigit()
    return number.isdigit()

if __name__ == '__main__':
    android = AndroidDevice()
    make_calls = llamada()
    android.select_device()
    while True:
        print('Marcar número de telefono:\n' +
              '\t 1) Mediante AdbShell\n' +
              '\t 2) Mediante UiAtomator\n' +
              'Enceder el WiFi\n' +
              '\t 3) Mediante AdbShell\n' +
              '\t 4) Mediante UiAtomator\n' +
              'Apagar el WiFi\n' +
              '\t 5) Mediante AdbShell\n' +
              '\t 6) Mediante UiAtomator\n' +
              'Funcion Calculadora\n' +
              '\t 7) Mediante AdbShell\n' +
              '\t 8) Mediante UiAtomatorr\n' +
              'Mensaje de voz\n' +
              '\t 9) Dejar mensaje de voz\n' +
              '10) Salir')
        option = input('Selecciona una opción: ')
        if option.isdigit():
            option = int(option)
            if option == 1:
                number = input('Ingresa el numero a marcar: ')
                if is_valid_number(number):
                    android.adb_calling_test(number, DELAY)
            if option == 2:
                number = input('Ingresa el numero a marcar: ')
                if is_valid_number(number):
                    android.uia_calling_test(number, DELAY)
            if option == 3:
                android.adb_wifi_test('ON')
            if option == 4:
                android.settings_wifi_test('ON')
            if option == 5:
                android.adb_wifi_test('OFF')
            if option == 6:
                android.settings_wifi_test('OFF')
            if option == 7:
                number = input('Ingresa la operación: ')
                while ('+' not in number and '*' not in number and '/' not in number and '-' not in number):
                    number = input('Caracter invalido: ')
                android.adb_claculator_SendText(number)
            if option == 8:
                number = input('Ingresa la operación: ')
                while ('+' not in number and '*' not in number and '/' not in number and '-' not in number):
                    number = input('Caracter invalido: ')
                android.ui_calculator(number)
            if option == 9:
                make_calls.llamada_demo()
            if option == 10:
                 break
            if option < 0 or option > 10:
                print('{0} No es una opcion valida'.format(option))
                pass
        else:
            print('{0} No es una opcion valida'.format(option))
            pass