import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    dictionary={}
    for file in os.listdir(directory):
        with open(os.path.join(directory,file),"r",encoding="utf-8") as f:
            dictionary[file]=f.read();
    return dictionary
    #raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words=[]
    for word in nltk.word_tokenize(document):
        word=word.lower()
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english"):
            words.append(word)
    return words
    #raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs={}
    for document in documents:
        for word in documents[document]:
            if word not in idfs:
                idfs[word]=math.log(len(documents)/ sum([ word in documents[doc] for doc in documents]) )
    return idfs
    #raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf={}
    for word in query:
        for file in files:
            tf_idf[file]=tf_idf.get(file,0)+ files[file].count(word)*idfs.get(word,0)
    return sorted(tf_idf,key = lambda k: tf_idf[k], reverse=True)[:n]
    #raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    query_words=set(query) #[ word for word in query if word not in nltk.corpus.stopwords.words("english")])
    counts={}
    td={}
    for sentence in sentences:
        counts[sentence]=0
        for word in query_words:
            counts[sentence]+= ( idfs.get(word,0) if word in sentences[sentence] else 0 )
        td[sentence]=len(query_words.intersection(set(sentences[sentence])))/len(set(sentences[sentence]))

    return sorted(counts,key=lambda k: ( counts[k], td[k]),reverse=True)[:n]
    #raise NotImplementedError


if __name__ == "__main__":
    main()
