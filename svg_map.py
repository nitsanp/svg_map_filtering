from yattag import Doc
from pyquery import PyQuery as pq
import lxml.html
import regex as re

map_path = 'svg_map.svg'
final_html = 'svg_map.html'

#open file
def openFile(path):
	with open(path, 'r') as file:
	    f = file.read()
	return f

#write file
def writeFile(result, path):
	with open(path, 'w') as file:
	    file.write(result)

#create html
def createHtmlMapFile(svg_map):
	doc, tag, text, line= Doc().ttl()

	doc.asis('<!DOCTYPE html>')

	with tag('html'):
		with tag('head'):
			with tag('title'):
				text('Blog Map')
			with tag('link'):
				doc.attr(rel="stylesheet", type="text/css", href="svg_map.css")
		with tag('body'):
		    doc.asis(svg_map)
		with tag('script'):
			doc.attr(src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js")
		with tag('script'):
			doc.attr(src="svg_map.js")

	return doc.getvalue()

#jQuery filters
def attribInListNoChildren(el, myList):
	if el.attrib['id'] in myList and len(el)==0:
		return True
	return False

def attribInList(el, myList):
	if el.attrib['id'] in myList:
		return True
	return False

def removeElement(el):
	print('removed:', el.attrib['id'], len(el))
	el.drop_tree()

def removeParent(el):
	print('removed parent of:', el.attrib['id'])
	el.getparent().remove()

def styleDisplayIsNone(root):
	# check for display="none" style
	for el in root.iter('g'):
		try:
			if 'display:none' in el.attrib['style']:
				removeElement(el)
		except:
			continue


def displayIsNone(root):
# 	#check for display="none"
	for el in root.iter('g'):
		try:
			if 'none' in el.attrib['display']:
				removeElement(el)
		except:
			continue


def hasChildren(root):
# 	# check if does not have children
	ids = ['compass', 'gridOverlay', 'terrs', 'biomes', 'cells', 
			'coordinates', 'cults', 'temperature', 'rural', 'urban',
			'towns', 'cities']
	population = ['rural', 'urban']
	burgLabels = ['towns', 'cities']

	for el in root.iter('g'):
		try:
			if attribInListNoChildren(el, ids):
				# general
				removeElement(el)
				# population
				if attribInListNoChildren(el, population):
					removeParent(el)
				# burg labels
				if attribInListNoChildren(el, burgLabels):
					removeParent(el)
		except:
			continue

#filter HTML
def filterHTML(html_map):
	root = lxml.html.fromstring(html_map)
	styleDisplayIsNone(root)
	displayIsNone(root)
	hasChildren(root)
	return root

#html to string
def htmlToString(html):
	return lxml.html.tostring(html, pretty_print=False, encoding='unicode')



svg_map = openFile(map_path)
html_map = createHtmlMapFile(svg_map)
result = filterHTML(html_map)
writeFile(htmlToString(result), final_html)