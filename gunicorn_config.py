command = '/home/www/vk_test_task/venv/bin/gunicorn'
#pythonpath = '/home/www/code/project/project'
bind = '127.0.0.1:8001'
workers = 5
user = 'www'
limit_request_fields = 32000
limit_request_field_size = 0
raw_env = 'DJANGO_SETTINGS_MODULE=vk_test_task.settings'
