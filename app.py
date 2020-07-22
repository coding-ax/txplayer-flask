from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# 允许跨域
cors = CORS(app=app, resources=r"/*")
import json
import datetime
import txplayer


@app.route('/')
def hello_world():
    return '当你看到这句话的时候，说明这个服务正在运行'


@app.route("/search", methods=["GET", "POST"])
def get_search_data():
    keyword = request.args.get("keyword")
    try:
        data = txplayer.searchTXplayer(keyword)
        return jsonify({
            'status': 200,
            'message': "搜索成功",
            'data': data
        })
    except Exception as e:
        print(e)
        return jsonify({
            'status': 300,
            'message': "未找到您要搜索的内容",
            'data': []
        })


@app.route("/player", methods=["GET", "POST"])
def get_data_by_id_count():
    id = request.args.get("id")
    count = request.args.get("count")
    try:
        data = txplayer.get_page_message(id, count)
        return jsonify({
            "code": 200,
            'data': data,
            'message': "查询成功"
        })
    except Exception as e:
        return jsonify({
            "code": 300,
            'message': "查询失败",
            "data": []
        })


@app.errorhandler(404)
def not_found():
    return '404 not found'


if __name__ == '__main__':
    app.run(debug=True, port=9000, host="0.0.0.0")
