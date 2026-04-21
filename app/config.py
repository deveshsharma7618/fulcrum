
class DevConfig:
    def __init__(self):
        self.ENV = "development"
        self.DEBUG = True
        self.PORT = 3000
        self.HOST = '0.0.0.0'

class ProductionConfig:
    def __init__(self):
        self.ENV = "production"
        self.DEBUG = False
        self.PORT = 80
        self.HOST = '0.0.0.0'
        
