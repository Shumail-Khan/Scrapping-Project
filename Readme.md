Scrapping Project to get results from Twitter, Youtube and Various News Sites, for a specific topic or query.

--------------------------------------------------------------------------------------------------------------

&nbsp;					Steps to Run

Create a virtual python environment using,

(i). 	python -m venv .venv

(ii).	.venv\\Scripts\\activate.bat

Install libraries

(iii).	pip install -r requirements.txt



Run

(iv).	python main.py


--------------------------------------------------------------------------------------------------------------

&nbsp;					Software

Step 1: Input (Seed)

•	Start with one keyword, phrase, or headline

Example:

“earthquake in Turkey August 2025”
•	This seed becomes your search query for all platforms (news, Twitter/X, YouTube).

Step 2: Data Collection

(a) News Websites

What to do

•	Collect articles from credible news sources:
o	International: BBC, CNN, Al Jazeera
o	Regional \& Urdu news websites (e.g., Geo News, Dawn Urdu, Jang)

How

•	Use web scraping tools (BeautifulSoup, Scrapy) or news APIs.
•	For Urdu articles:
o	First extract text in Urdu
o	Then translate to English (Google Translate API or similar)

What to extract

•	Headline
•	Article body
•	Publication time
•	Source name
•	Language (English / Urdu)

(b) Twitter (X)

What to do
•	Search tweets related to your seed keywords, hashtags, or article links.

How

•	Use:
o	Twitter (X) Official API (Academic track if available), or
o	Public datasets if API access is limited

What to extract

•	Tweet text
•	Author handle (hashed or anonymized for privacy)
•	Timestamp
•	Number of likes and retweets

(c) YouTube

What to do
•	Collect videos discussing the same topic.

How
•	Use YouTube Data API
•	Search using:
o	Video titles
o	Descriptions
o	Keywords

What to extract

•	Video title
•	Description
•	Transcript (if available)
•	Comments (optional)
•	Upload time

Step 3: Normalization (Make All Sources Comparable)

This step ensures news, tweets, and videos can be analyzed together.

Text Cleaning

•	Convert all text to:
o	Lowercase
o	Remove punctuation, links, emojis
o	Tokenize (split into words)

Translation

•	Translate all non-English text (e.g., Urdu) into English
•	Use Google Translate API or a multilingual NLP model

Final Storage Format

Store everything in a common structure like:

{
  "source\_type": "news / twitter / youtube",
  "source\_name": "BBC / Geo News / Twitter",
  "text": "translated and cleaned content",
  "timestamp": "YYYY-MM-DD HH:MM"
}

id	source\_type	source\_name	text (English, cleaned)	timestamp

1	news	BBC	strong earthquake hits southern turkey causing building collapse	2025-08-12 09:10
2	news	Geo News (Urdu→EN)	powerful earthquake strikes turkey several people injured	2025-08-12 09:25
3	twitter	X	massive earthquake in turkey today pray for victims	2025-08-12 09:30
4	youtube	TRT World	earthquake in turkey causes casualties rescue operations ongoing	2025-08-12 10:00
5	twitter	X	minor tremor felt in istanbul no damage reported	2025-08-12 10:15

This is for one query once it is done then you need to multiple querries

Your Input Becomes Multiple Queries

Example Queries

query\_id	query\_text
Q1	earthquake in turkey
Q2	pakistan cricket team going to world cup
Q3	trump peace team



Data Collection (Done Per Query)

For each query, you collect:

•	News articles
•	Tweets
•	YouTube content

Example: Query Q1 (Earthquake)

doc\_id	query\_id	source	text

1	Q1	BBC	earthquake hits turkey
2	Q1	Twitter	strong quake in turkey

Query Q2 (Cricket)

doc\_id	query\_id	source	text

10	Q2	Geo	pakistan team qualifies for world cup
11	Q2	Twitter	pakistan cricket squad announced

Query Q3 (Politics)

doc\_id	query\_id	source	text

20	Q3	CNN	trump announces peace team
21	Q3	Twitter	trump peace initiative details