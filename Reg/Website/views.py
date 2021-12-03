from flask import Blueprint, render_template, redirect, request
import requests, datetime, json, threading, time, pandas, os
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
        return render_template('index.html', tsks = tsks, pxs=pxs)


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
        
