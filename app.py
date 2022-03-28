#!/usr/bin/python3
from ws_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='192.168.42.113', port=5000)

    # koza koza koza
