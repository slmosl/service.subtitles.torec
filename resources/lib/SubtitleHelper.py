# -*- coding: utf-8 -*- 

import codecs
import urllib
import unicodedata

# import xbmcaddon
# import xbmc

# __addon__ = xbmcaddon.Addon()
# __version__ = __addon__.getAddonInfo('version')  # Module version
# __scriptname__ = __addon__.getAddonInfo('name')

def log(module, msg):
    # xbmc.log((u"### [%s] - %s" % (module, msg,)).encode('utf-8'),
    # level=xbmc.LOGDEBUG)
    print (u"### [%s] - %s" % (module, msg,)).encode('utf-8')


def build_search_string(item):
    if item['mansearch']:
        search_string = urllib.unquote(item['mansearchstr'])
    elif len(item['tvshow']) > 0:
        search_string = (
            u"%s- עונה %d (פרק %d)" % (
                item['tvshow'], int(item['season']), int(item['episode']),
            )
        ).replace(" ", "+")
    else:
        if str(item['year']) == "":
            item['title'], item['year'] = xbmc.getCleanMovieTitle(
                item['title']
            )
    
        search_string = item['title'].replace(" ", "+")
    
    log(__name__, "Search String [ %s ]" % (search_string,))
    return search_string
    
    
def normalize_string(str):
    return unicodedata.normalize(
        'NFKD', unicode(unicode(str, 'utf-8'))
    ).encode('ascii', 'ignore')

def convert_to_utf(file):
    """
    Convert a file in cp1255 encoding to utf-8

    :param file: file to converted from CP1255 to UTF8
    """
    try:
        with codecs.open(file, "r", "cp1255") as f:
            srt_data = f.read()

        with codecs.open(file, 'w', 'utf-8') as output:
            output.write(srt_data)
    except UnicodeDecodeError:
        log(__name__, "got unicode decode error with reading subtitle data")
