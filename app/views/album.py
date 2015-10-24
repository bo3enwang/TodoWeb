# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from flask.ext.login import login_required
from app.models import db, Album
# from sae.storage import Bucket
# import sae.const
import time

album = Module(__name__)
# bucket = Bucket('zovvenimage')#获取bucket

@album.route('/list')
@login_required
def album_list():
    albums = Album.query.all()
    return render_template('album/list.html', albums=albums)


@album.route('/add', methods=("GET", "POST"))
@login_required
def album_add():
    if request.method == 'POST':
        img_name = request.form['img_name']
        f = request.files['file']
        genkey = str(int(time.time()))
        img_key = img_name + genkey + '.'+f.filename.split('.')[-1]#生成图片存储名
        bucket.put_object(img_key, f.read())
        img_url = bucket.generate_url(img_key)
        al = Album(img_name=img_name, img_key=img_key, img_url=img_url)
        db.session.add(al)
        db.session.commit()
        flash("新增图片成功", "success")
        return redirect(url_for('album.album_list'))
    return render_template('album/upload.html')


@album.route("/<int:album_id>/delete/", methods=("POST",))
@login_required
def delete(album_id):
    al = Album.query.get_or_404(album_id)
    bucket.delete_object(al.img_key)
    db.session.delete(al)
    db.session.commit()
    flash("删除图片成功", "success")
    return jsonify(success=True,
                   redirect_url=url_for('album.album_list'))
