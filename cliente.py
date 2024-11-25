import sys
import Ice
import RemoteTypes as rt


class TestClient:
    def __init__(self, communicator):
        self.communicator = communicator
        self.factory = self.get_factory()

    def get_factory(self):
        factory_proxy = self.communicator.stringToProxy("factory:default -p 10000")
        return rt.FactoryPrx.checkedCast(factory_proxy)

    def test_rlist(self):
        print("Testing RList...")
        rlist = rt.RListPrx.checkedCast(self.factory.get(rt.TypeName.RList, "test_rlist"))
        assert rlist.length() == 0

        rlist.append("item1")
        rlist.append("item2")
        assert rlist.length() == 2
        assert rlist.contains("item1") is True
        assert rlist.contains("item3") is False

        popped_item = rlist.pop()
        assert popped_item == "item2"
        assert rlist.length() == 1
        print("RList passed.")

    def test_rdict(self):
        print("Testing RDict...")
        rdict = rt.RDictPrx.checkedCast(self.factory.get(rt.TypeName.RDict, "test_rdict"))
        assert rdict.length() == 0

        rdict.setItem("key1", "value1")
        rdict.setItem("key2", "value2")
        assert rdict.length() == 2
        assert rdict.contains("key1") is True
        assert rdict.contains("key3") is False

        value = rdict.getItem("key1")
        assert value == "value1"

        popped_value = rdict.pop("key1")
        assert popped_value == "value1"
        assert rdict.length() == 1
        print("RDict passed.")

    def test_rset(self):
        print("Testing RSet...")
        rset = rt.RSetPrx.checkedCast(self.factory.get(rt.TypeName.RSet, "test_rset"))
        assert rset.length() == 0

        rset.add("item1")
        rset.add("item2")
        assert rset.length() == 2
        assert rset.contains("item1") is True
        assert rset.contains("item3") is False

        popped_item = rset.pop()
        assert popped_item in ["item1", "item2"]
        assert rset.length() == 1
        print("RSet passed.")

    def run_tests(self):
        self.test_rlist()
        self.test_rdict()
        self.test_rset()
        print("All tests are passed.")


if __name__ == "__main__":
    with Ice.initialize(sys.argv) as communicator:
        try:
            client = TestClient(communicator)
            client.run_tests()
        except Exception as e:
            print(f"Test failed: {e}")
            sys.exit(1)
