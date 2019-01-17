""" indexdirs_xml.py  July 4, 2014
    Revised July 6 to include 'MW'
    June 5, 2015. Revised to include AP, PD
    python indexdirs_xml.py indexdirs.txt indexdirs.xml
"""
import sys,codecs
import re
import os
import xml.etree.cElementTree as ET
class Scan(object):
 def __init__(self,x):
  x = x.rstrip('\r\n')
  (self.scandir,self.year) = re.split(':',x)
  self.pfx = re.sub(r"Scan$","",self.scandir)
 def xmlstring(self):
  parts = ["<entry>",
           "  <pfx>%s</pfx>" % self.pfx,
           "  <year>%s</year>" % self.year,
           "  <title>%s</title>" % self.title,
           "  <dsize>%s</dsize>" % self.dsize,
           "  <dyear>%s</dyear>" % self.dyear,
           "  <authors>%s</authors>" % self.authors,
           "  <textdate>%s</textdate>" % self.textdate,
           "  <textpages>%s</textpages>" % self.textpages,
           "</entry>"]
  return '\n'.join(parts)

def parseheader(s):
 "s is a Scan object"
 pfx = s.pfx
 pfx1 = pfx.lower()
 headerfile = "../../%sScan/%s/downloads/%sheader.xml" %(s.pfx,s.year,pfx1)
 #try:
 if True:
  #namespaces make finding harder with ET.
  # So, read the file as a string, remove namespace, then parse as string
  with codecs.open(headerfile,"r","utf-8") as f:
   xmlstring0 = f.read()
  xmlns = 'xmlns="//www.tei-c.org/ns/1.0"'
  xmlstring = re.sub(xmlns,'',xmlstring0)
  with codecs.open("temp.xml","w","utf-8") as f:
   f.write(xmlstring)
  parser = ET.XMLParser(encoding="utf-8")
  #tree = ET.fromstring(xmlstring,parser=parser)
  tree = ET.parse("temp.xml",parser=parser)
 #except:
 # print "parseheader ERROR for ",headerfile
 # return
 root = tree.getroot()
 #root = tree
 node = root.find("teiHeader/fileDesc/titleStmt/title") # first
 s.title = node.text
 """
 node = root.find("teiHeader/fileDesc")
 for child in node:
  print child.tag
 exit(1)
 """
 node = root.find("teiHeader/fileDesc/extent") # first
 s.dsize = node.text  # size of digitization

 node = root.find("teiHeader/fileDesc/publicationStmt/date") # first
 s.dyear = s.year  # year of digitization
 monogr = root.find("teiHeader/fileDesc/sourceDesc/biblStruct/monogr")
 #print "monogr=",monogr
 nodes = root.findall("teiHeader/fileDesc/sourceDesc/biblStruct/monogr/author") # first
 nodes1 = [node.text for node in nodes if node.text != None]
 s.authors = ','.join([name for name in nodes1 if name.strip()!=''])
 node = root.find('teiHeader/fileDesc/sourceDesc/biblStruct/monogr/imprint/date')
 s.textdate = node.text
 node = root.find('teiHeader/fileDesc/sourceDesc/biblStruct/monogr/extent')
 s.textpages = node.text
 
 #out = ':'.join([s.pfx,s.title,s.dsize,s.dyear,s.authors,s.textdate,s.textpages])
 #print out.encode('utf-8')

def indexdirs_xml(filein,fileout):
 with codecs.open(filein,"r","utf-8") as f:
  scandirs = [Scan(x) for x in f]
 
 print len(scandirs)," Scan objects read from ",filein
 for rec in scandirs:
  parseheader(rec)
 fout = codecs.open(fileout,"w","utf-8")
 out = '<?xml version="1.0" encoding="UTF-8"?>'
 root = 'scandirs'
 fout.write("%s\n" % out)
 out = '<%s>' % root
 fout.write("%s\n" % out)
 for rec in scandirs:
  out = rec.xmlstring()
  fout.write("%s\n" % out)
 out = '</%s>' % root
 fout.write("%s\n" % out)
 fout.close()

if __name__  =="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 indexdirs_xml(filein,fileout)
