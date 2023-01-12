# 交互式分割标注

<!-- TOC -->

- [前置步骤](#%E5%89%8D%E7%BD%AE%E6%AD%A5%E9%AA%A4)
- [进行设置](#%E8%BF%9B%E8%A1%8C%E8%AE%BE%E7%BD%AE)
- [使用交互式标注](#%E4%BD%BF%E7%94%A8%E4%BA%A4%E4%BA%92%E5%BC%8F%E6%A0%87%E6%B3%A8)

<!-- /TOC -->

<!-- TODO: 交互式分割 in action -->

PaddleLabel 基于[EdgeFlow](https://arxiv.org/abs/2109.09406)模型在语义和实例分割项目中提供交互式分割支持。

## 前置步骤

1. 在使用自动预标注功能前请先参考 [此文档](/doc/CN/ML/install_ml.md) 安装 PaddleLabel-ML 辅助标注后端

2. 启动 PaddleLabel 和 PaddleLabel-ML

   打开两个命令行终端，第一个输入 `paddlelabel` 并回车，第二个输入 `paddlelabel-ml` 并回车，分别启动项目的 web 部分和辅助标注部分
   ![](/doc/CN/assets/start_two.png)

3. 创建项目

   您可以参考快速体验文档[创建内置样例项目](/doc/CN/quick_start.md#创建样例项目)或[导入一个数据集](/doc/CN/quick_start.md#导入数据集)

## 进行设置

1. 创建项目后直接进入标注页面，当鼠标悬浮在右侧工具栏“交互式分割”按钮上时，其左侧会出现“交互式分割设置”按钮，点击该按钮将弹出设置面板。
   ![](/doc/CN/assets/interact_button.png)
   ![](/doc/CN/assets/interact_setting.png)
2. 交互式分割设置中，机器学习后端网址为必填项，该网址可以通过观察 PaddleLabel-ML 启动时的命令行输出确定
   ![](/doc/CN/assets/ml_backend_url.png)
3. 模型和权重文件路径为选填项，如果留空，默认使用的模型是 HRNet18_OCR64 通用分割场景高精度模型。此外 EdgeFlow 还提供针对人像，遥感，医疗和瑕疵检测的垂类模型，您可以展开下方列表查看和下载。注意两个路径需要使用绝对路径，模型和权重文件要对应。
   <details> <summary markdown="span">点击查看更多模型</summary>

   | 模型类型     | 适用场景             | 模型结构            | 模型下载地址                                                                                                                       |
   | ------------ | -------------------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
   | 高精度模型   | 通用场景的图像标注   | HRNet18_OCR64       | [static_hrnet18_ocr64_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_cocolvis.zip)                       |
   | 轻量化模型   | 通用场景的图像标注   | HRNet18s_OCR48      | [static_hrnet18s_ocr48_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_cocolvis.zip)                     |
   | 高精度模型   | 通用图像标注场景     | EdgeFlow            | [static_edgeflow_cocolvis](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_edgeflow_cocolvis.zip)                                 |
   | 高精度模型   | 人像标注场景         | HRNet18_OCR64       | [static_hrnet18_ocr64_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr64_human.zip)                             |
   | 轻量化模型   | 人像标注场景         | HRNet18s_OCR48      | [static_hrnet18s_ocr48_human](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_human.zip)                           |
   | 轻量化模型   | 遥感建筑物标注场景   | HRNet18s_OCR48      | [static_hrnet18_ocr48_rsbuilding_instance](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18_ocr48_rsbuilding_instance.zip) |
   | 高精度模型\* | x 光胸腔标注场景     | Resnet50_Deeplabv3+ | [static_resnet50_deeplab_chest_xray](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_resnet50_deeplab_chest_xray.zip)             |
   | 轻量化模型   | 医疗肝脏标注场景     | HRNet18s_OCR48      | [static_hrnet18s_ocr48_lits](https://paddleseg.bj.bcebos.com/eiseg/0.4/static_hrnet18s_ocr48_lits.zip)                             |
   | 轻量化模型\* | MRI 椎骨图像标注场景 | HRNet18s_OCR48      | [static_hrnet18s_ocr48_MRSpineSeg](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_MRSpineSeg.zip)                 |
   | 轻量化模型\* | 质检铝板瑕疵标注场景 | HRNet18s_OCR48      | [static_hrnet18s_ocr48_aluminium](https://paddleseg.bj.bcebos.com/eiseg/0.5/static_hrnet18s_ocr48_aluminium.zip)                   |

   </details>

4. 完成设置后点击“确定”，模型会在后台加载，通常时间不超过 1 分钟。加载完成后页面顶部会弹出消息`模型加载完成，您可以开始使用智能标注工具了`。

## 使用交互式标注

1. 点击页面右侧工具栏中“交互式分割”按钮进入交互式分割模式。此时页面上一些工具会被置灰禁用，再次点击“交互式分割”按钮退出后会恢复
   ![](/doc/CN/assets/interact_mode.png)
2. 选中一个标签，之后在图像中前景位置鼠标左键点击添加正样本点；在模型过度分割，掩膜蔓延到背景的位置鼠标右键点击添加负样本点，点击可以进行多轮。此外您可以在此过程中通过调整分割阈值控制整体边缘位置
3. 无论语义还是实例分割项目，推荐每次只用交互式分割标注一个对象，这样标注精度更高。完成一个对象的标注后，按下鼠标中键保存结果和清空当前控制点
