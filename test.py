from app.Ticket_API import Request
import unittest

# unittest for the making requests to the tickets API
class RequestAPICase(unittest.TestCase):
    def setUp(self):
        self.request = Request()

    # test if the count is available
    def test_count(self):
        flag, content = self.request.getcount()
        self.assertTrue(flag, msg=content)
        self.assertIsInstance(content, int)

    # test if get all tickets is available
    def test_all(self):
        flag, content = self.request.alltickets()
        self.assertTrue(flag, msg=content)
        self.assertIsInstance(content, list)

    # test if get one ticket is available
    def test_oneticket(self):
        flag, content = self.request.getticket(1)
        self.assertTrue(flag, msg=content)
        self.assertTrue(content[0])
        self.assertIsInstance(content[1], dict)

    # test if get pagination tickets is available
    def test_pageticket(self):
        flag, content = self.request.ticketspage('')
        self.assertTrue(flag, msg=content)
        tickets, prevurl, nexturl, pageid = content
        i = 1
        self.assertEqual(prevurl, None)
        self.assertIsInstance(tickets, list)
        self.assertEqual(pageid, i)
        # test if the return next page and previous page is correct
        while nexturl:
            flag, content = self.request.ticketspage(nexturl, pageid+1)
            i += 1
            self.assertTrue(flag, msg=content)
            tickets, prevurl, nexturl, pageid = content
            self.assertIsInstance(tickets, list)
            self.assertEqual(pageid, i)
        while prevurl:
            flag, content = self.request.ticketspage(prevurl, pageid-1)
            i -= 1
            self.assertTrue(flag, msg=content)
            tickets, prevurl, nexturl, pageid = content
            self.assertIsInstance(tickets, list)
            self.assertEqual(pageid, i)


if __name__ == '__main__':
    unittest.main(verbosity=2)
