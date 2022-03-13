import os

from .serve import connexion_app

# connexion_app.run(port=5000)

ON_HEROKU = os.environ.get('ON_HEROKU')
if ON_HEROKU:
    port = int(os.environ.get("PORT", 17995))
else:
    port = 5000
print("=-=-=-=-=", os.environ.get('ON_HEROKU'), port)

connexion_app.run(host='0.0.0.0', port=port, debug=True)
