from app import create_app, db
from app.auth.models import User

# if __name__ == '__main__':

flask_app = create_app('prod')
flask_app.static_url_path=''
flask_app.static_folder='auth/static'
with flask_app.app_context():
    db.create_all()
    if not User.query.filter_by(s_id='108753123').first():
        User.create_user(u_s_id='108753123',
            u_name='123',
            u_major='資科',
            u_mail='108753123@nccu.edu.tw',
            u_state='正常',
            u_use_count=0,
            u_foul_count=0,
            u_password='123')
flask_app.run(debug=True)
#flask_app.run(ssl_context=('cert.pem', 'key.pem'))