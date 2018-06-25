#run.py
"""
    This file run the api.
"""
import os
from api import create_app

config_name = os.getenv('API_SETTINGS')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
