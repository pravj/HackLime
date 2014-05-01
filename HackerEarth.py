"""
This module communicates with HackerEarth API
Talk there to compile/run a source code file

Author  : Pravendra Singh (pravj)
Contact : hackpravj@gmail.com (https://pravj.github.io)
"""

import os
import json
import urllib2
import urllib
import config
from langmap import langmap


class HackerEarth:
	def __init__(self, source_file):
		self.key = self.SecretKey()
		self.source = self.SourceCode(source_file)
		self.lang = self.Language(source_file)
		self.file = source_file

		self.data =	{
    		'client_secret': self.key,
			'source': self.source,
			'lang': self.lang,
			'time_limit': config.time_limit,
			'memory_limit': config.memory_limit,
			'async': config.async
		}

	# returns client secret key from configuration file
	def SecretKey(self):
		return config.client_secret

	# return code buffer from a source code file
	def SourceCode(self, source_file):
		with open(source_file, 'r') as f:
			source = f.read()
			return source

	# returns language of code written in source code file
	def Language(self, source_file):
		# file extension
		extension = os.path.splitext(source_file)[1]

		# file's code language using langmap
		language = langmap[extension.lower()]

		return language

	# creates request to API endpoints and return responses
	def Contact(self, mode='compile'):
		# url for endpoint according to mode
		if(mode == 'compile'):
			url = config.compile_point
		elif(mode == 'run'):
			url = config.run_point

		# btw, why 'urlencode' is not there in 'urllib2' (o.O)
		req = urllib2.Request(url, urllib.urlencode(self.data))

		# urllib2 error handling
		try:
			res = urllib2.urlopen(req)
			# response in JSON format
			res = json.load(res)

		except urllib2.URLError as e:
			res = {'er': 'there was an error in request'}

		return res

	# handles what to write in output file 
	# according to API's response
	def Output(self, response):
		output = "see this on web : " + response['web_link']

		output += "\ncompile status : " + response['compile_status']
		output += "\nrun status : " + response['run_status']['status']

		if(response['run_status']['status'] == 'AC'):
			output += "\noutput : \n" + response['run_status']['output']

		if('time_used' in response['run_status']):
			output += "\ntime used : " + response['run_status']['time_used']

		output += "\nrun status detail : " + response['run_status']['status_detail']

		# output text
		return output
