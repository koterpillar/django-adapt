"""Settings module for test Django app."""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'tests.sample_app',
]

SECRET_KEY = 'irrelevant'
