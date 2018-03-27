# /usr/bin/env python
# *-* coding:utf-8 *-*
from flask import request
from flask_restful import Resource

from avc_analysis.extensions import report


class SaveReportResource(Resource):
    '''save report
    '''
    def post(self):
        token, userId = request.headers['Authorization'], request.headers['userId']
        obj = request.json
        name, result = obj['name'], obj['result']
        return report.save_report(name, result, userId)

class ReportListResource(Resource):
    '''get report list
    '''
    def get(self):
        token, userId = request.headers['Authorization'], request.headers['userId']
        return report.get_report_list(userId)

class SingleReportResource(Resource):
    '''get singile report
    '''
    def get(self, name):
        token, userId = request.headers['Authorization'], request.headers['userId']
        return report.get_report(name, userId)
