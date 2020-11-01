from flask import Flask
from mainapp.views import *
from flask_mongoengine import MongoEngine
import urllib
db = MongoEngine()


app=Flask(__name__)




app.add_url_rule('/delete_all_quote', view_func=Get_Releted_quote.as_view('delete_all_quote'))
app.add_url_rule('/get_all_quote', view_func=GetRequest.as_view('get_request'))
app.add_url_rule('/add_quote', view_func=GetRequest.as_view('post_request'))
app.add_url_rule('/rate_quote/<pk>', view_func=GetRequest.as_view('give_rate'))
app.add_url_rule('/delete_quote/<pk>', view_func=GetRequest.as_view('delete'))
app.add_url_rule('/get_related_quote', view_func=Get_Releted_quote.as_view('related_quote'))

app.config['MONGODB_SETTINGS'] = {
    'db': 'project1',
    'host': 'mongodb+srv://'+urllib.parse.quote_plus('priyam')+':'+urllib.parse.quote_plus('Priyam@13')+'@cluster0.1dcy1.mongodb.net/priyam?retryWrites=true&w=majority'
}
db.init_app(app)


 