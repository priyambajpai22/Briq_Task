from .models import *
import json



class Validation:
	def __init__(self,obj,model):
		self.obj=obj
		self.model=model

	def validate_and_save(self):
		
		try:
			data=self.model(**self.obj)
			data.save()
			return data.to_json()

		except Exception as E:
			#import pdb;pdb.set_trace()
			return json.dumps({'error':str(E)})