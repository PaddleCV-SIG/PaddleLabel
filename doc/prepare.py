from pathlib import Path
import sys
import subprocess

headers = {
    "CN/README.md": """---
layout: home
title: 项目简介
nav_order: 0
permalink: /
""",
    "CN/install.md": """---
layout: default
title: 安装
nav_order: 1
""",
    "CN/quick_start.md": """---
layout: default
title: 快速体验
nav_order: 2
""",
    "CN/manual/manual.md": """---
layout: default
title: 手动标注
nav_order: 3
has_children: true
""",
    # permalink: docs/labeling
    # 手动标注
    "CN/manual/classification.md": """---
layout: default
title: 图像分类
parent: 手动标注
nav_order: 1
""",
    "CN/manual/detection.md": """---
layout: default
title: 目标检测
parent: 手动标注
nav_order: 2
""",
    "CN/manual/semantic_segmentation.md": """---
layout: default
title: 语义分割
parent: 手动标注
nav_order: 3
""",
    "CN/manual/instance_segmentation.md": """---
layout: default
title: 实例分割
parent: 手动标注
nav_order: 4
""",
    "CN/manual/ocr.md": """---
layout: default
title: OCR
parent: 手动标注
nav_order: 5
""",
    # ML辅助
    "CN/ML/ml.md": """---
layout: default
title: 机器学习辅助标注
nav_order: 4
has_children: true
""",
    "CN/ML/install_ml.md": """---
layout: default
title: 机器学习后端安装
parent: 机器学习辅助标注
nav_order: 1
""",
    "CN/ML/classification_ml.md": """---
layout: default
title: 图像分类
parent: 机器学习辅助标注
nav_order: 2
""",
    "CN/ML/detection_ml.md": """---
layout: default
title: 目标检测
parent: 机器学习辅助标注
nav_order: 3
""",
    "CN/ML/interactive_segmentation.md": """---
layout: default
title: 交互式分割
parent: 机器学习辅助标注
nav_order: 4
""",
    "CN/ML/ocr_ml.md": """---
layout: default
title: OCR
parent: 机器学习辅助标注
nav_order: 5
""",
    "CN/training/training.md": """---
layout: default
title: 进行训练
nav_order: 4
has_children: true
permalink: docs/training
""",
    "CN/training/PdLabel_PdX.md": """---
layout: default
title: PaddleX 分类/检测/分割
parent: 进行训练
nav_order: 4
""",
    "CN/training/PdLabel_PdDet.md": """---
layout: default
title: PaddleDetection 道路标志检测
parent: 进行训练
nav_order: 2
""",
    "CN/training/PdLabel_PdClas.md": """---
layout: default
title: PaddleClas 花朵分类
parent: 进行训练
nav_order: 1
""",
    "CN/training/PdLabel_PdSeg.md": """---
layout: default
title: PaddleSeg 图像分割
parent: 进行训练
nav_order: 3
""",
    "EN/README.md": """---
layout: home
title: Introduction
nav_order: 0
permalink: /
""",
}

if len(sys.argv) == 1:
    base_url = "/PaddleLabel/"
else:
    base_url = sys.argv[1]

HERE = Path(__file__).parent.absolute()
for name, header in headers.items():
    # if name != "CN/install.md":
    #     continue
    path = HERE / name
    print("----")
    print(path)
    content = path.read_text()
    content = content.replace(".md", ".html")
    content = content.replace("/doc/", base_url)
    lines = content.split("\n")
    lines = [l for l in lines if not l.endswith(".mp4")]
    content = "\n".join(lines)
    # cmd = f"git rev-list --count HEAD {name}"
    cmd = f"git --no-pager log -1 --pretty='%ad' --date=iso {name}"
    # print(cmd)
    last_mod = subprocess.run(cmd.split(" "), capture_output=True, encoding="utf8").stdout.strip()
    if path.name != "README.md":
        header += f"permalink: {str(name).replace('.md', '.html').replace('CN/','').replace('EN/','')}\n"
    header += f"last_modified_date: {last_mod}\n---\n\n"

    content = header + content
    path.write_text(content)
