import csv
import requests
from bs4 import BeautifulSoup
from app.models.book import Book
from app.db.database import get_db
from sqlalchemy.orm import Session

BASE_URL = "https://books.toscrape.com"

def get_soup(url):
  response = requests.get(url)
  response.encoding = 'utf-8'
  response.raise_for_status()
  return BeautifulSoup(response.text, 'html.parser')

def parse_book(book_element):
    title = book_element.h3.a["title"]
    price = book_element.select_one(".price_color").text.strip()
    availability = book_element.select_one(".availability").text.strip()
    stars_class = book_element.select_one(".star-rating")["class"]
    stars = stars_class[1]
    image_rel_url = book_element.select_one("img")["src"]
    image_url = f"{BASE_URL}/{image_rel_url.replace('../', '')}"

    # Pegar o link para a página do livro
    book_rel_url = book_element.h3.a["href"]
    book_url = f"{BASE_URL}/catalogue/{book_rel_url.replace('../', '')}"

    # Buscar a página do livro
    book_soup = get_soup(book_url)

    # A categoria está no breadcrumb, normalmente em li:nth-child(3)
    breadcrumb = book_soup.select("ul.breadcrumb li a")
    category = breadcrumb[2].text.strip() if len(breadcrumb) > 2 else "Unknown"

    # Convert text stars rating to numeric
    stars_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    numeric_stars = stars_mapping.get(stars, 0)  # Default to 0 if not found
    
    return {
      "title": title,
      "price": float(price.replace("£", "")),
      "availability": availability,
      "stars": numeric_stars,
      "image_url": image_url,
      "category": category
    }

def scrap_all_books():
  books = []
  page_number = 1

  while page_number < 5:
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    print(f"Scraping page {page_number}...")

    try:
      soup = get_soup(url)
    except requests.HTTPError:
      print(f"Failed to retrieve page {page_number}. Stopping the scrape.")
      break

    book_items = soup.select('.product_pod')
    if not book_items:
      print(f"No more books found on page {page_number}. Stopping the scrape.")
      break

    for item in book_items:
      books.append(parse_book(item))

    page_number += 1

  return books

def save_to_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
      writer = csv.DictWriter(f, fieldnames=books[0].keys())
      writer.writeheader()
      writer.writerows(books)

    print(f"Scraped {len(books_data)} books and saved to 'books.csv'.")


def save_to_db(books):
  db: Session = next(get_db())

  for b in books:
    try:
      book = Book(
        title=b["title"],
        price=b["price"],
        availability=b["availability"],
        stars=b["stars"],
        image_url=b["image_url"],
        category=b["category"]
      )
      db.add(book)
    except Exception as e:
      print(f"Error saving book '{b['title']}': {e}")

  db.commit()
  db.close()

  print(f"Scraped {len(books_data)} books and saved to database.")

if __name__ == "__main__":
  books_data = scrap_all_books()
  save_to_csv(books_data)
  save_to_db(books_data)
