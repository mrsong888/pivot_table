from flask import Blueprint
from flask_restful import Api

from avc_analysis.api.resources import PivotResource
from avc_analysis.api.resources import DataBlockResource
from avc_analysis.api.resources import DataBlockSync
from avc_analysis.api.resources import DataBlockAllSync
from avc_analysis.api.resources import ReportListResource
from avc_analysis.api.resources import SaveReportResource
from avc_analysis.api.resources import SingleReportResource
from avc_analysis.api.resources import UploadFileResource

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(DataBlockResource, '/getData')
api.add_resource(DataBlockSync, '/SyncSingleData')
api.add_resource(DataBlockAllSync, '/SyncAllData')
api.add_resource(PivotResource, '/pivot')
api.add_resource(ReportListResource, '/ReportList')
api.add_resource(SaveReportResource, '/SaveReport')
api.add_resource(SingleReportResource, '/getReport/<name>')
api.add_resource(UploadFileResource, '/SaveFile')

