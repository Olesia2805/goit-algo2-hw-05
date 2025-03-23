# Результати порівняння:
#                        Точний підрахунок   HyperLogLog
# Унікальні елементи              100000.0      99652.0
# Час виконання (сек.)                0.45          0.1

# print("Results of comparison:")
# print(f"{'Exact count':<20}{'HyperLogLog':<20}")

import re
import time
from hyperloglog import HyperLogLog
import mmh3
import math


class HyperLogLog:
    def __init__(self, p=5):
        self.p = p
        self.m = 1 << p
        self.registers = [0] * self.m
        self.alpha = self._get_alpha()
        self.small_range_correction = 5 * self.m / 2  # Поріг для малих значень

    def _get_alpha(self):
        if self.p <= 16:
            return 0.673
        elif self.p == 32:
            return 0.697
        else:
            return 0.7213 / (1 + 1.079 / self.m)

    def add(self, item):
        x = mmh3.hash(str(item), signed=False)
        j = x & (self.m - 1)
        w = x >> self.p
        self.registers[j] = max(self.registers[j], self._rho(w))

    def _rho(self, w):
        return len(bin(w)) - 2 if w > 0 else 32

    def count(self):
        Z = sum(2.0**-r for r in self.registers)
        E = self.alpha * self.m * self.m / Z

        if E <= self.small_range_correction:
            V = self.registers.count(0)
            if V > 0:
                return self.m * math.log(self.m / V)

        return E


def load_ips_from_log(filename):
    try:
        wip_pattern = re.compile(r'"remote_addr":\s*"([\d.]+)"')
        ips = set()

        with open(filename, encoding="utf-8", errors="ignore") as file:
            for line in file:
                match = wip_pattern.search(line)
                if match:
                    ips.add(match.group(1))

        return ips
    except FileNotFoundError:
        print("File not found")
        return 0


def exact_load_ips(ips):
    return len(ips)


def hyperloglog_load_ips(ips):
    hll = HyperLogLog(12)
    for ip in ips:
        hll.add(ip)
    return hll.count()


def compare_methods(filename):
    ips = load_ips_from_log(filename)

    start_time = time.perf_counter()
    ips_exact = exact_load_ips(ips)
    exact_time = time.perf_counter() - start_time

    start_time = time.perf_counter()
    ips_hyperloglog = hyperloglog_load_ips(ips)
    hyperloglog_time = time.perf_counter() - start_time

    print(
        f"|{'Results of comparison:':<25}|" f"{'Exact count':^20}|{'HyperLogLog':^20}|"
    )
    print("-" * 70)
    print(f"|{'Unique elements':<25}|{ips_exact:^20}|{ips_hyperloglog:^20}|")
    print(
        f"|{'Execution time (s)':<25}|{exact_time:^20.10f}|{hyperloglog_time:^20.10f}|"
    )


if __name__ == "__main__":
    filename = "lms-stage-access.log"
    compare_methods(filename)
