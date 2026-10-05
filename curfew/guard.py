"""防沉迷：宵禁时段判定与每日时长额度结算。

口径：宵禁只算 [start_h, end_h) 半开区间；同一玩家同一服务日累计不超过
daily_limit_ms；settle 收到更大的服务日先清零再累计；同一 session_id 只结算一次；
remaining_ms 不为负；查询走字典索引，不全扫会话记录。
"""

DAY_MS = 86400000


class Guard:
    """防沉迷台账。"""

    def __init__(self, curfew_start_h, curfew_end_h, daily_limit_ms):
        self.start_h = curfew_start_h
        self.end_h = curfew_end_h
        self.limit_ms = daily_limit_ms
        self.settled_ids = set()
        self.used = {}
        self.day = 1
        self.scanned = 0

    def in_curfew(self, at_ms):
        """判断某个时刻是否在宵禁内：[start_h, end_h) 半开区间。"""
        hours = (at_ms % DAY_MS) // 3600000
        if self.start_h <= self.end_h:
            return self.start_h <= hours < self.end_h
        return hours >= self.start_h or hours < self.end_h

    def settle(self, session_id, player, day, played_ms):
        """结算一次会话：幂等、跨日清零、超额不再累计。"""
        if session_id in self.settled_ids:
            return False
        self.settled_ids.add(session_id)
        entry = self.used.get(player)
        if entry is None or day > entry[0]:
            used = 0
            settled_day = day if entry is None else max(day, entry[0])
        else:
            used, settled_day = entry[1], entry[0]
        used += played_ms
        if used > self.limit_ms:
            used = self.limit_ms
        self.used[player] = (settled_day, used)
        if day > self.day:
            self.day = day
        return True

    def remaining_ms(self, player, day):
        """当天还能玩多久：字典索引 O(1)，不为负。"""
        self.scanned += 1
        entry = self.used.get(player)
        if entry is None or day > entry[0]:
            used = 0
        else:
            used = entry[1]
        remaining = self.limit_ms - used
        return remaining if remaining > 0 else 0
