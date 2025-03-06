from flask import Flask
from routes.activity_routes import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix="")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)