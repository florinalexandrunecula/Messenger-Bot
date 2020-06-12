import unittest
from test_helper import *


class SimpleTest(unittest.TestCase):

    def test_add_even(self):
        add_even('engleza', '26 mai', users[0])
        self.assertTrue(users[0].calendar['26 mai'][0] == 'engleza')



    def test_change_nickname(self):
        actual = change_nickname(123, users[0], 'Ana')
        expected = 'Ti-ai schimbat numele in Ana'
        self.assertEqual(actual, expected)


    def test_cere_calendar(self):
        actual = cere_calendar(123)
        expected = 'http://tinyurl.com/y897kkze'
        self.assertEqual(actual, expected)

    # Returns True or False.
    def test_logout(self):
        actual = logoutUser(users[0].id)
        expected = 'cami a parasit conversatia'
        self.assertEqual(actual, expected)


    def test_login(self):


        actual = loginUser(id, 'Andrei')
        expected = 'Andrei a intrat pe server! Hai sa-l salutam'
        self.assertEqual(actual, expected)


if __name__=='__main__':
    unittest.main()

