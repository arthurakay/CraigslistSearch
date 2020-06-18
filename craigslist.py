#!/usr/bin/env python
from datetime import date, datetime, timedelta
from dateutil.parser import parse

from lxml import html
import requests

cities = {
    'annapolis': 'Annapolis, MD',
    'atlanta': 'Atlanta, GA',
    'austin': 'Austin, TX',
    'baltimore': 'Baltimore, MD',
    'boston': 'Boston, MA',
    'charleston': 'Charleston, SC',
    'charlotte': 'Charlotte, NC',
    'chicago': 'Chicago, IL',
    'cleveland': 'Cleveland, OH',
    'dallas': 'Dallas, TX',
    'denver': 'Denver, CO',
    'frederick': 'Frederick, MD',
    'houston': 'Houston, TX',
    'knoxville': 'Knoxville, TN',
    'losangeles': 'Los Angeles, CA',
    'madison': 'Madison, WI',
    'milwaukee': 'Milwaukee, WI',
    'newyork': 'New York, NY',
    'phoenix': 'Phoenix, AZ',
    'philadelphia': 'Philadelphia, PA',
    'portland': 'Portland, OR',
    'racine': 'Kenosha-Racine, WI',
    'raleigh': 'Raleigh / Duraham, NC',
    'saltlakecity': 'Salt Lake City, UT',
    'sanantonio': 'San Antonio, TX',
    'sandiego': 'San Diego, CA',
    'sfbay': 'San Francisco, CA',
    'washingtondc': 'Washington DC'
}

searchTerms = [
    'javascript',
    'python',
    'angular',
    'react',
    'node',
    'front-end',
    'frontend',
    'pentest',
    'penetration'
]

urls = {
    'Gigs': 'https://{0}.craigslist.org/search/ggg?query={1}&sort=date',
    'Jobs (part-time, contact, remote)': 'https://{0}.craigslist.org/search/sof?query={1}&is_telecommuting=1&employment_type=2&employment_type=3&sort=date'
}

link = '<li><a href="{0}" target="_blank">{1}</a></li>'

def parsePostsFromResponse(term, tree):
    '''
    Parses the Craiglist posts out of the raw HTML using XPATH syntax

    Args:
        term (str): The current search term
        tree (HTML document):

    Returns:
        newPostings: a list of strings in HTML format
    '''
    global yesterday

    postings = tree.xpath('//a[contains(@class, "result-title")]/@href')
    titles = tree.xpath('//a[contains(@class, "result-title")]/text()')
    dates = tree.xpath('//time[contains(@class, "result-date")]/@datetime')

    newPostings = []

    for i in range(len(postings)):
        postDate = parse(dates[i])

        if postDate > yesterday:
            newPostings.append(link.format(postings[i], titles[i]))

    if (len(newPostings) > 0):
        newPostings.insert(0, '<ul>')
        newPostings.append('</ul>')
        newPostings.insert(0, '<h4>Search: {0}</h4>'.format(term))

    return newPostings


def getPostsPerSearchTerm(url, key):
    '''
    Loop over all desired searchTerms and return all posts

    Args:
        url (str): URL blob where the search results can be found
        key (str): the Craigslist key representing a city

    Returns:
        results: a list of strings in HTML format
    '''
    global searchTerms
    results = []

    for term in searchTerms:
        page = requests.get(url.format(key, term))
        tree = html.fromstring(page.content)
        posts = parsePostsFromResponse(term, tree)

        # merge the lists
        results = results + posts

    return results


def getAllPostsPerCity(url):
    '''
    Loop over all cities to find the posts we want

    Args:
        url (str): URL blob where the search results can be found

    Returns:
        results: a list of strings in HTML format
    '''
    global cities
    results = []

    for key, city in cities.items():
        posts = getPostsPerSearchTerm(url, key)

        if (len(posts) > 0):
            posts.insert(0, '<h3>{0}</h3>'.format(city))
            results = results + posts

    return results


def setTime():
    '''
    Set the value of "yesterday" for use throughout this script

    Args:
        n/a

    Returns:
        n/a
    '''
    global yesterday
    yesterday = date.today() - timedelta(1)
    yesterday = datetime(yesterday.year, yesterday.month, yesterday.day)


def getCraigslistPosts():
    '''
    Perform a deep loop over our search criteria and return the related posts

    Args:
        n/a

    Returns:
        emailMessage (str): an HTML string to be used as an email body
    '''
    global emailMessage

    content = []
    emailMessage = ''

    setTime()

    for searchType, url in urls.items():
        results = getAllPostsPerCity(url)

        if (len(results) > 0):
            results.insert(0, '<h2>{0}'.format(searchType))
            content = content + results

    if (len(content) == 0):
        content.append('<p>No search results available over the past 24 hours.</p>')

    content.insert(0, '<html><head></head><body>')
    content.append('</body></html>')
    emailMessage = emailMessage.join(content)
    return emailMessage


def main():
    content = getCraigslistPosts()
    print(content)


if __name__ == '__main__':
    main()
