from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField,IntegerField,SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,InputRequired
from app.auth.models import User,Lend_log,Location,Report,Return_log,Umbrella




def sid_exists(form, field):
    s_id = User.query.filter_by(s_id=field.data).first()
    if s_id:
        raise ValidationError('學號已註冊')

def uid_exists(form, field):
    u_id = Umbrella.query.filter_by(u_id=field.data).first()
    if not u_id:
        raise ValidationError('雨傘編號不存在')



class RegistrationForm(Form):
    s_id=StringField('學號',validators=[DataRequired(),Length(max=9,message='請輸入學號，九位數字')	,sid_exists])
    name = StringField('姓名', validators=[DataRequired(), Length(1,15, message='1-15字')])
    # email = StringField('E-mail', validators=[DataRequired(), Email(), email_exists])
    major=SelectField('科系',validators=[DataRequired('請選擇科系')], choices=[('資科','資科'),('統計','統計'),('資管','資管'),('國貿','國貿'),('經濟','經濟'),('地政','地政'),('財政','財政'),('教育','教育'),('應數','應數'),('金融','金融'),('土語','土語')],default=1)
    # print('major',major)
    password = PasswordField('密碼', validators=[DataRequired()])
    confirm = PasswordField('再次輸入密碼', validators=[DataRequired(), EqualTo('password', message='密碼必須相同,請再次輸入')])
    submit = SubmitField('註冊')

class LoginForm(Form):
    sid=StringField('學號',validators=[DataRequired(),Length(9,message='請輸入學號，九位數字')])
    password = PasswordField('密碼', validators=[DataRequired()])
    stay_loggedin = BooleanField('記住我')
    submit = SubmitField('登入')

class HomeForm(Form):
    h_return = SubmitField(label='雨傘歸還')
    h_search = SubmitField(label='雨傘查詢')
    h_report = SubmitField(label='問題回報')

class SearchlocForm(Form):

    loc_id=SelectField('地點',validators=[DataRequired('請選擇地點')], choices=[('正門', '正門'), ('社資中心', '社資中心'), ('井塘樓', '井塘樓'), ('憩賢樓', '憩賢樓'), ('學思樓', '學思樓'), ('逸仙樓', '逸仙樓'), ('中正圖書館', '中正圖書館'), ('志希樓', '志希樓'), ('果夫樓', '果夫樓'), ('校友服務中心', '校友服務中心'), ('風樓', '風樓'), ('四維堂', '四維堂'), ('學生活動中心', '學生活動中心'), ('樂活小舖', '樂活小舖'), ('資訊大樓', '資訊大樓'), ('健康中心', '健康中心'), ('行政大樓', '行政大樓'), ('政大書城', '政大書城'), ('新聞館', '新聞館'), ('大智樓', '大智樓'), ('大仁樓', '大仁樓'), ('大勇樓', '大勇樓'), ('收發室', '收發室'), ('游泳館', '游泳館'), ('體育館', '體育館'), ('研究大樓', '研究大樓'), ('商學院館', '商學院館'), ('綜合院館', '綜合院館'), ('傳播學院', '傳播學院'), ('道藩樓', '道藩樓'), ('百年樓', '百年樓'), ('季陶樓', '季陶樓'), ('國際大樓', '國際大樓'), ('藝文中心', '藝文中心'), ('藝文中心大禮堂', '藝文中心大禮堂'), ('政大實幼', '政大實幼'), ('莊敬一舍', '莊敬一舍'), ('莊敬二舍', '莊敬二舍'), ('莊敬三舍', '莊敬三舍'), ('莊敬四舍', '莊敬四舍'), ('莊敬五、六舍', '莊敬五、六舍'), ('莊敬七、八舍', '莊敬七、八舍'), ('莊敬九舍', '莊敬九舍'), ('自強五、六舍', '自強五、六舍'), ('自強七、八舍', '自強七、八舍'), ('自強一、二、三舍', '自強一、二、三舍'), ('自強九舍', '自強九舍'), ('玫苑', '玫苑'), ('政大實小', '政大實小'), ('自強十舍', '自強十舍'), ('研創中心', '研創中心')],default=1)

    submit = SubmitField('查詢')

class LendForm(Form):
    submit = SubmitField('借用')

class DeleteForm(Form):
    submit = SubmitField('刪除')


class ReturnForm(Form):
    uid=IntegerField('雨傘編號',validators=[DataRequired(),uid_exists])

    loc_id=SelectField('地點',validators=[DataRequired('請選擇地點')], choices=[('正門', '正門'), ('社資中心', '社資中心'), ('井塘樓', '井塘樓'), ('憩賢樓', '憩賢樓'), ('學思樓', '學思樓'), ('逸仙樓', '逸仙樓'), ('中正圖書館', '中正圖書館'), ('志希樓', '志希樓'), ('果夫樓', '果夫樓'), ('校友服務中心', '校友服務中心'), ('風樓', '風樓'), ('四維堂', '四維堂'), ('學生活動中心', '學生活動中心'), ('樂活小舖', '樂活小舖'), ('資訊大樓', '資訊大樓'), ('健康中心', '健康中心'), ('行政大樓', '行政大樓'), ('政大書城', '政大書城'), ('新聞館', '新聞館'), ('大智樓', '大智樓'), ('大仁樓', '大仁樓'), ('大勇樓', '大勇樓'), ('收發室', '收發室'), ('游泳館', '游泳館'), ('體育館', '體育館'), ('研究大樓', '研究大樓'), ('商學院館', '商學院館'), ('綜合院館', '綜合院館'), ('傳播學院', '傳播學院'), ('道藩樓', '道藩樓'), ('百年樓', '百年樓'), ('季陶樓', '季陶樓'), ('國際大樓', '國際大樓'), ('藝文中心', '藝文中心'), ('藝文中心大禮堂', '藝文中心大禮堂'), ('政大實幼', '政大實幼'), ('莊敬一舍', '莊敬一舍'), ('莊敬二舍', '莊敬二舍'), ('莊敬三舍', '莊敬三舍'), ('莊敬四舍', '莊敬四舍'), ('莊敬五、六舍', '莊敬五、六舍'), ('莊敬七、八舍', '莊敬七、八舍'), ('莊敬九舍', '莊敬九舍'), ('自強五、六舍', '自強五、六舍'), ('自強七、八舍', '自強七、八舍'), ('自強一、二、三舍', '自強一、二、三舍'), ('自強九舍', '自強九舍'), ('玫苑', '玫苑'), ('政大實小', '政大實小'), ('自強十舍', '自強十舍'), ('研創中心', '研創中心')],default=1)

    submit = SubmitField('歸還')

class ReportForm(Form):
    uid=IntegerField('雨傘編號',validators=[DataRequired(),uid_exists])
    status=SelectField('雨傘狀態',validators=[DataRequired('請選擇雨傘狀態')], choices=[('拾獲','拾獲'),('損壞','損壞'),('遺失','遺失')],default=1)


    loc_id=SelectField('地點',validators=[DataRequired('請選擇地點')], choices=[('正門', '正門'), ('社資中心', '社資中心'), ('井塘樓', '井塘樓'), ('憩賢樓', '憩賢樓'), ('學思樓', '學思樓'), ('逸仙樓', '逸仙樓'), ('中正圖書館', '中正圖書館'), ('志希樓', '志希樓'), ('果夫樓', '果夫樓'), ('校友服務中心', '校友服務中心'), ('風樓', '風樓'), ('四維堂', '四維堂'), ('學生活動中心', '學生活動中心'), ('樂活小舖', '樂活小舖'), ('資訊大樓', '資訊大樓'), ('健康中心', '健康中心'), ('行政大樓', '行政大樓'), ('政大書城', '政大書城'), ('新聞館', '新聞館'), ('大智樓', '大智樓'), ('大仁樓', '大仁樓'), ('大勇樓', '大勇樓'), ('收發室', '收發室'), ('游泳館', '游泳館'), ('體育館', '體育館'), ('研究大樓', '研究大樓'), ('商學院館', '商學院館'), ('綜合院館', '綜合院館'), ('傳播學院', '傳播學院'), ('道藩樓', '道藩樓'), ('百年樓', '百年樓'), ('季陶樓', '季陶樓'), ('國際大樓', '國際大樓'), ('藝文中心', '藝文中心'), ('藝文中心大禮堂', '藝文中心大禮堂'), ('政大實幼', '政大實幼'), ('莊敬一舍', '莊敬一舍'), ('莊敬二舍', '莊敬二舍'), ('莊敬三舍', '莊敬三舍'), ('莊敬四舍', '莊敬四舍'), ('莊敬五、六舍', '莊敬五、六舍'), ('莊敬七、八舍', '莊敬七、八舍'), ('莊敬九舍', '莊敬九舍'), ('自強五、六舍', '自強五、六舍'), ('自強七、八舍', '自強七、八舍'), ('自強一、二、三舍', '自強一、二、三舍'), ('自強九舍', '自強九舍'), ('玫苑', '玫苑'), ('政大實小', '政大實小'), ('自強十舍', '自強十舍'), ('研創中心', '研創中心')],default=1)

    submit = SubmitField('回報')

