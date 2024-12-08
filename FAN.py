from DEVICE import Device


class Fan(Device):
    def __init__(self, name, location, owner):
        super().__init__(name, location, owner)
        self.speed = 0

    def set_speed(self, speed):
        self.speed = speed

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'speed': self.speed
        })
        return data

    @classmethod
    def from_dict(cls, data):
        fan = super().from_dict(data)
        fan.speed = data.get('speed', 0)
        return fan
