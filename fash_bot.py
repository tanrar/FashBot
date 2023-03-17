import os
import praw
from prawcore import NotFound

def ban_users_for_days(reddit, subreddit_name):
    try:
        subreddit = reddit.subreddit(subreddit_name)
    except NotFound:
        print(f"Subreddit {subreddit_name} not found.")
        return

    for message in reddit.inbox.unread():
        if message.author is not None:
            if message.body.lower() == "unban me":
                if unban_user_if_banned_by_bot(subreddit, message.author):
                    message.reply("You have been unbanned.")
                else:
                    message.reply("You were not banned by FashBot.")
            else:
                days = extract_days_from_message(message.body)
                if days is not None:
                    ban_user(subreddit, message.author, days)
            message.mark_read()

def extract_days_from_message(message):
    try:
        days = int(message.split(" ")[0])
        return days
    except ValueError:
        return None

def ban_user(subreddit, user, days):
    ban_reason = "Banned by FashBot"
    subreddit.banned.add(user, duration=days, ban_reason=ban_reason)
    print(f"{user} has been banned for {days} days.")

def unban_user_if_banned_by_bot(subreddit, user):
    ban_reason = "Banned by FashBot"
    ban_list = subreddit.banned(redditor=user.name)

    for ban_info in ban_list:
        if ban_info.ban_reason == ban_reason:
            subreddit.banned.remove(user)
            print(f"{user} has been unbanned.")
            return True
    return False
