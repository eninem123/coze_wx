#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试上传图片到飞书云文档功能
"""

import os
from feishu_messenger import FeishuMessenger


def test_drive_upload():
    """测试上传图片到飞书云文档"""
    print("=== 测试上传图片到飞书云文档 ===")
    
    # 初始化飞书消息管理器
    messenger = FeishuMessenger()
    
    # 测试图片路径（使用项目中已有的图片）
    test_image_path = "d:\\coze_wx\\img_v3_02uk_0a706dd4-cfb1-4b6a-973c-8198e6d7448g.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"❌ 测试图片不存在: {test_image_path}")
        return
    
    print(f"测试图片路径: {test_image_path}")
    print(f"图片大小: {os.path.getsize(test_image_path) / 1024 / 1024:.2f} MB")
    
    # 测试上传到云文档
    print("\n1. 测试上传图片到云文档...")
    
    # 生成文件名
    import time
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    file_name = f"test_image_{timestamp}.jpg"
    
    # 上传到云空间（默认parent_type为ccm_import_open）
    file_token = messenger.upload_image_to_drive(test_image_path, file_name)
    
    if file_token:
        print(f"✅ 上传到云文档成功！file_token: {file_token}")
        print(f"   文件名: {file_name}")
        print("\n2. 上传结果说明：")
        print(f"   • 文件已上传到飞书云空间")
        print(f"   • 可以使用返回的file_token在云文档中引用此图片")
        print(f"   • 例如在电子表格、多维表格中使用此file_token")
    else:
        print("❌ 上传图片到云文档失败！")


if __name__ == "__main__":
    test_drive_upload()
