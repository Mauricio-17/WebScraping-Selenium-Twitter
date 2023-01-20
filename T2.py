import time

from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Tweet
web = 'https://twitter.com/Xbox/status/1613219312709554176'
# web = 'https://twitter.com/search?q=python&src=typed_query'
# La ruta del driver de Google Chrome
path = "D:\STUDY\STUDY\PYTHON\chromedriver.exe"
driver = webdriver.Chrome(executable_path=path)
driver.get(web)
driver.maximize_window()

# We handle every tweet location to scrape
def get_data_tweet(element):
    try:
        username = element.find_element_by_xpath(".//span[contains(text(), '@')]").text
        commentary = element.find_element_by_xpath(".//div[@lang]").text
        tweet_data = [username, commentary] # This is to return the two data
    except:
        tweet_data = ['username', 'commentary']
        pass
    return tweet_data

usernames_data = []
commentaries_data = []
tweet_ids = set()  # We use set() to prevent a repeated tweet
scrolling = True
# It will stop when there are no longer tweets and every iteration represents a group of tweets
while scrolling:
    # Fetching a group of tweets
    tweets = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//article[@role="article"]')))
    # tweets = driver.find_elements_by_xpath('//article[@role="article"]')
    # We are looking the last 15 tweets, and it doesn't need to be more than 15 articles it can be less
    for tweet in tweets[-15:]:
        tweet_data = get_data_tweet(tweet)
        tweet_id = ''.join(tweet_data)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            commentary = " ".join(tweet_data[1].split())
            usernames_data.append(tweet_data[0])
            commentaries_data.append(commentary)

    # Scrolling further down
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # The PAGE size will increase till there is not more content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")

        """ Another condition to stop
        if new_height == last_height:
            scrolling = False
            break
        """
        if len(usernames_data) > 80:
            scrolling = False
            break # stopping the root loop
        else:
            last_height = new_height
            break # stopping inner loop

# Stopping the scraping
driver.quit()

# Preparing a CSV file by using PANDAS
df_tweets = pd.DataFrame({"usernames": usernames_data, "commentaries": commentaries_data})
df_tweets.to_csv("tweets_infinite_scroll.csv", index=False)
print(df_tweets)



