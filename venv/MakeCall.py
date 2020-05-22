# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import time

class llamada(object):
    def llamada_demo(self):
        account_sid = 'AC5e9cee07015dd5b5ed63b229009a89d2'
        auth_token = '83d23f9d35c7a753a28891b74ab6df5d'
        client = Client(account_sid, auth_token)

        call = client.calls.create(
                        machine_detection='DetectMessageEnd',
                        url='https://demo.twilio.com/welcome/voice/',
                        to='+524494026414',
                        from_='+14792754555'
                                )

        print(call.sid)