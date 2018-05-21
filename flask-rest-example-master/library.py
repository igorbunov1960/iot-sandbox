from werkzeug import url_decode
from flask import Flask, render_template, request, redirect, url_for, flash
import sys, pexpect
from time import sleep
from time import time
import struct
import binascii

class MethodRewriteMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
        return self.app(environ, start_response)

class Book(object):
    """A Fake model"""

    def __init__(self, id = None, name = None):
        self.id = id
        self.name = name


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'secret'
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)

@app.route('/vocs')
def list_vocs():
    """GET /vocs

    Lists all vocs"""
    vocs = [ Book(id=1, name=u'VOC: 68'), Book(id=2, name=u'VOC: 55') ] # Your query here ;)
    
    file = open('atmo_history.txt', 'w')
    file.close()
    
    gatt=pexpect.spawn('gatttool -t random -b C6:E9:37:EC:21:35 -I')
    gatt.logfile = open("/tmp/mylog", "wb")
    gatt.sendline('connect')
    gatt.expect('Connection successful') 
    print("success gatt notice!")

    #enable notice
    gatt.sendline('char-write-req 0x000f 0100')
    gatt.expect('Characteristic value was written successfully')
    print("Notice enable")

    #send sync time
    name_str = 'HST'
    name_bytes = name_str.encode('ASCII')
    time_ts = int(time())

    sendlist = name_bytes + time_ts.to_bytes(4, byteorder = 'big')

    cmd = 'const'.encode('ASCII')
    gatt.sendline('char-write-req 0x0011 %s' % ''.join(format(x, '02x') for x in sendlist))   
    
    gatt.expect('value.*', timeout=1000)
    param = gatt.after
    print(param)
    vocs.append(Book(id=3, name=param))
    return render_template('list_vocs.html', vocs=vocs)

@app.route('/vocs/<id>')
def show_voc(id):
    """GET /vocs/<id>

    Get a voc by its id"""
    voc = Book(id=id, name=u'My great voc') # Your query here ;)
    return render_template('show_voc.html', voc=voc)

@app.route('/vocs/new')
def new_voc():
    """GET /vocs/new

    The form for a new voc"""
    return render_template('new_voc.html')

@app.route('/vocs', methods=['POST',])
def create_voc():
    """POST /vocs

    Receives a voc data and saves it"""
    name = request.form['name']
    voc = Book(id=2, name=name) # Save it
    flash('Book %s sucessful saved!' % voc.name)
    return redirect(url_for('show_voc', id=2))

@app.route('/vocs/<id>/edit')
def edit_voc(id):
    """GET /vocs/<id>/edit

    Form for editing a voc"""
    voc = Book(id=id, name=u'Something crazy') # Your query
    return render_template('edit_voc.html', voc=voc)

@app.route('/vocs/<id>', methods=['PUT'])
def update_voc(id):
    """PUT /vocs/<id>

    Updates a voc"""
    voc = Book(id=id, name=u"I don't know") # Your query
    voc.name = request.form['name'] # Save it
    flash('Book %s updated!' % voc.name)
    return redirect(url_for('show_voc', id=voc.id))

@app.route('/vocs/<id>', methods=['DELETE'])
def delete_voc(id):
    """DELETE /vocs/<id>

    Deletes a vocs"""
    voc = Book(id=id, name=u"My voc to be deleted") # Your query
    flash('Book %s deleted!' % voc.name)
    return redirect(url_for('list_vocs'))

def saveData(data): 
    file = open('atmo_history.txt', 'a')
    file.write(data)
    file.close()
    print(data)

if __name__ == '__main__':
    app.run()
   
    
