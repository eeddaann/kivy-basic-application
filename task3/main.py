__author__ = 'Guinea Pig'

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from plyer import accelerometer


class Form(BoxLayout):
	"Expose KV file Id's to python"
	lX = ObjectProperty()
	lY = ObjectProperty()
	lZ = ObjectProperty()
	but = ObjectProperty()
	lStatus = ObjectProperty()


	def __init__(self):
		"Form constructor"
		super(Form, self).__init__()
		self.sensorEnabled = False


	def do_toggle(self):
		try:
			if not self.sensorEnabled:
				accelerometer.enable()
				# Enabling repetitive calls to get_acceleration
				# method every quarter of a second
				Clock.schedule_interval(self.get_acceleration, 1 / 4.)
				self.sensorEnabled = True
				# Change button text
				self.but.text = "Stop Accelerometer"
			else:
				accelerometer.disable()
				Clock.unschedule(self.get_acceleration)
				self.sensorEnabled = False
				self.but.text = "Start Accelerometer"
		except NotImplementedError:
			self.lStatus.text = "Accelerometer is not implemented for your platform"


	def get_acceleration(self, dt):
		val = accelerometer.acceleration[:3]
		if (not val == (None, None, None)):
			self.lX.text = "X: " + str(round(val[0], 2))
			self.lY.text = "Y: " + str(round(val[1], 2))
			self.lZ.text = "Z: " + str(round(val[2], 2))


class AccelApp(App):
	pass


if __name__ == '__main__':
	AccelApp().run()