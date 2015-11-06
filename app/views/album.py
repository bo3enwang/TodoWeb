# -*- coding:utf8 -*- 
__author__ = 'Zovven'
from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from flask.ext.login import login_required
from app.models import db, Album
from app.helps import slugify
# from sae.storage import Bucket
import time

album = Module(__name__)


# bucket = Bucket('zovvenimage')#获取bucket


@album.route('/list')
@login_required
def album_list():
    albums = Album.query.order_by(Album.upload_date.desc()).order_by(Album.type.desc()).all()
    return render_template('album/list.html', albums=albums)


@album.route('/add', methods=("GET", "POST"))
@login_required
def album_add():
    if request.method == 'POST':
        img_name = request.form['img_name']
        album_type = request.form['type']
        genkey = str(int(time.time()))
        uploaded_files = request.files.getlist("file")
        i = 1
        for f in uploaded_files:
            img_key = slugify(img_name) + genkey + str(i) + '.' + f.filename.split('.')[-1]  # 生成图片存储名
            bucket.put_object(img_key, f.read())
            img_url = bucket.generate_url(img_key)
            al = Album(img_name=img_name + '_' + str(i), img_key=img_key, img_url=img_url, type=album_type)
            db.session.add(al)
            i += 1
            print img_key
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
