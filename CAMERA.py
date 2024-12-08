from DEVICE import Device

class SecurityCamera(Device):
    def __init__(self, name, location, owner):
        super().__init__(name, location, owner)
        self.recording = False
        self.resolution = '1080p'

    def toggle_recording(self, status):
        self.recording = status

    def set_resolution(self, resolution):
        self.resolution = resolution

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'recording': self.recording,
            'resolution': self.resolution
        })
        return data

    @classmethod
    def from_dict(cls, data):
        camera = super().from_dict(data)
        camera.recording = data.get('recording', False)
        camera.resolution = data.get('resolution', '1080p')
        return camera