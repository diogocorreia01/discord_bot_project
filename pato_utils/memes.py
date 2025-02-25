import random
import praw
from pato_utils import constants

class MemeFetcher:
    def __init__(self):
        """Initialize the Reddit API connection."""
        self.reddit = praw.Reddit(
            client_id=constants.REDDIT_CLIENT_ID,
            client_secret=constants.REDDIT_CLIENT_SECRET,
            user_agent=constants.REDDIT_USER_AGENT
        )

    async def get_meme(self, ctx):
        """Fetches a random meme from the r/memes subreddit and sends it to the Discord channel."""
        try:
            subreddit = self.reddit.subreddit("memes")
            memes = [meme for meme in subreddit.hot(limit=50) if not meme.stickied]

            if memes:
                random_meme = random.choice(memes)
                await ctx.send(f"**{random_meme.title}**\n{random_meme.url}")
            else:
                await ctx.send("⚠️ Could not find any memes at the moment.")

        except Exception as e:
            await ctx.send(f"❌ An error occurred while fetching memes: {str(e)}")
