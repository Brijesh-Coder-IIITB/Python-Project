class Device:
    def __init__(self, name, location, owner):
        self.name = name
        self.location = location
        self.status = 'off'
        self.owner = owner

    def toggle_power(self, status):
        self.status = 'on' if status else 'off'
        return True

    def to_dict(self):
        return {
            'name': self.name,
            'location': self.location,
            'status': self.status,
            'owner':self.owner
        }

    @classmethod
    def from_dict(cls, data):
        device = cls(data['name'], data.get('location', 'Unknown'),data.get('owner'))
        device.status = data.get('status', 'off')
        return device