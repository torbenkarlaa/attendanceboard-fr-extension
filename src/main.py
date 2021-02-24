from input_handler import InputHandler
from trainer import Trainer

print('Starting facial recognition extension \n')

trainer = Trainer()
trainer.train()

input_handler = InputHandler()
input_handler.start()
