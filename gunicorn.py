from userApi import settings

bind = f'web:{settings.SERVER_PORT}'
workers = 2
threads = 4
max_requests = 1000
timeout = 30
