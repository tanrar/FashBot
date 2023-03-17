import unittest
from unittest.mock import Mock, MagicMock
from fash_bot import ban_users_for_days, extract_days_from_message, ban_user, unban_user_if_banned_by_bot

class TestRedditBot(unittest.TestCase):

    def test_extract_days_from_message(self):
        self.assertEqual(extract_days_from_message("8 days"), 8)
        self.assertEqual(extract_days_from_message("15 days"), 15)
        self.assertIsNone(extract_days_from_message("not a number days"))

    def test_ban_user(self):
        subreddit_mock = MagicMock()
        user_mock = MagicMock()

        ban_user(subreddit_mock, user_mock, 5)

        subreddit_mock.banned.add.assert_called_once_with(user_mock, duration=5, ban_reason="Banned by FashBot")

    def test_unban_user_if_banned_by_bot(self):
        subreddit_mock = MagicMock()
        user_mock = MagicMock(name="test_user")
        banned_by_bot_mock = MagicMock()
        banned_by_bot_mock.user = user_mock
        banned_by_bot_mock.ban_reason = "Banned by FashBot"

        subreddit_mock.banned.return_value = [banned_by_bot_mock]
        result = unban_user_if_banned_by_bot(subreddit_mock, user_mock)
        self.assertTrue(result)
        subreddit_mock.banned.remove.assert_called_once_with(user_mock)

    def test_not_unban_user_if_not_banned_by_bot(self):
        subreddit_mock = MagicMock()
        user_mock = MagicMock(name="test_user")
        not_banned_by_bot_mock = MagicMock()
        not_banned_by_bot_mock.user = user_mock
        not_banned_by_bot_mock.ban_reason = "Banned for another reason"

        subreddit_mock.banned.return_value = [not_banned_by_bot_mock]
        result = unban_user_if_banned_by_bot(subreddit_mock, user_mock)
        self.assertFalse(result)
        subreddit_mock.banned.remove.assert_not_called()

if __name__ == '__main__':
    unittest.main()
