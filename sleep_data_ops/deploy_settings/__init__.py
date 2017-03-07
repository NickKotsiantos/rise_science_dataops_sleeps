from sleep_data_ops.settings import * 

DEBUG = False
TEMPLATE_DEBUG = DEBUG


ALLOWED_HOSTS = [
'localhost',
'.herokuapp.com',
]


SECRET_KEY = get_env_variable("SECRET_KEY")