from app import create_app

APP = create_app()
import logging
logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    APP.run(debug=True, port=5000)