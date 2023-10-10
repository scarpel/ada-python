from random import randrange
from .dataTypes import ArticleItems

def splitUrl(url):
    index = url.find("//")
    if(index != -1):
        index = url.find("/", index+2)
        if(index != -1):
            rest = url[index+1:].split("/")
            if(rest[0] != ""): return [url[:index], *rest]
            else: return [url[:index]]
        else: return url
    else: return url.split("/")

def isOnlyDigits(str):
    if any(c.isalpha() for c in str):
            return False
    else: return True

def lazySplit(word, currentIndex, delimiter="/"):
    index = word.find(delimiter, currentIndex)
    if(index != -1): return index+1, word[currentIndex:index]
    else: return -1, word[currentIndex:]

def firstURLLazySplit(word, currentIndex, delimiter="/"):
    index = word.find(delimiter*2)
    if(index != -1): index += 2
    else: index = 0

    index = word.find("/", index)
    if(index != -1): return index+1, word[0:index]
    else: return -1, word[0:]
    
def removeNone(enum):
    if(None in enum): enum.remove(None)
    return enum

def isEndTag(tag):
    if(len(tag)>0):
        return True if tag[0] == '/' else False
    else: return False

def isLinkValid(src):
    if(src is None): return False
    else: return "http" in src

def sortArticleNodesByClass(articles):
    table = {}

    for article in articles:
        if(article.tagClass in table): table[article.tagClass].append(article)
        else: table[article.tagClass] = [article]
    
    return table

def gimmeRandom(n, min, max):
    arr = set()

    while(len(arr) != n):
        arr.add(randrange(min,max))
    
    arr = list(arr)
    arr.sort()
    return arr

def calculate_article_code(articleElements):
    return "".join([get_article_code(articleElements.get(ArticleItems.IMG)), get_article_code(articleElements.get(ArticleItems.HEADER)),
        get_article_code(articleElements.get(ArticleItems.TITLE)), get_article_code(articleElements.get(ArticleItems.DESCRIPTION))])

def get_article_code(articleItem):
    return "1" if articleItem is not None else "0"

def sort_by_url(urls):
    sorted = {}

    for url in urls:
        _, splittedUrl = firstURLLazySplit(url, 0)
        if(splittedUrl in sorted): sorted[splittedUrl].add(url)
        else: sorted[splittedUrl] = set([url])
    
    return sorted

def isArticleElementsTableEmpty(articleTable):
    return articleTable[ArticleItems.TITLE] is None and articleTable[ArticleItems.IMG] is None and articleTable[ArticleItems.HEADER] is None and articleTable[ArticleItems.DESCRIPTION] is None

def sumArticleElementsTableCode(articleTable):
    return sum([int(char) for char in articleTable.get(ArticleItems.CODE, calculate_article_code(articleTable))])

def getArticlesLink(articleTable):
    return articleTable[ArticleItems.TITLE].link
