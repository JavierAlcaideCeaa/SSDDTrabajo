"""Tests for Iterable class."""

import unittest
import RemoteTypes as rt
from remotetypes.iterable import Iterable
from typing import Optional
import Ice

class TestIterable(unittest.TestCase):
    """Test cases for the Iterable class."""

    def test_iter_returns_iterable(self):
        """Test iter returns an object of type Iterable."""
        data = ["item1", "item2", "item3"]
        iterable = Iterable(data)
        self.assertIsInstance(iterable, rt.Iterable)

    def test_next_returns_next_element(self):
        """Test next returns the next element."""
        data = ["item1", "item2", "item3"]
        iterable = Iterable(data)
        self.assertEqual(iterable.next(), "item1")
        self.assertEqual(iterable.next(), "item2")
        self.assertEqual(iterable.next(), "item3")

    def test_next_raises_stop_iteration(self):
        """Test next raises StopIteration when the end is reached."""
        data = ["item1", "item2"]
        iterable = Iterable(data)
        iterable.next()
        iterable.next()
        with self.assertRaises(rt.StopIteration):
            iterable.next()

    def test_next_raises_cancel_iteration(self):
        """Test next raises CancelIteration when the object is modified."""
        data = ["item1", "item2"]
        iterable = Iterable(data)
        data.append("item3")
        with self.assertRaises(rt.CancelIteration):
            iterable.next()

if __name__ == "__main__":
    unittest.main()
