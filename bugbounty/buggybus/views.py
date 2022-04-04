from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from buggybus.forms import JourneyForm, LoginForm, RegisterForm,SelectionForm
from datetime import date,datetime
from buggybus import db
from flask_login import login_user,login_required,logout_user
from buggybus.models import User


core = Blueprint('core',__name__)

@core.route('/',methods=['GET','POST'])
def index():
    # form=JourneyForm()
    # if form.validate_on_submit():
    #     session['from']=form.from_city.data
    #     session['to']=form.to_city.data
    #     # session['date']=form.date.data
    if request.method == "POST":
        req = request.form
        session['from'] = req.get("From")
        session['to'] = req["To"]
        Dat = req["Date"]  
        session['Year'] = Dat[0:4]
        session['Month'] = Dat[5:7]
        session['Day'] = Dat[8:10]
        # req_date=datetime.strptime(Dat,'%Y-%m-%d')
        if session['from']!='Select' and session['to']!='Select':
            return redirect(url_for("core.buslist"))
    
    return render_template('index.html')

@core.route('/contact', methods=['GET','POST'])
def contact():
    if request.method =="POST":
        session['msg']=request.form.get('message')
        if "<script>" in request.form.get('message'):
            return redirect(url_for("core.script"))
    return render_template('contact.html')

@core.route('/script')
def script():
    if "msg" in session:
       return render_template('script.html',message=session.get('msg'))
    else:
        return redirect(url_for("core.contact"))

@core.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm()
    # today=date.today()
    # born=form.DOB.data
    # age=today.year-born.year-((today.month, today.day) < (born.month, born.day))+2
    # name=form.name.data
    # country=form.country.data
    if form.validate_on_submit():
        flash("Sorry, Cannot register right now")
        return redirect(url_for('core.index'))
        
    return render_template('register.html',form=form)

@core.route('/login',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user=form.user_id.data
        passwd=form.password.data
        sql= f"SELECT * FROM users where username = '{user}' AND password = '{passwd}'"
        r=list(db.engine.execute(sql))
        if len(r)!=0:

            admin=User.query.filter_by(username='admin').first()
            login_user(admin)
            flash('Logged in successfully.')
            
            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    
    return render_template('login.html',form=form)

@core.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('core.index'))

@core.route('/buslist',methods=['GET', 'POST'])
def buslist():
    from_city=session.get('to')
    to_city=session.get('from')
    if request.method == 'POST':
        session['Passengers']=request.form.get('Passengers')
        return redirect(url_for('core.review'))
    # date=session.get('date')
    return render_template('buslist.html',from_city=from_city,to_city=to_city)

@core.route('/review')
@login_required
def review():
    from_city=session.get('to')
    to_city=session.get('from')
    # size=session['Passengers']
    # cost=size*2000
    cost=2000
    return render_template('review.html',from_city=from_city,to_city=to_city,cost=cost)

@core.route('/payment',methods=['GET','POST'])
@login_required
def payment():
    if request.method == "POST":
        username = request.form.get('username')
        password=request.form.get('password')
        session['user']=username
        lst=['admin','hemanth','amit']
        if username in lst:
            sql= f"SELECT * FROM users where username = '{username}' AND password = '{password}'"
            r=list(db.engine.execute(sql))
            if len(r)!=0:
                return redirect(url_for('core.finalticket'))
        
    return render_template('payment.html')

@core.route('/finalticket')
@login_required
def finalticket():
    if "user" in session:
        return render_template('finalticket.html')
    else:
        return redirect(url_for('core.payment'))
