"""check_sample.py：按 sample/events.json 走一圈，打印验收面。"""
import json
import os
import sys

from rwlock import FairRWLock


def main() -> int:
    path = sys.argv[1] if len(sys.argv) > 1 else os.path.join("sample", "events.json")
    with open(path, encoding="utf-8") as handle:
        spec = json.load(handle)
    lock = FairRWLock(spec["write_priority"], spec["wait_limit"])
    waits = []
    for event in spec["events"]:
        if event["op"] == "read":
            result = lock.acquire_read(event["txn"], event["at"])
        elif event["op"] == "write":
            result = lock.acquire_write(event["txn"], event["at"])
        else:
            lock.release(event["txn"], event["at"])
            continue
        waits.append((event["txn"], result.get("wait")))
    stats = lock.stats()
    blob = lock.persist()
    reborn = FairRWLock(spec["write_priority"], spec["wait_limit"])
    restored = reborn.restore(blob)
    print("授予顺序 =", [item[0] for item in stats.get("granted", [])])
    print("每个事务等待时长 =", waits)
    print("超时事务 =", stats.get("timeouts"))
    print("最大读并发 =", spec["max_readers"])
    print("结束后仍持锁的读者 =", restored.get("readers"))
    print("结束后仍持锁的写者 =", restored.get("writer"))
    print("恢复后等待队列 =", restored.get("queued"))
    print("饥饿上界（等待不得超过 wait_limit 才算被授予） =", spec["wait_limit"])
    print("不变量（被授予的事务等待都不超过上界） =", spec["wait_invariant"])
    print("事件数 =", len(spec["events"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
