from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openpyxl



app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACH_MODIFICATIONS'] = True


db = SQLAlchemy(app)

class utility(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column("name", db.String(200),nullable=False)
    param = db.Column(db.Integer)

    def __init__(self,name,param):
        self.name = name
        self.param = param

class engineers(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("name", db.String(200))
    province = db.Column(db.String(200))
    major = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    cell = db.Column(db.String(200))
    qq = db.Column(db.String(200))
    wechat = db.Column(db.String(200))
    registered_unit = db.Column(db.String(200))
    previous_unit = db.Column(db.String(200))
    registered = db.Column(db.String(200))
    note = db.Column(db.String(20000))

    def __init__(self,_id,name,province,major,phone,cell,qq,wechat,previous_unit,registered_unit,registered,note):
        self._id = _id
        self.name = name if name != None else '无姓名'#0
        self.province = province if province != None else '无省份' #1
        self.major = major if major != None else '无专业'#2
        self.phone = phone if phone != None else '无座机'#3
        self.cell = cell if cell != None else '无手机'#4
        self.qq = qq if qq != None else '无qq'#5
        self.wechat = wechat if wechat != None else '无微信'#6
        self.registered_unit = registered_unit if registered_unit != None else '无注册单位'#7
        self.previous_unit = previous_unit if previous_unit != None else '无前单位'#8
        self.registered = '否' if registered == None else registered #9
        self.note = note if note != None else '无备注'#10


def inject():
    wb = openpyxl.load_workbook('示范表格.xlsx')
    ws = wb.active
    _id = utility.query.filter_by(name="Last_person_id").first().param
    for row in range(2,len(list(ws.rows))+1):
        db.session.add(engineers(_id,*[e.value for e in ws[row]]))
        _id += 1
    utility.query.filter_by(name="Last_person_id").first().param = _id
    db.session.commit()
if __name__ == "__main__":
    db.create_all()
    db.session.commit()
    if utility.query.filter_by(name="Last_person_id").first() == None:
        db.session.add(utility("Last_person_id",1))
    inject()
    app.run(debug=True,host='0.0.0.0', port=8080)