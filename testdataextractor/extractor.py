from bs4 import BeautifulSoup
import json

class Extractor:
    def __init__(self,gold_file_name='test_data/1957284403.ofs.gold.xml'):
        self.file_name = gold_file_name

    def parse_comments(self, comments):
        '''
        comment = {
            "bloggerId": "author",
            "sentences": [], # all sentences in a comment,
            "parents": [] # the order depends on how beautifulsoup gives me the parents
        }
        '''

        parsed_comments = {}
        for c in comments:
            comment = {}
            comment['bloggerId'] = c['bloggerid']

            comment['sentences_ids'] = [s['id'] for s in c.findAll('s', recursive=False)]
            comment['parents'] = [p['id'] for p in c.findParents("comment")]
            parsed_comments[c['id']] = comment

        return parsed_comments

    def parse_article(self, html):
        soup = BeautifulSoup(html, "lxml")

        sentences = soup.findAll('s')
        parsed_sentences = {}
        for s in sentences:
            parsed_sentences[s['id']] = s.get_text()

        parsed_comments = self.parse_comments(soup.findAll('comment'))

        article = {
            'sentences': parsed_sentences,
            'comments': parsed_comments
        }

        return article

    def extract(self, dtype='dict', verbose=False):
        f = open(self.file_name, 'r')
        article_text = f.read()

        article = self.parse_article(article_text)

        if verbose:
            print len(article['comments'].values()), " comments parsed."
            print len(article['sentences'].values()), " sentences parsed."

        if dtype is 'json':
            json_article = json.dumps(article, indent=4)
            return json_article
        else:
            return article

