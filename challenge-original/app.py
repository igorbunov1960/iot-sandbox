'''Importing the app from views '''
from views import app

'''Running the app '''
if __name__ == '__main__': 
    app.run(debug=True) #prints errors on the web page incase of anything.
