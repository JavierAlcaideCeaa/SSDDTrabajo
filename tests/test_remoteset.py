"""Tests for RemoteSet class."""

import unittest
import RemoteTypes as rt
from remotetypes.remoteset import RemoteSet
from typing import Optional
import Ice

class TestRemoteSet(unittest.TestCase):
    """Test cases for the RemoteSet class."""

    def setUp(self):
        """Set up a RemoteSet instance."""
        self.remote_set = RemoteSet("test_set")

    def test_remove_existing_element(self):
        """Test RSet.remove removes an existing element."""
        self.remote_set.add("item1")
        self.remote_set.remove("item1")
        self.assertFalse(self.remote_set.contains("item1"))

    def test_remove_non_existing_element(self):
        """Test RSet.remove raises KeyError for non-existing element."""
        with self.assertRaises(rt.KeyError):
            self.remote_set.remove("item1")

    def test_length(self):
        """Test RSet.length returns the correct length."""
        self.remote_set.add("item1")
        self.remote_set.add("item2")
        self.assertEqual(self.remote_set.length(), 2)

    def test_contains_false(self):
        """Test RSet.contains returns False if the value does not exist."""
        self.assertFalse(self.remote_set.contains("item1"))

    def test_contains_true(self):
        """Test RSet.contains returns True if the value exists."""
        self.remote_set.add("item1")
        self.assertTrue(self.remote_set.contains("item1"))

    def test_hash_same(self):
        """Test RSet.hash returns the same value if the set is not modified."""
        self.remote_set.add("item1")
        hash1 = self.remote_set.hash()
        hash2 = self.remote_set.hash()
        self.assertEqual(hash1, hash2)

    def test_hash_different(self):
        """Test RSet.hash returns different values if the set is modified."""
        self.remote_set.add("item1")
        hash1 = self.remote_set.hash()
        self.remote_set.add("item2")
        hash2 = self.remote_set.hash()
        self.assertNotEqual(hash1, hash2)

    def test_add_new_element(self):
        """Test RSet.add adds a new element to the set."""
        self.remote_set.add("item1")
        self.assertTrue(self.remote_set.contains("item1"))

    def test_add_existing_element(self):
        """Test RSet.add does not add an existing element to the set."""
        self.remote_set.add("item1")
        self.remote_set.add("item1")
        self.assertEqual(self.remote_set.length(), 1)

    def test_pop_returns_element(self):
        """Test RSet.pop returns an element from the set."""
        self.remote_set.add("item1")
        item = self.remote_set.pop()
        self.assertEqual(item, "item1")

    def test_pop_removes_element(self):
        """Test RSet.pop removes the returned element from the set."""
        self.remote_set.add("item1")
        self.remote_set.pop()
        self.assertFalse(self.remote_set.contains("item1"))

    def test_pop_raises_key_error(self):
        """Test RSet.pop raises KeyError if the set is empty."""
        with self.assertRaises(rt.KeyError):
            self.remote_set.pop()

if __name__ == "__main__":
    unittest.main()
