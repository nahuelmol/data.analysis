import subprocess

def run():
    command = [
        'gunicorn',
        'mybackend.asgi:application',
        '-k', 'uvicorn.workers.UvicornWorker'
    ]

    subprocess.run(command)

if __name__ == '__main__':
    run()
