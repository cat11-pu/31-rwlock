"""rwlock.py：读写锁（基线：读优先、无队列、写立刻失败）。"""
from __future__ import annotations


class FairRWLock:
    def __init__(self, write_priority: bool = True, wait_limit: int = 5):
        self.write_priority = write_priority
        self.wait_limit = wait_limit
        self.readers = set()
        self.writer = None
        self.queue = []
        self.granted = []
        self.timeouts = []
        self.started = {}

    def acquire_read(self, txn: str, at: int) -> dict:
        """基线：读优先，来了就给。"""
        self.readers.add(txn)
        self.started[txn] = at
        self.granted.append((txn, at))
        return {"granted": True, "wait": 0}

    def acquire_write(self, txn: str, at: int) -> dict:
        """基线：有持有者就直接失败，不排队。"""
        if not self.readers and self.writer is None:
            self.writer = txn
            self.started[txn] = at
            self.granted.append((txn, at))
            return {"granted": True, "wait": 0}
        return {"granted": False, "wait": None}

    def release(self, txn: str, at: int) -> dict:
        released = txn in self.readers or self.writer == txn
        self.readers.discard(txn)
        if self.writer == txn:
            self.writer = None
        return {"released": released}

    def pending(self) -> list:
        return list(self.queue)

    def persist(self) -> bytes:
        raise NotImplementedError("快照还没实现")

    def restore(self, blob: bytes = None) -> dict:
        raise NotImplementedError("重启恢复还没实现")

    def stats(self) -> dict:
        return {"readers": sorted(self.readers), "writer": self.writer, "queued": len(self.queue),
                "granted": list(self.granted), "timeouts": list(self.timeouts)}
