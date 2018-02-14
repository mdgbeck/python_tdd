if 'DJANGO_DEBUG_FALSE' in os.environ:
    DEBUG = False
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
    ALLOWED_HOSTS = [os.environ['SITENAME']]

else:
    DEBUG = True
    SECRET_KEY = 'insecure-key-for-dev'
    ALLOWED_HOSTS = []
