import mechanize
import urllib
from HTMLParser import HTMLParser
import os

# get Attr from list of attrs
def getAttr(attrs, attr):
  result = [item for item in attrs if item[0] == attr]
  if(result != []):
    return result[0][1]
  else:
    return None

# create a subclass and override the handler methods
class ImageParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == 'img'):
          global imageCounter
          linkClass = getAttr(attrs, 'class')
          if( linkClass is None):
                  return;

          linkClass = linkClass.strip()
          if(linkClass == 'dev-content-full'):
            href = getAttr(attrs, 'src')
            extension = href.split('.')[-1]

            if(extension == 'gif'):
              return

            try:
              print "Loading Image #"+str(imageCounter)
              urllib.urlretrieve(href, str(imageCounter)+"."+extension)
              imageCounter = imageCounter + 1
            except HTTPError:
              print "Error what happened ? Wtf "
              pass
    def handle_endtag(self, tag):
      return
    def handle_data(self, data):
      return

# create a subclass and override the handler methods
class MainParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if(tag == 'a'):
          linkClass = getAttr(attrs, 'class')

          if(linkClass == 'thumb'):
            href = getAttr(attrs, 'href')
            imageParser = ImageParser()
            response = mechanize.urlopen(href)
            imageParser.feed(response.read())

    def handle_endtag(self, tag):
      return
    def handle_data(self, data):
      return

url = "http://www.deviantart.com/dailydeviations/"
# Messages
print ("Starting Script for load background Images")
print "Cleaning directory"

filelist = [ f for f in os.listdir(".") if (f.endswith(".jpg") or f.endswith(".png") ) ]
print filelist
for f in filelist:
  os.remove(f)

print ("Loading images from: "+url)

# Load response from DeviantArt and imageCounter
response = mechanize.urlopen(url)
imageCounter = 0;

# instantiate the parser and fed it some HTML
parser = MainParser()
parser.feed(response.read())

# Finishing Messages
print ("All finished. Success")
