import os
from api import create_app

CURR_ENV = os.environ
if 'FLASK_ENV' not in CURR_ENV:
    config_name = 'development'
else:
    config_name = CURR_ENV['FLASK_ENV']
app = create_app(config_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
