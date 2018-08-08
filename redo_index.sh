#echo "Remake indexdirs.xml"
#python indexdirs_xml.py indexdirs.txt indexdirs.xml
echo "Remaking index2.html"
# Aug 21, 2015. Now using indexdirs_edit.xml, rather than indexdirs.xml
python index_make2.py indexdirs_edit.xml index2.html
echo "Copying index2.html to /docs/index.html home page"
cp index2.html ../../../index.html
echo "index2.html is the  homepage"
