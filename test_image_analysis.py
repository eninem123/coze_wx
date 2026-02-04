#!/usr/bin/env python3
# 测试豆包图片分析功能

from image_analyzer import DoubaoImageAnalyzer

# 创建分析器实例
analyzer = DoubaoImageAnalyzer()

# 测试本地图片分析
local_image_path = "e:\coze_wx\img_v3_02uk_0a706dd4-cfb1-4b6a-973c-8198e6d7448g.jpg"

print(f"=== 测试本地图片分析 ===")
print(f"分析图片: {local_image_path}")

# 执行分析
result = analyzer.analyze_stock_image(local_image_path)

if result:
    print(f"\n✅ 分析成功！")
    print(f"\n分析结果:")
    print(result)
else:
    print(f"\n❌ 分析失败！")
