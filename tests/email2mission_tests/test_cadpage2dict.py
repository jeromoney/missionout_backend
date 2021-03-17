import unittest

EXAMPLE_EMAIL = '''
                CALL: CAR CRASH
                PLACE: Wendys
                ADDR: 123 HUCKLEBERRY LN
                CITY: BREMERTON
                ID: Some identifier for this alarm (123456) 
                PRI: Internal priority level (HIGH, A, 123, etc)
                DATE: CAD date (10/17/2012)
                TIME: CAD time 
                MAP: Map page or number: 123-456: Page 5, etc::
                UNIT: UNIT1, UNIT2, etc::
                INFO: Notes, data: other information
                '''


class Cadpage2DictTestCase(unittest.TestCase):
    def test_smoke_test(self):
        import email2mission.cadpage2dict
        email_dict = email2mission.cadpage2dict.parse_email(EXAMPLE_EMAIL)
        self.assertIn("CALL", email_dict.keys())


if __name__ == '__main__':
    unittest.main()
