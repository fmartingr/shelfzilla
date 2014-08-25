import sys
import json
from datCrawl import datCrawl
from datCrawl.downloaders import DefaultDownloader
from crawler import ListadoManga
from progressbar import ProgressBar

datcrawl = datCrawl()
datcrawl.register_downloader(DefaultDownloader)
datcrawl.register_crawler(ListadoManga)

# datcrawl.run('http://www.listadomanga.es/coleccion.php?id=60')
# datcrawl.run('http://www.listadomanga.es/coleccion.php?id=561')
# datcrawl.run('http://www.listadomanga.es/coleccion.php?id=1037')
# datcrawl.run('http://www.listadomanga.es/coleccion.php?id=1410')
# datcrawl.run('http://www.listadomanga.es/coleccion.php?id=98')

# exit

ids = []
for i in range(1, 11):
    ids.extend(datcrawl.run("http://www.listadomanga.es/lista.php?genero={}".format(i)))
_list = []
errors = 0
success = 0
custom_options = {
    'end': len(ids)-1,
    'width': 50,
    'fill': '#',
    'format': '%(progress)s%% [%(fill)s%(blank)s]'
}


f = open('data.json', 'w')


p = ProgressBar(**custom_options)
print("Crawling process in progress...")
for _id in ids:
    value = datcrawl.run("http://www.listadomanga.es/coleccion.php?id=%d" % _id)
    if value is "Error":
        errors += 1
    else:
        success += 1
        _list.append(value)

    sys.stdout.write("\r %s" % p)
    p += 1
    sys.stdout.flush()
json.dump(_list,f)

print "  <-- Completed!"
f.close()
print ""
print "Summary:"
print "--------"
print "Success: %d" % success
print "Errors: %d" % errors
