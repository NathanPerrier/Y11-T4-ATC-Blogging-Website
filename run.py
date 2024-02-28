from backend.main import *
from backend.config import *

app = create_app()

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        Tests.run_tests()
        app.run(debug=True, port=5000)