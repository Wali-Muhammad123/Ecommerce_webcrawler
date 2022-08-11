import re
import pandas as pd
from bs4 import BeautifulSoup
def price_convert(n):
    n=n.strip('Rs.')
    nn=n.split(',')
    m=''.join([str(item) for item in nn])
    return int(m)
def rating_convert(n):
    try:
        array=re.findall(r'[0-9]+',n)
        return int(array[0])
    except TypeError:
        pass
def rating_retriever(n):
    m_ratingss=[]
    for each in n:
        try:
            soup=BeautifulSoup(str(each))
            tag=soup.span
            m_ratingss.append(tag.string)
        except AttributeError:
            m_ratingss.append(None)
    return m_ratingss
