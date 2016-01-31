import os
from __init__ import app

app.debug = False

if __name__ == "__main__":
    app.run('0.0.0.0', port=os.environ.get('PORT', 5000))
