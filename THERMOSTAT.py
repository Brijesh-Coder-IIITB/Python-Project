from DEVICE import Device

class Thermostat(Device):
    def __init__(self, name, location, owner):
        super().__init__(name, location, owner)
        self.temperature = 72
        self.mode = 'auto'

    def set_temperature(self, temp):
        self.temperature = temp

    def set_mode(self, mode):
        self.mode = mode

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'temperature': self.temperature,
            'mode': self.mode
        })
        return data

    @classmethod
    def from_dict(cls, data):
        thermostat = super().from_dict(data)
        thermostat.temperature = data.get('temperature', 72)
        thermostat.mode = data.get('mode', 'auto')
        return thermostat