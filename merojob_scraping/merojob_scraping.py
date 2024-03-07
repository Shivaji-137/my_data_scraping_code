# -*- coding: utf-8 -*-
"""merojob_scraping.ipynb
A scraping of jobs from Nepal's popular job seeking site, merojob.com

Written by -----> Shivaji Chaulagain <-------
"""

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import re

def get_jobs_data(title):
    title_encoded = title.replace(' ', "%20")
    base_url = "https://merojob.com/search/?q={}&page={}"

    # Get total number of pages
    req = requests.get(base_url.format(title_encoded, 1))
    soup = bs(req.content, 'lxml')
    pagenbr = int(re.findall(r'\d+', soup.find(id='job-count').get_text())[-1])

    # Fetch job links and companies
    links = []
    companies = []
    print("Please wait ", end='')
    for i in range(1, pagenbr + 1):
        reqs = requests.get(base_url.format(title_encoded, i))
        soups = bs(reqs.content, 'lxml')
        companies.extend(name.get('title') for name in soups.find_all('h3', class_='h6'))
        links.extend("https://merojob.com" + cont.find('a').get('href') for cont in soups.find_all(itemprop='title'))
        print(".", end='')
    print('done')

    # Fetch job details
    information = []
    print("Loading ", end = '')
    for link, company in zip(links, companies):
        inform = {'Company': company}

        sou = bs(requests.get(link).content, 'lxml')
        title = sou.find('h1', itemprop="title").get_text(strip=True)
        inform['Title'] = title

        body = sou.find_all('div', class_="card-body p-0 table-responsive")
        for co in body:
            for con in co.find_all('tr'):
                info = [con.get_text(separator=' ', strip=True)]
                for j in info:
                    key = j.split(':')[0]
                    value = j.split(':')[1]
                    inform[key] = value

        inform['No. of Vacancy/s '] = inform.get('No. of Vacancy/s ', '').replace('[', '').replace(']', '')
        information.append(inform)
        print(".",end='')
    print("done")

    return pd.DataFrame(information).replace(np.nan, 'No information')

if __name__ == "__main__":
    job_title = input("Enter the job you want to search for: ")
    df_result = get_jobs_data(job_title)
    print(df_result)
