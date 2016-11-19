from configparser import ConfigParser

secrets = ConfigParser()
if len(secrets.read('secrets.ini')) == 0:
    raise RuntimeError('Could not open the secrets file')

def get_secret(section, key):
    return secrets.get(section, key)
