# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
# from sae.storage import Bucket
# import sae.const

album = Module(__name__)


@album.route('/list')
def album_list():
    # bucket = Bucket('zovvenimage')
    # hhe = bucket.generate_url('274543-106.jpg')
    return render_template('album/list.html')
