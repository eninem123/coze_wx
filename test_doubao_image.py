#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试豆包大模型图片分析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from image_analyzer import DoubaoImageAnalyzer

def test_doubao_image_analysis():
    """
    测试豆包图片分析功能
    """
    print("=" * 60)
    print("📸 测试豆包大模型图片分析功能")
    print("=" * 60)
    
    # 创建豆包图像分析器
    analyzer = DoubaoImageAnalyzer()
    
    # 测试图片URL
    test_image_url = "https://example.com/stock_chart.jpg"
    
    print(f"\n测试1: 通用图片分析")
    print("-" * 40)
    general_analysis = analyzer.analyze_image(test_image_url)
    if general_analysis:
        print("✅ 通用图片分析成功:")
        print(general_analysis[:200] + "..." if len(general_analysis) > 200 else general_analysis)
    else:
        print("❌ 通用图片分析失败")
    
    print(f"\n测试2: 股票图片分析")
    print("-" * 40)
    stock_analysis = analyzer.analyze_stock_image(test_image_url)
    if stock_analysis:
        print("✅ 股票图片分析成功:")
        print(stock_analysis[:200] + "..." if len(stock_analysis) > 200 else stock_analysis)
    else:
        print("❌ 股票图片分析失败")
    
    print(f"\n测试3: 提示词生成")
    print("-" * 40)
    if stock_analysis:
        prompt = analyzer.generate_stock_prompt(stock_analysis)
        if prompt:
            print("✅ 提示词生成成功:")
            print(prompt)
        else:
            print("❌ 提示词生成失败")
    else:
        print("⚠️  跳过提示词生成测试（股票分析失败）")
    
    print(f"\n" + "=" * 60)
    print("测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_doubao_image_analysis()
