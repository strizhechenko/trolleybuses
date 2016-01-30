import os
from __init__ import app

app.debug = False

if __name__ == "__main__":
    # app.run(port=os.environ.get('PORT', 5000))
    app.run(port=80)
