from ..items import DarkWebScrapingItem
import nltk
nltk.download('stopwords')
from collections import Counter
import lxml.html.clean
from string import punctuation
import logging

import scrapy
from scrapy.utils.log import configure_logging
from nltk.corpus import stopwords
from nltk import PorterStemmer
from bs4 import BeautifulSoup


stemmer = PorterStemmer()


# GLOBALS
STOPS = set(stopwords.words("english"))

def cleanme(content):
    """
    input: A String
    return: A Word Count Dictionary 
    - Remove Tags
    - Special Character Free (\n, \r, \t, extra_space)
    - Remove Punctuations
    - Create Word List
    - Remove Stop words (English)
    - Use Steaming
    - Word Count | TF-IDF
    """
    # Remove Tags
    cleaner = lxml.html.clean.Cleaner(
        allow_tags=[''],
        remove_unknown_tags=False,
        style=True,
    )
    html = lxml.html.document_fromstring(content)
    html_clean = cleaner.clean_html(html)
    text = html_clean.text_content().strip()

    # Special Character Free
    text.lower()
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', ' ')

    # Remove Punctuations
    text = text.translate(str.maketrans('', '', punctuation))

    # Create Word List
    word_list = text.split(' ')

    # Remove Stop words (English)
    filtered_words = [word for word in word_list if word not in STOPS]

    # Steaming
    # tokens = [stemmer.stem(t) for t in filtered_words] # no stemming 06-09-2020 | will consider lemmatization

    # Word Count
    # return dict(Counter(tokens)) # no stemming
    return dict(Counter(filtered_words))

    # TF-IDF
    # word_counter = Counter(tokens)
    # total_words = sum(word_counter.values())
    # for key in word_counter:
    #     word_counter[key] = word_counter[key]/total_words
    # return word_counter


class DRL(scrapy.Spider):

    name = 'DRL'
    allowed_domains = ['onion']

    start_urls =  ['http://jaz45aabn5vkemy4jkg4mi4syheisqn2wn2n4fsuitpccdackjwxplad.onion/']+ \
                  ['http://ly75dbzixy7hlp663j32xo4dtoiikm6bxb53jvivqkpo6jwppptx3sad.onion/'] + \
                  ['http://5xtktk7q63l533qiiupxc5nvnivzzn4mvonwaajl6vdp5p7bjatkcbad.onion/'] + \
                  ['http://5xtktk7q63l533qiiupxc5nvnivzzn4mvonwaajl6vdp5p7bjatkcbad.onion/'] + \
                  ['http://fc3ryhftqfgwyroq7pt63f7jif4jknfrmd3pbdwm4sz3myelf4wfz7qd.onion/'] + \
                  ['http://r3q6nxpmfdxhzz3oumaseyfr5qujvg4cayzvj2ygy6rfskz4bbhugnyd.onion/'] + \
                  ['http://7nroowrqwdgbyajwrynxtypkdi46f22akwki73etfu2wwmra3ytdhoyd.onion/'] + \
                  ['http://hpcphv5q3lhiebh6c765lslihne4tn6ui5dnd636eo2ic3ytv7c72qid.onion/'] 
                  
                    
    # Logging
    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='DRL_LOGS.log',
        format='%(levelname)s %(asctime)s: %(message)s',
        level=logging.ERROR
    ) 

    def parse(self, response):

        soup = BeautifulSoup(response.body, "html.parser")
        links = set()
        try:
            for link in soup.findAll('a'):
                inspect_link = link.get('href')
                if '.onion' in inspect_link:
                    links.update({inspect_link})
        except:
            pass

        # Title
        title = soup.title.text
        title_keywords = cleanme(title)

        # Meta Keywords & Description
        meta_tags = soup.find_all('meta')

        for meta_tag in meta_tags:
            if meta_tag.get('name') in ['keywords', 'Keywords']:
                keywords =  cleanme(meta_tag.get('content'))
                break
            else:
                keywords = ''

        for meta_tag in meta_tags:
            if meta_tag.get('name') in ['description', 'Description']:
                # description =  cleanme(meta_tag.get('content')) # not cleaning description as it's not a part of search param | 06-09-2020
                description =  str(meta_tag.get('content'))
                break
            else:
                description = ''

        word_frequency = cleanme(response.text)
        # print(dir(response))

        ## Older yield
        # yield {
        #     'url': response.url,
        #     'title': title,
        #     'title_keywords': title_keywords,
        #     'keywords': keywords,
        #     'description': description,
        #     'meta': response.meta,
        #     'links': links,
        #     'word_frequency': word_frequency
        # }

        ## New yield for API v1: 06-09-2020 | In v1 revision 2, we will be providing back the content also on a new endpoint
        ## Removing proxy key from Meta Data
        meta_data = {key:val for key, val in response.meta.items() if key not in ['proxy', 'download_timeout']}
        # item = DarkWebScrapingItem()
        # item['url'] = response.url
        # item['title'] = title
        # item['title_keywords'] = title_keywords
        # item['keywords'] = keywords
        # item['description'] = description
        # item['meta'] = meta_data
        # item['links'] = links

        # yield item

        yield {
            'url': response.url,
            'title': title,
            'title_keywords': title_keywords,
            'keywords': keywords,
            'description': description,
            'meta': meta_data,
            'body' : soup.body.get_text(" ")
        }

        # Recursion |  Change Depth Settings in Settings.py
        next_pages = links

        for next_page in next_pages:
            if next_page:
                yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse)