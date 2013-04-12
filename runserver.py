

# app as application for wsgi
from Capstone import app as application



#application.run(host='0.0.0.0', port=80)
application.run(debug=True)