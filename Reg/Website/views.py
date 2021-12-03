from flask import Blueprint, render_template, redirect, request
from flask.templating import render_template_string
import requests, datetime, json, threading, time, pandas, os, sys
from . import db
from os.path import join, dirname, realpath
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOADS_PATH = join(dirname(realpath(__file__)), 'files/')


class Notee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    url = db.Column(db.String(1000))
    proxies_am = db.Column(db.Integer, default = 0)
    threads = db.Column(db.Integer, default = 0)
    wait = db.Column(db.Integer, default = 0)
    amount = db.Column(db.Integer, default = 0)
    good = db.Column(db.Integer, default = 0)
    bad = db.Column(db.Integer, default = 0)
    date = db.Column(db.DateTime, default = datetime.utcnow)


class Proxyy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typee = db.Column(db.Integer, default = 0)
    adress = db.Column(db.String(1000))
    port = db.Column(db.Integer, default = 0)
    login = db.Column(db.String(1000))
    passe = db.Column(db.String(1000))

views = Blueprint('views',__name__)



@views.route('/', methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        if request.form['form-name'] == 'form1':
            tsk_name = request.form['name']
            tsk_url = request.form['url']
            tsk_threads = int(request.form['threads'])
            tsk_proxy = request.form['proxy']
            tsk_wait = int(request.form['wait'])
            tsk_emna = request.files['emails']
            name_emna = secure_filename(tsk_emna.filename)
            tsk_emna.save((f'{UPLOADS_PATH}{name_emna}'))
            names = []
            emails = []
            a = pandas.read_excel(f'{UPLOADS_PATH}{name_emna}', engine='openpyxl', header=None)
            names += a[0].tolist()
            emails += a[1].tolist()
            tsk_amount = len(names)


            pos = Proxyy.query.all()
            proxies = []

            for i in pos:
                proxies.append(f'{i.login}:{i.passe}@{i.adress}:{i.port}')

            if int(tsk_proxy)>len(proxies):
                tsk_proxy=len(proxies)
            ns = Notee(name = tsk_name, proxies_am = tsk_proxy, threads = tsk_threads, wait = tsk_wait, amount = tsk_amount, url=tsk_url)
            











            while len(proxies)<len(emails):
                proxies*=3

            
            for i in range(tsk_threads):
                t = threading.Thread(target=roc, args=(emails, names, proxies, tsk_url, i, tsk_threads, tsk_wait))
                t.start()
            tsks = Notee.query.order_by(Notee.date).all()
            try:
                db.session.add(ns)
                db.session.commit()

                return redirect('/')
            except:
                return('meh, ERROR')
        else:
            px_adr = request.form['adress']
            px_pass = request.form['pass']
            px_login = request.form['login']
            px_port = request.form['port']
            px_type = request.form['type']


            ok = Proxyy(typee = px_type, port = px_port, login = px_login, adress = px_adr, passe = px_pass)

            try:
                db.session.add(ok)
                db.session.commit()
                return redirect('/')
            except:
                return('meh error')


    else:
        tsks = Notee.query.order_by(Notee.date).all()
        pxs = Proxyy.query.order_by(Proxyy.adress).all()
        return render_template_string('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
        
            <div id='inputs'>
        <form action="/" method="POST" enctype="multipart/form-data">
            <h1 style='color:white; font-size: 40px;'>ЗАДАНИЯ</h1>
            <input autocomplete="off" type="hidden" name="form-name" id='form-name' value="form1">
            <input autocomplete="off" placeholder="NAME" type="" name="name" id='name'>
            <input autocomplete="off" placeholder="url" type="" name="url" id='url'>
            <input autocomplete="off" placeholder="threads" type="" name="threads" id='threads'>
            <input autocomplete="off"  placeholder="proxy" type="" name="proxy" id='proxy'>
            <input autocomplete="off" placeholder="wait" type="" name="wait" id='wait'>
            <input autocomplete="off" placeholder="emails" type="file" name="emails" id='emails'>
            <input id ='subm' type="submit" value="SUBMIT">
        </form>


        <form action="/" method="POST" enctype="multipart/form-data" id='proxies'>
            <h1 style='color:white; font-size: 40px;'>ПРОКСИ</h1>
            <input autocomplete="off" type="hidden" name="form-name" id='form-name' value="form2">
            <input autocomplete="off" placeholder="adress" type="" name="adress" id='adress'>
            <input autocomplete="off" placeholder="port" type="" name="port" id='port'>
            <input autocomplete="off" placeholder="login" type="" name="login" id='login'>
            <input autocomplete="off" placeholder="password" type="" name="pass" id='pass'>
            <select name="type" id="type">
                <option id='http/https' name='http/https' value="http/https">http/https</option>
                <option id='socks5' name='socks5' value="socks5">socks5</option>
            </select>
            <input id ='subm' type="submit" value="SUBMIT">
        </form>
    </div>
    <div id='tabless'>
        
        <table>
            <tr>
                <th>Название</th>
                <th>Дата</th>
                <th>Ссылка</th>
                <th>Потоки</th>
                <th>Прокси</th>
                <th>Интервалы</th>
                <th>Количество</th>
            </tr>
    
            {% for tsk in tsks %}
            <tr>
                <th>{{tsk.name}}</th>
                <th>{{tsk.date}}</th>
                <th>{{tsk.url}}</th>
                <th>{{tsk.threads}}</th>
                <th>{{tsk.proxies_am}}</th>
                <th>{{tsk.wait}}</th>
                <th>{{tsk.amount}}</th>
            </tr>
            {% endfor %}
        </table>

        <table id = 'prx'>
            <tr>
                <th>Адресс</th>
                <th>Порт</th>
                <th>Логин</th>
                <th>Пароль</th>
                <th>Тип</th>

            </tr>
    
            {% for tsk in pxs %}
            <tr>
                <th>{{tsk.adress}}</th>
                <th>{{tsk.port}}</th>
                <th>{{tsk.login}}</th>
                <th>{{tsk.passe}}</th>
                <th>{{tsk.typee}}</th>
            </tr>
            {% endfor %}
        </table>

    </div>



</body>
<style>

body
{
    background-color: #4158D0;
    background-color: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
    height: 100%;
    background-position: center;
    background-repeat: no-repeat;
    background-size: cover;
    font-family: 'Roboto', sans-serif;
}


th
{
    border: 1px solid;
    padding: 8px;
    color: #000000;
    font-weight: 600;
    border: 2px solid rgba(255, 255, 255, 0.5);
}
table
{
    border-collapse: collapse;
    margin-top: 20px;
    margin-left: 5px;
    color: #642B73;
    background: rgba(255, 255, 255, 0.2);
    border: 2px solid #642B73;  /* fallback for old browsers */
    border: 2px solid -webkit-linear-gradient(to right, #C6426E, #642B73);  /* Chrome 10-25, Safari 5.1-6 */
    border: 2px solid linear-gradient(to right, #C6426E, #642B73); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
}
input, select
{
    display: block;
    margin:5px;
    margin-bottom: 10px;
    background: rgba(255, 255, 255, 0.3);
    border: none;
    font-size: 15px;
    font-weight: 400;
    color: rgba(0, 0, 0, 0.8);
    border-radius: 5px;
    height: 30px;
    text-transform: uppercase;
    padding-left: 5px;
    cursor: pointer;
}

select
{
    width: 120px;
    color: rgba(0, 0, 0, 0.8);
}

#subm
{
    background: #DD5E89;  /* fallback for old browsers */
    background: -webkit-linear-gradient(to right, #F7BB97, #DD5E89);  /* Chrome 10-25, Safari 5.1-6 */
    background: linear-gradient(to right, #F7BB97, #DD5E89); /* W3C, IE 10+/ Edge, Firefox 16+, Chrome 26+, Opera 12+, Safari 7+ */
    border: none;
    color: white;
    font-size: 20px;
    border-radius: 10px;
    width: 150px;
    height: 50px;
    margin-bottom: 30px;

}

#inputs
{
    display: flex;
}

#proxies, #prx
{
    margin-left: auto; 
    margin-right: 0;
}

#tabless
{
    display: flex;
}



::placeholder { /* Chrome, Firefox, Opera, Safari 10.1+ */
  color: rgba(0, 0, 0, 0.5);
  opacity: 1; /* Firefox */
}
</style>
</html>''', tsks = tsks, pxs=pxs)


@views.route('/', methods = ['POST'])
def pxies():
    px_adr = request.form['adress']
    px_pass = request.form['pass']
    px_login = request.form['login']
    px_port = request.form['port']
    px_type = request.form['type']


    ok = Proxyy(typee = px_type, port = px_port, login = px_login, adress = px_adr, passe = px_pass)

    try:
        db.session.add(ok)
        db.session.commit()
        return redirect('/')
    except:
        return('meh error')















def roc(emails, names, proxies,url,j,threads, wait):
    for i in range(round(len(emails)/threads*(j-1)), round(len(emails)/threads*j)):
        req(email=emails[i],name=names[i],proxy=proxies[i],url=url,typee=None)
        time.sleep(wait)







ak = 0

dl = 0

def req(name,email,url,proxy,typee):
    global dl
    global ak
    try:
        date = str(datetime.now()).split(' ')[0]

        time = str(datetime.now()).split(' ')[1].split('.')[0]

        if proxy!=None and typee=='http':
            proxyDict = { 
              "http"  : "http://{proxy}", 
              "https" : "https://{proxy}", 
            }
        elif proxy!=None and typee=='socks':
            proxyDict = { 
              "http"  : "http://{proxy}", 
              "https" : "https://{proxy}", 
            }

        def finde(rec,word,pls=30):
            a = (rec.content.decode("utf-8")).find(word)
            return(rec.content.decode("utf-8")[a:a+pls])


        s = requests.session()

        r = s.get(f'{url}?js_include')
        webid = (finde(r,'webinar_id').split('"')[1])
        sesid = (finde(r,'session_id',40).split('\'')[1])
        auh = sesid = (finde(r,'authorization',220).split('"')[2])

        lh = {
            'webinar_id':webid,
            'timezone_difference':'03:00:00',
            'timezone_operation':'+',
            'user_time_gmt':date,
            'user_date_gmt':time,
            'user_timezone':'Europe%2FMinsk',
            'session_id':'v19rcintana39elnugrugejkk1',
        }

        l = s.post('http://req.easywebinar.com/wp-content/plugins/webinar_plugin/webinar-db-interaction/webinar_session.php', data=lh)

        tas = json.loads(l.content.decode('utf-8'))[0]



        up = {
        'webinar_id':webid,
        'webinar_check_time':tas['webinar_date'].split(' ')[0],
        'schedule_id':tas['schedule_id'],
        'aten_name':name,
        'aten_skype':'',
        'aten_phone':'',
        'aten_email':email,
        'webinar_date':tas['webinar_date'].split(' ')[0],
        'webinar_start_date':tas['webinar_date'].split(' ')[0],
        'max_attendee':'',
        'webinar_time':(tas['webinar_date'].split(' ')[1]).replace(':','%3A'),
        'after_webinar_enabled':0,
        'after_webinar_hours':0,
        'video_length':0,
        'selected_timezone_id':0,
        'attendee_date_time_in_gmt':str(tas['webinar_date'].split(' ')[0])+'+'+(tas['webinar_date'].split(' ')[1]).replace(':','%3A'),
        'storing_mode':'Save',
        'is_yesterday_reply':0,
        'session_id':sesid,
        'attendee_timezone_name':'Europe%252FMinsk',
        }


        asfd = s.post('http://req.easywebinar.com/wp-content/plugins/webinar_plugin/webinar-db-interaction/webinar-ajax-file.php', data = up, headers = {'Authorization':auh})
        ak+=1
        if ak%20==0:
            admin = Notee.query.filter_by(Notee.date).update(dict(good=ak,bad=dl))
            db.session.add(admin)
            db.session.commit()
        print(f'{ak}')
    except Exception as e:
        
        dl+=1
        print(f'{ak}')
        
