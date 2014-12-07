import afiiuni

reload(afiiuni)
from afiiuni import *
import sys
from vanilla import *
from mojo.UI import *
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.events import addObserver, removeObserver

# font = None

toAfii = 0
toUni = 1

AVAIL_CYRL = "Available Cyrl glyphs"
RENAME_TO = "Rename to"


def getNameAndSuffix (glyphname):
	if '.' in glyphname:
		gn = glyphname.split('.')
		return gn[0], ('.' + '.'.join(gn[1:]))
	else:
		return glyphname, ''


def getListOfCyrillicGlyphs (font):
	cyrllist = []
	# print font
	# if font != None:
	# print 'we there'
	for glyphname in font.keys():
		gname, gsuffix = getNameAndSuffix(glyphname)
		# print gname, gsuffix
		if isCyrillic(gname):
			cyrllist.append(gname + gsuffix)
			# for glyphname in font.keys():
			# uni = font[glyphname].unicode
			# 	if uni != None:
			# 		afii = getAfiiByUnicode(uni)
			# 		if afii != None:
			# 			cyrllist.append(glyphname)
			# 	else:
			# 		if '.' in glyphname:
			# 			gn = glyphname.split('.')
			# 			realname = gn[0]
			# 			if 'uni' in realname:
			# 				realname = realname.replace('uni','')
			# 				afii = getAfiiByUnicode(realname)
			# 			elif 'u' in realname:
			# 				realname = realname.replace('u','')
			# 				afii = getAfiiByUnicode(realname)
			# 			elif 'afii' in realname:
			# 				afii = 'uni' + getUnicodeByAfii(realname)
			# 			# afii = getAfiiByUnicode(realname)
			# 			if afii != None:
			# 				gn[0] = afii
			# 				afii = '.'.join(gn)
			# 				cyrllist.append(glyphname)
	return cyrllist


def getListUniNames (listOfCyrlGlyphs):
	cyrllist = []
	for glyphname in listOfCyrlGlyphs:
		gname, gsuffix = getNameAndSuffix(glyphname)
		if 'uni' in gname:
			cyrllist.append([gname + gsuffix, gname + gsuffix])
		if 'afii' in gname:
			cyrllist.append([gname + gsuffix, getUniNameByAfii(gname) + gsuffix])
	return cyrllist


def getListAfiiNames (listOfCyrlGlyphs):
	cyrllist = []
	for glyphname in listOfCyrlGlyphs:
		# for glyphname in listOfCyrlGlyphs:
		gname, gsuffix = getNameAndSuffix(glyphname)
		if 'uni' in gname:
			# print gname, getAfiiByUnicode(gname.replace('uni',''))
			cyrllist.append([gname + gsuffix, getAfiiByUnicode(gname.replace('uni', '')) + gsuffix])
		if 'afii' in gname:
			cyrllist.append([gname + gsuffix, gname + gsuffix])
	return cyrllist


# def getListOfCyrillicGlyphsUniSys(font):
# cyrllist = []
# 	if font != None:
# 		for glyphname in font.keys():
# 			uni = font[glyphname].unicode
# 			if uni != None:
# 				afii = getAfiiByUnicode(uni)
# 				if afii != None:
# 					uniname = 
# 					cyrllist.append([glyphname, afii])

# def getListOfCyrillicGlyphsAfiiSys(font):
# 	cyrllist = []
# 	if font != None:

# 	# if listglyph != None:
# 		for glyphname in font.keys():
# 			# if 'afii' not in glyphname:
# 			uni = font[glyphname].unicode
# 			if uni != None:
# 				afii = getAfiiByUnicode(uni)
# 				if afii != None:
# 					cyrllist.append([glyphname, afii])
# 					# print afii, glyphname#, "%04X" % (uni)
# 			else:
# 				if '.' in glyphname:
# 					gn = glyphname.split('.')
# 					realname = gn[0]
# 					if 'uni' in realname:
# 						realname = realname.replace('uni','')
# 					elif 'u' in realname:
# 						realname = realname.replace('u','')
# 					afii = getAfiiByUnicode(realname)
# 					if afii != None:
# 						gn[0] = afii
# 						afii = '.'.join(gn)
# 						cyrllist.append([glyphname, afii])
# 							# print afii, glyphname
# 	return cyrllist

class CyrillicExchangerTool(BaseWindowController):
	def __init__ (self):
		self.direction = toAfii
		self.w = FloatingWindow((250, 400), title = 'Cyrl')

		displayListOfGlyphs = []
		# listCyrlGlyphs = getListOfCyrillicGlyphs(CurrentFont())
		# for currentName in listCyrlGlyphs:
		# 	displayListOfGlyphs.append({"Current name": currentName, "Rename to": '?'})

		self.w.ListGlyphs = List((5, 5, -5, -70), displayListOfGlyphs,
		                         # [{"Current name": "A", "Rename to": "a"}, {"Current name": "B", "Rename to": "b"}],
		                         columnDescriptions = [{"title": AVAIL_CYRL}, {"title": RENAME_TO}],
		                         allowsEmptySelection = True, allowsMultipleSelection = False,
		                         drawFocusRing = False,
		                         selectionCallback = self.listGlyphsSelectionCallback)

		self.w.radioSelectMethod = RadioGroup((10, -60, 160, 46), ["to Afii", "to Uni"],  # isVertical = False,
		                                      callback = self.radioSelectMethodCallback)
		self.w.btnRename = Button((100, -50, 120, 21), title = 'Rename', callback = self.btnRenameCallback)
		self.w.btnRename.enable(False)
		self.updateList()
		self.w.open()

	def updateList (self):
		displayListOfGlyphs = []
		glist = []
		self.w.ListGlyphs.set([])
		listCyrlGlyphs = getListOfCyrillicGlyphs(CurrentFont())
		# print listCyrlGlyphs
		if self.direction == toAfii:
			glist = getListAfiiNames(listCyrlGlyphs)
		else:
			# if self.direction == toUni:
			glist = getListUniNames(listCyrlGlyphs)

		for currentName, renameto in glist:
			displayListOfGlyphs.append({AVAIL_CYRL: currentName, RENAME_TO: renameto})

		self.w.ListGlyphs.set(displayListOfGlyphs)

	def radioSelectMethodCallback (self, sender):
		# print 'sender', sender.get()
		self.direction = sender.get()
		self.w.btnRename.enable(True)
		# if self.direction == toAfii:
		# 	self.direction = toUni
		# else:
		# 	self.direction = toAfii
		# print self.direction
		self.updateList()

	def btnRenameCallback (self, sender):
		displayListOfGlyphs = self.w.ListGlyphs.get()
		# for pair in displayListOfGlyphs:
		# 	print pair[AVAIL_CYRL], pair[RENAME_TO]
		font = CurrentFont()
		# if self.direction == toUni:
		for pair in displayListOfGlyphs:
			print pair[AVAIL_CYRL], '>>', pair[RENAME_TO]
			if not font.has_key(pair[RENAME_TO]):
				font.renameGlyph(pair[AVAIL_CYRL], pair[RENAME_TO], True, True, True)



		# for originglyph, renameglyph in self.w.ListGlyphs.get():
		# 	print originglyph, renameglyph


	def listGlyphsSelectionCallback (self, sender):
		pass

	# font.selection = [self.w.ListGlyphs[sender.getSelection()[0]]['Current name']]#self.w.ListGlyphs[sender.getSelection()[0]]['Current name']


font = CurrentFont()
CyrillicExchangerTool()

