import unittest

from werkzeug import Response

import Utils
from Email2Mission.OauthCreator import oauth_creator


class OauthCreatorTestCase(unittest.TestCase):
    def test_OauthCreator(self):
        Utils.set_local_environment()
        result = oauth_creator()
        self.assertIsInstance(result, Response)


if __name__ == '__main__':
    unittest.main()
