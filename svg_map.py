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
def styleDisplayIsNone(root):
	# check for display="none" style
	for el in root.iter('g'):
		try:
			if 'display:none' in el.attrib['style']:
				print("removed:", el.attrib['style'])
				el.drop_tree()
		except:
			continue

def displayIsNone(root):
# 	#check for display="none"
	for el in root.iter('g'):
		try:
			if 'none' in el.attrib['display']:
				print("removed:", el.attrib['display'])
				el.drop_tree()
		except:
			continue

def hasChildren(root):
# 	# check if does not have children
	ids = ['compass', 'gridOverlay', 'terrs', 'biomes', 'cells', 
			'coordinates', 'cults', 'temperature', 'rural', 'urban',
			'towns', 'cities']

	for el in root.iter('g'):
		try:
			if(el.attrib['id'] in ids):
				if not len(el):
					# general
					print('removed:', len(el))
					el.drop_tree()
					# population
					if el.attrib['id'] == 'rural' or el.attrib['id'] == 'urban':
						print('removed population:', el)
						el.getparent().remove()
					# burg labels
					if el.attrib['id']== 'towns' or el.attrib['id'] == 'cities':
						print('removed burgLabels:', el)
						el.getparent().remove()
		except:
			continue

#filter HTML
def filter_HTML(html_map):
	root = lxml.html.fromstring(html_map)
	styleDisplayIsNone(root)
	displayIsNone(root)
	hasChildren(root)
	return root



svg_map = openFile(map_path)
html_map = createHtmlMapFile(svg_map)
result = filter_HTML(html_map)
writeFile(lxml.html.tostring(result, pretty_print=False, encoding='unicode'), final_html)