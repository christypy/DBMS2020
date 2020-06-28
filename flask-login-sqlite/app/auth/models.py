from datetime import datetime
from app import db, bcrypt
from app import login_manager
from flask_login import UserMixin
from sqlalchemy import Date

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    s_id = db.Column(db.String(10),unique=True,index=True )
    name = db.Column(db.String(20))
    major=db.Column(db.String(4))
    mail = db.Column(db.String(30))
    state=db.Column(db.String(5))
    use_count=db.Column(db.Integer())
    foul_count=db.Column(db.Integer())
    password = db.Column(db.String(80))

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    @classmethod
    def create_user(cls, u_s_id,u_name,u_major,u_mail,u_state,u_use_count,u_foul_count, u_password):

        user = cls(s_id=u_s_id,
                   name=u_name,
                   major=u_major,
                   mail=u_mail,
                   state=u_state,
                   use_count=u_use_count,
                   foul_count=u_foul_count,
                   password=bcrypt.generate_password_hash(u_password).decode('utf-8')
            )
        db.session.add(user)
        print('user',user)
        db.session.commit()
        return user


class Lend_log(db.Model):
    __tablename__ = 'Lend_log'

    l_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    l_time = db.Column(db.TIMESTAMP)
    loc_id=db.Column(db.Integer, db.ForeignKey('Location.loc_id'))
    s_id=db.Column(db.Integer, db.ForeignKey('users.s_id'))
    u_id=db.Column(db.Integer, db.ForeignKey('users.s_id'))
class Location(db.Model):
    __tablename__ = 'Location'

    loc_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    # Lend_log = db.relationship('Lend_log', backref='Location')
    building_name = db.Column(db.String(30))
    # um_count=db.Column(db.Integer)
class Report(db.Model):
    __tablename__ = 'Report'

    re_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    u_id = db.Column(db.Integer, db.ForeignKey('Umbrella.u_id'))
    state=db.Column(db.String(10))
    s_id=db.Column(db.Integer, db.ForeignKey('users.s_id'))  
    loc_id=db.Column(db.Integer, db.ForeignKey('Location.loc_id'))  
class Return_log(db.Model):
    __tablename__ = 'Return_log'

    r_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    l_id = db.Column(db.Integer, db.ForeignKey('Lend_log.l_id'))
    s_id=db.Column(db.Integer, db.ForeignKey('users.s_id'))

    r_time=db.Column(db.TIMESTAMP)
    loc_id=db.Column(db.Integer, db.ForeignKey('Location.loc_id'))  
    lending_time=db.Column(db.NUMERIC)
class Umbrella(db.Model):
    __tablename__ = 'Umbrella'

    u_id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    u_color = db.Column(db.String(30))
    u_size=db.Column(db.String(5))
    loc_id=db.Column(db.Integer, db.ForeignKey('Location.loc_id'))  
    u_status=db.Column(db.String(5))
 


@login_manager.user_loader
def load_user(s_id):
    
    return User.query.get(int(s_id))

