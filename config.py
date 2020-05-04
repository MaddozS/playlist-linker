import configparser

class Config:
    """
    Simple class that retrieves all the configurations from config.cfg file
    """
    client_id = None
    client_secret = None
    redirect_uri = None

    def __init__(self, file):
        
        # Reading config.cfg
        config = configparser.ConfigParser()
        config.read(file)

        # Setting up spotify configuration
        self.client_id = config.get('SPOTIFY', 'CLIENT_ID')
        self.client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
        self.redirect_uri = config.get('SPOTIFY', 'REDIRECT_URI')