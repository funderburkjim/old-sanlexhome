# coding=utf-8
""" hack_index_make2.py 
 Aug 21, 2015.
 Special code to help with the revision of titles.
 This is similar to index_make2.py, but only prints, 
 the dictionary codes and titles.
"""
import sys,codecs
import re
import os
import xml.etree.cElementTree as ET
import string
# True means funded DFG-NEH Project 2010-2013
# False means not so funded
asteriskData = {"ACC":True , "AE":False , "AP":False , "AP90":True,
       "BEN":True , "BHS":True , "BOP":True , "BOR":True,
       "BUR":True , "CAE":False , "CCS":True , "GRA":True,
       "GST":True , "IEG":True , "INM":True , "KRM":True,
       "MCI":True , "MD":False , "MW":False , "MW72":True,
       "MWE":True , "PD":True , "PE":True , "PGN":True,
       "PUI":True , "PWG":False , "PW":False , "SCH":False,
       "SHS":False , "SKD":True , "SNP":True , "STC":True,
       "VCP":True , "VEI":True , "WIL":False , "YAT":True}
class Scan(object):
 def __init__(self,e):
  self.pfx = e.find('pfx').text
  self.year = e.find('year').text
  self.title = e.find('title').text
  self.dsize = e.find('dsize').text
  self.dyear = e.find('dyear').text
  self.authors = e.find('authors').text
  textdate = e.find('textdate').text
  textpages = e.find('textpages').text
  textdate = re.sub('[ \n]','',textdate)
  m = re.search(r'^([0-9,]+)',textdate)
  if m:
   textdate = m.group(1)
  else:
   textdate=''
  self.textdate = textdate
  textpages = re.sub('[ \n]','',textpages)
  m = re.search(r'^([0-9,]+)',textpages)
  if m:
   textpages = m.group(1)
  else:
   textpages = ''
  self.textpages = textpages
 def toStringdbg(self):
  parts = [
           "pfx=%s" % self.pfx,
           "title=%s" % self.title,
           "dsize=%s" % self.dsize,
           "dyear=%s" % self.dyear,
           "authors=%s" % self.authors,
           "textdate=%s" % self.textdate,
           "textpages=%s" % self.textpages,
           ]
  return ','.join(parts)
  
def parse_indexdirs(filein):
 "returns a dict of Scan objects, indexed by pfx"
 d = {} # returned
 parser = ET.XMLParser(encoding="utf-8")
 tree = ET.parse(filein,parser=parser)
 root = tree.getroot()
 for entry in root:
  rec = Scan(entry)
  d[rec.pfx]=rec
 return d

def headerdiv():
 div ="""
 <div id="header">
  <table>
  <tr>
  <td>
  <img src="/images/cologne_univ_seal.gif" id="logo" alt="IITS" title="Cologne Sanskrit Lexicon"/>
  <br/>
  <span class="style19">
   UNIVERSIT&Auml;T ZU K&Ouml;LN <br />
  </span>
  </td>
  <!--&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-->
  <td>
  <span class="style1">Cologne Digital Sanskrit Dictionaries</span>
  </td>
  </tr>
  </table>
  <hr/>
 </div>
"""
 lines = string.split(div, '\n\r') 
 return lines

def purpos1ediv():
 divused ="""
 <div id="purpose1">
   <h2>Purpose</h2>
   <p>
    This web page provides access to some of the Sanskrit lexicons prepared
    by the Institute of Indology and Tamil Studies, Cologne University.
    A 1997 review of the Cologne Digital Sanskrit Lexicon project
    (<a href="/CDSL.pdf">CDSL</a>)
    may be of interest.</p>
   <p>
    The data is made available to scholars
    and students in two forms. The first form is  that of <em>scanned images</em> of the
    works, which provides a convenient substitute to  the physical books.
    The second form is a <em>digitization</em> of the scanned images, which
    permits computer-aided analyses and displays of the work.
   </p>
  </div>
"""

 div ="""
 <div id="purpose1">
   <p>
    This web page provides access to many of the Sanskrit lexicons prepared
    by the Institute of Indology and Tamil Studies, Cologne University.
   <br/>
    The dictionaries are organized primarily by the secondary language
    (English, German, etc.), and then by date of publication.
   <br/>
    Each dictionary has several types of display, as well as a comprehensive
       selection of materials for download.
   </p>
   
   <p>
     <a href='/scans/csldoc/index.html' target="_csldoc"><b>Documentation</b></a>
   &nbsp; &nbsp;
    (Previous Cologne Sanskrit-Lexicon <a href='index_prev.html'>Home Page</a>)
   &nbsp; &nbsp;
   <span style="position:absolute;right:11%">
    Found an error? 
    <a href='/scans/csldoc/contrib/index.html' target="_csldoc">
      <b>Help us on <img src="/images/github-9-16.gif">GitHub</b>
    </a>
   </span>
   </p> 

  </div>
"""
 lines = string.split(div, '\n\r') 
 return lines

def make_link(href,title,text):
 return "<a href='%s' title='%s'>%s</a>" %(href,title,text)

def make_links(data):
 parts=[]
 for (href,title,text) in data:
  parts.append(make_link(href,title,text))
  parts.append("&nbsp;")
 return parts


def dict_line_extralinks(s):
 "return extra links"
 extradata = {
  'WIL':[
       ('/scans/WILScan/index.php?sfx=jpg','Scanned edition, jpg','S'),
       ('#deprecated','Deprecated','Deprecated')
       ],
  'MD':[
      ('/scans/MDScan/index.php?sfx=jpg','Scanned edition, jpg','S')
      ],
  'MW':[
      ('/scans/MWScan/index.php?sfx=pdf','Scanned edition, pdf','S1'),
      ('/scans/MWScan/index.php?sfx=jpg','Scanned edition, jpg','S2'),
      ('/talkMay2008/markingMonier.html','Marking-Monier','Markup'),
      ('#deprecated','Deprecated','Deprecated')
      ],
  'AE': [
      ('/scans/AEScan/index.php?sfx=pdf','Scanned edition, pdf','S1'),
      ('/scans/AEScan/index.php?sfx=jpg','Scanned edition, jpg','S2'),
      ('#deprecated','Deprecated','Deprecated')
      ],
  'PWG':[
      ('/pwgindex.html','Scanned edition','S'),
      ('#deprecated','Deprecated','Deprecated')
      ],
  'PW':[
      ('/pwindex.html','Scanned edition','S'),
      ('#deprecated','Deprecated','Deprecated')
      ],
  'SCH':[
      ('/scans/SCHScan/index.php','Scanned edition','S')
      ],
  'CCS':[
      ('/scans/CCSScan/index.php?sfx=png','Scanned edition','S')
      ],
  'CAE':[
      ('/scans/CAEScan/index.php?sfx=png','Scanned edition','S')
      ],
  'STC':[
      ('/scans/STCScan/index.php?sfx=jpg','Scanned edition','S'),
      ('/scans/STCScan/web/index_fr.php',u'semi-numérique','SD'),
      ],
  'PGN':[
      ('/scans/PGNScan/2014/web/webscan/index.php','Scanned edition','S')
      ]
 }

 if s.pfx in extradata:
  return make_links(extradata[s.pfx])
 else:
  return [] # no extra links for this pfx

def dict_line_links(s):
 """Return list of strings
    June 15: for AP,PD, return special message
 """
 if s.pfx in ['AP','PD']:
  message = "<i>available on special request for research purposes</i>"
  parts = [message]
  return parts
 # usual case : links to various displays
 basedir = "/scans/%sScan/%s/web" % (s.pfx,s.year)

 data = [
  ('%s/webtc/indexcaller.php' % basedir,'Basic Display','B'),
  ('%s/webtc1/index.php' % basedir,'List Display','L'),
  ('%s/webtc2/index.php' % basedir,'Advanced Search','A'),
  ('%s/mobile1/index.php' % basedir,'Mobile-Friendly','M'),
  ('%s/webtc/download.html' % basedir,'Downloads','D')
 ]
 if s.pfx == 'STC':
  data = [
  ('%s/webtc/indexcaller_fr.php' % basedir,'Recherche simple','B'),
  ('%s/webtc1/index.php' % basedir,'Recherche par liste','L'),
  ('%s/webtc2/index.php' % basedir,u'Recherche avancée','A'),
  ('%s/mobile1/index.php' % basedir,u'Écran de recherche pour téléphones portables','M'),
  ('%s/webtc/download_fr.html' % basedir,u'Téléchargements','D')
  ]

 parts = make_links(data)
 for link in dict_line_extralinks(s):
  parts.append(link)
 return parts


def dict_line(s,title_in):
 "'s' is a Scan element. Returns a string."
 parts=[]
 if title_in != '':
  title = title_in
  title1=s.title
 else:
  title = s.title
  title1= s.title # ?
 pfx1 = s.pfx
 # June 5, 2015
 #asterisk = ''
 #if asteriskData[pfx1]:
 # asterisk = ' <span title="funded by the DFG-NEH Project 2010-2013">*</span>'
 #pfx1 = "%s%s" %(pfx1,asterisk)
 parts.append(pfx1)
 parts.append(s.textdate)
 #parts.append("  <td width='6%%'><span style='font-size:10px;'>%s</span></td>" % pfx1)
 #parts.append("  <td width='6%%'><span style='font-size:10px;'>%s</span></td>" % s.textdate)

 basedir = "/scans/%sScan/%s/web" % (s.pfx,s.year)
 titlelink = "<a href='%s/index.php'>%s</a>" %(basedir,title)
 """ commented out
 titlelink = "<a href='%s/index.php'>%s</a>" %(basedir,title)
 if s.pfx == 'STC':
  titlelink = "<a href='%s/index_fr.php'>%s</a>" %(basedir,title)
 elif s.pfx == 'AP':
  basedir1 = "/scans/awork/homepage"
  titlelink = "<a href='%s/ap-sample.php'>%s</a>" % (basedir1,title)
 elif s.pfx == 'PD':
  basedir1 = "/scans/awork/homepage"
  titlelink = "<a href='%s/pd-sample.php'>%s</a>" % (basedir1,title)

 parts.append("  <td width='58%%' style='font-size:12pt;' title='%s,%s,%s pages'>%s</td>" % (s.authors,title1,s.textpages,titlelink))
 """
 #parts.append('%s,%s,%s pages'% (s.authors,title1,s.textpages))
 parts.append('%s,%s'% (s.authors,title1))
 if s.pfx == 'STC':
  parts.append('%s/index_fr.php' % basedir)
 else:
  parts.append('%s/index.php' % basedir)
 parts.append(title)
 """
 parts.append("<td class='tdlist'>")
 for link in dict_line_links(s):
  parts.append(link)
 parts.append("</td>")
 """
 try:
  ans = ":".join(parts)
  #ans = "\n   ".join(parts)
 except:
  print "ERROR JOINING"
  for part in parts:
   print "part = ",part
  exit(1)
 return ans

def section_sort(pfxs,pfxdict):
 """ pfxs is a list of pairs (pfx,title)
 """
 def sortkey(t):
  (pfx,title)=t
  return pfxdict[pfx].textdate
 return sorted(pfxs,key = sortkey)

def table_headers():
 """ returns a string ( <tr><th></th>...</tr>) 
  compare dict_line
 """
 parts=[]
 bgcolor="#FFFFCC" #pale yellow
 bgcolor="#D3D3D3" #LightGray
 style = "background:%s; font-size=12px; font-weight:bold; font-color:black;text-align:left;" % bgcolor
 parts.append('<tr style="%s">' % style)
 parts.append('  <th>ID</th>')
 parts.append('  <th>date</th>')
 parts.append('  <th>Dictionary</th>')
 parts.append('  <th>Displays and Downloads</th>')

 parts.append('</tr>')
 return '\n'.join(parts)

def section_lines(pfxs,section_title,pfxdict):
 pfxs = section_sort(pfxs,pfxdict)
 lines = []
 #lines.append('\n')
 colspan=4
 #lines.append('<tr style="background:#FFFFCC"><td colspan="%s" style="vertical-align:center;"><h2>%s</h2></td></tr>' % (colspan,section_title))
 #add column titles for first one
 if section_title.startswith('Sanskrit-English'):
  #lines.append(table_headers())
  pass
 for (pfx,title) in pfxs:
  #lines.append('<tr style="background:#FFFFCC">%s</tr>' %dict_line(pfxdict[pfx],title))
  lines.append(dict_line(pfxdict[pfx],title))

 return lines

def san_english(pfxdict):
 pfxs = [
  ("AP90","Apte Practical Sanskrit-English Dictionary"),
  ("BEN","Benfey Sanskrit-English Dictionary"),
  ("BHS","Edgerton Buddhist Hybrid Sanskrit Dictionary"),
  ("CAE","Cappeller Sanskrit-English Dictionary"),
  ("GST",u"Goldstücker Sanskrit-English Dictionary"),
  ("MD","Macdonell Sanskrit-English Dictionary"),
  ("MW72","Monier-Williams Sanskrit-English Dictionary"),
  ("MW","Monier-Williams Sanskrit-English Dictionary"),
  ("SHS","Shabda-Sagara Sanskrit-English Dictionary"),
  ("WIL","Wilson Sanskrit-English Dictionary"),
  ("YAT","Yates Sanskrit-English Dictionary"),
  ("AP","Practical Sanskrit-English Dictionary, revised edition"),
  ("PD","An Encyclopedic Dictionary of Sanskrit on Historical Principles")
 ]
 section_title='Sanskrit-English Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def english_san(pfxdict):
 pfxs=[
  ("AE","Apte Student's English-Sanskrit Dictionary"),
  ("MWE","Monier-Williams English-Sanskrit Dictionary"),
  ("BOR","Borooah English-Sanskrit Dictionary")
 ]
 section_title='English-Sanskrit Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def san_french(pfxdict):
 pfxs=[
 ("BUR",u"Burnouf Dictionnaire Sanscrit-Français"),
 ("STC",u"Stchoupak Dictionnaire Sanscrit-Français")
  ]
 section_title='Sanskrit-French Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def san_german(pfxdict):
 pfxs=[
  ("PW",u"Böhtlingk Sanskrit-Wörterbuch in kürzerer Fassung"),
  ("PWG",u"Böhtlingk and Roth Grosses Petersburger Wörterbuch"),
  ("SCH",u"Schmidt Nachträge zum Sanskrit-Wörterbuch"),
  ("CCS",u"Cappeller Sanskrit Wörterbuch"),
  ("GRA",u"Grassman Wörterbuch zum Rig Veda")
 ]
 section_title='Sanskrit-German Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def san_latin(pfxdict):
 pfxs = [
  ("BOP","Bopp Glossarium Sanscritum")
 ]
 section_title='Sanskrit-Latin Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def san_san(pfxdict):
 pfxs_sandict=[
  ("SKD",""),
  ("VCP","")
 ]
 pfxs=pfxs_sandict
 #section_title='Sanskrit-Sanskrit Dictionaries and Concordances'
 section_title='Sanskrit-Sanskrit Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def san_special(pfxdict):
 pfxs=[
  ("KRM",""),
  ("ACC","Aufrecht's Catalogus Catalogorum"),
  ("PUI",""),
  ("VEI",""),
  ("PE",""),
  ("MCI",""),
  ("SNP","Meulenbeld's Sanskrit Names of Plants"),
  ("PGN",""),
  ("IEG",""),
  ("INM","")
 ]
 section_title = 'Specialized Dictionaries'
 return section_lines(pfxs,section_title,pfxdict)

def deprecated_line(href,title):
 colspan=4
 return '<tr style="background:#FFFFCC"><td colspan="%s"><a href="%s">%s</a></td></tr>\n' % (colspan,href,title)

def deprecated(pfxdict):
 colspan=4
 lines=[]
 section_title = '<a id="deprecated">Deprecated Editions</a>'
 lines.append('\n')
 lines.append('<tr style="background:#FFFFCC"><td colspan="%s"><h2>%s</h2></td></tr>' % (colspan,section_title))
 def dl(h,t): # for convenience
  return deprecated_line(h,t)
 lines.append(dl('/scans/MWScan/2012/web/index.php','Monier-Williams Sanskrit-English Dictionary, 2012/2013 displays'))
 lines.append(dl('/monier/indexcaller.php','Monier-Williams Sanskrit-English Dictionary, 2008'))
 lines.append(dl('/mwquery/index.html','Monier-Williams Advanced Search, 2008'))
 lines.append(dl('/scans/MWScan/tamil/index.html','Sanskrit and Tamil  Dictionaries, 2005'))
 lines.append(dl('/scans/WILScan/web/index.php','Wilson Sanskrit-English Dictionary, semi-digitized edition, 2008'))
 lines.append(dl('/aequery/index.html','Apte English-Sanskrit Dictionary, 2007'))
 lines.append(dl('/scans/PWGScan/disp2/index.php','Boehtlingk &amp; Roth Sanskrit-German Dictionary, 2011'))
 lines.append(dl('/scans/PWScan/disp2/index.php','Boehtlingk + Schmidt Sanskrit-German Dictionary, 2012'))

 return lines

def misc():
 colspan=4
 lines=[]
 section_title = '<a">Miscellany</a>'
 lines.append('\n')
 lines.append('<tr style="background:#FFFFCC"><td colspan="%s"><h2>%s</h2></td></tr>' % (colspan,section_title))
 def dl(h,t): # for convenience
  return deprecated_line(h,t)
 lines.append(dl('/scans/KALEScan/disp1/index1.php?sfx=png','Kale Higher Sanskrit Grammar, 1894 (Scanned)'))
 lines.append(dl('/scans/MWScan/Westergaard/disp/index.php','Westergaard Linguae Sanscritae, 1841 (Scanned)'))
 lines.append(dl('/scans/KALEScan/WRScan/disp2/index.php',"Whitney's Roots, 1885 (Scanned)"))
 lines.append(dl('/work/fflexphp/web/index.php','MW Inflected forms'))
 lines.append(dl('/work/fflexphp/web1/index.php','MW Inflected forms, v2'))
 #lines.append(dl('',''))
 return lines

def dictdiv(pfxdict):
 """The list of dictionaries, and their forms. Return list of string.
 """
 ans = []
 #ans.append('<table width="90%">')
 parts = [san_english(pfxdict),english_san(pfxdict),
  san_french(pfxdict), san_german(pfxdict),
  san_latin(pfxdict), san_san(pfxdict),
  san_special(pfxdict),
  #deprecated(pfxdict),
  #misc()
 ]
 ipart=0
 for part in parts:
  # part is itself a list of strings
  for p in part:
   ipart = ipart+1
   #ans = ans + ['<tr><td>'] + part + ['</td></tr>']
   ans.append('%d:%s' %(ipart,p))
 #ans.append('</table>')
 return ans


def index01_bodylines(pfxdict):
 # use '+' on lists to concatenate them
 #lines=headerdiv() + purpos1ediv() + dictdiv(pfxdict) 
 lines = dictdiv(pfxdict) 
 return lines

def index01(filein,fileout):
 pfxdict = parse_indexdirs(filein)
 #print pfxdict["PW"].toStringdbg().encode('utf-8')

 lines = [] # array of lines to be output
 #head = """<?xml version="1.0" encoding="UTF-8"?>
 # Aug 21, 2015. Change to HTML5 
 head = """<!DOCTYPE html>
<html>
<head>
 <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
 <title>IITS Koeln </title>
 <link type="text/css" rel="stylesheet" href="/scans/awork/Cologne.css" />
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
</head>
<body>
"""
 tail = u"""
<!--
<hr/>
   <h2>Funding</h2>
 <p>Die mit * gekennzeichneten Werke sind unter dem
DFG-NEH Project 2010-2013 <br/>
entstanden:
 26*/37 digitalisierte Wörterbücher = *198/300 MB   
 </p>
-->
<hr/>
   <h2>Credits</h2>
  <p>The digitizations of works marked with an asterisk (*) were funded by the DFG-NEH Project 2010-2013.</p>
  </p>
     <p>The markup of the  Monier-Williams Sanskrit-English Dictionary is described in detail 
          <a href='talkMay2008/markingMonier.html'>here</a>.
     <br/>
     The markup of the various dictionaries was designed and implemented by: </p>
     <ul>
      <li>
       <a href="mailto:th.malten@uni-koeln.de">Thomas Malten</a> (Cologne University) and <a href="/images/Aurorachana_Staff_2006(1).jpg">assistants</a> in India
      </li>
      <li>
       <a href="//www.sanskritlibrary.org">Peter Scharf</a> (Brown University)
      </li>
      <li>
       Malcolm D. Hyman 
       (Max-Planck-Institut für Wissenschaftsgeschichte, Berlin)
      </li>
      <li>
       Jim Funderburk
      </li>
     </ul>
  <hr/>
  <div id="footer">
   Jim Funderburk maintains this web site.
   <p>Last modified: Aug 4, 2015</p>
  </div>

<script type="text/javascript" src="/js/piwik_analytics.js"></script>

</body>
</html>
"""
 headlines = string.split(head, '\n\r') 
 taillines = string.split(tail, '\n\r') 
 bodylines=index01_bodylines(pfxdict)
 #for line in headlines:
 # lines.append(line)
 for line in bodylines:
  lines.append(line)
 #for line in taillines:
 # lines.append(line)

 fout = codecs.open(fileout,"w","utf-8")
 for line in lines:
  fout.write("%s\n" % line)
 fout.close()

if __name__  =="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 index01(filein,fileout)
 print "DID YOU CHANGE 'Date last modified'?"
