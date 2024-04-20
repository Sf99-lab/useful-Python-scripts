from bs4 import BeautifulSoup
import requests
import csv


def scrape_lottery_posts(url):
  headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
  response = requests.get(url, headers=headers)

  #print(response)
  soup = BeautifulSoup(response.content, "html.parser")

  # Find all news entries
  news_entries = soup.find_all("p", class_="newsstory")
  #print(news_entries)

  # Extract data from each entry
  data = []
  base_url = "https://www.lotterypost.com"
  for entry in news_entries:
    title = entry.find("a").text.strip()
    date = entry.find("time")["datetime"]
    comment_count = int(entry.find_all("a")[1].text.split()[0])  # Extract number from "X comments"
    news_url = f"{base_url}{entry.find('a')['href']}"
    data.append({
      "title": title,
      "date": date,
      "comment_count": comment_count,
       "url": news_url
    })

  # Sort data by comment count (descending)
  data.sort(key=lambda entry: entry["comment_count"], reverse=True)

  return data

# Example usage (replace with actual Lottery Post URL)
url = "https://www.lotterypost.com/news" 
data = scrape_lottery_posts(url)
# Write data to CSV file
with open('lottery_posts.csv', 'w', newline='') as csvfile:
  csv_writer = csv.writer(csvfile)
  header = ['Title', 'Date', 'Comment Count', 'URL']
  csv_writer.writerow(header)
  for entry in data:
    row = [entry['title'], entry['date'], entry['comment_count'], entry['url']]
    csv_writer.writerow(row)

print("Lottery post data saved to lottery_posts.csv")

# Print the top 3 most commented posts
for entry in data[:3]:
  print(f"Title: {entry['title']}, Date: {entry['date']}, URL: {entry['url']}, Comments: {entry['comment_count']}")
