from config import server
from route import Routes

app = server.app

routes = Routes()
if __name__ == "__main__":
    app.run()