from app.temperatures import temperatures

class Temperature_storage:
    def __init__(self):
        self.temperatures: temperatures()

    def get_temperatures(self):
        return self.temperatures
    
    def set_temperatures(self, temperatures):
        self.temperatures = temperatures