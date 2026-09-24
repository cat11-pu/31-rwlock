import unittest

from lockapi import LockManager
from rwlock import FairRWLock


class TestFairRWLock(unittest.TestCase):
    def test_read_granted_when_free(self):
        lock = FairRWLock()
        self.assertTrue(lock.acquire_read("r1", 0)["granted"])

    def test_write_granted_when_free(self):
        lock = FairRWLock()
        self.assertTrue(lock.acquire_write("w1", 0)["granted"])

    def test_write_refused_when_busy(self):
        lock = FairRWLock()
        lock.acquire_read("r1", 0)
        self.assertFalse(lock.acquire_write("w1", 1)["granted"])

    def test_stats_shape(self):
        self.assertIn("timeouts", FairRWLock().stats())

    def test_manager_wraps_lock(self):
        manager = LockManager()
        manager.acquire_read("r1", 0)
        self.assertEqual(manager.lock.stats()["readers"], ["r1"])


if __name__ == "__main__":
    unittest.main()
