# -*- coding: utf-8 -*-
from pathlib import Path
import inspect

from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog, input_dialog
from prompt_toolkit.styles import Style

from simple_file_format import eiseg_label2_paddlelabel

HERE = Path("__file__").parent.absolute()
print(HERE)

# print(inspect.signature(input_dialog))
# exit()


def run():
    # 0. 使用指南
    message_dialog(
        title="PaddleLabel Tools Tui 使用指南",
        text="""
    - 按空格/回车进行选择
    - 完成选择/输入后按Tab切换到确定/退出按钮部分
    - 按空格/回车进行确定
    """,
    ).run()

    # 1. 工具选择
    result = radiolist_dialog(
        title="PaddleLabel Tools Tui",
        text="请选择需要使用的工具",
        values=[
            ("eiseg_label2paddlelabel", "转换EISeg标签列表到PaddleLabel格式"),
        ],
    ).run()

    # 2.1 eiseg 格式标签列表转 PaddleLabel格式
    if result == "eiseg_label2paddlelabel":
        pj_category = radiolist_dialog(
            title="EISeg标签列表转PaddleLabel格式",
            text="请选择标签列表所属项目类型",
            values=[
                ("detection", "目标检测"),
                ("semantic_segmentation", "语义分割"),
            ],
        ).run()

        eiseg_label_path = None
        while eiseg_label_path is None:
            eiseg_label_path = input_dialog(
                title="EISeg标签列表转PaddleLabel格式",
                text=f"""
请输入EISeg标签列表文件文件路径
- 可以为绝对路径
- 可以为相对 {str(HERE)} 的相对路径
                """,
            ).run()
            eiseg_label_path = Path(eiseg_label_path).absolute()
            if not eiseg_label_path.exists():
                message_dialog(
                    title="EISeg标签列表转PaddleLabel格式",
                    text=f"未能找到 {str(eiseg_label_path)} 文件，请确认文件存在，路径输入正确",
                    ok_text="重新输入",
                ).run()
                eiseg_label_path = None
            assert eiseg_label_path is not None
            eiseg_label2_paddlelabel(
                eiseg_label_path,
                add_background=pj_category == "semantic_segmentation",
                label_id_delta=1,
            )


if __name__ == "__main__":
    run()
