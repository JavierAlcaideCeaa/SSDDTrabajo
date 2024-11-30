"""Tests for RemoteList class."""

import unittest
import os
import Ice
import RemoteTypes as rt
from remotetypes.remotelist import RemoteList

class TestRemoteList(unittest.TestCase):
    """Test cases for the RemoteList class."""

    def setUp(self):
        """Set up a RemoteList instance."""
        self.remote_list = RemoteList("test_list")
        self._clear_remote_list()  # Clear the JSON file before each test

    def tearDown(self):
        """Clean up after each test."""
        self._clear_remote_list()  # Clear the JSON file after each test

    def _clear_remote_list(self):
        """Clear the JSON file for the RemoteList."""
        if os.path.exists(f"{self.remote_list.id_}.json"):
            os.remove(f"{self.remote_list.id_}.json")

    def test_remove_existing_element(self):
        """Test RList.remove removes an existing element."""
        self.remote_list.append("item1")
        self.remote_list.remove("item1")
        self.assertFalse(self.remote_list.contains("item1"))

    def test_remove_non_existing_element(self):
        """Test RList.remove raises KeyError for non-existing element."""
        with self.assertRaises(rt.KeyError):
            self.remote_list.remove("item1")

    def test_length(self):
        """Test RList.length returns the correct length."""
        self.remote_list.append("item1")
        self.remote_list.append("item2")
        self.assertEqual(self.remote_list.length(), 2)

    def test_contains_false(self):
        """Test RList.contains returns False if the value does not exist."""
        self.assertFalse(self.remote_list.contains("item1"))

    def test_contains_true(self):
        """Test RList.contains returns True if the value exists."""
        self.remote_list.append("item1")
        self.assertTrue(self.remote_list.contains("item1"))

    def test_hash_same(self):
        """Test RList.hash returns the same value if the list is not modified."""
        self.remote_list.append("item1")
        hash1 = self.remote_list.hash()
        hash2 = self.remote_list.hash()
        self.assertEqual(hash1, hash2)

    def test_hash_different(self):
        """Test RList.hash returns different values if the list is modified."""
        self.remote_list.append("item1")
        hash1 = self.remote_list.hash()
        self.remote_list.append("item2")
        hash2 = self.remote_list.hash()
        self.assertNotEqual(hash1, hash2)

    def test_append_new_element(self):
        """Test RList.append adds a new element to the end of the list."""
        self.remote_list.append("item1")
        self.assertTrue(self.remote_list.contains("item1"))

    def test_pop_returns_last_element(self):
        """Test RList.pop returns an element from the end of the list."""
        self.remote_list.append("item1")
        item = self.remote_list.pop()
        self.assertEqual(item, "item1")

    def test_pop_removes_last_element(self):
        """Test RList.pop removes the returned element from the end of the list."""
        self.remote_list.append("item1")
        self.remote_list.pop()
        self.assertFalse(self.remote_list.contains("item1"))

    def test_pop_returns_indicated_element(self):
        """Test RList.pop returns the element at the indicated position."""
        self.remote_list.append("item1")
        self.remote_list.append("item2")
        item = self.remote_list.pop(0)
        self.assertEqual(item, "item1")

    def test_pop_removes_indicated_element(self):
        """Test RList.pop removes the element at the indicated position."""
        self.remote_list.append("item1")
        self.remote_list.append("item2")
        self.remote_list.pop(0)
        self.assertFalse(self.remote_list.contains("item1"))

    def test_pop_raises_index_error(self):
        """Test RList.pop raises IndexError if the position does not exist."""
        with self.assertRaises(rt.IndexError):
            self.remote_list.pop(0)

    def test_get_item_returns_indicated_element(self):
        """Test RList.getItem returns the element at the indicated position."""
        self.remote_list.append("item1")
        item = self.remote_list.get_item(0)
        self.assertEqual(item, "item1")

    def test_get_item_maintains_indicated_element(self):
        """Test RList.getItem maintains the element at the indicated position."""
        self.remote_list.append("item1")
        self.remote_list.get_item(0)
        self.assertTrue(self.remote_list.contains("item1"))

    def test_get_item_raises_index_error(self):
        """Test RList.getItem raises IndexError if the position does not exist."""
        with self.assertRaises(rt.IndexError):
            self.remote_list.get_item(0)

if __name__ == "__main__":
    unittest.main()
