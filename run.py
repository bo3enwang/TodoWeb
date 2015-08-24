# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from app import create_app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)