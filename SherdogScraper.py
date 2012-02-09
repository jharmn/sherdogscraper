#!/usr/bin/env python
import os
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

__author__ = "Jason Harmon (jason@wheelspecs.com)"
__version__ = "0.0.1"
__copyright__ = "Copyright (c) 2012 Jason Harmon"
__license__ = "New-style BSD"

class SherdogScraper:
	def __init__(self, logger):
		self.__logger = logger

	def getEventDetails(self, sherdogEventID):
		
		"""
		This function will retrieve and return all event details from sherdog.com for a given event ID.
		
		name: getEventDetails
		@param sherdogEventID
		@return event
		"""

		self.__logger.log('########## Getting event details ##########')
		event = {}
		event['ID'] = sherdogEventID
		self.__logger.log('ID: %s' % event['ID'])
		url = 'http://www.sherdog.com/fightfinder/fightfinder.asp?eventID=%s' % sherdogEventID
		soup = BeautifulSoup(self.getHtml(url))
		event['title'] = soup.find("div", {"class" : "Txt30Blue Bold SpacerLeft8"}).h1.string
		self.__logger.log('Title: %s' % event['title'])
		event['promotion'] = soup.find("div", {"class" : "Txt13Orange Bold SpacerLeft8"}).a.string
		self.__logger.log('Promotion: %s' % event['promotion'])
		tempDate = soup.find("div", {"class" : "Txt13White Bold SpacerLeft8"}).string
		tempYear = tempDate.split(' ')[2]
		tempDay = "%.2d" % int(tempDate.split(' ')[1].rstrip(','))
		tempMonth = tempDate.split(' ')[0]
		if tempMonth == 'January': tempMonth = '01'
		elif tempMonth == 'February': tempMonth = '02'
		elif tempMonth == 'March': tempMonth = '03'
		elif tempMonth == 'April': tempMonth = '04'
		elif tempMonth == 'May': tempMonth = '05'
		elif tempMonth == 'June': tempMonth = '06'
		elif tempMonth == 'July': tempMonth = '07'
		elif tempMonth == 'August': tempMonth = '08'
		elif tempMonth == 'September': tempMonth = '09'
		elif tempMonth == 'October': tempMonth = '10'
		elif tempMonth == 'November': tempMonth = '11'
		elif tempMonth == 'December': tempMonth = '12'
		event['date'] = "%s-%s-%s" % (tempYear, tempMonth, tempDay)
		self.__logger.log('Date: %s' % event['date'])
		try:
			event['venue'] = soup.find("div", {"class" : "Txt13Gray Bold SpacerLeftBottom8"}).findAll(text=True)[0].rstrip().rstrip(',')
			self.__logger.log('Venue: %s' % event['venue'])
		except:
			event['venue'] = ''
			self.__logger.log('Venue: Not Found')
		try:
			event['city'] = soup.find("div", {"class" : "Txt13Gray Bold SpacerLeftBottom8"}).findAll(text=True)[1].rstrip().lstrip()
			self.__logger.log('City: %s' % event['city'])
		except:
			event['city'] = ''
			self.__logger.log('City: Not Found')
		table = soup.find("table", {"class" : "fight_event_card"})
		event['fights'] = []
		try:
			rows = table.findAll('tr')
			rowcount = 0
			for row in rows:
				if not rowcount == 0:
					cols = row.findAll('td')
					
					fight = {}
					fight['ID'] = cols[0].string
					fight['fighter1'] = cols[1].a['href'].rsplit('-', 1)[1]
					fight['fighter2'] = cols[3].a['href'].rsplit('-', 1)[1]
					if cols[1].findAll(text=True)[1] == 'Winner':
						fight['winner'] = cols[1].a['href'].rsplit('-', 1)[1]
					else:
						fight['winner'] = None
					fight['result'] = cols[4].string
					fight['round'] = cols[5].string
					fight['time'] = cols[6].string
					event['fights'].append(fight)
					self.__logger.log('Fight %s: %s vs. %s' % (fight['ID'], fight['fighter1'], fight['fighter2']))
				rowcount = rowcount + 1
		except:
			pass

		self.__logger.log('###### Finished getting event details #####')
		return event

	def getFighterDetails(sherdogFighterID):

		"""
		This function will retrieve and return all event details from sherdog.com for a given event ID.
		
		name: getEventDetails
		@param sherdogEventID
		@return event
		"""

		self.__logger.log('######### Getting fighter details #########')

		fighter = {}
		fighter['ID'] = ''
		fighter['name'] = ''
		fighter['nickName'] = ''
		fighter['association'] = ''
		fighter['height'] = ''
		fighter['weight'] = ''
		fighter['birthYear'] = ''
		fighter['birthDay'] = ''
		fighter['birthMonth'] = ''
		fighter['city'] = ''
		fighter['country'] = ''

		url = 'http://www.sherdog.com/fightfinder/fightfinder.asp?fighterID=%s' % sherdogFighterID

		fighter['ID'] = sherdogFighterID
		self.__logger.log('ID: %s' % fighter['ID'])

		soup = BeautifulSoup(self.getHtml(url))

		table = soup.find("span", {"id" : "fighter_profile"})
		rows = table.findAll('tr')
		for row in rows:
			infoItem = row.findAll('td')
			if infoItem[0].string == None:
				continue
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Name':
				fighter['name'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('Name: %s' % fighter['name'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Nick Name':
				fighter['nickName'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('Nickname: %s' % fighter['nickName'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Association':
				fighter['association'] = infoItem[1].a.string.rstrip(' ').rstrip('\n')
				self.__logger.log('Association: %s' % fighter['association'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Height':
				fighter['height'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('Height: %s' % fighter['height'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Weight':
				fighter['weight'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('Weight: %s' % fighter['weight'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Birth Date':
				fighter['birthYear'] = infoItem[1].string.rstrip(' ').rstrip('\n').split('-')[0]
				fighter['birthMonth'] = infoItem[1].string.rstrip(' ').rstrip('\n').split('-')[1]
				fighter['birthDay'] = infoItem[1].string.rstrip(' ').rstrip('\n').split('-')[2]
				self.__logger.log('DOB: %s-%s-%s' % (fighter['birthDay'], fighter['birthMonth'], fighter['birthYear']))
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'City':
				fighter['city'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('City: %s' % fighter['city'])
			if infoItem[0].string.rstrip(' ').rstrip('\n') == 'Country':
				fighter['country'] = infoItem[1].string.rstrip(' ').rstrip('\n')
				self.__logger.log('Country: %s' % fighter['country'])
		
		self.__logger.log('##### Finished getting fighter details ####')
		return fighter

	def getHtml(self, url):
		"""
                This function will retrieve and return html for a given url

                name: getHtml 
                @param url
                @return html
                """
		
		try:
			client = urlopen(url)
			data = client.read()
			client.close()
		except:
			self.__logger.log('Error getting data from: %s' % url)
		else:
			self.__logger.log('Retrieved URL: %s' % url)
		
			return data

#			def writeFighterThumb(fighter, fighterDir):
#			fighterThumb = fighter['ID'] + '.jpg'
#			thumbPath = os.path.join(fighterDir, fighterThumb)
#			if not xbmcvfs.exists(thumbPath):
#				thumbUrl = soup.find("span", {"id" : "fighter_picture"}).img['src']
#				if not thumbUrl == 'http://www.cdn.sherdog.com/fightfinder/Pictures/blank_fighter.jpg':
#					downloadFile(thumbUrl, thumbPath)
