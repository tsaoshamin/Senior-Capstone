app = Flask(__name__)

from Capstone.views import aview
from Capstone.database import db_session

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
