from bs4 import BeautifulSoup
import requests
import csv

def scrape_lottery_posts(url, base_url="https://www.lotterypost.com"):
  data = []
  while url:  # Loop until there's no more "Next Month" link
    print(url)
    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
     }
    response = requests.get(url, headers=headers)  
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all news entries on current page
    news_entries = soup.find_all("p", class_="newsstory")

    # Extract data from each entry
    for entry in news_entries:
      title = entry.find("a").text.strip()
      date = entry.find("time")["datetime"]
      #comment_count = int(entry.find_all("a")[1].text.split()[0])  # Extract number from "X comments"
      comment_count = 0  # Set default comment count to 0
      anchors = entry.find_all("a")
      if len(anchors) > 1:  # Check if there are at least 2 anchor tags
        comment_count_element = anchors[1]
        comment_count = int(comment_count_element.text.split()[0])
      news_url = f"{base_url}{entry.find('a')['href']}"
      data.append({
        "title": title,
        "date": date,
        "comment_count": comment_count,
        "url": news_url
      })

    # Find the "Next Month" link using specific class names
   # pagination = soup.find("a", class_="fas fa-angle-left")  # Assuming pagination section exists
    #if pagination:
    next_month_link = soup.find("a", class_="iconlink bold")  # Look for the specific class combination
    if next_month_link:
      url = f"{base_url}{next_month_link['href']}"  # Update URL for next iteration
    else:
      url = None  # No "Next Month" link found, exit the loop
    #else:
    #  url = None  # No pagination section found, exit the loop
      
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
