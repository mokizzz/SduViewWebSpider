from os import popen

print('Server opened.')
result = popen('python manage.py runserver 127.0.0.1:8000')
res = result.read()
for line in res.splitlines():
    print(line)
