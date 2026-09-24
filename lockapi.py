"""lockapi.py：对外门面（老接口 acquire_*/release 不能改）。"""
from __future__ import annotations

from rwlock import FairRWLock


class LockManager:
    def __init__(self, write_priority: bool = True, wait_limit: int = 5):
        self.lock = FairRWLock(write_priority, wait_limit)

    def acquire_read(self, txn: str, at: int) -> dict:
        return self.lock.acquire_read(txn, at)

    def acquire_write(self, txn: str, at: int) -> dict:
        return self.lock.acquire_write(txn, at)

    def release(self, txn: str, at: int) -> dict:
        return self.lock.release(txn, at)

    def snapshot(self) -> bytes:
        return self.lock.persist()

    def rebuild(self, blob: bytes = None) -> dict:
        return self.lock.restore(blob)
