from flask import Blueprint, render_template, redirect, url_for
from flask import request
import config
from exts import db, csrf
import os
from models import Cloth

bp = Blueprint("ClothChange", __name__, url_prefix="/cloth/")


@bp.route('/')
def my_wardrobes():
    clothes = Cloth.query.all()
    # return "success"
    return render_template('wardrobes.html', clothes=clothes)


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'file' in request.files:
        f = request.files.get('file')  # 获取图片文件对象
        if not f:
            return 'Invalid image.', 400
        filename = f.filename  # 获取文件名
        f.save(os.path.join(config.CLOTH_UPLOAD_PATH, filename))
        # 保存图片文件
        last_cloth = Cloth.query.order_by(-Cloth.uid).first()
        cloth = Cloth(
            cloth_name=filename,
            uid=last_cloth.uid + 1,
            status=False
        )
        db.session.add(cloth)
        db.session.commit()
    return render_template('upload.html')


@bp.route('/myconsole')
def console():
    return redirect(url_for('ClothChange.my_wardrobes'))


@bp.route('/myconsole/<int:uid>/')
def detail_page(uid):
    cloth = Cloth.query.filter_by(uid=uid).first()
    return render_template('myconsole.html', cloth=cloth)


@csrf.exempt
@bp.route('/status/<cloth_name>', methods=['POST'])
def to_cloth(cloth_name):
    cloth = Cloth.query.filter_by(cloth_name=cloth_name).first()
    if not cloth.status:
        worn_cloth = Cloth.query.filter_by(status=True).first()
        if worn_cloth:
            worn_cloth.status = False
            db.session.add(worn_cloth)
    cloth.status = not cloth.status
    db.session.add(cloth)
    db.session.commit()
    return render_template('myconsole.html', cloth=cloth)
