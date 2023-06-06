import base64
from exts import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)


class Cloth(db.Model):
    __tablename__ = "cloth"
    uid = db.Column(db.Integer, primary_key=True)
    cloth_name = db.Column(db.String(100), nullable=False)
    coor = db.Column(db.Text)
    status = db.Column(db.Boolean)

    def to_json(self):
        with open(r'static/images/uploads/' + self.cloth_name, 'rb') as f:
            res = str(base64.b64encode(f.read()))
        json_cloth = {
            'cloth_name': self.cloth_name,
            'coor': self.coor,
            'cloth': res
        }
        return json_cloth


class IndoorClimate(db.Model):
    __tablename__ = "indoor_climate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime)
    temp_in = db.Column(db.Float, nullable=False)
    humi_in = db.Column(db.Float, nullable=False)
    api_in = db.Column(db.Float)

    @staticmethod
    def from_json(json_in):
        time = datetime.now()
        temp_in = json_in.get('temp_in')
        humi_in = json_in.get('humi_in')
        api_in = json_in.get('api_in')
        # 待加入：错误识别
        return IndoorClimate(time=time, temp_in=temp_in, humi_in=humi_in, api_in=api_in)


class OutdoorClimate(db.Model):
    __tablename__ = "outdoor_climate"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime)
    weather = db.Column(db.String(100))
    temp_out = db.Column(db.Float, nullable=False)
    humi_out = db.Column(db.Float, nullable=False)
    pressure_out = db.Column(db.String(10), nullable=False)

    @staticmethod
    def from_json(json_out):
        weather = json_out.get('lives')[0].get('weather')
        temp_out = json_out.get('lives')[0].get('temperature_float')
        humi_out = json_out.get('lives')[0].get('humidity_float')
        pressure_out = json_out.get('lives')[0].get('windpower')
        time = datetime.now()
        # 待加入：错误识别
        return OutdoorClimate(time=time, weather=weather, temp_out=temp_out,
                              humi_out=humi_out, pressure_out=pressure_out)


class WeatherForecast(db.Model):
    __tablename__ = "weather_forecast"
    date = db.Column(db.String(50), primary_key=True)
    week = db.Column(db.Integer)
    day_weather = db.Column(db.String(50))
    night_weather = db.Column(db.String(50))
    day_temp = db.Column(db.Float)
    night_temp = db.Column(db.Float)

    @staticmethod
    def from_json(json_forecast):
        date = json_forecast.get('date')
        week = json_forecast.get('week')
        day_weather = json_forecast.get('dayweather')
        night_weather = json_forecast.get('nightweather')
        day_temp = json_forecast.get('daytemp_float')
        night_temp = json_forecast.get('nighttemp_float')
        # 待加入：错误识别
        return WeatherForecast(date=date, week=week, day_weather=day_weather, night_weather=night_weather,
                               day_temp=day_temp, night_temp=night_temp)
