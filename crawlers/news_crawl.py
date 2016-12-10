# -*- coding: utf-8 -*-
import sys
import os
from __builtin__ import False
from bs4.builder import HTML
sys.path.append(os.path.abspath('../moneyweb'))
#import moneyweb
from database import db

from urllib import urlopen, urlencode, quote_plus, quote, unquote_plus
import urllib2
from bs4 import BeautifulSoup
import re

STOPWORDS = set("a able about above across actually after afterwards again against ain all almost alone along already also although always am among amongst an and another any anybody anyhow anyone anything anyway anyways anywhere apart are aren around as aside at away b be because been before behind between beyond both but by c came can cannot cant co ca com come comes could couldn't couldn course currently d did didn didn't do does doesn doing don done down dr during e each edu eg eight either else et etc even ever every ex f far few for from g go goes going gone got gotten h had hadn hadn't has hasn hasn't have haven having he hello help hence her here hers herself hi him himself his hither how howbeit however i ie if in inc inner insofar instead into inward is isn it its itself j jr just k keep keeps kept know known knows l last lately later latter latterly least less lest let like liked likely little ll ltd m mainly many may maybe me mean meanwhile merely might mon more moreover most mostly mr mrs ms much must my myself n name namely nd near nearly need needs neither never nevertheless new next nine no nobody non none noone nor not nothing novel now nowhere o obviously of off often oh ok okay old on once one ones only onto or other others otherwise ought our ours ourselves out outside over overall own p particular particularly per perhaps placed please plus pm possible presumably probably provides q que quite qv r rather rd re really right s said same saw say saying says second secondly see seeing seem seemed seeming seems seen self selves sent shall she should shouldn shouldn't since six so some somewhat soon sorry still sub such sup sure t take taken tell tends th than thank thanks thanx that thats that's that'd the their theirs them themselves then thence there thereafter thereby therefore therein theres thereupon these they think this those though three through throughout thru thus to together too took toward towards tried tries truly try trying twice two u un under unless until unto up upon us use used useful uses using usually uucp v value various ve very via viz vs w want wants was wasn wasn't way we  well went were weren what whatever when whence whenever where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why will wish with within without won wonder would wouldn wouldn't x y yes yet you your yours yourself yourselves z zero".split())

def crawl_google_news(term):
    qterm = quote_plus(term)  
    url = "https://news.google.com/news?cf=all&hl=en&pz=1&ned=us&output=rss&q=%s" % qterm
    
    content = download_html(url, cache=False)
    parsed = parse_google_news_xml(content)
    
    q = r"\b(%s)\b" % term.replace(' ', '|')
    term_re = re.compile(q, re.IGNORECASE)
    for url in parsed:
        try:
            parags, comment_date = extract_parags_from_url(url)
            quotes = extract_quotes_from_parags(parags, term)
            
            for q in quotes:
                vals = {"source": url, "person": term, "text": q}
                print vals
                if comment_date:
                    vals['date'] = comment_date
                db.comments.insert_one(vals)
        except:
            pass


def parse_google_news_xml(str):
    import xml.etree.ElementTree as ET
    from urlparse import urlsplit, urlparse, parse_qsl
    root = ET.fromstring(str)
    results = []
    for item in root.findall('channel')[0].findall('item'):
        gurl =  item.find('link').text
        parsed = dict(parse_qsl(urlsplit(gurl).query))
        url = unquote_plus(parsed['url'])
        results.append(url)
    return results

def download_html(url, cache = True):
    html = None
    if cache:
        rec = db.cached_html.find_one({"url": url})
        if rec:
            html = rec['html']
            print "Got in cache "
            print html
            
    if not html:
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        html = opener.open(url).read().decode('utf-8')
        db.cached_html.insert_one({"url": url, "html": html})
    
    return html
    
def extract_parags_from_url(url, cache = True):
    import urllib2
    print url  
    
    html = download_html(url)
                    
    raw = BeautifulSoup(html, "lxml").get_text()
    comment_date = None
    
    parags = [scrub_text(p) for p in raw.split('\n') if p and is_english_text(p) ]
    
    date_p1 = re.compile(r"\b\d\d? ?\/ ?\d\d? ?\/ ?\d\d(\d\d)?\b")
    months = "january february march april may june july august september october november december".split(' ')
    date_p2 = re.compile(r"\b(%s) \d\d?, \d\d\d\d\b" % ('|'.join(months),) , re.IGNORECASE)
    
    date_search = date_p1.search(raw)
    if date_search:
        from dateutil.parser import parse
        comment_date = parse(date_search.group())
        
    return parags, comment_date



def extract_quotes_from_parags(parags, term):
    q = r"\b(%s)\b" % term.replace(' ', '|')
    term_re = re.compile(q, re.IGNORECASE)
    
    quotes = []
    for p in parags:
        if '"' in p:
            segments = p.split('"')
            inside_quotes =  ' '.join([ q for (i,q) in enumerate(segments) if (i%2) == 1 and len(q) > 20 ])
            outside_quotes =  ' '.join([ q for (i,q) in enumerate(segments) if (i%2) == 0])
            in_this_parag = (term_re.search(outside_quotes) != None)
            
            if inside_quotes and (in_this_parag or in_prev_parag):
                quotes.append(inside_quotes)
        else:
            in_this_parag = (term_re.search(p) != None)
        
        in_prev_parag = in_this_parag
    
    return quotes

    
    for url in parsed:
        try:
            parags = extract_parags_from_url(url)
            in_prev_parag = False
        except:
            pass


def scrub_text(t):
    return t.replace(u'’', u"'").replace(u'“', u'"').replace(u'”', u'"')
    
def is_english_text (str):
    code_marks = ['//', '{', '&&', '||']
    for c in code_marks:
        if c in str:
            return False
    
    words = str.lower().split(' ')
    
    return len(set(words) & STOPWORDS) > 2

if __name__ == "__main__":    
    crawl_google_news("Nancy Pelosi")