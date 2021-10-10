#Part I of the project, that is, the following code for retrieving reviews, was inspired by the 
# work done by John Watson Rooney on his youtube channel:
# https://www.youtube.com/channel/UC8tgRQ7DOzAbn9L7zDL8mLg
# https://www.youtube.com/watch?v=DIT8rwyPEns&t=270s 

import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewlist = []

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.replace('Amazon.com: Customer reviews: ', '').strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass

for x in range(1,999):
    soup = get_soup(f'https://www.amazon.com/Apple-iPhone-XR-Fully-Unlocked/product-reviews/B07P6Y7954/ref=cm_cr_getr_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&formatType=current_format&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break
df = pd.DataFrame(reviewlist)
df.to_excel('Iphone_XR.xlsx', index=False)
print('Fin.')
