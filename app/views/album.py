# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from sae.storage import Bucket, Connection
from app import saeconfig

album = Module(__name__)


@album.route('/list')
def album_list():
    if request.method == 'POST':
        c = Connection(accesskey=saeconfig['ACCESS_KEY'], secretkey=saeconfig['SECRET_KEY'], account='zovvenimage')
        bucket = c.get_bucket('img')
        imglist = bucket.list()
        return render_template('album/list.html', imglist=imglist)
