# coding=utf-8
import logging
import os

try:
    from urllib.parse import urlencode, parse_qs
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs

import requests
import json


def version():
    """版本变更信息
    """
    versions = []
    versions.append({
        'v': '0.0.1',
        'c': ['数据块服务基本功能获取']
    })
    return versions


__version__ = version()[-1]['v']

_logger = logging.getLogger(__name__)
null_handler = logging.NullHandler()
_logger.addHandler(null_handler)


def is_valid_response(response):
    return 200 <= response.status_code <= 299


def is_json_response(response):
    content_type = response.headers.get('Content-Type', '')
    return content_type == 'application/json' or content_type.startswith('application/json;')


class DataBlockApiError(Exception):
    """Raised if a request fails to the DataBlock API."""

    def __str__(self):
        try:
            message = self.response.json()['message']
        except Exception:
            message = None
        return "%s: %s" % (self.response.status_code, message)

    @property
    def response(self):
        return self.args[0]


class DataBlockApi(object):

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None
        self.BASE_URL = ''
        self.BASE_AUTH_URL = ''
        self.DATABLOCK_CACHE_DIR = './cache'

    def init_app(self, app):
        self.client_id = app.config['DATABLOCK_CLIENT_ID']
        self.client_secret = app.config['DATABLOCK_CLIENT_SECRET']
        self.base_url = app.config.get('DATABLOCK_BASE_URL', self.BASE_URL)
        self.auth_url = app.config.get('DATABLOCK_AUTH_URL', self.BASE_AUTH_URL)
        self.cache_path = app.config.get('DATABLOCK_CACHE_DIR', self.DATABLOCK_CACHE_DIR)
        self.client = requests.session()
        self.client.keep_alive = False
	self._report_name = 'ReportList.txt'
	self._file_list_name = 'upload_file.txt'

    #订阅
    def subscribe_block(self, blockId):
        pass
    #退订
    def unsubscribe_block(self, blockId):
        pass
    #同步所有
    def sync_all_blocks(self, blockId, token, userId):
        cacheDir = ''.join([os.path.abspath(self.cache_path), '/', userId])
	if not os.path.exists(cacheDir):
	    os.makedirs(cacheDir)
        cacheKey = ''.join([cacheDir, '/', blockId.split('/')[-1], '.json'])
	data = self.client.get(self.base_url + '/' + blockId, headers={'Authorization': 'bearer' + token})
        with open(cacheKey, 'w') as f:
            f.write(data.content)
        data = json.loads(data.content)
        for d in data['returnValue']:
	    temp_key = ''.join([cacheDir, '/', d['id'].split('/')[-1].split('$')[0], '.json'])
	    data = self.client.get(self.base_url + '/' + d['id'].split('$')[0], headers={'Authorization': 'bearer' + token})
	    with open(temp_key,'w') as f:
		f.write(data.content)
        return {'code':'success','message':'operation success'}
    #同步
    def sync_block(self, blockId, token, userId):
        cacheDir = ''.join([os.path.abspath(self.cache_path), '/', userId])
	if not os.path.exists(cacheDir):
	    os.makedirs(cacheDir)
	cacheKey = ''.join([cacheDir, '/', blockId.split('/')[-1], '.json'])
        data = self.client.get(self.base_url + '/' + blockId, headers={'Authorization': 'bearer' + token})
        with open(cacheKey, 'w') as f:
            f.write(data.content)
            contents = data.content
        return {'code':'success','message':'operation success'}


    def load_block(self, blockId, token, userId):
        cacheDir = ''.join([os.path.abspath(self.cache_path), '/', userId])
        if not os.path.exists(cacheDir):
            os.makedirs(cacheDir)
	cacheKey = ''.join([cacheDir, '/', blockId.split('/')[-1], '.json'])
        if (not os.path.exists(cacheKey)):
            data = self.client.get(self.base_url + '/' + blockId, headers={'Authorization': 'bearer' + token})
            with open(cacheKey, 'w') as f:
                f.write(data.content)
            contents = data.content
        else:
            with open(cacheKey) as cacheData:
                contents = cacheData.read()
	result = json.loads(contents)
        upload_path = ''.join([cacheDir, '/', 'upload', '/'])
	file_list_path = upload_path + self._file_list_name
        if os.path.exists(upload_path) and os.path.exists(file_list_path):
            with open(file_list_path) as f:
	        contents = f.read()
	        file_list = contents.split('\n')[:-1] if any(contents.split('\n')[:-1]) else []
		result['upload_file_list'] = file_list 
        return result


class ReportAip(DataBlockApi):

    def save_report(self, name, result, userId):
        report_name = name + '.json'
        report_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', report_name])
        reportlist_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', self._report_name])
        if os.path.exists(report_path):
            return {'code': 'fail', 'message': 'report_name existed'}
        with open(report_path, 'w') as f:
            f.write(json.dumps(result))
        with open(reportlist_path, 'a') as f:
            f.write(name + '\n')
        return {'code': 'success', 'message': 'operation success'}

    def get_report_list(self, userId):
        reportlist_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', self._report_name])
        if not os.path.exists(reportlist_path):
            return {'code': 'fail', 'message': 'reportlist not existed'}
        with open(reportlist_path) as f:
            contents = f.read()
            report_name_list = contents.split('\n')[:-1] if any(contents.split('\n')[:-1]) else []
        return dict(result=report_name_list)

    def get_report(self, name, userId):
        report_name = name + '.json'
        report_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', report_name])
        with open(report_path) as f:
            contents = f.read()
        return json.loads(contents)

    def save_file(self, file_obj, userId):
        upload_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', 'upload', '/'])
	file_list_path = upload_path + self._file_list_name
	if not os.path.exists(upload_path):
	    os.makedirs(upload_path)
	ALLOWED_EXTENSIONS = ['txt', 'json', 'csv', 'excel', 'png', 'jpg']
        if file_obj and file_obj.filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS:
            filename = secure_filename(file_obj.filename)
	    file_obj.save(os.path.join(upload_path, filename))
	    with open(file_list_path, 'a') as f:
	        f.write(filename.rsplit('.')[0] + '\n')
            return {'code': 'success', 'message': 'operation success'}
        else:
    	    return {'code': 'fail', 'message': 'unsupport type'}

    def modify_report(self, name, result, userId, newname=None):
        if newname:
            new_report_name = newname + '.json'
            new_report_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', new_report_name])
	    reportlist_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', self._report_name])
	    self.delete_report(name, userId)
	    with open(new_report_path, 'w') as f:
	        f.write(json.dumps(result))
	    with open(reportlist_path, 'a') as f:
	        f.write(newname + '\n')
        else:
	    report_name = name + '.json'
            report_path = ''.join([os.path.abspath(self.cache_path), '/', userId, '/', report_name])
            with open(report_path, 'w') as f:
	        f.write(json.dumps(result))
	return {'code': 'success', 'message': 'operation success'}
	
    def delete_report(self):
        pass 
