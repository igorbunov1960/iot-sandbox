'''Importing Flask from the flask module. '''
from flask import Flask, render_template, url_for, request, redirect, session
from models import BucketListItems, Users

app = Flask(__name__) #connecting the web page to the python app. Determines the root path

'''Initialize the Users and BucketListItems classes '''
users = Users()
buckets = BucketListItems()

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
def sign_in():
    if request.method == 'POST':
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        if users.validate_login(email, password) == 'login successful':
            session['email'] = email
            return redirect(url_for('add_bucketlist'))
    return render_template('sign_in.html')

@app.route('/add_bucketlist', methods=['POST', 'GET'])
def add_bucketlist():
    if request.method == 'POST':
        bucketlist_name = request.form['bucketlistName']
        buckets.add_bucketlist(bucketlist_name)
        return redirect(url_for("view_bucketlist"))
    return render_template('add_bucketlist.html', buckets = buckets) 

@app.route('/edit_bucketlist', methods=['POST', 'GET'])
def edit_bucketlist():
    if request.method == 'POST':
        bucketlist_name = request.form['bucketlistName']
        new_name = request.form['newBucketlistName']
        buckets.edit_bucketlist(bucketlist_name, new_name)
        return render_template('bucketlist_view.html', buckets=buckets)
    return render_template('edit_bucketlist.html', buckets=buckets)
    
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

@app.route('/view_buckelist', methods=['GET'])
def view_bucketlist():
    return render_template('bucketlist_view.html', buckets=buckets)

@app.route('/view_bucketlist_item/<bucketlist_name>', methods=["GET"])
def view_bucketlist_items(bucketlist_name):
    return render_template('bucketlist_item_view.html', buckets= buckets, bucketlist_name = bucketlist_name)

app.config.from_object('config') #secret key for session management.

