# OCR 手动标注

<!-- TOC -->

- [数据集格式](#%E6%95%B0%E6%8D%AE%E9%9B%86%E6%A0%BC%E5%BC%8F)
  - [PaddleOCR txt](#paddleocr-txt)
- [数据标注](#%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8)
- [下一步](#%E4%B8%8B%E4%B8%80%E6%AD%A5)

<!-- /TOC -->

{: .note }
有关数据集[导入](../quick_start.html#导入数据集)，[导出](../quick_start.html#导出数据集)，[训练/验证/测试集划分](../quick_start.html#数据集划分)步骤请参快速开始文档

PaddleLabel 目前支持 PaddleOCR txt 格式的数据集导入导出。

## 数据集格式

### PaddleOCR txt

PaddleOCR txt 格式中，所有标注数据存储在 Label.txt 文件中。

样例数据集结构如下

```shell
数据集路径
├── image
│   ├── 1.jpg
│   ├── 2.png
│   ├── 3.webp
│   └── ...
└── Label.txt # 可选

# Label.txt
05.jpg	[{"points": [[x1, y1], [x2, y2], [x3, y3], [x4, y4]], "transcription": "文字内容", "illegibility": true, "language": "ch"}, ...]
```

## 数据标注

## 下一步

您可以继续浏览[自动预标注使用方法](/PaddleLabel/CN/ML/auto_inference.md)了解如何使用 PaddleLabel-ML 提高 OCR 项目标注效率。
