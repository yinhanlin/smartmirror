import base64
import json
from flask import Blueprint, render_template, request, jsonify
from exts import mail
from flask_mail import Message
import requests

from models import IndoorClimate, OutdoorClimate, WeatherForecast

bp = Blueprint("DisInformation", __name__, url_prefix="/")
url = ' http://10.129.212.159:2023/test'
weather_req = 'https://restapi.amap.com/v3/weather/weatherInfo?key=96a0ca8c61138af5aa19f97bcac8de84&city=110108'


class Forecast:
    today = {}
    tomorrow = {}
    the_day_after = {}


@bp.route("/")
def index():
    indoor_env = IndoorClimate.query.filter_by(id=1).first()
    # 获取当前天气
    weather_base_url = weather_req + '&extensions=base'
    response_base = requests.get(weather_base_url)
    outdoor_base_msg = {}
    # 检查响应状态码
    if response_base.status_code == 200:
        # 解析JSON数据
        json_base_data = response_base.json()
        outdoor_base_msg = OutdoorClimate.from_json(json_base_data)
    else:
        # 请求失败，处理错误
        print('请求失败，response_base状态码:', response_base.status_code)
    # 获取预报天气
    weather_all_url = weather_req + '&extensions=all'
    response_all = requests.get(weather_all_url)
    forecast = Forecast()
    week_num = {'1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六', '7': '日'}
    weather_events = {
        '晴': 'qingtian', '少云': 'shaoyun', '晴间多云': 'duoyunzhuanqing', '多云': 'duoyun', '阴': 'yintian',
        '有风': 'baitianyoufeng', '平静': 'pingjing', '微风': 'weifeng', '和风': 'weifeng', '清风': 'feng',
        '强风/劲风': 'qiangfeng', '疾风': 'qiangfeng', '大风': 'dafeng', '烈风': 'liefeng',
        '风暴': 'liefeng', '狂爆风': 'liefeng', '飓风': 'redaifengbao', '热带风暴': 'redaifengbao',
        '霾': 'mai', '中度霾': 'mai', '重度霾': 'mai', '严重霾': 'mai', '热': 're', '冷': 'leng',
        '阵雨': 'zhenyu', '雷阵雨': 'leizhenyu', '雷阵雨并伴有冰雹': 'bingbao',
        '小雨': 'xiaoyu', '中雨': 'zhongyu', '大雨': 'dayu', '暴雨': 'baoyu', '大暴雨': 'baoyu', '特大暴雨': 'baoyu',
        '强阵雨': 'qiangzhenyu', '强雷阵雨': 'qiangleizhenyu', '极端降雨': 'jiduanjiangyu', '毛毛雨/细雨': 'xiaoyu',
        '雨': 'xiaoyu',
        '小雨-中雨': 'zhongyu', '中雨-大雨': 'dayu', '大雨-暴雨': 'baoyu', '暴雨-大暴雨': 'baoyu',
        '大暴雨-特大暴雨': 'baoyu',
        '雨雪天气': 'yujiaxue', '雨夹雪': 'yujiaxue', '阵雨夹雪': 'yujiaxue', '冻雨': 'bingbao',
        '雪': 'xiaoxue', '阵雪': 'zhenxue', '小雪': 'xiaoxue', '中雪': 'zhongxue', '大雪': 'daxue', '暴雪': 'baoxue',
        '小雪-中雪': 'zhongxue', '中雪-大雪': 'daxue', '大雪-暴雪': 'baoxue',
        '浮尘': 'fuchen', '扬沙': 'baitianyangsha', '沙尘暴': 'shachenbao', '强沙尘暴': 'shachenbao_1',
        '龙卷风': 'longjuanfeng',
        '雾': 'youwu', '浓雾': 'youwu', '强浓雾': 'youwu', '轻雾': 'youwu', '大雾': 'youwu', '特强浓雾': 'youwu'
    }
    # 检查响应状态码
    if response_all.status_code == 200:
        # 解析JSON数据
        json_all_data = response_all.json()
        json_casts = json_all_data.get('forecasts')
        count = 0
        forecasts = ["", "", ""]
        original_forecasts = json_casts[0].get('casts')
        for i in range(len(original_forecasts)):
            print(i)
            if i == 3:
                break
            forecasts[i] = WeatherForecast.from_json(original_forecasts[i])
        for cast in json_casts[0].get('casts'):
            if count == 0:
                forecast.today = WeatherForecast.from_json(cast)
                forecast.today.week = week_num[forecast.today.week]
                count = 1
            elif count == 1:
                forecast.tomorrow = WeatherForecast.from_json(cast)
                forecast.tomorrow.week = week_num[forecast.tomorrow.week]
                count = 2
            elif count == 2:
                forecast.the_day_after = WeatherForecast.from_json(cast)
                forecast.the_day_after.week = week_num[forecast.the_day_after.week]
                count = 3
            else:
                break
    else:
        # 请求失败，处理错误
        print('请求失败，response_all状态码:', response_all.status_code)
    # return "Success"

    return render_template('index.html', indoor_env=indoor_env,
                           weather_events=weather_events, outdoor_climate=outdoor_base_msg,
                           forecasts=forecasts, week_num=week_num)


@bp.route("/test", methods=["POST"])
def test():
    try:
        my_json = request.get_json()
        print(my_json)
        get_school = my_json.get("school")
        get_name = my_json.get("name")
        get_age = my_json.get("age")
        mydata = {"name": get_name, "age": get_age, "school": get_school}
        response = requests.post(url=url, data=json.dumps(mydata))
        return "response"
    except Exception as e:
        print(e)
        return jsonify(msg="Wrong")


@bp.route("/test1", methods=['POST'])
def the_test():
    with open(r'uploads/02b054679034407996be23ae2c556688.png', 'rb') as f:
        res = base64.b64encode(f.read())
        return res


@bp.route("/mail/test")
def mail_test():
    message = Message(subject="邮箱测试", recipients=["177574296@qq.com"], body="这是一条测试邮件")
    mail.send(message)
    return "邮件发送成功"


@bp.route("/test2")
def bs_test():
    return render_template('test.html')
