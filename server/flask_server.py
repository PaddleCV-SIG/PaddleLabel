from flask import Flask, request, send_from_directory  # ,json, jsonify, Response
from flask_cors import CORS, cross_origin
import numpy as np
import cv2, json
import base64, os, yaml


class FlaskServer:
    def __init__(self, port):
        self.port = port
        if not os.path.exists('data'):
            os.makedirs('data')
        self.datasavepath = 'data'
        self.tags = []

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

    def reader_yamlfile(self, filename):
        if not os.path.exists(filename):
            return None
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def write_yamlfile(self, filename, data):
        with open(filename, "w", encoding="utf-8") as f:
            yaml.dump(data, f)

    def dataset_config_file(self,dataset_id):
        return 'dataset_' + str(dataset_id) + '.yaml'
    def annotation_config_file(self,dataset_id):
        return 'dataset_' + str(dataset_id) + '_annotation.yaml'

    def init_annotion_sets(self,dataset_id,image_path_list):
        data = {
            'dataset_id': dataset_id,
            'annotations': []
        }
        for path in image_path_list:
            data['annotations'].append({
                'pic_path': path,
                'datas': []
            })
        data['annotations_num'] = len(data['annotations'])
        annotation_path = os.path.join(self.datasavepath,self.annotation_config_file(dataset_id))
        with open(annotation_path, "w", encoding="utf-8") as f:
            yaml.dump(data, f)


    def run_flask_server(self):
        '''
        run http server
        :return:
        '''
        app = Flask(__name__)
        app.config['SECRET_KEY'] = 'LabelImage FOR Paddle'
        app.config['CORS_HEADERS'] = 'Content-Type'
        cors = CORS(app, resources={r"/foo": {"origins": "*"}})
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

        @app.route('/', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def index():
            return send_from_directory(root, 'index.html')
        
        @app.route('/favicon.ico', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def favicon():
            return send_from_directory(root, "favicon.ico")

        @app.route('/assets/<path:path>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def assets(path):
            return send_from_directory(root + "/assets", path)

        @app.route('/upload/<labeltype>/<dataset_id>', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def upload(labeltype,dataset_id):
            '''
            upload data path to server
            接收之前先把原来的数据集信息删除
            接收paddlex传过来的数据图片路径，写入文件
            '''
            # exist_data = os.listdir(self.datasavepath)
            # for file in exist_data:
            #     print('delete file {}'.format(file))
            #     os.remove(os.path.join(self.datasavepath, file))
            pics_path = json.loads(request.get_data(as_text=True))['pics_path']
            image_path = os.path.join(pics_path, 'JPEGImages')
            
            dataset_name = self.dataset_config_file(dataset_id)
            path = os.path.join(self.datasavepath, dataset_name)
            pre_data = {
                'label_type': labeltype, # 标注类型
                'dataset_id': dataset_id, # 数据集id
                'image_num': len(image_path), # 图片数量
                'image_path': image_path
            }
            yaml.dump(pre_data)
            self.write_yamlfile(path, pre_data)
            self.init_annotion_sets(dataset_id, image_path)
            result = {
                "code": 0,
                "data": {
                    "size": len(image_path),  # 有效图片总数
                    "id": dataset_id,  # 数据集ID
                    "message": "success"
                }
            }

            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/get/dataset_info/<dataset_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def dataset_info(dataset_id):
            '''
            返回数据集的信息
            :return:
            '''
            path = self.dataset_config_file(dataset_id)
            dataset_info = self.reader_yamlfile(os.path.join(self.datasavepath,path))
            result = {
                "code": 0,
                'dataset_info':dataset_info
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/get/picture/<dataset_id>/<pic_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_picture(dataset_id,pic_id):
            '''
            get image path by dataset_id + pic_id
            前端请求后把对应的图片转成base64编码传过去
            '''
            pic_id = int(pic_id)
            data = self.reader_yamlfile(os.path.join(self.datasavepath,self.dataset_config_file(dataset_id)))
            image_path = os.path.join(data['image_path'], pic_id)
            try:
                image = self.cv2_to_base64(cv2.imread(image_path))
            except:
                image = None

            # self.reader_yamlfile(os.path.join(self.datasavepath,'dataset_' + str(dataset_id) + '.yaml'))
            result = {
                "code": 0,
                "data": [
                    {
                        "pic_id": pic_id,
                        "data": image
                    }
                ]
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/set/annotation/<dataset_id>/<pic_id>', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'image/x-png'])
        def set_annotation(dataset_id, pic_id):
            '''
            set annotation by dataset_id + pic_id
            以图片为单位给我
            '''
            pic_id = int(pic_id)
            datas = json.loads(self.reader_request('datas'))
            annotation_path = os.path.join(self.datasavepath, self.annotation_config_file(dataset_id))
            if not os.path.exists(annotation_path):
                result = {
                    "code": 1,
                }
            else:
                pre_data = self.reader_yamlfile(annotation_path)
                pre_data['annotations'][pic_id]['datas'] = datas
                with open(annotation_path, "w", encoding="utf-8") as f:
                    yaml.dump(pre_data, f)
                result = {
                    "code": 0,
                }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/get/annotation/<dataset_id>/<pic_id>', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_annotation(dataset_id,pic_id):
            '''
            get annotation by dataset_id + pic_id
            '''
            pic_id = int(pic_id)
            annotation_path = os.path.join(self.datasavepath,self.annotation_config_file(dataset_id))
            data = self.reader_yamlfile(annotation_path)
            if data is None:
                result = {
                    "code": 1,
                    "data": None
                }
            else:
                result = {
                    "code": 0,
                    "data":data['annotations'][pic_id]['datas']
                }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def get_tags():
            '''
            读取所有标签
            '''
            result = {
                "code": 0,
                "data": self.tags
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag/add', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def add_tags():
            '''
            add tags
            '''
            req = json.loads(request.get_data(as_text=True))
            name = req['name']
            color = req['color']
            self.tags.append({
                    "name": name,
                    "color": color
            })
            result = {
                "code": 0,
                "data": 'success'
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/tag/delete', methods=['POST'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def delete_tags():
            '''
            delete tags
            '''
            req = json.loads(request.get_data(as_text=True))
            name = req['name']
            color = req['color']
            len_del = len(self.tags)
            for i in range(len(self.tags)):
                if self.tags[i]['name'] == name:
                    del self.tags[i]
                    break
            if (len(self.tags) - len_del)<0:
                del_result = 0
            else:
                del_result = 1
            result = {
                "code": del_result,  # 0: 成功. 1: 资源不存在
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/transform/submit/<dataset_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def transform_submit(dataset_id):
            # 读取对应数据集的信息
            path = self.dataset_config_file(dataset_id)
            dataset_info = self.reader_yamlfile(os.path.join(self.datasavepath, path))
            # 读取对应数据集已标注的annotation
            annotation_path = os.path.join(self.datasavepath, self.annotation_config_file(dataset_id))
            annotation_data = self.reader_yamlfile(annotation_path)
            ##################
            #这里进行转换吧
            ##################
            result = {
                "code": 0,
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json

        @app.route('/transform/progress/<task_id>', methods=['GET'])
        @cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
        def transform_progress(task_id):
            # unfinished
            result = 'unfinished function for 查询进度'
            result = {
                "code": 1,  # 0: 转换完成. 1: 转换中. 2: 转换失败。3: 任务不存在
                "data": {
                    "task_id": 123,
                    "dataset_id": "bulabula",
                    "progress": 52,  # 百分比
                    "message": "3号图片转换失败<br>18号图片转换失败<br>"
                }
            }
            return json.dumps(result, ensure_ascii=False)  # 返回json


        app.run(threaded=True, host='0.0.0.0', port=self.port, debug='False')


if __name__ == '__main__':
    server = FlaskServer(port=627)
    server.run_flask_server()
