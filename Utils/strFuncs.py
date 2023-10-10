def get_until(text, delimiter, start=0, end=None):
    end = len(text) if end is None else end
    delimiterIndex = text.find(delimiter, start, end)
    return text[start: end if delimiterIndex<0 else delimiterIndex]

def get_tag_until(text, delimiter, start=0, end=None):
    end = len(text) if end is None else end
    delimiterIndex = text.find(delimiter, start, end)
    word = text[start: end if delimiterIndex<0 else delimiterIndex]

    nlIndex = word.find("\n")

    if(nlIndex>0): return word[:nlIndex]
    else: return word

def get_until_if_exists(text, delimiter, likelyStart=0, end=None):
    if(likelyStart>-1):
        delimiterIndex = text.find(delimiter, likelyStart, end)
        return text[likelyStart: end if delimiterIndex == -1 else delimiterIndex]
    else: 
        return ""

def find_and_go_after(text, word, delimiter, start=0, end=None):
    end = len(text) if end is None else end
    wordIndex = text.find(word, start, end)
    if(wordIndex>-1):
        wordIndex = text.find(delimiter, wordIndex, end) 
        return wordIndex+len(delimiter) if wordIndex>-1 else -1
    else: return -1

def find_until(text, word, delimiter, start=0, end=None):
    end = len(text) if end is None else end
    delimiterIndex = text.find(delimiter, start, end)
    wordIndex = text.find(word, start, end)
    return wordIndex if (wordIndex>-1 and wordIndex+len(word)<=delimiterIndex) else -1

def find_end(text, word, start=0, end=None):
    end = len(text) if end is None else end
    wordIndex = text.find(word, start, end)
    return wordIndex + len(word) if wordIndex>-1 else -1

def index_after(text, word, start, end):
    wordIndex = text.find(word, start, end) 
    return wordIndex+len(word) if wordIndex>-1 else -1

def index_before(text, word, start, end):
    wordIndex = text.find(word, start, end) 
    return wordIndex-1 if wordIndex>-1 else -1

def get_body_or_main(rawHtml):
    if("<main" in rawHtml):
        start, end = get_start_end_tag(rawHtml, "main")
    else:
        start, end = get_start_end_tag(rawHtml, "body")
    
    return rawHtml[start:end].strip().replace("scr+ipt", "script")

def get_start_end_tag(html, tag, start=0):
    start = find_and_go_after(html, f"<{tag}", ">", start)
    end = html.find(f"</{tag}>", start)
    return start, end
