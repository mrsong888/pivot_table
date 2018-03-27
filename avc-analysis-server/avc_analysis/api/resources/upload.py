# /usr/bin/env python
# *-* coding:utf-8 *-*
from flask import request, make_response
from flask_restful import Resource

from avc_analysis.extensions import report

class UploadFileResource(Resource):
    '''upload file
    '''
    _html = '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
    def get(self):
        return make_response(self._html)

    def post(self):
        token, userId = request.headers['Authorization'], request.headers['userId']
	file_obj = request.files['file']
        return report.save_file(file_obj, userId)
