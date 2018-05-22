'''Importing Flask from the flask module. '''
from flask import Flask, render_template, url_for, request, redirect, session, send_from_directory, jsonify
from models import BucketListItems, Users
import random
import time
from threading import Thread
import pexpect

app = Flask(__name__) #connecting the web page to the python app. Determines the root path

'''Initialize the Users and BucketListItems classes '''
users = Users()
buckets = BucketListItems()
atmos = []


class MyThread(Thread):
    """
    A threading example
    """

    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        """Запуск потока"""
        child = pexpect.spawn("bluetoothctl")
        child.logfile = open("/mylog", "wb")
        child.send("scan on\n")
        try:
            while True:
                # child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})) ATMOTUBE")
                child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})) ATMOTUBE")
                ##        child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2})).*")
                ##        bdaddr = child.match.group(1)
                ##        param = child.after
                ##        if 'ATMOTUBE' in str(param):
                ##            param = child.match.group(0)
                ##            print(bdaddr)

                ##        print(param)
                bdaddr = child.match.group(1)
                print(bdaddr)
                atmos.append(bdaddr)
        ##        if bdaddr not in bdaddrs:
        ##            bdaddrs.append(bdaddr)
        ##            results.write(str(bdaddr))
        except KeyboardInterrupt:
            child.close()

@app.route("/") #@ a decorator, wraps a function and modify its behaviour. / refers to the homepage
def main():
    return render_template('home_page.html')

@app.route("/sign_up", methods = ['POST', 'GET']) #sign up page
def sign_up():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        name = request.form['inputName']
        users.register_user(name, email, password)
        return redirect(url_for("sign_in"))
    return render_template('sign_up.html')

@app.route('/sign_in', methods = ['POST', 'GET']) #sign in page
##def sign_in():
##    if request.method == 'POST':
##        email = request.form['inputEmail']
##        password = request.form['inputPassword']
##        if users.validate_login(email, password) == 'login successful':
##            session['email'] = email
##            return redirect(url_for('add_bucketlist'))
##    return render_template('sign_in.html')
def sign_in():
    return render_template('bucketlist_view.html', buckets=atmos)

@app.route('/add_bucketlist', methods=['POST', 'GET'])
def add_bucketlist():
    if request.method == 'POST':
        bucketlist_name = request.form['bucketlistName']
        buckets.add_bucketlist(bucketlist_name)
        return redirect(url_for("view_bucketlist"))
    return render_template('add_bucketlist.html', buckets = buckets) 

@app.route('/edit_bucketlist', methods=['POST', 'GET'])
def edit_bucketlist():
    name = "Thread scan"
    my_thread = MyThread(name)
    my_thread.start()
    global atmos
    return jsonify(results=atmos)

@app.route('/trash_counter', methods=['GET'])
def trash_counter():
    global atmos
    return jsonify(results = atmos)

@app.route('/delete_bucketlist', methods=['POST', 'GET'])
def delete_bucketlist():
    if request.method == 'POST':
        bucketlist_name = request.form['bucketlistName']
        buckets.delete_bucketlist(bucketlist_name)
        return render_template('bucketlist_view.html', buckets=buckets)
    return render_template('delete_bucketlist.html', buckets = buckets)

@app.route('/add_bucketlist_item/<bucketlist_name>', methods=["POST", "GET"])
def add_bucketlist_item(bucketlist_name):
    if request.method == 'POST':
        bucketlist_item = request.form['bucketlistItem']
        buckets.add_bucketlist_item(bucketlist_name, bucketlist_item)
        return render_template("bucketlist_item_view.html", buckets = buckets, bucketlist_name=bucketlist_name)

        #for obj in buckets.all_items:
        #    if bucketlist_item not in [obj for obj in buckets.all_items if obj.bucketlist_name == bucketlist_name]:
        #        buckets.add_bucketlist_item(bucketlist_name, bucketlist_item)
        #       return render_template("bucketlist_item_view.html", buckets = buckets)
    return render_template('add_bucketlist_item.html', buckets = buckets, bucketlist_name=bucketlist_name)


@app.route('/edit_bucketlist_item/<bucketlist_name>/<bucketlist_item>', methods=['GET', 'POST'])
def edit_bucketlist_item(bucketlist_name, bucketlist_item):
    if request.method == "POST":
        bucketlist_item = request.form['bucketlistItem']
        new_name = request.form['newBucketlistItemName']
        buckets.edit_bucketlist_item(bucketlist_name, bucketlist_item, new_name)
        return render_template('bucketlist_item_view.html', buckets=buckets, bucketlist_name=bucketlist_name, bucketlist_item=bucketlist_item) 
    return render_template('edit_bucketlist_item.html', buckets = buckets, bucketlist_name=bucketlist_name, bucketlist_item=bucketlist_item)   

@app.route('/delete_bucketlist_item/<bucketlist_name>/<bucketlist_item>', methods = ["GET", "POST"])
def delete_bucketlist_item(bucketlist_name, bucketlist_item):
    if request.method == 'POST':
        bucketlist_item = request.form['bucketlistItem']
        buckets.remove_bucketlist_item(bucketlist_name, bucketlist_item)
        return render_template("bucketlist_item_view.html", buckets=buckets, bucketlist_name=bucketlist_name, bucketlist_item=bucketlist_item)
    return render_template('delete_bucketlist_item.html', buckets=buckets, bucketlist_name=bucketlist_name, bucketlist_item=bucketlist_item)

##@app.route('/view_buckelist', methods=['GET'])
##def view_bucketlist():
##    return render_template('bucketlist_view.html', buckets=buckets)

@app.route('/view_bucketlist_item/<bucketlist_name>', methods=["GET"])
def view_bucketlist_items(bucketlist_name):
    return render_template('bucketlist_item_view.html', buckets= buckets, bucketlist_name = bucketlist_name)

app.config.from_object('config') #secret key for session management.

