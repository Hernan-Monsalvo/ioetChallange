import unittest
from main import calculate
from exceptions import DataError, DayOutboundError


class TestPaymentCalculator(unittest.TestCase):

    def test_input1(self):
        """
        Simple test case 1
        """
        input1 = "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        output1 = ("RENE", 215)
        self.assertEqual(calculate(input1), output1)

    def test_input2(self):
        """
        Simple test case 2
        """
        input2 = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        output2 = ("ASTRID", 85)
        self.assertEqual(calculate(input2), output2)

    def test_continuous_schedule(self):
        """
        Test to ensure the correct behavior in schedules that cross the different periods
        """
        result = ("HUGO", 340)
        self.assertEqual(calculate("HUGO=MO04:00-22:00"), result)

    def test_outbounds_schedule(self):
        """
        Test to ensure the correct behavior in schedules that cross to different day
        """
        input = "RAMON=MO22:00-02:00"
        with self.assertRaises(DayOutboundError):
            calculate(input)

    def test_wrong_format(self):
        """
        Test to ensure the validation of correct data structure
        """
        wrong_format1 = "HUGOMO04:00-22:00"
        with self.assertRaises(DataError):
            calculate(wrong_format1)

        wrong_format2 = "HUGO=MO04:0022:00"
        with self.assertRaises(DataError):
            calculate(wrong_format2)

        wrong_format3 = "HUGO=MO0400-2200"
        with self.assertRaises(DataError):
            calculate(wrong_format3)

        wrong_format4 = "HUGO=04:00-22:00"
        with self.assertRaises(DataError):
            calculate(wrong_format4)


if __name__ == '__main__':
    unittest.main(verbosity=2)
