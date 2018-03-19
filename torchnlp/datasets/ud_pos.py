import os
import io

from torchnlp.utils import download_extract
from torchnlp.datasets.dataset import Dataset


def ud_pos_dataset(directory='data/',
                   train=False,
                   dev=False,
                   test=False,
                   train_filename='en-ud-tag.v2.train.txt',
                   dev_filename='en-ud-tag.v2.dev.txt',
                   test_filename='en-ud-tag.v2.test.txt',
                   name='en-ud-v2',
                   check_file='en-ud-v2/en-ud-tag.v2.train.txt',
                   url='https://bitbucket.org/sivareddyg/public/downloads/en-ud-v2.zip'):
    """
    Load the Universal Dependencies - English Dependency Treebank dataset.

    Corpus of sentences annotated using Universal Dependencies annotation. The corpus comprises
    254,830 words and 16,622 sentences, taken from various web media including weblogs, newsgroups,
    emails, reviews, and Yahoo! answers.

    More details:
    http://universaldependencies.org/
    https://github.com/UniversalDependencies/UD_English

    Citation:
    Natalia Silveira and Timothy Dozat and Marie-Catherine de Marneffe and Samuel Bowman and
    Miriam Connor and John Bauer and Christopher D. Manning (2014).
    A Gold Standard Dependency Corpus for {E}nglish

    Args:
        directory (str, optional): Directory to cache the dataset.
        train (bool, optional): If to load the training split of the dataset.
        dev (bool, optional): If to load the development split of the dataset.
        test (bool, optional): If to load the test split of the dataset.
        train_filename (str, optional): The filename of the training split.
        dev_filename (str, optional): The filename of the development split.
        test_filename (str, optional): The filename of the test split.
        name (str, optional): Name of the dataset directory.
        check_file (str, optional): Check this file exists if download was successful.
        url (str, optional): URL of the dataset `tar.gz` file.

    Returns:
        :class:`tuple` of :class:`list` of :class:`str`: Tuple with the training tokens, dev tokens
        and test tokens in order if their respective boolean argument is true.

    Example:
        >>> from torchnlp.datasets import ud_pos_dataset
        >>> train = ud_pos_dataset(train=True)
        >>> train[17] # Sentence at index 17 is shortish
        {
          'tokens': ['Guerrillas', 'killed', 'an', 'engineer', ',', 'Asi', 'Ali', ',', 'from',
                     'Tikrit', '.'],
          'ud_tags': ['NOUN', 'VERB', 'DET', 'NOUN', 'PUNCT', 'PROPN', 'PROPN', 'PUNCT', 'ADP',
                      'PROPN', 'PUNCT'],
          'ptb_tags': ['NNS', 'VBD', 'DT', 'NN', ',', 'NNP', 'NNP', ',', 'IN', 'NNP', '.']
        }
    """
    download_extract(url=url, directory=directory, check_file=check_file)

    ret = []
    splits = [(train, train_filename), (dev, dev_filename), (test, test_filename)]
    split_filenames = [dir_ for (requested, dir_) in splits if requested]
    for filename in split_filenames:
        full_path = os.path.join(directory, name, filename)
        examples = []
        with io.open(full_path, encoding='utf-8') as f:
            sentence = {'tokens': [], 'ud_tags': [], 'ptb_tags': []}
            for line in f:
                line = line.strip()
                if line == '' and len(sentence['tokens']) > 0:
                    examples.append(sentence)
                    sentence = {'tokens': [], 'ud_tags': [], 'ptb_tags': []}
                elif line != '':
                    token, ud_tag, ptb_tag = tuple(line.split('\t'))
                    sentence['tokens'].append(token)
                    sentence['ud_tags'].append(ud_tag)
                    sentence['ptb_tags'].append(ptb_tag)
        ret.append(Dataset(examples))

    if len(ret) == 1:
        return ret[0]
    else:
        return tuple(ret)
