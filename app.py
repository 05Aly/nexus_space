import os
import sys
from pathlib import Path

# Add project root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()

class VercelPathFixer:
    """
    Middleware to restore the original request path from Vercel's rewrite headers
    or strip Vercel's serverless function prefix (/api/index) so Django URL routing works.
    """
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        original_uri = environ.get('HTTP_X_FORWARDED_URI') or environ.get('HTTP_X_MATCHED_PATH')
        if original_uri:
            environ['PATH_INFO'] = original_uri.split('?')[0]
        else:
            path = environ.get('PATH_INFO', '')
            for prefix in ['/api/index', 'api/index', '/api', 'api']:
                if path.startswith(prefix):
                    path = path[len(prefix):]
                    break
            environ['PATH_INFO'] = path if path.startswith('/') else ('/' + path if path else '/')

        return self.application(environ, start_response)

app = VercelPathFixer(django_app)
application = app
