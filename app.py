from flask import Flask

from server import app


def create_app(app: Flask):
    return app.run()


if __name__ == '__main__':
    create_app(app)
