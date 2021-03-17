import sys
sys.path.append('/Users/justin/Projects/missionout_backend')

import unittest
import firebase_setup
import firebase_admin


class FirebaseTestCase(unittest.TestCase):
    def test_firebase_setup(self):
        import sys
        sys.path.append('/Users/justin/Projects/missionout_backend')
        import utils
        utils.set_local_environment()
        app = firebase_setup.setup_firebase_environment()
        self.assertTrue(type(app) is firebase_admin.App)


if __name__ == '__main__':
    unittest.main()
