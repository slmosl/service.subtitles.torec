# -*- coding: utf-8 -*- 

import os
import re

import urllib
import unicodedata

import xbmcaddon
import xbmc


__addon__      = xbmcaddon.Addon()
__version__    = __addon__.getAddonInfo('version') # Module version
__scriptname__ = __addon__.getAddonInfo('name')

def log(module, msg):
    #xbmc.log((u"### [%s] - %s" % (module, msg,)).encode('utf-8'), level=xbmc.LOGDEBUG)
    print (u"### [%s] - %s" % (module, msg,)).encode('utf-8')
    
def clean_title(item):
    title = os.path.splitext(item["title"])
    tvshow = os.path.splitext(item["tvshow"])
    if len(title) > 1:
        if re.match(r'^\.[a-z]{2,4}$', title[1], re.IGNORECASE):
            item["title"] = title[0]
        else:
            item["title"] = ''.join(title)
    else:
        item["title"] = title[0]

    if len(tvshow) > 1:
        if re.match(r'^\.[a-z]{2,4}$', tvshow[1], re.IGNORECASE):
            item["tvshow"] = tvshow[0]
        else:
            item["tvshow"] = ''.join(tvshow)
    else:
        item["tvshow"] = tvshow[0]

    item["title"] = unicode(item["title"], "utf-8")
    item["tvshow"] = unicode(item["tvshow"], "utf-8")
    # Removes country identifier at the end
    item["title"] = re.sub(r'\([^\)]+\)\W*$', '', item["title"])
    item["tvshow"] = re.sub(r'\([^\)]+\)\W*$', '', item["tvshow"])
    
def parse_rls_title(item):
    regexHelper = re.compile('\W+', re.UNICODE)
    
    item["title"] = regexHelper.sub(' ', item["title"])
    item["tvshow"] = regexHelper.sub(' ', item["tvshow"])

    groups = re.findall(r"(.*) (?:s|season|)(\d{1,2})(?:e|episode|x|\n)(\d{1,2})", item["title"], re.I)

    if len(groups) == 0:
        groups = re.findall(r"(.*) (?:s|season|)(\d{1,2})(?:e|episode|x|\n)(\d{1,2})", item["tvshow"], re.I)

    if len(groups) > 0 and len(groups[0]) == 3:
        title, season, episode = groups[0]
        item["tvshow"] = regexHelper.sub(' ', title).strip()
        item["season"] = str(int(season))
        item["episode"] = str(int(episode))
        log(__name__, "TV Parsed Item: %s" % (item,))

    else:
        groups = re.findall(r"(.*)(\d{4})", item["title"], re.I)
        if len(groups) > 0 and len(groups[0]) >= 1:
            title = groups[0][0]
            item["title"] = regexHelper.sub(' ', title).strip()
            item["year"] = groups[0][1] if len(groups[0]) == 2 else item["year"]

            log(__name__, "MOVIE Parsed Item: %s" % (item,))	
	
def build_search_string(item):
    if item['mansearch']:
        search_string = urllib.unquote(item['mansearchstr'])
    elif len(item['tvshow']) > 0:
        search_string = ("%s S%.2dE%.2d" % (item['tvshow'],
                                                int(item['season']),
                                                int(item['episode']),)
                                              )#.replace(" ","+")      
    else:
        if str(item['year']) == "":
          item['title'], item['year'] = xbmc.getCleanMovieTitle( item['title'] )
    
        search_string = item['title']#.replace(" ","+")
    
    log( __name__ , "Search String [ %s ]" % (search_string,)) 
    return search_string
    
    
def normalizeString(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('ascii', 'ignore')
