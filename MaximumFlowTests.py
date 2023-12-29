"""
CS3C, The Max flow problem tests
Abhram Medina

"""
import unittest
from assignment10 import *

class maxFlowTestCases(unittest.TestCase):
    # ValueError test if source and sink are the same
    def testSameSourceAndSink(self):
        graph = FlowGraph("graph with same source and sink", "abcd", [
            ("a", "b", 3),
            ("a", "c", 2),
            ("b", "d", 2),
            ("c", "d", 3),
            ("b", "c", 5)])
        with self.assertRaises(ValueError): graph.max_flow("a", "a")

    # Test case for if there's no path from source to sink
    def testEmptySet(self):
        graph = FlowGraph("graph with no path from source to sink", "abc", [
            ("a", "b", 5)
        ])
        # no path from a to c
        actual = graph.max_flow("a", "c")
        # so expected is an empty set
        expected = set()
        self.assertSetEqual(expected, actual)


    # Two vertices with a single edge test case
    def testTwoVertsTest(self):
        graph = FlowGraph("graph with only two vertices", "ab", [("a", "b", 10)])
        actual_mf = graph.max_flow("a", "b")

        expected_result = {("a", "b", 10)}

        # Verify if the max flow is as expected
        self.assertSetEqual(actual_mf, expected_result)

    # Sample Usage test case
    def testSampleUsage(self):
        graph = FlowGraph("graph from sample usage", "abcd", [
            ("a", "b", 3),
            ("a", "c", 2),
            ("b", "d", 2),
            ("c", "d", 3),
            ("b", "c", 5)])
        actual_mf = graph.max_flow("a", "d")
        expected_mf = {
            ("a", "b", 3),
            ("b", "d", 2),
            ("a", "c", 2),
            ("c", "d", 3),
            ("b", "c", 1),
        }
        self.assertSetEqual(expected_mf,actual_mf)
    # test case for maximum flow example from reading
    def testMaximumFlow(self):
        graph = FlowGraph("graph from maximum flow example", "sabcdt", [
            ("s", "a", 3),
            ("s", "b", 2),
            ("a", "b", 1),
            ("a", "d", 4),
            ("a", "c", 3),
            ("b", "d", 2),
            ("c", "t", 2),
            ("d", "t", 3),
        ])
        actual_mf = graph.max_flow("s", "t")
        expected_mf = {
            ("s", "a", 3),
            ("s", "b", 2),
            ("a", "d", 1),
            ("b", "d", 2),
            ("a", "c", 2),
            ("d", "t", 3),
            ("c", "t", 2)
        }
        self.assertSetEqual(expected_mf,actual_mf)

    # test case for graph of my creation
    def testOtherGraph(self):
        graph = FlowGraph("My graph", "sabcdt", [
            ("s", "a", 5),
            ("s", "b", 2),
            ("a", "b", 3),
            ("b", "d", 5),
            ("a", "c", 2),
            ("b", "c", 2),
            ("c", "t", 4),
            ("d", "t", 3),
        ])
        actual_mf = graph.max_flow("s", "t")
        expected_mf = {
            ("s", "a", 5),
            ("s", "b", 2),
            ("a", "b", 3),
            ("a", "c", 2),
            ("b", "c", 2),
            ("b", "d", 3), # diff
            ("c", "t", 4),
            ("d", "t", 3),
        }
        self.assertSetEqual(expected_mf,actual_mf)



if __name__ == "__main__":
    unittest.main()