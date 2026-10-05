"""防沉迷：宵禁时段判定与每日时长额度结算。

缺陷：宵禁按闭区间把整点也算进去、每日额度跨服务日不清零、同一会话重复结算、
额度用超也不拦、每次判定全扫会话记录。
"""

DAY_MS = 86400000


class Guard:
    """防沉迷台账。"""

    def __init__(self, curfew_start_h, curfew_end_h, daily_limit_ms):
        self.start_h = curfew_start_h
        self.end_h = curfew_end_h
        self.limit_ms = daily_limit_ms
        self.sessions = []
        self.used = {}
        self.day = 1
        self.scanned = 0

    def in_curfew(self, at_ms):
        """判断某个时刻是否在宵禁内。缺陷：闭区间（正好到点也算宵禁）。"""
        hours = (at_ms % DAY_MS) // 3600000
        return hours >= self.start_h or hours <= self.end_h

    def settle(self, session_id, player, day, played_ms):
        """结算一次会话。缺陷：不查 req、跨日不清零、超额照记。"""
        self.sessions.append((session_id, player, played_ms))
        self.used[player] = self.used.get(player, 0) + played_ms
        self.day = day
        return True

    def remaining_ms(self, player, day):
        """当天还能玩多久。缺陷：全扫会话记录。"""
        self.scanned += len(self.sessions)
        return self.limit_ms - self.used.get(player, 0)
