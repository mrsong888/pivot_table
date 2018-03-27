import json
import pandas as pd
import numpy as np 
from flask import request
from collections import defaultdict
from flask_jwt_simple import jwt_required
from flask_restful import Resource
from avc_analysis.extensions import block

class PivotResource(Resource):
    """ analysis query resource
    """
    _pd_aggfunc_maping = {'sum': np.sum, 'len': len, 'mean': np.mean}
    # method_decorators = [jwt_required]
    	
    def post(self):
	token, userId = request.headers['Authorization'], request.headers['userId']
	obj = request.json
        index, columns, operations, url = obj.get('index'), obj.get('columns'), obj.get('operations'), obj['blockUrl']
	meta_data = block.load_block(url, token, userId)['returnValue']
	df = pd.DataFrame(meta_data)
	if not index:
	    return {'code': 'fail', 'message': 'argument index  missed'}, 400
	if operations is None:
	    if columns is None:
	        pivot_res = pd.pivot_table(df, index=index)
		result = defaultdict(dict, dict(index_name=index, values_name=pivot_res.columns.tolist(), shape=pivot_res.values.shape, values=pivot_res.values.tolist()))
	        if len(index) == 1:
		    result[index[0]] = pivot_res.index.tolist()
		    result['labels'].update({index[0]: [i for i in xrange(pivot_res.index.shape[0])], 'values_sub': [i for i in xrange(pivot_res.columns.shape[0])]}) 
	        else:
		    for sub, val in enumerate(index):
		        result[val] = pivot_res.index.levels[sub].tolist()
			result['labels'].update({val: pivot_res.index.labels[sub].tolist()})              
	    else:
	        pivot_res = pd.pivot_table(df, index=index, columns=columns)
		result = defaultdict(dict, dict(index_name=index, columns_name=columns, shape=pivot_res.values.shape, values=pivot_res.values.tolist(), values_name=pivot_res.columns.levels[0].tolist(), labels=dict(values_sub=pivot_res.columns.labels[0].tolist())))
		if len(index) == 1:
		    result[index[0]] = pivot_res.index.tolist()
		    result['labels'].update({index[0]: [i for i in xrange(pivot_res.index.shape[0])]})
		else:
		    for sub, val in enumerate(index):
		        result[val] = pivot_res.index.levels[sub].tolist()
			result['labels'].update({val: pivot_res.index.labels[sub].tolist()})
		for sub, val in enumerate(columns, 1):
		    result[val] = pivot_res.columns.levels[sub].tolist()
		    result['labels'].update({val: pivot_res.columns.labels[sub].tolist()})
	else:
 	    result = defaultdict(dict, dict(index_name=index, values_name=[]))
            for k, op in enumerate(operations):
		result['values_name'].append(op['values'])
	        if columns is None:
		    if op.get('method') is None:
		        pivot_res = pd.pivot_table(df, index=index, values=op['values'])
		    else:
			pivot_res = pd.pivot_table(df, index=index, values=op['values'], aggfunc=self._pd_aggfunc_maping[op['method']])
		    if k == 0:
		        result['labels']['values_sub'] = []
			result['values'] = pivot_res.values
		        if len(index) == 1:
		            result[index[0]] = pivot_res.index.tolist()
			    result['labels'].update({index[0]: [i for i in xrange(pivot_res.index.shape[0])]})
		        else:
			    for sub, val in enumerate(index):
			        result[val] = pivot_res.index.levels[sub].tolist()
		                result['labels'].update({val: pivot_res.index.labels[sub].tolist()})
		    else:
		        result['values'] = np.concatenate((result['values'], pivot_res.values), axis=1)
		    result['labels']['values_sub'].append(k)
		else:
		    if op.get('method') is None:
		        pivot_res = pd.pivot_table(df, index=index, columns=columns, values=[op['values']])
		    else:
			pivot_res = pd.pivot_table(df, index=index, columns=columns, values=[op['values']], aggfunc=self._pd_aggfunc_maping[op['method']])
		    if k == 0:
			result['columns_name'] = columns
		        result['values'] = pivot_res.values
			result['labels']['values_sub'] = pivot_res.columns.labels[0]
			if len(index) == 1:
			    result[index[0]] = pivot_res.index.tolist()
			    result['labels'].update({index[0]: [i for i in xrange(pivot_res.index.shape[0])]})
			else:
			    for sub, val in enumerate(index):
			        result[val] = pivot_res.index.levels[sub].tolist()
				result['labels'].update({val: pivot_res.index.labels[sub].tolist()})
			for sub, val in enumerate(columns, 1):
			    result[val] = pivot_res.columns.levels[sub].tolist()
			    result['labels'].update({val: pivot_res.columns.labels[sub]})
		    else:
			result['values'] = np.concatenate((result['values'], pivot_res.values), axis=1)
			temp_sub = pivot_res.columns.labels[0] + k  
		        result['labels']['values_sub'] = np.concatenate((result['labels']['values_sub'], temp_sub))
			for sub, val in enumerate(columns, 1):
			    result['labels'][val] = np.concatenate((result['labels'][val], pivot_res.columns.labels[sub]))
	    if columns:
	        for val in columns:
		    result['labels'][val] = result['labels'][val].tolist()
		result['labels']['values_sub'] = result['labels']['values_sub'].tolist()
	    result['shape'] = result['values'].shape
	    result['values'] = result['values'].tolist()
		    
        return result
