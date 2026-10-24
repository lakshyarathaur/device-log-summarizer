
import math
import unittest

MAX_VALUE = 500.0


def clean_readings(values):
   
    if values is None:
        return []
    try:
        iterator = iter(values)
    except TypeError:
        return []

    cleaned = []
    for item in iterator:
        if item is None or isinstance(item, bool):
            continue
        try:
            number = float(item)
        except (TypeError, ValueError):
            continue
        if math.isnan(number) or number < 0:
            continue
        cleaned.append(min(number, MAX_VALUE))  # inf is clipped to 500.0
    return cleaned


class TestCleanReadings(unittest.TestCase):
    def test_mixed_input(self):
        raw = ["12.5", 7, None, "abc", -3, "-0.1", 750, "500", 0]
        self.assertEqual(clean_readings(raw), [12.5, 7.0, 500.0, 500.0, 0.0])

    def test_empty_list(self):
        self.assertEqual(clean_readings([]), [])

    def test_all_invalid(self):
        self.assertEqual(clean_readings([None, "x", -1, "", float("nan")]), [])

    def test_non_iterable_and_none(self):
        self.assertEqual(clean_readings(None), [])
        self.assertEqual(clean_readings(42), [])


if __name__ == "__main__":
    unittest.main()
