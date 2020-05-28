from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

from app2 import app as app1
from flask_main import app as app2

application = DispatcherMiddleware(app2, {
    '/app1': app1.server
})

if __name__ == '__main__':
    run_simple('localhost', 8050, application)