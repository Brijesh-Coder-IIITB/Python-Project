from DEVICE import Device

class Light(Device):
    def __init__(self, name, location, owner):
        super().__init__(name, location, owner)
        self.brightness = 100
        self.color = '#FFFFFF'

    def set_brightness(self, brightness):
        self.brightness = brightness

    def set_color(self, color):
        self.color = color

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'brightness': self.brightness,
            'color': self.color
        })
        return data

    @classmethod
    def from_dict(cls, data):
        light = super().from_dict(data)
        light.brightness = data.get('brightness', 100)
        light.color = data.get('color', '#FFFFFF')
        return light