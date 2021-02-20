import threading

from connector import Connector
from input_handler import InputHandler

print('Starting facial recognition extension \n')

connector = Connector()
listener_thread = threading.Thread(target=connector.subscribe_person_update)
listener_thread.start()

input_handler = InputHandler()
input_handler.start()
