import os
from cliq import app, db
from cliq.models import User
from flask_script import Manager, prompt_bool

manager = Manager(app)

@manager.command
def dbinit():
    db.create_all()
    db.session.add(User(name="Ohm Patel", year="2021", major="CS/Math", email="2ompatel@gmail.com", bio="I like to code.", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Aviral Somani", year="2021", major="CS",email="aviral.somani@vanderbilt.edu", bio="ohm sux", facebook="aviral.somani.9", instagram="av.ral", twitter="aviral_somani", linkedin="aviralsomani", phone="4694493340"))
    db.session.add(User(name="Aditya Gokhale", year="2021", major="CS",email="aditya.p.gokhale@vanderbilt.edu", bio="dank memes", facebook="Aditya711", instagram="agokhale11", twitter="", linkedin="", phone="3147950655"))
    db.session.add(User(name="Ayaz Hafiz", year="2021", major="CS", email="ayaz.hafiz.1@gmail.com", bio="I like chemistry", facebook="ayazhafiz", instagram="dvmvnds", twitter="dvmvnds", linkedin="ayazhafiz", phone="4692680852"))
    db.session.add(User(name="Joe Cots", year="2021", major="CS", email="J.cots@gmail.com", bio="I like swimming in pools.", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Bill Johnson", year="2018", major="Chem", email="B.johnson@gmail.com", bio="VU 2018", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Nahendra Reddy", year="2017", major="HOD", email="N.Reddy@gmail.com", bio="live for dying", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Teo Lee", year="2020", major="Bio", email="T.lee@gmail.com", bio="Corinthians 2:13", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Leo Ceks", year="2019", major="Math", email="L.ceks@gmail.com", bio="I like biking and fishing", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Xi Shin", year="2019", major="English", email="X.shin@gmail.com", bio="environmental sustainibility is cool", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Lisa Su", year="2021", major="Music", email="L.su@gmail.com", bio="send me the code", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="Marcus Bucks", year="2021", major="CS", email="m.bucks@gmail.com", bio="I like to code.", facebook="opatel99", instagram="opatel99", snapchat="opatel99", twitter="mildused", linkedin="opatel99", phone="9018288482"))
    db.session.add(User(name="William Zhao", year="2021", major="CS", email="William.zhao@vanderbilt.edu", bio="programming is the bomb dot com!", facebook="William.zhao.10", instagram="wzhao1", snapchat="williezhao", twitter="williezhao", linkedin="williezhao", phone="7892147435"))
    db.session.add(User(name="Kevin Jin", year="2021", major="CS", email="Kevin.jin@vanderbilt.edu", bio="Stacks on stacks bro!", facebook="kevinjin", instagram="kevinjin", snapchat="kevinjin", twitter="kevinjin", linkedin="kevinjin", phone="9086754532"))
    db.session.add(User(name="Anjali Mahapatra", year="2021", major="undecided", email="anjali.mahapatra@vanderbilt.edu", bio="Maybe premed?", facebook="anjalimahapatra", instagram="anjalimahapatra", snapchat="anjalimahapatra", twitter="anjalimahapatra", linkedin="anjalimahapatra", phone="6156789342"))
    db.session.add(User(name="Pranav Kodali", year="2021", major="Biochem", email="Pranav.kodali@vanderbilt.edu", bio="I love cells.", facebook="pkodali", instagram="pkodali", snapchat="pkodali", twitter="pkodali", linkedin="pkodali", phone="9876453241"))
    db.session.add(User(name="Yoanna Ivanova", year="2021", major="BME", email="yoanna.ivanova@vanderbilt.edu", bio="I really love tea", facebook="yoanna.ivanova", instagram="yoanna.ivanova", snapchat="yoanna.ivanova", twitter="yoanna.ivanova", linkedin="yoanna.ivanova", phone="4657898973"))
    db.session.commit()
    print('Initialized the database')
    
@manager.command
def dbdrop():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        print('Dropped the database')

@manager.command
def again():
    if prompt_bool(
        "Are you sure you want to lose all your data"):
        db.drop_all()
        dbinit()

@manager.command
def start():
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 80)))

if __name__ == '__main__':
    manager.run()
