# PaddleLabel 版本更新记录

<!-- TOC -->

- [v1.0.2](#v102)
- [v1.0.1 2023-01-26](#v101-2023-01-26)

<!-- /TOC -->

## v1.0.2

修复 eiseg 的导入里 frontend_id 有 0
注掉所有标注列表里的眼睛

<!-- separator -->

## v1.0.1 2023-01-26

- 前端
  - 【目标检测】：修复 自动推理添加结果类型为 ocr 矩形的问题
  - 【自动推理】：改善 为各个类型项目设置较为合理的默认自动推理阈值
- 后端
  - 【更新提示】：改善 在检测到更新时指引用户访问本页面查看更新内容
  - 【windows 中文路径】：改善 全面从 cv2.imread 转向 PIL.Image.open，取得更好的中文路径支持
  - 【样例数据集】：改善 备份旧版样例数据集并重新创建，去除一些旧版中的文件
  - 【目标检测】：修复 coco 格式导出长宽翻转错误

<!-- separator -->

- v1.0.0 2023-01-17
  - 【OCR】新增 OCR 项目标注能力，支持 [PP-OCRv3](https://github.com/PaddlePaddle/PaddleOCR/blob/release/2.6/doc/doc_ch/PP-OCRv3_introduction.md) 模型预标注
  - 【导入/导出】新增 EISeg 格式导入，新增大量[自动化测试](https://github.com/PaddleCV-SIG/PaddleLabel/actions/workflows/cypress.yml)，修复诸多导入导出 bug
  - 【文档】重新梳理后[文档](https://paddlecv-sig.github.io/PaddleLabel/)内容简洁清晰并和软件一同打包发布，进一步降低上手难度

<!-- separator -->

- v0.5.0 2022-11-30
  - 【界面】全面升级分类、检测及分割的前端标注界面体验，显著提升标注流畅度
  - 【分类】新增 PPLCNet 预训练模型，为分类功能提供预标注能力
  - 【检测】新增 PicoDet 预训练模型，为检测功能提供预标注能力
  - 【分割】(1)优化语义分割及实例分割关于实例的区分，实例分割通过'确认轮廓'来区分实例; (2)新增根据类别或根据实例选择颜色显示模式; (3)修复交互式分割 localStorage 超限问题

<!-- separator -->

- v0.1.0 2022-08-18
  - 【分类】支持单分类与多分类标注及标签的导入导出。简单灵活实现自定义数据集分类标注任务并导出供[PaddleClas](https://github.com/PaddlePaddle/PaddleClas)进行训练
  - 【检测】支持检测框标注及标签的导入导出。快速上手生成自己的检测数据集并应用到[PaddleDetection](https://github.com/PaddlePaddle/PaddleDetection)
  - 【分割】支持多边形、笔刷及交互式等多种标注方式，支持标注语义分割与实例分割两种场景。多种分割标注方式可灵活选择，方便将导出数据应用在[PaddleSeg](https://github.com/PaddlePaddle/PaddleSeg)获取个性化定制模型
