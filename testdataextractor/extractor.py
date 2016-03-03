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

        parsed_links = self.parse_links(soup.findAll(lambda tag:Extractor.is_valid_link(tag)))

        article = {
            'sentences': parsed_sentences,
            'comments': parsed_comments,
            'links': parsed_links
        }

        return article

    @staticmethod
    def is_valid_link(tag):
        if tag.name != 'link':
            return False
        link = tag

        l_conf = link['link_confidence']
        l_val = link['validation']
        arg = link.find_next_sibling('argument')
        sent = link.find_next_sibling('sentiment')
        a_val = arg['validation']
        s_val = sent['validation']
        a_conf = arg['val_confidence']
        s_conf = sent['val_confidence']
        args = [l_val, a_val, s_val, l_conf, a_conf, s_conf]

        return all(el == '1' or el == 'yes' for el in args)

    def parse_links(self, links):
        parsed_links = {}
        for link_html in links:
            arg_html = link_html.find_next_sibling('argument')
            sent_html = link_html.find_next_sibling('sentiment')
            link = {}
            link['art_sentence'] = link_html['art_sentence']
            link['com_sentence'] = link_html['com_sentence']
            link['confidence'] = link_html['link_confidence']
            link['validation'] = link_html['validation']

            arg = {}
            arg['label'] = arg_html['label']
            arg['confidence'] = arg_html['val_confidence']
            arg['validation'] = arg_html['validation']

            sent = {}
            sent['label'] = sent_html['label']
            sent['confidence'] = sent_html['val_confidence']
            sent['validation'] = sent_html['validation']

            link['argument'] = arg
            link['sentiment'] = sent
            parsed_links[link_html['id']] = link
        return parsed_links


    def extract(self, dtype='dict', verbose=False):
        f = open(self.file_name, 'r')
        article_text = f.read()

        article = self.parse_article(article_text)

        if verbose:
            print len(article['comments'].values()), " comments parsed."
            print len(article['sentences'].values())," sentences parsed."
            print len(article['links'].values()),    " links parsed."

        if dtype is 'json':
            json_article = json.dumps(article, indent=4)
            return json_article
        else:
            return article

