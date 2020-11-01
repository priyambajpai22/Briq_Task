from flask_mongoengine import MongoEngine
import pymongo 
import urllib
from .constant import *

db = MongoEngine()
cluster=pymongo.MongoClient('mongodb+srv://'+urllib.parse.quote_plus('priyam')+':'+urllib.parse.quote_plus('Priyam@13')+'@cluster0.1dcy1.mongodb.net/priyam?retryWrites=true&w=majority')



class Quotes(db.Document):
	quote = db.StringField(required=True)
	author = db.StringField(max_length=50)
	rating = db.IntField(null=True,blank=True)
	recommended=db.BooleanField(default=False)
	added_by=db.StringField(required=True)

	def save(self,*args,**kwargs):
		#import pdb;pdb.set_trace()
		if self.rating!=None and  self.rating>3:
			if self.rating>5:
				raise  ValueError(MAX_VALUE_ERR0R)
			self.recommended=True
		return super(Quotes,self).save(*args,**kwargs)


	def __str__(self):
		return self.author