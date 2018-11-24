#!/usr/bin/env python

from datetime import date, datetime, timedelta
from dateutil.parser import parse
from lxml import html
import requests

cities = {
    'austin': 'Austin, TX',
    'baltimore': 'Baltimore, MD',
    'boston': 'Boston, MA',
    'charlotte': 'Charlotte, NC',
    'chicago': 'Chicago, IL',
    'cleveland': 'Cleveland, OH',
    'denver': 'Denver, CO',
    'frederick': 'Frederick, MD',
    'losangeles': 'Los Angeles, CA',
    'madison': 'Madison, WI',
    'milwaukee': 'Milwaukee, WI',
    'newyork': 'New York, NY',
    'philadelphia': 'Philadelphia, PA',
    'racine': 'Kenosha-Racine, WI',
    'saltlakecity': 'Salt Lake City, UT',
    'sfbay': 'San Francisco, CA',
    'washingtondc': 'Washington DC'
}

searchTerms = [
    'javascript',
    'python',
    'pentest',
    'penetration'
]

yesterday = date.today() - timedelta(1)
yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)

url = 'https://{0}.craigslist.org/search/ggg?query={1}&sort=date'
link = '<li><a href="{0}" target="_blank">{1}</a></li>'

print('<html><head></head><body>')

for key, value in cities.items():
    print('<h2>{0}</h2>'.format(value))

    for term in searchTerms:
        print('<h3>Search: {0}</h3>'.format(term))

        page = requests.get(url.format(key, term))
        tree = html.fromstring(page.content)

        postings = tree.xpath('//a[contains(@class, "result-title")]/@href')
        titles = tree.xpath('//a[contains(@class, "result-title")]/text()')
        dates = tree.xpath('//time[contains(@class, "result-date")]/@title')

        print('<ul>')

        for i in range(len(postings)):
            postDate = parse(dates[i])

            if postDate > yesterday:
                print(link.format(postings[i], titles[i]))

        print('</ul>')

print('</body></html>')