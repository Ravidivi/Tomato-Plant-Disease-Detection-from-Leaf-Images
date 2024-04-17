from flask import Flask
app=Flask(__name__)
@app.route('/')
def first():
    return("Today, I'm learn a new thing!")
@app.route('/Next')
def second():
    return("I'm excited to extend this one!!")
if __name__=='__main__':
    app.run()
