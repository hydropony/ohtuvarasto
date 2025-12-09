import unittest
from warehouse import Warehouse


class TestWarehouse(unittest.TestCase):
    def setUp(self):
        self.warehouse = Warehouse(10)

    def test_constructor_creates_empty_warehouse(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.warehouse.balance, 0)

    def test_new_warehouse_has_correct_capacity(self):
        self.assertAlmostEqual(self.warehouse.capacity, 10)

    def test_adding_increases_balance(self):
        self.warehouse.add_to_warehouse(8)

        self.assertAlmostEqual(self.warehouse.balance, 8)

    def test_adding_decreases_available_space(self):
        self.warehouse.add_to_warehouse(8)

        # available space should be capacity - added amount = 2
        self.assertAlmostEqual(self.warehouse.available_space(), 2)

    def test_taking_returns_correct_amount(self):
        self.warehouse.add_to_warehouse(8)

        received_amount = self.warehouse.take_from_warehouse(2)

        self.assertAlmostEqual(received_amount, 2)

    def test_taking_increases_space(self):
        self.warehouse.add_to_warehouse(8)

        self.warehouse.take_from_warehouse(2)

        # warehouse should have space 10 - 8 + 2 = 4
        self.assertAlmostEqual(self.warehouse.available_space(), 4)

    def test_negative_capacity(self):
        self.warehouse = Warehouse(-1)
        self.assertAlmostEqual(self.warehouse.capacity, 0)

    def test_negative_balance(self):
        self.warehouse = Warehouse(10, -1)
        self.assertAlmostEqual(self.warehouse.balance, 0)

    def test_add_negative(self):
        self.setUp()
        self.warehouse.add_to_warehouse(-1)
        self.assertAlmostEqual(self.warehouse.balance, 0)

    def test_add_overflow(self):
        self.setUp()
        self.warehouse.add_to_warehouse(11)
        self.assertAlmostEqual(self.warehouse.balance, 10)

    def test_take_negative(self):
        self.warehouse = Warehouse(10, 5)
        self.warehouse.take_from_warehouse(-1)
        self.assertAlmostEqual(self.warehouse.balance, 5)

    def test_take_overflow(self):
        self.warehouse = Warehouse(10, 5)
        res = self.warehouse.take_from_warehouse(10)
        self.assertAlmostEqual(self.warehouse.balance, 0)
        self.assertAlmostEqual(res, 5)

    def test_print(self):
        self.warehouse = Warehouse(10, 5)
        expected = "balance = 5, space = 5"
        self.assertEqual(str(self.warehouse), expected)
