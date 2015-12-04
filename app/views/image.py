# -*- coding:utf8 -*- 
__author__ = 'Zovven'

from flask import Module, render_template, flash, redirect, url_for, request, g, jsonify
from flask.ext.login import login_required
from app.models import db, Image
from app.helps import slugify
import time
# sae获取图片仓库,上传时解开
# from sae.storage import Bucket
image = Module(__name__)


# sae获取图片仓库,上传时解开
# bucket = Bucket('zovvenimage')

@image.route('')
@login_required
def image_list():
    images = Image.query.order_by(Image.upload_date.desc()).order_by(Image.img_type.desc()).all()
    return render_template('admin/imageList.html', images=images)


@image.route('/add', methods=("GET", "POST"))
@login_required
def image_add():
    if request.method == 'POST':
        img_name = request.form['img_name']
        img_type = request.form['img_type']
        gen_key = str(int(time.time()))
        uploaded_files = request.files.getlist("file")
        i = 1
        for f in uploaded_files:
            img_key = slugify(img_name) + gen_key + str(i) + '.' + f.filename.split('.')[-1]  # 生成图片存储名
            bucket.put_object(img_key, f.read())
            img_url = bucket.generate_url(img_key)
            _image = Image(img_name=img_name + '_' + str(i), img_key=img_key, img_url=img_url, img_type=img_type)
            db.session.add(_image)
            i += 1
        db.session.commit()
        flash("新增图片成功", "success")
        return redirect(url_for('image.image_list'))
    return render_template('admin/imageEdit.html')


@image.route("/<int:img_id>/delete/", methods=("POST",))
@login_required
def delete(img_id):
    _image = Image.query.get_or_404(img_id)
    bucket.delete_object(_image.img_key)
    db.session.delete(_image)
    db.session.commit()
    flash("删除图片成功", "success")
    return jsonify(success=True,
                   redirect_url=url_for('image.image_list'))
