# APIs

## 选择图片后，上传文件/目录至PaddleX的路径中

- Path: /upload
- Method: POST
- Type: form-data
- Data: pics
- Return:

```json
{
  "code": 0,
  "data": {
      "size": 5, // 有效图片总数
      "id": "bulabula", // 数据集ID
      "message": "5张图片因大小/格式不对添加失败！"
      //...其他信息
  },
}
```

## 获取图片

- Path: /get/picture/{dataset_id}/{pic_id}
- Method: GET
- Return: 二进制图片

## 获取已有标注信息

- Path: /get/annotation/{dataset_id}/{pic_id}
- Method: GET
- Return:

```json
{
    "code": 0,
    "data": [
        {
            "content": [
                {
                    "x": 329.05296950240773,
                    "y": 130.97913322632422
                },
                //...
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
                "visibility": false
            },
            "labelLocation": {
                "x": 422.792937399679,
                "y": 213.80417335473513
            },
            "contentType": "rect"
        }
    ]
}
```

## 添加/修改标注信息

- Path: /set/annotation/{dataset_id}/{pic_id}
- Method: POST
- Data:

```json
[
    {
        "content": [
            {
                "x": 329.05296950240773,
                "y": 130.97913322632422
            },
            //...
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
            "visibility": false
        },
        "labelLocation": {
            "x": 422.792937399679,
            "y": 213.80417335473513
        },
        "contentType": "rect"
    },
    //...
]
```

- Return:

```json
{
    "code": 0,
    "data": "success"
}
```

## 格式转存

### 提交转存任务

- Path: /transform/submit/{type}/{dataset_id}
- Method: GET
- Return:

```json
{
    "code": 0,
    "data": {
        "task_id": 123,
        "dataset_id": "bulabula"
    }
}
```

### 查询进度

- Path: /transform/progress/{task_id}
- Method: GET
- Return:

```json
{
    "code": 1, // 0: 转换完成. 1: 转换中. 2: 转换失败。3: 任务不存在
    "data": {
        "task_id": 123,
        "dataset_id": "bulabula",
        "progress": 52, // 百分比
        "message": "3号图片转换失败<br>18号图片转换失败<br>"
    }
}
```

### 导入PaddleX

- Path: /import_paddlex/{dataset_id}
- Method: GET
- Return:

```json
{
    "code": 0,
    "data": "success"
}
```