from flask import render_template, request, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm, HomeForm, LendForm, ReturnForm, ReportForm, SearchlocForm,DeleteForm
from app.auth import authentication
from app.auth.models import User, Lend_log, Location, Report, Return_log, Umbrella
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from sqlalchemy import and_,or_
from datetime import datetime


@authentication.route('/register', methods=['GET', 'post'])
def register_user():

    if current_user.is_authenticated:
        flash('你已經登入')
        return redirect(url_for('authentication.homepage'))
    form = RegistrationForm(request.form)

    if request.method == 'POST' and form.validate_on_submit():
        User.create_user(
            u_s_id=form.s_id.data,
            u_name=form.name.data,
            u_major=form.major.data,
            u_mail=form.s_id.data+'@nccu.edu.tw',
            u_state='正常',
            u_use_count=0,
            u_foul_count=0,
            u_password=form.password.data

        )

        flash("註冊成功")
        return redirect(url_for('authentication.log_in_user'))

    return render_template('registration.html', form=form)


@authentication.route('/')
def index():
    return redirect(url_for('authentication.log_in_user'))


@authentication.route('/login', methods=['GET', 'POST'])
def log_in_user():
    if current_user.is_authenticated:
        flash('你已經登入')
        return redirect(url_for('authentication.homepage'))
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user1 = User.query.filter_by(s_id=form.sid.data).first()

        print('user1', user1, form.stay_loggedin.data, type(user1))

        if not user1 or not user1.check_password(form.password.data):
            flash("學號或密碼錯誤")
            return redirect(url_for('authentication.log_in_user'))

        login_user(user1, form.stay_loggedin.data)
        return(redirect(url_for('authentication.homepage')))

    return render_template('login.html', form=form)


@authentication.route('/homepage', methods=['GET', 'POST'])
def homepage():
    getuser= User.query.filter_by(s_id=current_user.s_id).first()
        

    if '使用中' in getuser.state :
        getu_id1 = Lend_log.query.filter_by(s_id=current_user.s_id)[-1].u_id
        getlen = Lend_log.query.filter_by(s_id=current_user.s_id)[-1]

        now = datetime.now()
        data1 = now-getlen.l_time
        lending_time=(data1.total_seconds()/60)/60/24
        print('lending_time',lending_time,type(lending_time))
        if lending_time >=3:
            flash('你已借用雨傘三天，麻煩請歸還！已停權')
            getuser.state='使用中(停權)'

            db.session.commit()
        elif lending_time >=2:
            flash('你已借用雨傘兩天，請儘早歸還')
        elif lending_time >=1:
            flash('你已借用雨傘一天，請儘早歸還')
    else:
        getu_id1='0'

    if request.method == 'POST':
        
        
        
        if request.values['h_search'] == '雨傘查詢':
            return redirect(url_for('authentication.searchloc'))
        elif request.values['h_search'] == '雨傘歸還':
            return redirect(url_for('authentication.returnpage'))
        elif request.values['h_search'] == '問題回報':
            return redirect(url_for('authentication.report'))



    return render_template('homepage.html', getu_id1=getu_id1)

@authentication.route('/deletepage', methods=['GET', 'POST'])
def deletepage():
    form = DeleteForm(request.form)
    getumbrella = Umbrella.query.filter(or_(Umbrella.u_status == '遺失', Umbrella.u_status == '損壞')).all()

    getlocucount = Umbrella.query.filter(or_(Umbrella.u_status == '遺失', Umbrella.u_status == '損壞')).count()

    if request.method == 'POST':

        print('request', request.values['lend_b'])
        
                # if form.status.data=='損壞':
        Umbrella.query.filter_by(u_id=request.values['lend_b']).delete()
        db.session.commit()
        flash('已刪除雨傘紀錄')
        return redirect(url_for('authentication.deletepage'))

    return render_template('deletepage.html', form=form, getumbrella=getumbrella, getlocucount=getlocucount)






@authentication.route('/searchloc', methods=['GET', 'POST'])
def searchloc():
    form = SearchlocForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():

        search_locid = Location.query.filter_by(
            building_name=form.loc_id.data).first().loc_id
        return(redirect(url_for('authentication.lend', search_locid=search_locid)))

    return render_template('searchloc.html', form=form)


@authentication.route('/lend/<search_locid>', methods=['GET', 'POST'])
def lend(search_locid):
    form = LendForm(request.form)
    getumbrella = Umbrella.query.filter(
        and_(Umbrella.loc_id == search_locid, Umbrella.u_status == '正常')).all()
    getlocucount = Umbrella.query.filter_by(loc_id=search_locid).count()
    getlocname = Location.query.filter_by(
        loc_id=search_locid).first().building_name

    if request.method == 'POST':

        print('request', request.values['lend_b'])
        # lend_log
        now = datetime.now()
        report_data = Lend_log(
            l_time=now,
            loc_id=search_locid,
            s_id=current_user.s_id,
            u_id=request.values['lend_b'])
        print('report_data', report_data)
        db.session.add(report_data)
        # updata
        up_sid = User.query.filter_by(s_id=current_user.s_id).first()
        up_sid.state = '使用中'
        up_sid.use_count = up_sid.use_count+1
        up_u_loc = Umbrella.query.filter_by(
            u_id=request.values['lend_b']).first()
        up_u_loc.u_status = '使用中'
        up_u_loc.loc_id = 0
        up_loc_count = Location.query.filter_by(loc_id=search_locid).first()
        up_loc_count.um_count = Umbrella.query.filter_by(
            loc_id=search_locid).count()

        db.session.commit()
        flash('借用成功')
        return redirect(url_for('authentication.homepage'))

    return render_template('lend.html', form=form, getumbrella=getumbrella, getlocucount=getlocucount, getlocname=getlocname)


@authentication.route('/returnpage', methods=['GET', 'POST'])
def returnpage():
    form = ReturnForm(request.form)
    try:
        getlen = Lend_log.query.filter_by(s_id=current_user.s_id)[-1]
    except:
        flash('不存在')

    if request.method == 'POST' and form.validate_on_submit():
        getub = Umbrella.query.filter_by(u_id=form.uid.data).first()
        getusr = User.query.filter_by(s_id=current_user.s_id).first()
        getlocid = Location.query.filter_by(building_name=form.loc_id.data).first()
        # flash(form.loc_id.data)

        # lreturn_log
        now = datetime.now()
        data1 = now-getlen.l_time

        report_data = Return_log(
            l_id=getlen.l_id,
            r_time=now,
            s_id=current_user.s_id,
            loc_id=getlocid.loc_id,
            lending_time=(data1.total_seconds()/60)/60)
        db.session.add(report_data)
        # if now-getlen.l_time >
        # updata
        getub.u_status = '正常'
        getub.loc_id = getlocid.loc_id
        

        if '停權' in getusr.state :
            if getusr.foul_count >=４:
                getusr.foul_count=getusr.foul_count+1
                getusr.state='停權'
            else:
                flash('超過三天歸還，紀錄違規一次')
                getusr.foul_count=getusr.foul_count+1

        getusr.state = '正常'
        db.session.commit()
        
        flash('歸還成功')
        return redirect(url_for('authentication.homepage'))
    return render_template('returnpage.html', form=form)


@authentication.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        getusr=User.query.filter_by(s_id=current_user.s_id).first()
        getuid = Umbrella.query.filter_by(u_id=form.uid.data).first()

        getlocid = Location.query.filter_by(building_name=form.loc_id.data).first()
        if '使用中' in getusr.state :
            getu_id1 = Lend_log.query.filter_by(s_id=current_user.s_id)[-1].u_id
            
            if form.status.data=='拾獲':
                if getu_id1==form.uid.data :
                    flash('你正在使用這把傘 無法拾獲')
                    return redirect(url_for('authentication.report'))
                else:
                    if getuid.u_status=='使用中':
                        flash('此雨傘為借用中雨傘')
                        return redirect(url_for('authentication.report'))
                    elif getuid.u_status=='遺失':
                        getuid.u_status = '正常'
                    else:
                        flash('此雨傘未遺失 請確認編號')
                        return redirect(url_for('authentication.report'))

            elif form.status.data != '拾獲':

                if getu_id1==form.uid.data : 
                    if getusr.foul_count >=4:
                        getusr.foul_count=getusr.foul_count+1
                        flash('帳號已停權')
                        getusr.state='停權'
                    else:
                        getusr.foul_count=getusr.foul_count+1
                        flash('借用傘遺失損壞 違規次數+1')
                        getusr.state='正常'
                elif getuid.u_status=='使用中':
                    flash('此雨傘為借用中雨傘')
                    return redirect(url_for('authentication.report'))
                else:
                    getuid.u_status = form.status.data
        # elif  getusr.state !='使用中':
        elif '使用中'not in getusr.state :
            if form.status.data=='拾獲':
                if getuid.u_status=='使用中':
                        flash('此雨傘為借用中雨傘')
                        return redirect(url_for('authentication.report'))
                elif getuid.u_status=='遺失':
                    getuid.u_status = '正常'
                else:
                    flash('此雨傘未遺失 請確認編號')
                    return redirect(url_for('authentication.report'))
            else:
                if getuid.u_status=='使用中':
                        flash('此雨傘為借用中雨傘')
                        return redirect(url_for('authentication.report'))
                else:
                    getuid.u_status = form.status.data


        # getuid.u_status = form.status.data
        getuid.loc_id = getlocid.loc_id



        
        db.session.commit()

        # Add data
        report_data = Report(
            u_id=getuid.u_id,
            state=getuid.u_status,
            s_id=current_user.s_id,
            loc_id=str(getuid.loc_id))
        print('report_data', report_data)
        db.session.add(report_data)

        db.session.commit()

        flash("回報成功")
        return(redirect(url_for('authentication.homepage')))

    return render_template('report.html', form=form)


@authentication.route('/logout', methods=['GET'])
@login_required
def log_out_user():
    # session.clear()
    logout_user()
    return redirect(url_for('authentication.log_in_user'))


@authentication.app_errorhandler(404)
def page_not_found(error):
    flash('沒有此頁面喔～')
    return redirect(url_for('authentication.log_in_user'))
