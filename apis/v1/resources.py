import os
from flask import jsonify, request, url_for, redirect
from apis.v1 import api_v1
from exts import db
from models import IndoorClimate, OutdoorClimate, Cloth

# 目标计算机的IP地址和端口号
target_ip = '192.168.137.1'
target_port = 6666
url = f"http://{target_ip}:{target_port}/"


@api_v1.route('/post/indoor', methods=['POST'])
def get_indoor_msg():
    indoor_msg = IndoorClimate.from_json(request.json)
    # print(indoor_msg)
    db.session.add(indoor_msg)
    db.session.commit()
    return jsonify(status="success of indoor_msg")


@api_v1.route('/post/outdoor', methods=['POST'])
def get_outdoor_msg():
    outdoor_msg = OutdoorClimate.from_json(request.json)
    # print(outdoor_msg)
    db.session.add(outdoor_msg)
    db.session.commit()
    return jsonify(status="success of outdoor_msg")


@api_v1.route('/post/clothes/', methods=['POST'])
def get_cloth_name():
    cloth = Cloth.query.filter_by(status=True).first()
    if not cloth:
        return jsonify(cloth_name=None)
    else:
        return jsonify(cloth_name=cloth.cloth_name)


@api_v1.route('/post/clothes/<cloth_name>', methods=['POST'])
def to_cloth(cloth_name):
    cloth = Cloth.query.filter_by(cloth_name=cloth_name).first()
    cloth_file = Cloth.to_json(cloth)
    return jsonify(cloth_file)


@api_v1.route('/delete/clothes/<cloth_name>', methods=['POST'])
def delete_cloth(cloth_name):
    print("删除请求获取！")
    cloth = Cloth.query.filter_by(cloth_name=cloth_name).first()
    os.remove("static/images/uploads/" + cloth_name)
    db.session.delete(cloth)
    db.session.commit()
    print("删除成功！")
    return redirect(url_for('ClothChange.my_wardrobes'))
