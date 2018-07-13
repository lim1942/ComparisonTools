import os
import json
import flask
from urllib import parse
from flask import Flask, jsonify, request

from python_utils.data_spider import get_data
from python_utils.for_excel import read_info_by_file,write_info_to_file


FILE_PATH = 'page_utils'
app = Flask(__name__)

@app.route('/', methods=['GET',"POST"])
def index():
    with open('index.html','rb') as f:
    	index = f.read()
    return index


@app.route('/page_utils/<path>', methods=['GET',"POST"])
def files(path):
    filename = os.path.join(FILE_PATH,path)
    with open(filename,'rb') as f:
    	con = f.read()
    return con


@app.route('/get_data', methods=['GET',"POST"])
def get_datas():
	ir_sitename_base = parse.unquote(request.args.get('ir_sitename_base'))
	channel_path_base = parse.unquote(request.args.get('channel_path_base'))
	page = request.args.get('page')
	data = get_data(ir_sitename_base, channel_path_base, page)
	return data


@app.route('/excel/read', methods=['GET',"POST"])
def excel_read():
    return read_info_by_file()


@app.route('/excel/write', methods=['GET',"POST"])
def excel_write():
    ir_sitename = parse.unquote(request.args.get('ir_sitename'))
    channel_path = (request.args.get('channel_path'))
    state = request.args.get('state')
    state_info = request.args.get('state_info')
    return write_info_to_file(ir_sitename, channel_path, state,state_info)



if __name__ == '__main__':
        
    print('。')
    print('。。。')
    print('。。。。。')
    print('。。。。。。。')
    print('。。。。。。。。。')
    print('。。。。。。。。。。')
    print('。。。。服务器启动成功')
    app.run(host='127.0.0.1',port=1212)