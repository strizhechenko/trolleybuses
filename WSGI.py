import os
from __init__ import APP

APP.debug = False

if __name__ == "__main__":
    APP.run('0.0.0.0', port=os.environ.get('PORT', 5000))
