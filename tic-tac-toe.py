from view.MainScreen import MainScreen
from tkinter import Tk

root = Tk()
root.withdraw()

mainScreen: MainScreen = MainScreen()
mainScreen.on_execute()