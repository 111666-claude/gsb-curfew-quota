# curfew-quota

防沉迷：宵禁时段判定与每日时长额度。仓库里没有命令行入口，现状值用 `scripts/check.py` 打印，
只用 Python 标准库。

```
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **宵禁时段**：只把 `[start_h, end_h)` 这个半开区间算作宵禁；正好等于结束整点不算宵禁。
- **每日额度**：同一玩家同一服务日的累计时长不超过 `daily_limit_ms`，超出部分不再累计。
- **跨日重置**：`settle` 收到更大的服务日时，先把当日累计清零再累计。
- **幂等**：同一个 `session_id` 只结算一次，重复上报不增加累计。
- **不变量**：`remaining_ms` 不小于 0；同一串结算重复执行结果相同。
- **代价**：查询不许全扫会话记录，`scanned` 不随会话数乘查询次数增长；10 万玩家每秒 10 万次查询。

## 输出契约（不改格式）

```
edge=..
rollover=..
dup=..
work=..
```

## 目录

```
curfew/guard.py      宵禁与额度台账
scripts/check.py     打印现状值
tests/test_guard.py  unittest 用例
```
