from enum import Enum
from os.path import join as os_join
from datetime import date

class Counter(dict):
    def union(self, counter):
        for key,value in counter.items():
            self.add(key, value)

    def add(self, name, number=1):
        if(name in self):
            self[name] += number
        else:
            self[name] = number
        
    def remove(self, name, number=1):
        if(name in self):
            self[name] -= number
            if(self[name] == 0):
                del self[name]
    
    def decrease(self, name, number=1):
        if(self.get(name, 0)>0): self[name] -= number
    
    def decreaseAll(self, number=1):
        for key, value in self.items():
            if(value>0): self[key] = value - number

    def isEmpty(self):
        return True if len(self.keys) == 0 else False
    
    def getAllEqualOrAbove(self, number):
        return [ key for key,value in self.items() if (value>=number)]
    
    def getKeyWithHigherValue(self):
        return max(self, key=self.get)
    
    def to_s(self):
        return [ f"{key}({value})" for key,value in self.items()]

class ArticleTagCounter(Counter):
    def merge(self, articleCounter):
        self.union(articleCounter)
    
    def verify(self, minTagsForAcceptance, maxTagForAcceptance):
        if(len(self.keys())>=minTagsForAcceptance and self.get("img", 0) == 1 and (self.get("span", 0)+self.get("text", 0)) < 6 and self.get("div", 0) < 4 and self.lazyCount(maxTagForAcceptance)):
            return True
        else: return False
    
    def clear(self):
        if(len(self)>0):
            super().clear()
    
    def lazyCount(self, max):
        sum = 0
        for value in self.values():
            sum += value
            if(sum>max): return False
        return True

class InterpreterEnvironment:
    def __init__(self, minTagsForAcceptance=3, minNumOccurences=5, maxTagsForAcceptance=10):
        self.tagCounter = ArticleTagCounter()
        self.articleClasses = Counter()
        self.minNumOccurences = minNumOccurences
        self.minTagsForAcceptance = minTagsForAcceptance
        self.maxTagsForAcceptance = maxTagsForAcceptance
    
    def resetTagCounter(self):
        if(len(self.tagCounter.keys())>0):
            self.tagCounter = ArticleTagCounter()
    
    def checkArticleClasses(self):
        newArticleClasses = Counter()

        self.articleClasses.pop(None, None)

        for articleClass, count in self.articleClasses.items():
            if(count>=self.minNumOccurences): newArticleClasses.add(articleClass, count)
        
        self.articleClasses = newArticleClasses
    
    def createURLInfo(self, url, maxFailedAttemps=1):
        return URLInfo(url, set(self.articleClasses.keys()), maxFailedAttemps)

class URLInfo():
    def __init__(self, url, articleClasses = set(), maxFailedAttemps=1):
        self.url = url
        self.maxFailedAttemps = maxFailedAttemps
        self.tags = Counter()
        self.invalidTags = set()
        self.articleClasses = articleClasses
        self.articleElements = {}
        self.lastTagsUpdate = date.today()
    
    def isEmpty(self):
        return len(self.tags) == 0

class WebSitesInfo:
    def __init__(self):
        self.nonNewsWebSites = set(["https://www.google.com", "https://www.bing.com", "https://duckduckgo.com/", "https://www.yahoo.com"])
        self.newsWebSitesInfo = {}
        self.newsWebSitesScores = Counter()

class LazySplitter:
    def __init__(self, word, delimiter):
        self.word = word + "" if word[-1] == delimiter else delimiter
        self.delimiter = delimiter
        self.index = 0

    def next(self):
        end = self.word.find(self.delimiter, self.index)
        if(end != -1): 
            word = self.word[self.index:end]
            self.index = end+1
            return word
        else: return None

class URLLazySplitter:
    def __init__(self, word):
        self.delimiter = "/"
        self.word = word + "" if word[-1] == self.delimiter else self.delimiter
        self.index = self._getFirstIndex()

    def _getFirstIndex(self):
        index  = self.word.find("//")
        if(index != -1):
            return index + 2
        else: return 0
    
    def reset(self, word):
        self.word = word + "" if word[-1] == self.delimiter else self.delimiter
        self.index = self._getFirstIndex()

    def next(self):
        end = self.word.find(self.delimiter, self.index)
        if(end != -1): 
            word = self.word[self.index:end]
            self.index = end+1
            return word
        else: return None

class ArticleItems(Enum):
    IMG = 0
    HEADER = 1
    TITLE = 2
    DESCRIPTION = 3
    CODE = 4

def createArticleElementsTable(img=None, header=None, title=None, description=None):
    return {ArticleItems.IMG: img, ArticleItems.HEADER: header, ArticleItems.TITLE: title, ArticleItems.DESCRIPTION: description}

class LabeledObject:
    def __init__(self, label, obj):
        self.label = label
        self.object = obj

class DatabaseInfo():
    def __init__(self, path, databaseFile, browser):
        self.path = path
        self.databaseFile = databaseFile
        self.browser = browser
    
    def get_path(self):
        return os_join(self.path, self.databaseFile)

def createScheduleObj(title=None, date=None, startTime=None, endTime=None):
    return {
        ScheduleOperators.TITLE: title,
        ScheduleOperators.DATE: date,
        ScheduleOperators.TIME: [startTime, endTime]
    }

class ScheduleOperators(Enum):
    NONE = 0
    TITLE = 1
    TIME = 2
    DATE = 3
    INTERVAL = 4
    ACTION = 5

class ScheduleActions(Enum):
    ADD = 0
    DEL = 1
    MOD = 2
    NONE = 3
