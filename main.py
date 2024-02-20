import requests
from bs4 import BeautifulSoup
import json

def scrape_site(url,already_saved_authors):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')

    quotes_list=[]
    authors_list=[]
    for i in range(0, len(quotes)):
        tagsforquote = tags[i].find_all('a', class_='tag')
        quote_dict = {"quote":quotes[i].text,"author":authors[i].text,"tags":[tagforquote.text for tagforquote in tagsforquote]}
        quotes_list.append(quote_dict)
        if authors[i].text not in already_saved_authors:
            already_saved_authors.append(authors[i].text)
            author_name_prepered = '-'.join(authors[i].text.replace('\'','').replace('\u00e9','e').replace('.',' ').split())
            author=scrape_author(f"https://quotes.toscrape.com/author/{author_name_prepered}/",authors[i].text)
            authors_list.append(author)
        
    return quotes_list,authors_list

def scrape_author(url, name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text)
    birth_place = soup.find_all('span', class_="author-born-location")
    birth_date = soup.find_all('span', class_="author-born-date")
    description = soup.find_all('div', class_="author-description")

    author_dict = {"fullname":name,
                   "born_date":birth_date[0].text,
                   "born_location":birth_place[0].text,
                   "description":description[0].text}
    return author_dict
    
        

if __name__=="__main__":
    already_saved_authors = ['Albert Einstein','Steve Martin']
    authors_list = []
    quotes_list = []
    for i in range(1,11):
        quotes, authors = scrape_site(f'https://quotes.toscrape.com/page/{i}/',already_saved_authors)
        quotes_list.extend(quotes)
        authors_list.extend(authors)
        print(f"Page {i} complete")
    
    with open('more_quotes.json','w') as fh:
        json.dump(quotes_list,fh)
    with open('more_authors.json','w') as fh:
        json.dump(authors_list,fh)

    
