"""Tests for RemoteDict class."""

import unittest
import os
import RemoteTypes as rt
from remotetypes.remotedict import RemoteDict

class TestRemoteDict(unittest.TestCase):
    """Test cases for the RemoteDict class."""

    def setUp(self):
        """Set up a RemoteDict instance."""
        self.remote_dict = RemoteDict("test_dict")
        self._clear_remote_dict()  # Clear the JSON file before each test

    def tearDown(self):
        """Clean up after each test."""
        self._clear_remote_dict()  # Clear the JSON file after each test

    def _clear_remote_dict(self):
        """Clear the JSON file for the RemoteDict."""
        if os.path.exists(f"{self.remote_dict.id_}.json"):
            os.remove(f"{self.remote_dict.id_}.json")

    def test_remove_existing_element(self):
        """Test RDict.remove removes an existing element."""
        self.remote_dict.set_item("key1", "value1")
        self.remote_dict.remove("key1")
        self.assertFalse(self.remote_dict.contains("key1"))

    def test_remove_non_existing_element(self):
        """Test RDict.remove raises KeyError for non-existing element."""
        with self.assertRaises(rt.KeyError):
            self.remote_dict.remove("key1")

    def test_length(self):
        """Test RDict.length returns the correct length."""
        self.remote_dict.set_item("key1", "value1")
        self.remote_dict.set_item("key2", "value2")
        self.assertEqual(self.remote_dict.length(), 2)

    def test_contains_false(self):
        """Test RDict.contains returns False if the key does not exist."""
        self.assertFalse(self.remote_dict.contains("key1"))

    def test_contains_true(self):
        """Test RDict.contains returns True if the key exists."""
        self.remote_dict.set_item("key1", "value1")
        self.assertTrue(self.remote_dict.contains("key1"))

    def test_hash_same(self):
        """Test RDict.hash returns the same value if the dict is not modified."""
        self.remote_dict.set_item("key1", "value1")
        hash1 = self.remote_dict.hash()
        hash2 = self.remote_dict.hash()
        self.assertEqual(hash1, hash2)

    def test_hash_different(self):
        """Test RDict.hash returns different values if the dict is modified."""
        self.remote_dict.set_item("key1", "value1")
        hash1 = self.remote_dict.hash()
        self.remote_dict.set_item("key2", "value2")
        hash2 = self.remote_dict.hash()
        self.assertNotEqual(hash1, hash2)

    def test_set_item(self):
        """Test RDict.set_item sets an item in the dict."""
        self.remote_dict.set_item("key1", "value1")
        self.assertTrue(self.remote_dict.contains("key1"))

    def test_get_item_raises_key_error(self):
        """Test RDict.get_item raises KeyError if the key does not exist."""
        with self.assertRaises(rt.KeyError):
            self.remote_dict.get_item("key1")

    def test_get_item_returns_value(self):
        """Test RDict.get_item returns the value for a valid key."""
        self.remote_dict.set_item("key1", "value1")
        item = self.remote_dict.get_item("key1")
        self.assertEqual(item, "value1")

    def test_get_item_maintains_value(self):
        """Test RDict.get_item maintains the key and its value."""
        self.remote_dict.set_item("key1", "value1")
        self.remote_dict.get_item("key1")
        self.assertTrue(self.remote_dict.contains("key1"))

    def test_pop_raises_key_error(self):
        """Test RDict.pop raises KeyError if the key does not exist."""
        with self.assertRaises(rt.KeyError):
            self.remote_dict.pop("key1")

    def test_pop_returns_value(self):
        """Test RDict.pop returns the value for a valid key."""
        self.remote_dict.set_item("key1", "value1")
        item = self.remote_dict.pop("key1")
        self.assertEqual(item, "value1")

    def test_pop_removes_value(self):
        """Test RDict.pop removes the key and its value from the dict."""
        self.remote_dict.set_item("key1", "value1")
        self.remote_dict.pop("key1")
        self.assertFalse(self.remote_dict.contains("key1"))

if __name__ == "__main__":
    unittest.main()
