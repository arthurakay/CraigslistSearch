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

url = 'https://{0}.craigslist.org/search/ggg?query={1}&sort=date'
link = '<li><a href="{0}" target="_blank">{1}</a></li>'

def getCraigslistPosts(yesterday):
    global cities
    global searchTerms
    global emailMessage

    content = []
    emailMessage = ''

    content.append('<html><head></head><body>')

    for key, value in cities.items():
        newSearchResults = []

        for term in searchTerms:
            page = requests.get(url.format(key, term))
            tree = html.fromstring(page.content)

            postings = tree.xpath('//a[contains(@class, "result-title")]/@href')
            titles = tree.xpath('//a[contains(@class, "result-title")]/text()')
            dates = tree.xpath('//time[contains(@class, "result-date")]/@title')

            newPostings = []

            for i in range(len(postings)):
                postDate = parse(dates[i])

                if postDate > yesterday:
                    newPostings.append(link.format(postings[i], titles[i]))

            if (len(newPostings) > 0):
                newPostings.insert(0, '<ul>')
                newPostings.append('</ul>')
                newPostings.insert(0, '<h3>Search: {0}</h3>'.format(term))

                # merge the lists
                newSearchResults = newSearchResults + newPostings

        if (len(newSearchResults) > 0):
            newSearchResults.insert(0, '<h2>{0}</h2>'.format(value))
            content = content + newSearchResults

    content.append('</body></html>')
    emailMessage = emailMessage.join(content)
    return emailMessage

def main():
    yesterday = date.today() - timedelta(1)
    yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)
    content = getCraigslistPosts(yesterday)
    print(content)

if __name__ == '__main__':
    main()
