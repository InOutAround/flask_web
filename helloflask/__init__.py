from flask import Flask, g, make_response, Response, request, session
from flask import render_template, Markup
from datetime import date, datetime, timedelta

# Session = browser 기준(user기준), 나만 사용하는 공간
# application context = 모든 사람들과 공유하는 공간
# get, post : get은 용량 제한이 있고, 편지지 머리에 있어서 찾기 더 빠름... post는 form, body에 있는 것 , 중요한 자료는 post(편지지)에 적어 보낸다.
# request는 기본적으로 str이다
# cookie는 도메인, 브라우저, 경로에 만들 수 있다. client에 떠있는 것
# {% %} 이때 개행이나 공백을 없애고 싶을 때 -를 붙인다. ex) {%-  -%}
app = Flask(__name__)
app.debug = True # use only debug
# app.jinja_env.trim_blocks = True


app.config.update(
    SECRET_KEY = "X1234Ydfsf1",
    SESSION_COOKIE_NAME = 'pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME = timedelta(31) # 31 days
)


@app.template_filter('ymd')
def datetime_ymd(dt, fmt='%m-%d'):
    if isinstance(dt,date):
        return dt.strftime(fmt)
    else:
        return dt    

@app.template_filter('simpledate')
def simpledate(dt):
    if not isinstance(dt,date):
        dt = datetime.strptime(dt, "%Y-%M-%d %H:%m")

    if (datetime.now() - dt).days < 1:
        fmt = "%H:%M"
    else:
        fmt = "%M/%d"

    return "<strong>%s</strong>"

@app.route('/')
def idx():
    rds = []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i == 2:
            checked = 'checked'
        text = 'RadioTest' + str(i)
        rds.append( FormInput(id, name, value, checked, text))
        today = date.today()
    return render_template('app.html', title = "testtttt9999",radiosList = rds, today = today )



@app.route('/top100')
def top100():
    return render_template('application.html', title = "main!!")

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/tmpl')
def t():
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic" # 반복되는 html 요소를 묶어서 할 수 있음
    lst = [("만남1","김건모"), ("만남2","노사연"),("만남3","김국진")]
    tit = Markup('<strong>Title<strong>')
    return render_template('index.html', title = tit, mu=h, list= lst) # index.html 랜더링




# cookie
@app.route('/wc')
def wc():
    key = request.args.get('key')
    val = request.args.get('val')
    res = Response("SET COOKIE")
    res.set_cookie(key, val)
    session['Token'] = "123x"
    return make_response(res)

@app.route('/rc')
def rc():
    key = request.args.get('key') # token
    val = request.cookies.get(key)
    return "cookie[{}], val[{}], session[{}]".format(key,val,session.get('Token'))

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다."

# Session
app.secret_key = "X1234Ydfsf1"






@app.route("/res1")
def res1():
    custom_res = Response("Custom Response", 201, {"test":"ttt"}) # 3번째 파라미터는 header에 정보가 저장된다.
    return make_response(custom_res) # stream으로 내려보내는 것, 무거운 것을 가볍게 만드는 것... 중요

# WSGI(WebServer Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), # body를 string으로 보내서 plain
                    ('Context-Length', str(len(body)))]
        start_response('200 OK', headers)
        return [body]

    return make_response(application)


# @app.before_request # request 전에 무조건 연결되는 곳, web filter enc-kr -> utf-8
# def before_request():
#     print("before_request!!")
#     g.str = "한글" # application 영역

# @app.route("/gg")
# def helloworld2():
#     return "hello world " + getattr(g, 'str', '111')




@app.route('/rp')
def rp():
    q = request.args.get('q')
    return "q = %s" % str(q)

@app.route('/rplist')
def rplist():
    q = request.values.getlist('q') # list로 받을 때 
    return "q = {}".format(q)



# 날 형식 바꾸기
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd("%Y-%m-%d")) # 1번인자 : str매개, 2번인자 : 1번인자 없을 때 default, 3반인자 : 함수형
    return "우리나라 시간 형식 = " + str(datestr)


@app.route('/requen')
def reqenv():
    print()



