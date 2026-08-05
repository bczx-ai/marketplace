---
name: taobao
displayName: "🛍️ 淘宝/京东/拼多多比价技能"
description: "获取商品在淘宝、天猫、京东、拼多多、抖音、快手上的最优价格和优惠券，用于用户购物或查询优惠信息。"
version: 1.0.3
tags:
  - office_productivity
license: "Unknown"
---

# 买手技能
全网比价，获取中国在线购物平台商品价格、优惠券

```yaml
# 参数解释
source:
  0: 全部
  1: 淘宝/天猫
  2: 京东
  3: 拼多多
  4: 苏宁
  5: 唯品会
  6: 考拉
  7: 抖音
  8: 快手
  10: 1688
```

## 搜索商品
```shell
uv run scripts/main.py search --source=0 --keyword='{keyword}'
uv run scripts/main.py search --source=0 --keyword='{keyword}' --page=2
```

## 商品详情及购买链接
```shell
uv run scripts/main.py detail --source={source} --id={goodsId}
```

## 关于脚本
本技能提供的脚本不会读写本地文件，可放心使用。 脚本仅作为客户端请求三方网站`maishou88.com`的商品和价格数据。