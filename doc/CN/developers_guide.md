# Developer Guide

PaddleLabel's backend development centers around [connexion](https://github.com/spec-first/connexion). Unlike other tool that generate openapi spec based on your code, with connexion you write openapi spec first and connexion takes care of routing and integrity check based on openapi spec.

Other important dependencies are [SQLAlchemy](https://www.sqlalchemy.org/) for ORM, [marshmallow](https://marshmallow.readthedocs.io/en/stable/) for serialization and [Flask](https://flask.palletsprojects.com/en/2.0.x/).

Backend defaults to using sqlite database, but as we are using sqlalchemy this can be easilly switched to PostgreSQL. Connexion also allows using multiple frameworks as backend, we will decouple sqlalchemy and marshmallow from flask to allow swithing to others in the future. As we have such plan, using any flask specific functions is discoraged. eg: you should use pplabel.api.util.abort instead of flask.abort

Useful softwares for development

- [stoplight studio](https://stoplight.io/studio/): Edit openapi spec with GUI. Note that this app currently doesn't sync changes from file system. Do reload it if you changed the spec with say your text editor. Or after a save in stoplight all modifications would be gone.
- [Swagger Editor](https://editor.swagger.io/): Provides better linting than stoplight, gives more accurate format error location.
- [insomnia](https://github.com/Kong/insomnia): Like postman but less complex, for api testing

## Project Structure

This structure is chosen to avoid circular import.

```shell
PaddleLabel
├── README.md
├── docker-compose-dev.yml # docker support
├── Dockerfile.dev
├── setup.py # packaging
├── MANIFEST.in
├── requirements.txt
├── pplabel # core code
│   ├── api # code that handles api calls
│   │   ├── __init__.py
│   │   ├── util.py
│   │   ├── controller # handler for api calls
│   │   │   ├── __init__.py
│   │   │   ├── annotation.py
│   │   │   ├── base.py
│   │   │   ├── data.py
│   │   │   ├── label.py
│   │   │   ├── project.py
│   │   │   ├── setting.py
│   │   │   ├── tag.py
│   │   │   └── task.py
│   │   ├── model # sqlalchemy models
│   │   │   ├── __init__.py
│   │   │   ├── annotation.py
│   │   │   ├── base.py
│   │   │   ├── data.py
│   │   │   ├── label.py
│   │   │   ├── project.py
│   │   │   ├── setting.py
│   │   │   ├── tag.py
│   │   │   ├── tag_task.py
│   │   │   └── task.py
│   │   ├── schema # marshmallow schemas for (de)serialization
│   │   │   ├── __init__.py
│   │   │   ├── annotation.py
│   │   │   ├── base.py
│   │   │   ├── data.py
│   │   │   ├── label.py
│   │   │   ├── project.py
│   │   │   ├── setting.py
│   │   │   ├── tag.py
│   │   │   ├── tag_task.py
│   │   │   └── task.py
│   ├── task # implements support for various annotations tasks, eg: import/export for classification project
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── classification.py
│   │   ├── detection.py
│   │   ├── segmentation.py
│   │   │── util
│   │   │   ├── __init__.py
│   │   │   ├── file.py
│   │   │   └── manager.py
│   │   └── io # implements io code for various file formats
│   │       ├── __init__.py
│   │       └── natural_image.py
│   ├── util.py
│   ├── config.py
│   ├── default_setting.json
│   ├── __init__.py
│   ├── __main__.py
│   ├── openapi.yml
│   ├── serve.py
└── test
    ├── __init__.py
    └── test_task.py

```

## Request Handling Process

When a request arrives at backend

1. connexion does integrity check on request parameters based on openapi spec
1. connexion decides routing (ie: which function handles this request) based on openapi spec.
1. If the request comes with a not null request_id in header, the request_id will be checked against all request_ids in the past request_id_timeout seconds. If the request_id already exists, this request will be rejected. This prevents the same action, especially create, from being executed more than once. Leave request_id blank if the request don't need such protection.
1. path parameters are passed as parameters to the handler function, request body is available as connexion.request.json
1. Models are de-serialized with marshmallow. Also provides integrity check
1. Further checks are implemented as pre/post triggers for http actions. Like pre_add trigger that rejects creating label with duplicate name under a project.
1. request is handled, data is persisted in database.
1. returns

## Routing

Controllers for endpoints are defined in pplabel.controller. The filename responsible for a path has the same name as the endpoint collection just without the ending s. eg: /projects is handled with functions in pplabel.controller.project.

A function with the same name as request method is used to handle requests. eg: POST /projects is handled with pplabel.controller.project.post. An exception is while GET with path parameter is handled with get, GET without path paramter is handled with get_all.

We provide a standard CRUD template in pplabel.controller.base.crud. It also supports implementing triggers to custermize each handler's behavior.

To add a new endpoint just add a new file under pplabel/controller folder and implement get_all, get, post, put, delete functions in it.

In order to customize method name while generating frontend api calls with openapi-generator, the operationId field is used. The [openapi.yaml](https://github.com/PaddleCV-SIG/PaddleLabel/blob/develop/pplabel/openapi.yml) may not be valid in some openapi spec editors (duplicate operationId) but this type of error can be safely ignored. The routing for /collection/item/collection type endpoints, eg: /projects/{project_id}/tasks, receive special treatment in [resolving](https://github.com/PaddleCV-SIG/PP-Label/blob/develop/pplabel/util.py#L12). In Resolver.resolve_operation_id, the special dict defines the routing for such endpoints. The key is in format f'{endpoint url} {operationId}' and the value is a function for handling the endpoint.

## Naming Scheme

Generally, singular for one item, plural for a collection of items

- Backend
  - Python Variable, Table Columns: snake_case
  - Table Names: camelCase, singular
  - API
    - Endpoint: lower case, plural for a collection
- Frontend
  - camelCase

## Testing

Unit test is not yet implemented. For API and import/export testing see [paddlelabel-test](https://github.com/linhandev/pp-label-test) repo.

## Response Code

- 2xx
  - 200: OK
  - 201: Successfully created
- 4xx
  - 400: connexion and marshmallow constraint fail usually return this, read detail
  - 401: not properlly autherized. Not logged in or isn't allowed to a method
  - 404: an item is not found
  - 409: Conflict, normally due to failing a unique constraint

## Heroku

There is a heroku backend for demo purpose at <https://pplabel.herokuapp.com/api>. The database will be wiped after each redeploy. Redeploy is triggered under two situations:

- new commit to backend code
- if there's no request to backend after certain time, the backend will be recycled. The first new request will take around a minute.

```shell
git push heroku develop:main
heroku ps:restart env
heroku ps:restart web
heroku logs --tail
```

## Note

- In front end, there are if clauses using if(something) to test if something exists. All indexes (xx.xx_id or xx.id) will start from 1.
- Though internally label.id start from 1, but to be compatable with other tools, in labels.txt and xx_list.txt files, labels start from 0.
- All primary keys are named xx_id in backend and xxId in frontend. For example the primary key for annotation table is annotation_id or annotationId. annotation.id is a value user specify mainly for import/export. This value may be changed by user and shouldn't be used as index.

# 互兼容测试

- 待制作数据集
- [ ] 代表数据集已经制作
- [x] 代表已经通过初步测试
- [ ] ~~代表近期不计划支持该格式~~

## EasyData

样例数据集 2023.1.6

- 分类
  - 单分类
    - [ ] ~~EasyData 格式~~
    - [ ] COCO
    - [ ] VOC
    - [x] 文件夹
  - 多分类
    - [ ] ~~EasyData 格式~~
    - [ ] COCO
    - [ ] VOC
    - [ ] ~~文件夹：给的样例和单分类一样，多分类没法通过一个文件夹描述，感觉这个格式支持意义不大~~
- 检测
  - [ ] ~~EasyData 格式~~
  - [x] COCO
  - [x] VOC
- 实例分割
  - [ ] ~~EasyData 格式~~
  - [x] COCO
- 语义分割
  - [ ] 带边缘的伪彩色，label 格式也不一样，待研究
- OCR
  - [x] paddleocr txt
  - [ ] paddleocr coco
  - [ ] EasyData txt
  - [ ] EasyData coco

导出结果

## LabelMe

{: .note-title }

> PaddleLabel 会将数据集路径下所有的图片作为任务导入，使用 labelme 提供的脚本进行数据集格式转换时请不要生成可视化图片，需要在官方给的命令基础上添加一个 --noviz 选项

2023.1.6

- 元素测试
  - [ ] labelme 格式，包含 labelme 支持的所有元素种类
- 分类
  - [ ] labelme flags 分类
- 检测
  - [ ] labelme 格式矩形
  - [x] voc 矩形
    - 使用 labelme 提供的[脚本](https://github.com/wkentaro/labelme/blob/main/examples/bbox_detection/labelme2voc.py)从 labelme 格式转换，转换命令为 `python labelme2voc.py data_annotated data_dataset_voc --labels labels.txt --noviz`
- 实例分割
  - [ ] labelme 格式
  - [ ] voc class+object 格式
    - 使用 labelme 提供的[脚本](https://github.com/wkentaro/labelme/blob/main/examples/instance_segmentation/labelme2voc.py)从 labelme 格式转换，转换命令为`python labelme2voc.py data_annotated data_dataset_voc --labels labels.txt --noviz`
  - [x] coco 格式
    - 使用 labelme 提供的[脚本](https://github.com/wkentaro/labelme/blob/main/examples/instance_segmentation/labelme2coco.py)从 labelme 格式转换，转换命令为`python labelme2voc.py data_annotated data_dataset_coco --labels labels.txt --noviz`
- 语义分割
  - [ ] labelme 格式
  - [ ] voc class 格式
    - 使用 labelme 提供的[脚本](https://github.com/wkentaro/labelme/blob/main/examples/semantic_segmentation/labelme2voc.py)从 labelme 格式转换，转换命令为`python labelme2voc.py data_annotated data_dataset_voc --labels labels.txt --noviz`

## LabelImg

LabelImg 已经终止开发，使用 py38, pyqt5==5.12.3 环境运行

2023.1.6

- [x] voc
- [ ] createml
- [x] yolo

## EISeg

2023.1.8

- 语义/实例分割
  - [x] coco
  - [x] eiseg json
- 语义分割
  - [x] 灰度 mask
    - 需要将所有待标注图片放到 `JPEGImages` 文件夹中
    - 需要在 EISeg 中保存 labels.txt，并使用 paddlelabel_tools 按照提示进行转换
  - [x] 伪彩色 mask
    - 需要将所有待标注图片放到 `JPEGImages` 文件夹中
    - 需要在 EISeg 中保存 labels.txt，并使用 paddlelabel_tools 按照提示进行转换
  - [ ] labelme
- 检测
  - [x] coco
  - [x] voc
  - [ ] ~~yolo~~：EISeg 目前导出的 yolo 应该不是常用格式，没法兼容
    - 需要在 EISeg 中保存 labels.txt，并使用 paddlelabel_tools 按照提示进行转换

## LabelBox

## LabelStudio

## PPOCRLabel

## 用户贡献

- 语义分割
  - [ ] 视盘，伪彩色 mask，背景不是黑色
  - [ ]

## PaddleClas

- [ ] https://paddleclas.bj.bcebos.com/data/PULC/person_exists.tar
- https://paddleclas.bj.bcebos.com/data/PULC/pulc_demo_imgs.zip
- https://paddleclas.bj.bcebos.com/data/PULC/text_image_orientation.tar
- https://paddleclas.bj.bcebos.com/data/PULC/safety_helmet.tar
- https://paddleclas.bj.bcebos.com/data/PULC/language_classification.tar
- https://paddleclas.bj.bcebos.com/data/PULC/textline_orientation.tar
- https://paddleclas.bj.bcebos.com/data/PULC/traffic_sign.tar
- https://paddleclas.bj.bcebos.com/data/PULC/car_exists.tar
- https://paddleclas.bj.bcebos.com/data/PULC/person_exists.tar
- https://paddleclas.bj.bcebos.com/data/PULC/pa100k.tar
- https://paddleclas.bj.bcebos.com/data/PULC/safety_helmet.tar

## PaddleSeg

## PaddleDet

## PaddleOCR


http://host.robots.ox.ac.uk/pascal/VOC/voc2008/htmldoc/voc.html#SECTION00031000000000000000
