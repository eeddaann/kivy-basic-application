from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import accelerometer
import nxt.locator
import nxt.motor


class InputForm(BoxLayout):
    # Expose KV file Id's to python
    brickname = ObjectProperty()
    status = ObjectProperty()

    def __init__(self):
        # Form constructor
        super(InputForm, self).__init__()
        self.status.text = "please connect bluetooth device"

    def clean(self):
        self.brickname.text = ""  # on focus change the value to null string

    def start(self):
        try:  # try to connect to device
            self.roboLego = nxt.locator.find_one_brick(name=self.brickname.text)
            self.rMotor = nxt.Motor(self.roboLego, nxt.motor.PORT_C)
            self.lMotor = nxt.Motor(self.roboLego, nxt.motor.PORT_A)
            self.status.text = "Device connected"
        except:  # if connection failed
            self.status.text = "couldn't find bluetooth device"

    def forward(self):
        self.rMotor.run()  # all motors should run for moving forward
        self.lMotor.run()

    def stop(self):
        self.rMotor.brake()  # all motors should brake for stopping
        self.lMotor.brake()

    def right(self):
        self.lMotor.run()  # left motor go forward and right one, stops to achieve right turn
        self.rMotor.brake()

    def left(self):
        self.lMotor.brake() # right motor go forward and left one, stops to achieve right turn
        self.rMotor.run()


class KivyApp(App):
    pass


if __name__ == '__main__':
    KivyApp().run()
