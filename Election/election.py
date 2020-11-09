from datetime import datetime
 
from flask import Flask, render_template
from views import index

app = Flask(__name__)
app.config.from_object('default_config')
for logger in app.config.get('LOGGERS', ()):
    app.logger.addHandler(logger)

JINJA_GLOBAL_FUNCTIONS = {
    
}

app.jinja_env.globals.update(JINJA_GLOBAL_FUNCTIONS)

app.register_blueprint(index.index_page, url_prefix='/')

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    from models import db_commit, db_end
    db_commit()
    db_end()
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
