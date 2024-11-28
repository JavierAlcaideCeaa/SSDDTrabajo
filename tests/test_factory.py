"""Tests for Factory class."""

import unittest
import Ice
import RemoteTypes as rt
from remotetypes.factory import Factory

class TestFactory(unittest.TestCase):
    """Test cases for the Factory class."""

    def setUp(self):
        """Set up the Ice communicator and factory."""
        self.communicator = Ice.initialize()
        self.adapter = self.communicator.createObjectAdapterWithEndpoints("FactoryAdapter", "default -p 0")
        self.adapter.activate()
        self.factory = Factory()
        self.factory.set_adapter(self.adapter)

    def tearDown(self):
        """Clean up the Ice communicator."""
        self.communicator.destroy()

    def test_get_rdict_new(self):
        """Test Factory.get creates a new RDict."""
        rdict = self.factory.get(rt.TypeName.RDict, "test_rdict")
        self.assertIsInstance(rdict, rt.RDictPrx)

    def test_get_rlist_new(self):
        """Test Factory.get creates a new RList."""
        rlist = self.factory.get(rt.TypeName.RList, "test_rlist")
        self.assertIsInstance(rlist, rt.RListPrx)

    def test_get_rset_new(self):
        """Test Factory.get creates a new RSet."""
        rset = self.factory.get(rt.TypeName.RSet, "test_rset")
        self.assertIsInstance(rset, rt.RSetPrx)

    def test_get_rdict_existing(self):
        """Test Factory.get returns an existing RDict."""
        rdict1 = self.factory.get(rt.TypeName.RDict, "test_rdict_existing")
        rdict2 = self.factory.get(rt.TypeName.RDict, "test_rdict_existing")
        self.assertIs(rdict1, rdict2)

    def test_get_rlist_existing(self):
        """Test Factory.get returns an existing RList."""
        rlist1 = self.factory.get(rt.TypeName.RList, "test_rlist_existing")
        rlist2 = self.factory.get(rt.TypeName.RList, "test_rlist_existing")
        self.assertIs(rlist1, rlist2)

    def test_get_rset_existing(self):
        """Test Factory.get returns an existing RSet."""
        rset1 = self.factory.get(rt.TypeName.RSet, "test_rset_existing")
        rset2 = self.factory.get(rt.TypeName.RSet, "test_rset_existing")
        self.assertIs(rset1, rset2)

if __name__ == "__main__":
    unittest.main()
