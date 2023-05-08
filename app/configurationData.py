class configurationData:
    def __init__(self, tolerance, targetTemp):
        self.configurationData = {"tolerance": tolerance, "targetTemp": targetTemp}
    def get_configurationData(self):
        return self.configurationData
    def set_configurationData(self,tolerance, targetTemp):
        print(tolerance, targetTemp)
        self.configurationData = {"tolerance": tolerance, "targetTemp": targetTemp}
        print(self.configurationData['tolerance'], self.configurationData['targetTemp'])
