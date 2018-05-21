# import modules and files

from modules import flask
from flask import * # Flask library used to connected python with web app
import bluetooth
import database

# Initilialise flask app
app = Flask(__name__)

carParkData = {()}

# First page shown when user accesses website
@app.route('/')
def index():
    global carParkData
    carParkData = database.get_all_data() # Retrieve data from database

    return render_template('first.html', carParkData = carParkData) # Render Web App template

# Connect to Car Park Page
@app.route('/connect', methods=['GET', 'POST'])
def connect():

    # If user just viewing page
    if(request.method == 'GET'):
        return render_template('connect.html')

    # If user submits form to connect to car park form

    if (request.form['carpark'] != '1'):
        return render_template('reciept.html', message='Can not connect to Car Park', leaving=False)


    # Call function to communicate request to Arduino
    if(request.form['entering'] == 'true'):
        message = bluetooth.enter(request.form['userid'])
    else:

        message = bluetooth.leave(request.form['userid'])

        payment = ''

        # Calculate cost using price for car park and time spent (encoded in message)
        if 'not in car park' not in message:
            start = 39 + len(request.form['userid'])
            minute = int(message[start:start + 2])
            start = 34 + len(request.form['userid'])
            hour = int(message[start:start + 2])
            price = int(carParkData[0]['price'])

            leaving = True

            cost = hour * price

            if( minute > 0 ):
                cost += price

            payment = 'Amount Due: $' + str(cost)


        return render_template('reciept.html', message = message, payment = payment, leaving = True)

    return render_template('reciept.html', message=message, leaving = False)

# Admin page
@app.route('/admin', methods=['GET', 'POST'])
def admin():

    # Retrieve most recent data from database
    global carParkData
    carParkData = database.get_all_data()

    # If user is on login page
    if(request.method == 'GET'):
        return render_template('admin_login.html')

    # If user has submitted login form

    # Check database for admin user
    login_request = database.admin_login(request.form['username'],request.form['password'])

    if login_request is None:
        message = 'Incorrect username or password'

        return render_template('reciept.html', message=message, leaving=False)

    # Format data for display
    for row in carParkData:
        if(row['batteryLevel'] > 0):
            row['batteryLevel'] = 'High'
        elif (int(row['batteryLevel']) == 0):
            row['batteryLevel'] = 'Medium'
        elif (int(row['batteryLevel']) < 0):
            row['batteryLevel'] = 'Low'
        if (row['motionLevel'] == 0):
            row['motionLevel'] = 'Stable'
        else:
            row['motionLevel'] = 'UNSTABLE'

    return render_template('admin_view.html',  carParkData = carParkData)


# Start App

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)