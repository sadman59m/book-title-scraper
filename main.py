# scrap the title of the books that have a star rating of 2
import requests
import bs4
from typing import List
from bs4.element import Tag

def get_title(url: str) -> List[str]:
    # get the html page
    page_book_titles: List[str] = []
    html_page: str = requests.get(url).text

    # format the html page content in a readable way and get the product_pod class elements
    soup: str = bs4.BeautifulSoup(html_page, 'lxml')
    # .select() method always retuns an array. if nothing, then an empty array
    products: List[Tag] = soup.select('.product_pod')

    # loop throug every producs in the array
    for product in products:
        #get the two star rating class
        if len(product.select('.star-rating.Two')) != 0:
            # select the <a> under <h3>
            product_a: Tag = product.select('h3 > a')[0]
            book_title: str = product_a['title']
            page_book_titles.append(book_title)
            
    return page_book_titles


if __name__ == "__main__":
    all_titles: List[str] = []

    base_url = "https://books.toscrape.com/catalogue/page-{}.html"

    # get all titles for all 50 pages
    for page in range(1, 51):
        page_titles: List[str] = get_title(base_url.format(page))
        # all the page titles to the all titles array
        all_titles.extend(page_titles)
        print(f"page {page} done")

    with open('book_titles.txt', 'w') as file:
        for title in all_titles:
            file.write(title + '\n')

    print('Scraping completed. Check the "book_titles.txt" file for the titles. Thank you')