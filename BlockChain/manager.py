from flask_script import Manager
import blockchain_server

def configure_app():
    app = blockchain_server.init_app()
    return app

app = configure_app()

manager = Manager(app)

if __name__ == '__main__':
    manager.run()