'''
All this does it call the Controller functions.
'''
from visualizer.control import Controller

controller = Controller()

def update():
    controller.update()

controller.start()