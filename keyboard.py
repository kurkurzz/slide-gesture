from pynput.keyboard import Key, Controller, Listener

keyboard = Controller()

def right_key():
	keyboard.press(Key.right)
	keyboard.release(Key.right)

def left_key():
	keyboard.press(Key.left)
	keyboard.release(Key.left)
