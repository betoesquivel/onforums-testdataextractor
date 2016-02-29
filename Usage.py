# Copy the testdataextractor subfolder into your project's root directory
# Then you can call the extractor from your project's root directory like this:
from testdataextractor.extractor import Extractor
import pprint

obj = Extractor('path_to_test_file_name')
article = obj.extract()
pprint.pprint(article)

# article has the sentences
sents = article['sentences']
print sents

# article has the comments
comms = article['comments']
print article['comments']

# access any single sentence
sents['s78']

# access any single comment
comms['c10']

# access a comment's sentences ids
comms['c10']['sentences_ids']

# you get the idea
