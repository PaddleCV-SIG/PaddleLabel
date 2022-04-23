import os

from .serve import connexion_app


def run(): 
    port = int(os.environ.get("PORT", 17995))
    connexion_app.run(host="0.0.0.0", port=port, debug=True)

run()