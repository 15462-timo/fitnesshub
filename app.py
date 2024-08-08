from flask import * #importing flask
import pymysql
import sms

app=Flask(__name__)

connection=pymysql.connect(host='localhost',user='root',password='',database='fitness_hub') #we are connecting to database tai1_soko_garden which is the localhost server
cursor=connection.cursor()#function cursor allows  code to execute sql commands in a database session
app.secret_key="mysecretkey" #set secret key to secure our session

@app.route('/') # routing function home
def home():
    connection=pymysql.connect(host='localhost',user='root',password='',database='fitness_hub') #we are connecting to database tai1_soko_garden which is the localhost server
    print('database connected successfully')
    return render_template('index.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        password1 = request.form['password1']
        password2 = request.form['password2']

        #validating the passwords
        if len(password1) <8:
            return render_template('signup.html',error='PASSWORD MUST BE MORE THAN 8 CHARACTERS')
        elif password1 != password2:
            return render_template('signup.html', error1="PASSWORDS DONT MATCH")
        else:
            sql='''INSERT INTO users (username,email,phone,password) VALUES (%s,%s,%s,%s)'''
            cursor.execute(sql,(username,email,phone,password1))
            connection.commit()
            return render_template('signup.html',success='SIGNED UP SECCESSFULLY')
    else:
        return render_template('signup.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password1=request.form['password1']

        tai_sql="SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(tai_sql,(username,password1))
        connection.commit()

        if cursor.rowcount==0:
            return render_template('login.html',error='INVALID CREDENTIALS')
        else:
            session['key']=username #when we log in the user creates his/her own session, we are linking the session key with the username
            return redirect('/')
    else:
        return render_template('login.html')
    
@app.route('/logout')
def logout():
    session.clear() #we are terminating our session
    return redirect('/login')
    
@app.route('/add_trainer', methods=['POST','GET'])
def add_trainer():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        national_ID = request.form['national_ID']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        #validating the passwords
        if len(password1) <8:
            return render_template('add_trainer.html',error='PASSWORD MUST BE MORE THAN 8 CHARACTERS')
        elif password1 != password2:
            return render_template('add_trainer.html', error1="PASSWORDS DONT MATCH")
        else:
            sql='''INSERT INTO trainers (firstname,lastname,national_ID,email,password) VALUES (%s,%s,%s,%s,%s)'''
            cursor.execute(sql,(firstname,lastname,national_ID,email,password1))
            connection.commit()
            return render_template('add_trainer.html',success='SIGNED UP SECCESSFULLY')
    else:
        return render_template('add_trainer.html')

@app.route('/owl_carousel') # routing function home
def owl_carousel():
    return render_template('owl_carousel.html')

@app.route('/classes') # routing function home
def classes():
    return render_template('classes.html')

@app.route('/trainers') # routing function home
def trainers():
    return render_template('trainers.html')

@app.route('/aboutus') # routing function home
def aboutus():
    return render_template('aboutus.html')


@app.route('/contactus') # routing function home
def contactus():
    return render_template('contactus.html')


if __name__=='__main__':
    app.run(debug=True)