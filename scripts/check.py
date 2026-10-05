"""打印各场景下的现状值。"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from curfew.guard import Guard  # noqa: E402


def edge():
    return Guard(22, 8, 3600000).in_curfew(8 * 3600000)


def rollover():
    guard = Guard(22, 8, 3600000)
    guard.settle("s1", "p1", 1, 3600000)
    return guard.remaining_ms("p1", 2)


def dup():
    guard = Guard(22, 8, 36000000)
    guard.settle("s1", "p1", 1, 1800000)
    guard.settle("s1", "p1", 1, 1800000)
    return guard.remaining_ms("p1", 1)


def work():
    guard = Guard(22, 8, 36000000)
    for index in range(3000):
        guard.settle("s-%d" % index, "p-%d" % index, 1, 1000)
    for index in range(3000):
        guard.remaining_ms("p-0", 1)
    return guard.scanned


def main():
    print("edge=%s" % edge())
    print("rollover=%d" % rollover())
    print("dup=%d" % dup())
    print("work=%d" % work())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
