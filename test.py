from app import app
from app.Ticket_API import Request
import unittest

class RequestAPICase(unittest.TestCase):
    def setUp(self):
        self.request = Request()

    # test if the count is available
    def test_count(self):
        flag, content = self.request.getcount()
        self.assertTrue(flag,msg=content)
        self.assertIsInstance(content, int)

    # test if get all tickets is available
    def test_all(self):
        flag, content = self.request.alltickets()
        self.assertTrue(flag,msg=content)
        self.assertIsInstance(content, list)

    # test if get one ticket is available
    def test_oneticket(self):
        flag, content = self.request.getticket(1)
        self.assertTrue(flag,msg=content)
        self.assertTrue(content[0])
        self.assertIsInstance(content[1], dict)

    # test if get pagination is available
    def test_pageticket(self):
        flag, content = self.request.ticketspage('')
        self.assertTrue(flag,msg=content)
        tickets, prevurl, nexturl = content
        self.assertEqual(prevurl, None)
        self.assertIsInstance(tickets, list)
        # test if the return next page and previous page is correct
        while nexturl:
            flag, content = self.request.ticketspage(nexturl)
            self.assertTrue(flag,msg=content)
            tickets, prevurl, nexturl = content
            self.assertIsInstance(tickets, list)
        self.assertEqual(nexturl, None)
        while prevurl:
            flag, content = self.request.ticketspage(prevurl)
            self.assertTrue(flag,msg=content)
            tickets, prevurl, nexturl = content
            self.assertIsInstance(tickets, list)
        self.assertEqual(prevurl, None)


if __name__ == '__main__':
    unittest.main(verbosity=2)
