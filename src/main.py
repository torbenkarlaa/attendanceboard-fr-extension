from assets.messages import Messages
from input_handler import InputHandler
from trainer import Trainer

print(Messages.HEADER)
print(Messages.MAIN_START)

trainer = Trainer()
trainer.train()

input_handler = InputHandler()
input_handler.start()
