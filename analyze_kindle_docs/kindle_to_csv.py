from os import listdir
from os.path import isfile, join
import csv

from bs4 import BeautifulSoup

files = [f for f in listdir("./boooks/") if isfile(join("./boooks/", f))]

with open('books.csv', 'w', newline='') as csvfile:
    fieldnames = ['title', 'author', 'date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for f in files:
        with open(join("./boooks/", f)) as html_doc:
            soup = BeautifulSoup(html_doc, 'html.parser')
            books = soup.find_all("div", class_="myx-fixed-left-grid-inner")
            print('num', len(books))
            for book in books:
                title = book.find("div", class_="myx-color-base myx-text-overflow inline_myx myx-text-align")
                if title is None:
                    print(book.prettify())
                    continue
                author = book.find("div", class_="myx-column myx-text-overflow myx-color-base myx-spacing-top-small myx-span3")
                date = book.find("div",class_="myx-column myx-span2 myx-span2-5 myx-color-secondary myx-spacing-top-small")
                writer.writerow({'title': title.attrs['title'], 'author': author.attrs['title'], 'date':date.get_text()})
                #print(title.attrs['title'], "\t", author.attrs['title'], "\t", date.get_text())
