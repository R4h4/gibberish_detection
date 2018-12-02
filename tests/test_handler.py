import unittest
import index


class TestHandlerCase(unittest.TestCase):

    def test_response(self):
        print("testing response.")
        result = index.handler({'queryStringParameters': {'string': 'Karsten'}}, None)
        print(result)
        self.assertEqual(result['statusCode'], 200)
        self.assertEqual(result['headers']['Content-Type'], 'application/json')
        self.assertIn(False, result['body'])


if __name__ == '__main__':
    unittest.main()
