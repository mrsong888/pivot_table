import json
import pandas as pd
import numpy as np 
from flask import request
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
	    result = {'code': 'fail', 'message': 'argument index  missed'}
            return result, 400
        if operations is None:
            if columns is None:
	        pivot_res = pd.pivot_table(df, index=index)
                values_list = list(pivot_res.columns)
                res = dict(values_list=values_list, result=json.loads(pivot_res.reset_index().to_json(orient='records')))
            else:
		res = {}
                pivot_res = pd.pivot_table(df, index=index, columns=columns)
		values_list = list(pivot_res.columns.levels[0])
		columns_list = list(pivot_res.columns.levels[1])
		for values in values_list:
		    sub_pivot_res = getattr(pivot_res, values)
		    res[values] = json.loads(sub_pivot_res.reset_index().to_json(orient='records'))
		res['values_list'] = values_list
		res['columns_list'] = columns_list
        else:
	    temp_result, cur_result, result = {}, None, []
	    for op in operations:
                if columns is None:
		    if op.get('method') is None:
                        pivot_res = pd.pivot_table(df, index=index, values=op['values']) 
		    else:
			pivot_res = pd.pivot_table(df, index=index, values=op['values'], aggfunc=self._pd_aggfunc_maping[op['method']])   
                    if not temp_result:
		        temp_result = json.loads(pivot_res.reset_index().to_json(orient='records'))
		    else:
  		        cur_result = json.loads(pivot_res.reset_index().to_json(orient='records'))
	    	        for k, v in zip(temp_result, cur_result):
	                    k.update(v)
                            result.append(k)
			temp_result = result[:]
			del result[:] 
                else:
		    if op.get('method') is None:
		        pivot_res = pd.pivot_table(df, index=index, columns=columns, values=[op['values']])
		    else:
		        pivot_res = pd.pivot_table(df, index=index, columns=columns, values=[op['values']], aggfunc=self._pd_aggfunc_maping[op['method']])
		    sub_pivot_res = getattr(pivot_res, op['values'])
		    temp_result[op['values']] = json.loads(sub_pivot_res.reset_index().to_json(orient='records'))
		    temp_result['columns_list'] = list(sub_pivot_res.columns)
	    res = temp_result if columns else dict(values_list=[i['values'] for i in operations],result=temp_result)	    
		         		     
        return res 
