#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试图片上传功能
"""

import os
from feishu_messenger import FeishuMessenger


def test_image_upload():
    """测试图片上传功能"""
    print("=== 测试图片上传功能 ===")
    
    # 初始化飞书消息管理器
    messenger = FeishuMessenger()
    
    # 测试图片路径（使用项目中已有的图片）
    test_image_path = "d:\\coze_wx\\img_v3_02uk_0a706dd4-cfb1-4b6a-973c-8198e6d7448g.jpg"
    
    if not os.path.exists(test_image_path):
        print(f"❌ 测试图片不存在: {test_image_path}")
        return
    
    print(f"测试图片路径: {test_image_path}")
    print(f"图片大小: {os.path.getsize(test_image_path) / 1024 / 1024:.2f} MB")
    
    # 测试上传图片
    print("\n1. 测试上传图片...")
    image_key = messenger.upload_image(test_image_path)
    
    if image_key:
        print(f"✅ 上传成功！image_key: {image_key}")
        
        # 测试发送图片消息（这里需要一个有效的open_id）
        # 注意：实际测试时需要替换为真实的open_id
        test_open_id = "ou_your_open_id_here"
        
        if test_open_id != "ou_your_open_id_here":
            print("\n2. 测试发送图片消息...")
            success = messenger.send_image_message(test_open_id, image_key)
            if success:
                print("✅ 发送图片消息成功！")
            else:
                print("❌ 发送图片消息失败！")
        else:
            print("\n⚠️  请替换 test_open_id 为真实的open_id以测试发送图片消息功能")
            print(f"   已获得的image_key: {image_key}")
    else:
        print("❌ 上传图片失败！")


if __name__ == "__main__":
    test_image_upload()
