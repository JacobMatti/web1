from flask import Flask, render_template, request
import praw

app = Flask(__name__)

# Reddit API credentials
client_id = '38LfH0N75mClIleS9wpheg'
client_secret = 'l0aS_mo8Ly0cPRCdJelomHCOGdqsEg'
user_agent = 'bob by u/Open-Package-4790'

# Authenticate via OAuth
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent)


def scrape_reddit_subreddit(subreddit_name, limit=20):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        top_posts = subreddit.top(limit=limit)

        subreddit_data = []

        for post in top_posts:
            post_info = {
                'Title': post.title,
                'Author': post.author.name if post.author else None,  # Handle NoneType for author
                'Score': post.score,
                'URL': post.url
                # Add more fields if needed
            }
            subreddit_data.append(post_info)

        return subreddit_data
    except Exception as e:
        print(f"Error: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    subreddit_data = None
    subreddit_name = None

    if request.method == 'POST':
        subreddit_name = request.form['subreddit']
        subreddit_data = scrape_reddit_subreddit(subreddit_name, limit=5)

    return render_template('index.html', subreddit_data=subreddit_data, subreddit_name=subreddit_name)

