from flask import Flask, g
from flask import render_template
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    print('run: create_app()')
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SESSION_COOKIE_NAME'] = 'gogglekaap'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/gogglekaap?charset=utf8'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@3.35.27.89:3306/gogglekaap?charset=utf8' #EC2 ubuntu 서버 Docker mySQL 연동
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
    if app.config['DEBUG']:
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1 #디버깅 모드에서 캐시 제거
    
    '''DB INIT'''
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        migrate.init_app(app, db, render_as_batch=True)
    else :
        migrate.init_app(app, db)
    
    '''ROUTE INIT'''
    from gogglekaap.routes import base_route, auth_route
    app.register_blueprint(base_route.bp)
    app.register_blueprint(auth_route.bp)
                
    '''CSRF INIT'''
    csrf.init_app(app)
         
    '''REQUEST HOOK'''
    #요청 전에 DB세션 생성
    @app.before_request
    def before_request():
        g.db = db.session
        
        
    #요청 끝나면 DB세션 클로즈
    @app.teardown_request
    def teardown_request(exception):
        if hasattr(g, 'db'):
            g.db.close()
           
        
    
    
    @app.errorhandler(404)
    def page_404(error):
        return render_template('/404.html'), 404

    return app