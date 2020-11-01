from flask.views import View
from flask import request
import json
from flask.views import MethodView
from .models import Quotes
from .validation import Validation
import difflib
import pymongo 
from bson.json_util import dumps
from .models import cluster
from .constant import *






class GetRequest(MethodView):
	model=Quotes
	database=cluster['priyam']
	collections=database['quotes']

	def permission(self,request):
		if request.json==None:
			return json.dumps({'error':NULL_BODY})
		if 'added_by' not in request.json:
			return json.dumps({'error':ID_NOT_PASSED})

		if request.json['added_by']==None:
			return json.dumps({'error':ID_NULL_ERROR})


	def id_check(self,pk):
		if pk==None:
			return json.dumps({'error':PK_ERROR})
		obj=self.model.objects(id=pk)
		if len(obj)==0:
			return json.dumps({'error':INVALID_PK})



	def get(self):
		''' RETURN DATA DEPENDING UPONE QUERY PRAMAS'''
		if 'quote' in request.args:
			if request.args['quote']=='rated':
				return dumps([x for x in self.collections.find({"rating":{"$ne":None}})])

			if request.args['quote']=='unrated':
				return dumps([x for x in self.collections.find({"rating":{"$eq":None}})])
			if  request.args['quote']=='recommanded':
				return dumps([x for x in self.collections.find({"recommanded":{"$eq":True}})])

		return self.model.objects.all().to_json()
		


	def post(self):
		''' ADD  NEW DOCUMENT '''
		data=self.permission(request)
		if data!=None:
			return data
		data=Validation(model=self.model,obj=request.json)
		return data.validate_and_save()



	def put(self,pk=None):

		'''UPDATE RAING BY ID'''
		data=self.id_check(pk)
		if data!=None:
			return data
		if 'rating' not in request.json and request.json['rating']!=None:
			return json.dumps({'error':KEY_ERROR})	
		obj=self.model.objects(id=pk)[0]
		#import pdb;pdb.set_trace()
		try:
			obj.rating=request.json['rating']
			obj.save()
			return obj.to_json()

		except  Exception as E:
			return json.dumps({'error':str(E)})



	def delete(self,pk=None):
		'''DELETE SINGLE DOCUMENT BY ID '''

		data=self.id_check(pk)
		if data!=None:
			return data
		self.permission(request)
		obj=self.model.objects(id=pk)[0]
		obj.delete()
		return json.dumps({'msg':SINGLE_DELETE})

		



class Get_Releted_quote(GetRequest):

	def get(self):
		unratedoject={x['quote']: x for x in self.collections.find({"rating":{"$eq":None}})}
		recommanded={x['quote']: x for x in self.collections.find({"recommended":{"$eq":True}})}
		related_quote= list(map(lambda unrated_quote: difflib.get_close_matches(unrated_quote,recommanded.keys(),cutoff=0.7),unratedoject.keys())) 
		i=0
		related_filtered_object=[]
		while i<len(related_quote):
			if len(related_quote[i])>0:
				related_filtered_object.append([unratedoject[list(unratedoject.keys())[i]]])

			i=i+1

		return dumps(related_filtered_object)


	def delete(self):
		data=self.model.objects.delete()
		return json.dumps({'msg':ALL_DELETE})








