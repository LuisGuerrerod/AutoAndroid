from subprocess import check_call, check_output
from uiautomator import Device
import time

NO_CONNECTED = 'No devices connected'
NO_SELECTED = 'No devices selected'
CALLING = 'Calling'

class AndroidDevice(object):

    def __init__(self):
        self.device = None
        self.call_status = None
        self.d = None

    def select_device(self, device=1):
        list_devices = check_list()
        if list_devices:
            if device <= 0 or device > len(list_devices):
                print(NO_SELECTED)
                exit()
            else:
                self.device = list_devices[device - 1].split()[0].decode('utf-8')
                self.d = Device(self.device)
                return self.device
        else:
            print(NO_CONNECTED)
            exit()

    def dial_number(self, number):
        if self.device:
            check_call(['adb', '-s', self.device, 'shell', 'am', 'start',
                        '-a', 'android.intent.action.CALL', '-d', 'tel:{0}'.format(number)])
            self.call_status = CALLING

    def hang_up(self):
        if self.call_status == CALLING:
            check_call(['adb', 'shell', 'input', 'keyevent 6'])
            self.call_status = None

    def adb_open_settings(self):
        check_call(['adb', 'shell', 'am', 'start', '-a', 'android.settings.SETTINGS'])

    def turn_on_wifi(self):
        check_call(['adb', '-s', self.device, 'shell', 'svc wifi enable'])

    def turn_off_wifi(self):
        check_call(['adb', '-s', self.device, 'shell', 'svc wifi disable'])

    def adb_calling_test(self, number, delay=5):
        self.dial_number(number)
        time.sleep(delay)
        self.hang_up()

    def adb_wifi_test(self, on_off):
        if on_off == 'ON':
            self.turn_on_wifi()
        elif on_off == 'OFF':
            self.turn_off_wifi()

    def uiaviewer_generator(self, name_file):
        self.d.screenshot('{0}.png'.format(name_file))
        self.d.dump('{0}.uix'.format(name_file))

    def initial_state(self):
        self.d.screen.on()
        self.d.press.home()

    def type_number(self, number):
        for digit in number:
            self.d(text='{0}'.format(digit), className='android.widget.TextView').click()

    def uia_calling_test(self, number, delay=2):
        self.initial_state()
        flag = False
        if self.d(descriptionContains='Phone', className='android.widget.TextView').count == 1:
            self.d(descriptionContains='Phone', className='android.widget.TextView').click()
            # self.d(descriptionContains='key pad', className='android.widget.ImageButton').click()
            self.type_number(number)
            self.d(descriptionContains='dial', className='android.widget.ImageButton').click()
            time.sleep(delay)
            if self.d(descriptionContains='Phone', className='android.widget.TextView').count == 1:
                self.d(descriptionContains='End', className='android.widget.ImageButton').click()
        elif self.d(descriptionContains='Teléfono', className='android.widget.TextView').count == 1:
            self.d(descriptionContains='Teléfono', className='android.widget.TextView').click()
            self.d(descriptionMatches='teclado', className='android.widget.ImageButton').click()
            self.d(descriptionMatches='', className='android.widget.EditText').click()
            self.type_number(number)
            self.d(descriptionMatches='marcar', className='android.widget.ImageButton').click()
            time.sleep(delay)
            self.d(descriptionMatches='Finalizar llamada', className='android.widget.ImageButton').click()

    def quick_turn_on_wifi(self):
        status = self.d(descriptionContains='Wi-Fi', className='android.widget.Switch').checked
        if not status:
            self.d(descriptionContains='Wi-Fi', className='android.widget.Switch').click()
        else:
            print('WiFi actalmente encendido')

    def quick_turn_off_wifi(self):
        status = self.d(descriptionContains='Wi-Fi', className='android.widget.Switch').checked
        if status:
            self.d(descriptionContains='Wi-Fi', className='android.widget.Switch').click()
        else:
            print('WiFi actualmente apagado')

    def uia_quick_wifi_test(self, on_off):
        self.d.open.quick_settings()
        time.sleep(3)
        if on_off == 'ON':
            self.quick_turn_on_wifi()
        elif on_off == 'OFF':
            self.quick_turn_off_wifi()
        time.sleep(3)
        self.initial_state()

    def setting_turn_on_wifi(self):
        status = self.d(index='2', className='android.widget.Switch').checked
        if (status == False):
            self.d(index='2', className='android.widget.Switch').click()
        else:
            print('WiFi actalmente encendido')

    def setting_turn_off_wifi(self):
        status = self.d(index='2', className='android.widget.Switch').checked
        if status:
            self.d(index='2', className='android.widget.Switch').click()
        else:
            print('WiFi actualmente apagado')

    def setting_turn_ES_wifi(self):
        status = self.d(text='Sí', className='android.widget.Switch').checked
        if status:
            self.d(text='Sí', className='android.widget.Switch').click()
        else:
            print('WiFi actualmente apagado')

    def settings_wifi_test(self, on_off):
        self.initial_state()
        self.adb_open_settings()
        flag = False
        try:
            flag = self.d(text='Wireless & networks', className='android.widget.TextView').checked
            flag = True
        except:
            flag = False
        if flag:
            self.d(text='Wireless & networks', className='android.widget.TextView').click()
            if on_off == 'ON':
                self.d(text='Wi-Fi', className='android.widget.TextView').click()
                self.setting_turn_on_wifi()
            elif on_off == 'OFF':
                self.d(text='Wi-Fi', className='android.widget.TextView').click()
                self.setting_turn_off_wifi()
            time.sleep(3)
            self.d.press.home()
        else:
            self.d(text='Internet y red', className='android.widget.TextView').click()
            if on_off == 'ON':
                self.setting_turn_on_wifi()
            elif on_off == 'OFF':
                self.setting_turn_ES_wifi()
            time.sleep(3)
            self.d.press.home()

    def adb_claculator_SendText(self, number, delay=5):
        self.dial_calculator()
        time.sleep(3)
        self.dial_calculator_enter(number)
        time.sleep(delay)
        self.hang_up()

    def dial_calculator(self):
        if self.device:
            check_call(['adb', 'shell', 'monkey -p', 'com.android.calculator2', '1'])

    def dial_calculator_enter(self, number):
        if self.device:
            check_call(['adb', 'shell', 'input text', '\'' + number + '\'', ''])

    def ui_calculator(self, number, delay=5):
        self.initial_state()
        flag = False
        self.d(descriptionContains='Apps', className='android.widget.TextView').click()
        #self.d.swipe(500, 1500, 500, 200, 3)
        time.sleep(1)
        self.d(descriptionMatches='Calculator', className='android.widget.TextView').click()
        self.type_number_calculator(number);
        self.d(descriptionContains='equals', className='android.widget.ImageView').click()

    def type_number_calculator(self, number):
        for digit in number:
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            character = '{0}'.format(digit)
            if (character in numbers):
                self.d(text=character, className='android.widget.Button').click()
            else:
                if (character == 'X' or character == 'x' or character == '*'):
                    character = 'multiply'
                elif (digit == '/'):
                    character = 'divide'
                elif (digit == '-'):
                    character = 'minus'
                elif (digit == '+'):
                    character = 'plus'
                self.d(descriptionContains=character, className='android.widget.ImageView').click()


def check_list():
    output = check_output(['adb', 'devices'])
    lines = output.splitlines()[1:-1]
    if not lines or lines[0] == b'':
        return None
    else:
        return lines