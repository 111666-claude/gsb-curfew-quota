"""防沉迷：宵禁时段判定与每日时长额度结算。"""

DAY_MS = 86400000


class Guard:
    """防沉迷台账：宵禁按半开区间判定，额度按玩家+服务日累计，会话幂等。"""

    def __init__(self, curfew_start_h, curfew_end_h, daily_limit_ms):
        self.start_h = curfew_start_h
        self.end_h = curfew_end_h
        self.limit_ms = daily_limit_ms
        self.seen = set()
        self.used = {}
        self.day = 1
        self.scanned = 0

    def in_curfew(self, at_ms):
        """判断某个时刻是否在宵禁 [start_h, end_h) 内，结束整点不算。"""
        hours = (at_ms % DAY_MS) // 3600000
        if self.start_h <= self.end_h:
            return self.start_h <= hours < self.end_h
        return hours >= self.start_h or hours < self.end_h

    def settle(self, session_id, player, day, played_ms):
        """结算一次会话：同一会话只记一次，跨服务日清零，累计不超过日额度。"""
        if session_id in self.seen:
            return False
        self.seen.add(session_id)
        cur_day, used = self.used.get(player, (day, 0))
        if day > cur_day:
            cur_day, used = day, 0
        self.used[player] = (cur_day, min(self.limit_ms, used + played_ms))
        if day > self.day:
            self.day = day
        return True

    def remaining_ms(self, player, day):
        """当天还能玩多久，O(1) 台账查询，不扫会话记录。"""
        self.scanned += 1
        cur_day, used = self.used.get(player, (day, 0))
        if day > cur_day:
            used = 0
        return max(0, self.limit_ms - used)
