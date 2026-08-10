# Market Calendar for iPhone

一个通过 GitHub Pages 发布的可订阅投资事件日历。

## iPhone 订阅

打开：`https://desolatepuppy.github.io/market-calendar/`

或在 iPhone 的“设置 → App → 日历 → 日历账户 → 添加账户 → 其他 → 添加已订阅的日历”中粘贴：

`https://desolatepuppy.github.io/market-calendar/investment3_portfolio_watch_pdt.ics`

## 内容范围

- 美国 CPI、PPI、非农、零售销售
- FOMC 决议与会议纪要
- On / HP / 小米 / 上海复旦 / 紫光财报验证节点
- Nintendo 海外定价和经营复盘节点
- Sandisk投资者日与DRAM/NAND/NOR/SLC NAND月度复核
- 现代电气月度订单、盈利及估值复核
- Investment 3.5月度评分与资本授权复盘
- SpaceX 2026 年主要流通盘解锁节点
- 不写持仓股数、成本或私人账户数据

## 更新

1. 编辑 `events.json`。
2. 运行 `python generate_ics.py`。
3. 运行 `python scripts/validate_calendar.py`。
4. 提交更新后的 `events.json`、`investment3_portfolio_watch_pdt.ics` 和兼容别名 `calendar.ics`。

订阅URL不会改变，iPhone会按系统节奏刷新。发布日期可能被官方修改，使用前请核对事件描述中的官方链接。
