from os import popen

print('Server opened.')
result = popen('python manage.py runserver 0.0.0.0:8000')
res = result.read()
for line in res.splitlines():
    print(line)
