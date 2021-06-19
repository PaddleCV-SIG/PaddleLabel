from flask import Flask, request  # ,json, jsonify, Response
from flask_cors import CORS, cross_origin
import numpy as np
import cv2, json
import base64


class FlaskServer:
    def __init__(self, port):
        self.port = port

    def cv2_to_base64(self, image):
        '''
        image encoder to base64 data
        :return:
        '''
        img_str = cv2.imencode('.jpg', image)[1].tobytes()
        b64_code = base64.b64encode(img_str)
        img_str = str(b64_code, encoding='utf-8')
        return img_str

    def base64_to_cv2(self, b64str):
        data = base64.b64decode(b64str.encode('utf8'))
        data = np.frombuffer(data, np.uint8)
        data = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return data

    def reader_request(self, name):
        '''
        读取表单中的内容
        :return:
        '''
        try:
            result = request.form.get(name)
        except:
            print('读取失败')
            return None
        else:
            return result

    def run_flask_server(self):
        '''
        run http server
        :return:
        '''
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'LabelImage FOR Paddle'
        app.config['CORS_HEADERS'] = 'Content-Type'
        cors = CORS(app, resources={r"/foo": {"origins": "*"}})

        @app.route('/upload', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def upload():
            '''
            upload data path to server
            '''
            image_path = self.reader_request('pics')

            result = {
                "code": 0,
                "data": {
                    "size": 5,  # 有效图片总数
                    "id": "bulabula",  # 数据集ID
                    "message": "5张图片因大小/格式不对添加失败！"
                }
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/get/picture/<dataset_id>/<pic_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_picture(dataset_id,pic_id):
            '''
            get image by dataset_id + pic_id
            '''
            print(dataset_id)
            print(pic_id)
            # unfinished
            image = 'unfinished function'
            # image = self.cv2_to_base64(image)

            result = {
                "code": 0,
                "data": [
                    {
                        "dataset_id": dataset_id,
                        "pic_id": pic_id,
                        "data": image
                    }
                ]
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/get/annotation/<dataset_id>/<pic_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_annotation(dataset_id,pic_id):
            '''
            get annotation by dataset_id + pic_id
            '''
            print(dataset_id)
            print(pic_id)

            # unfinished
            annotation = 'unfinished function'
            result = {
                "code": 0,
                "data": [
                    {#anotation 里面的数据
                        "content": [
                            {
                                "x": 329.05296950240773,
                                "y": 130.97913322632422
                            },#...
                        ],
                        "rectMask": {
                            "xMin": 329.05296950240773,
                            "yMin": 130.97913322632422,
                            "width": 187.4799357945425,
                            "height": 165.6500802568218
                        },
                        "labels": {
                            "labelName": "未命名",
                            "labelColor": "red",
                            "labelColorRGB": "255,0,0",
                            "visibility": False
                        },
                        "labelLocation": {
                            "x": 422.792937399679,
                            "y": 213.80417335473513
                        },
                        "contentType": "rect"
                    }
                ]
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/set/annotation/<dataset_id>/<pic_id>', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'image/x-png'])
        def set_annotation(dataset_id,pic_id):
            '''
            set annotation by dataset_id + pic_id
            '''

            datas = self.reader_request('datas')
            print(datas)
            # unfinished for set_annotation
            set_annotation_result = 'unfinished function'
            result = {
                "code": 0,
                "data": set_annotation_result
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag/<dataset_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_tags(dataset_id):
            '''
            读取所有标签
            '''
            # unfinished
            tags = 'unfinished function for get all tags'
            result = {
                "code": 0,
                "data": [
                    {
                        "name": "tag1",
                        "color": "#FFF000"
                    },# tags里面的内容
                ]
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag/<dataset_id>/add', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def add_tags(dataset_id):
            '''
            add tags
            '''
            code = self.reader_request('code')
            data = self.reader_request('data')

            # unfinished

            result = 'unfinished function for add tags'
            result = {
                "code": 0,
                "data": result
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag/<dataset_id>/delete', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def delete_tags(dataset_id):
            '''
            delete tags
            '''
            code = self.reader_request('code')
            data = self.reader_request('data')

            # unfinished
            result = 'unfinished function for delete tags'

            result = {
                "code": 0, # 0: 成功. 1: 资源不存在
                "data": result
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/transform/submit/<type>/<dataset_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def transform_submit(type,dataset_id):
            # unfinished
            result = 'unfinished function for 提交转存任务'
            result = {
                "code": 0,
                "data": {
                        "task_id": 123,
                        "dataset_id": "bulabula"
                    }
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/transform/progress/<task_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def transform_progress(task_id):
            # unfinished
            result = 'unfinished function for 查询进度'
            result = {
                "code": 1, # 0: 转换完成. 1: 转换中. 2: 转换失败。3: 任务不存在
                "data": {
                    "task_id": 123,
                    "dataset_id": "bulabula",
                    "progress": 52, # 百分比
                    "message": "3号图片转换失败<br>18号图片转换失败<br>"
                }
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/import_paddlex/<dataset_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def import_paddlex(dataset_id):
            # unfinished
            result = 'unfinished function for paddlex导入数据'
            result = {
                "code": 1,  # 0: 转换完成. 1: 转换中. 2: 转换失败。3: 任务不存在
                "data": {
                    "code": 0,
                    "data": "success"
                }
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        app.run(threaded=True, host='0.0.0.0', port=self.port, debug='False')


if __name__ == '__main__':
    server = FlaskServer(port=9528)
    server.run_flask_server()
