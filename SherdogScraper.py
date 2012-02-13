#!/usr/bin/env python
import os
import collections
import datetime
import urllib
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup

__version__ = "0.0.1"
__license__ = "GPLv2"

class SherdogScraper:

	# declare necessary constants for script operation
	__fighterURL__ = 'http://www.sherdog.com/fighter/X-%s'
	__fighterSearchURL__ = 'http://www.sherdog.com/stats/fightfinder?weight=%s&SearchTxt=%s'
	__eventURL__ = 'http://www.sherdog.com/events/X-%s'
	__organizationURL__ = 'http://www.sherdog.com/organizations/X-%s'

	def getOrganizationList(self):

		"""
		Returns a list of all of the organizations/promotions from sherdog.com's fightfinder
		Returns:	
		organizations - A list of dictionaries containing the fight organizations as scraped from sherdog.com
		organizations fields:
		ID -- Organization's ID
		name -- Organizations's name
		
		"""

		organizations = []
		url = self.__organizationURL__ % ''
		
		# retrieve html and initialise beautifulsoup object for parsing
                soup = BeautifulSoup(self.getHtml(url))

		# store the list of organizations
		select = soup.html.find('select', { 'name' : 'organization_id'})
		for option in select.findAllNext('option'):
			organization = {}
			organization['ID'] = option['value']
			organization['name'] = option.string
			organizations.append(organization)
		return organizations


	def getEventList(self, organizationID):

		"""
		Return list of events for a given organization ID from sherdog.com's fightfinder
		Returns:
		events - A list of all of the events for the given Organization

		events fields:
		ID -- Event's ID
		Date -- The date of the event
		Title -- The title of the event
		Location -- Where the event took place

		"""

		events = []

		# generate event url
		url = self.__organizationURL__ % organizationID
	
		# retrieve html and initialise beautifulsoup object for parsing
                soup = BeautifulSoup(self.getHtml(url))

		# find events from table
		table = soup.find("table", {"class" : "event"})
		rows = table.findAll("tr")
		rowcount = 0
		for row in rows:
			if rowcount > 0:	
				cells = row.findAll("td")
				id = cells[1].a['href'].rsplit("-")[1]
				month = row.find("span", {"class" : "month"}).string
				day = row.find("span", {"class" : "day"}).string
				year = row.find("span", {"class" : "year"}).string
				tempDate = "%s %s, %s" % (month, day, year)
				eventDate = datetime.datetime.strptime(tempDate, '%b %d, %Y')
				name = cells[1].findAll(text=True)[0].string
				location = cells[2].findAll(text=True)[0].string
				events.append({'ID' : id, 'date' : eventDate, 'name': name, 'location': location})
			rowcount = rowcount + 1
		return events


	def getEventDetails(self, eventID):
		
		"""
		Return event details for a given event ID from sherdog.com's fightfinder.
		
		Arguments:
		eventID -- A String containing the event's numeric event ID from sherdog.com
		
		Returns:
		eventDetails -- A dictionary containing the events details as scraped from sherdog.com.
		
		eventDetails keys:
		ID -- Event's ID
		title -- Event's full title
		promotion -- Promotion which ran the event
		date -- Date of event (YYYY-MM-DD)
		venue -- Event's venue
		city -- City in which event took place
		fights -- A list containing dictionaries (fightDetails[]) with the details of each fight on the event
	
		fightDetails keys:
		ID -- Fight's ID
		fighter1 -- Sherdog ID for the first fighter
		fighter2 -- Sherdog ID for the second fighter
		winner -- Sherdog ID for the winning fighter
		result -- Method of victory/Type of decision
		referee -- Referee that presided over the fight
		round -- Round in which fight ended
		time -- Time at which final round ended
		"""
		
		# initialise empty dict to store event details
		eventDetails = {}
		
		# store event ID in dict
		eventDetails['ID'] = eventID
		
		# generate event url
		url = self.__eventURL__ % eventID
		
		# retrieve html and initialise beautifulsoup object for parsing
		soup = BeautifulSoup(self.getHtml(url))
		
		pageTitle = soup.html.head.title.string
		pageTitleArr = pageTitle.split(' - ', 1)	
		# find and store event title in dict
		eventDetails['title'] = pageTitle
		
		# find and store promotion name in dict
		eventDetails['promotion'] = pageTitleArr[0]
		
		# find events date
		tempDate = soup.find("div", {"class" : "authors_info"}).find("span", {"class" : "date"}).string
		
		# store event date in dict
		eventDetails['date'] = datetime.datetime.strptime(tempDate, '%b %d, %Y') 
		eventTemp = ''
		try:
			# find and store venue in dict
			eventTemp = soup.find("span", {"class" : "author"}).findAll(text=True)[0].split("\r\n")
			eventDetails['venue'] = eventTemp[0].lstrip().rstrip(",")
		except:
			# store blank string if no venue listed
			eventDetails['venue'] = ''
		
		try:
			# find and store city in dict
			eventDetails['city'] = eventTemp[1].lstrip().rstrip() 
		except:
			# store blank string if no city listed
			eventDetails['city'] = ''
		
		# find list of fights for event
		table = soup.find("div", {"class" : "module_fight_card"})
		
		# initialise empty list to store fightDetails dicts
		eventDetails['fights'] = []
	
		
		fightDetails = {}
		fights = []
		fightDetails['fighter1'] = soup.find("div", {"class" : "fighter left_side"}).a['href'].rsplit("-", 1)[1]
		fightDetails['fighter2'] = soup.find("div", {"class" : "fighter right_side"}).a['href'].rsplit("-", 1)[1]

		leftResult = ''
		rightResult = ''
		winner = ''
		leftResult = soup.find("div", {"class" : "fighter left_side"}).find("span", {"class" : "final_result win"})
		rightResult = soup.find("div", {"class" : "fighter right_side"}).find("span", {"class" : "final_result win"})
		
		if leftResult != None and leftResult.string == 'win':
			fightDetails['winner'] = fightDetails["fighter1"]
		if rightResult != None and leftResult.string == 'win':
			fightDetails['winner'] = fightDetails["fighter2"]
		
		tempCells =  soup.find("table", {"class" : "resume"}).findAll("td")
		fightDetails['ID'] = int(tempCells[0].findAll(text=True)[1].strip())
		fightDetails['result'] = tempCells[1].findAll(text=True)[1].strip()
		fightDetails['referee'] = tempCells[2].findAll(text=True)[1].strip()
		fightDetails['round'] = tempCells[3].findAll(text=True)[1].strip()
		fightDetails['time'] = tempCells[4].findAll(text=True)[1].strip()
		fights.append(fightDetails)

		# find all rows in the fights table
		rows = soup.find("div", {"class" : "content table"}).findAll("tr")
		
		# set rowcount to 0
		rowcount = 0
			
		# loop through all rows in fights table
		for row in rows:
			
			# ignore first row in table
			if not rowcount == 0:
				
				# find all columns in table
				cols = row.findAll('td')
				
				# initialise empty dict to store fight details
				fightDetails = {}
				
				# find and store fight ID
				fightDetails['ID'] = int(cols[0].string)
				
				# find and store ID for fighter1
				fightDetails['fighter1'] = cols[1].a['href'].rsplit('-', 1)[1]
				# find and store ID for fighter2
				fightDetails['fighter2'] = cols[5].a['href'].rsplit('-', 1)[1]
				
				# check that fight was not a draw
				win = cols[1].find("span").find(text=True)
				if win == 'win':
					# find and store winner ID
					fightDetails['winner'] = fightDetails['fighter1']
				else:
					# store blank string if no winner
					fightDetails['winner'] = ''
				
				# find and store result
				fightDetails['result'] = cols[6].find(text=True).string
				
				# find and store round in which fight ended
				fightDetails['referee'] = cols[6].find("span").string
				
				# find and store round in which fight ended
				fightDetails['round'] = cols[7].string
				
				# find and store end time of fight
				fightDetails['time'] = cols[8].string
				
				# add fightDetails dict to fights list
				fights.append(fightDetails)
			
			# increase rowcount by 1
			rowcount = rowcount + 1
	
		sort_on = "ID"
		sortFights = [(dict_[sort_on], dict_) for dict_ in fights]
		sortFights.sort()
		eventDetails['fights'] = [dict_ for (key, dict_) in sortFights]
		# return the scraped details
		return eventDetails


	def getFighterSearch(self, query, weightClass):
			
		"""
		Return a list of fightrs based on the query and weight class provided
		
		Arguments:
		query -- A string containing the search for a fighters first, last, or nick name
		weightClass -- Optional: the weight class ID to search in
		11 = Catch Weight
		10 = Flyweight
		9 = Bantamweight
		7 = Featherweight
		8 = Pound for Pound
		6 = Lightweight
		5 = Welterweight
		4 = Middleweight
		3 = Light Heavyweight
		2 = Heavyweight
		1 = Super Heavyweight

		Returns:
		fighters -- A list of fighters

		fighters keys:
		ID --  Fighter's ID
		name -- Fighter's full name
		nickName --  Fighter's current nickname
		association -- Fighter's current camp/association
                height -- Fighter's height
                weight -- Fighter's weight (in lbs)
		"""

		# generate fighter url
                url = self.__fighterSearchURL__ % (urllib.quote_plus(query), weightClass)

                # retrieve html and initialise beautifulsoup object for parsing
                soup = BeautifulSoup(self.getHtml(url))

		rows = soup.find("table", {"class" : "fightfinder_result"}).findAll("tr")
		rowCount = 0
		fighters = []
		for row in rows:
			if rowCount > 0:
				cells = row.findAll("td")
				fighter = {}
				fighter['ID'] = cells[1].a['href'].rsplit("-")[1]
				fighter['name'] = cells[1].a.string
				fighter['height'] = "%s %s" % (cells[2].strong, cells[2].find(text=True))
				fighter['weight'] = "%s %s" % (cells[3].strong, cells[3].find(text=True))
				fighter['association'] = cells[4].string
				fighters.append(fighter)
			rowCount = rowCount + 1
		return fighters

	def getFighterDetails(self, fighterID):
		
		"""
		Return fighter details for a given fighter ID from sherdog.com's fightfinder.
		
		Arguments:
		fighterID -- A String containing the fighter's numeric ID from sherdog.com
		
		Returns:
		fighterDetails -- A dictionary containing the fighters details as scraped from sherdog.com
		
		fighterDetails keys:
		ID -- Fighter's ID
		name -- Fighter's full name
		nickName -- Fighter's current nickname
		association -- Fighter's current camp/association
		height -- Fighter's height
		weight -- Fighter's weight (in lbs)
		birthDate -- Fighter's date of birth
		city -- Fighter's city of birth
		country -- Fighter's country of birth
		thumbUrl -- URL of fighter image
		"""
		
		# initialise empty dict to store fighter details
		fighterDetails = {}
		# set all keys to empty values
		fighterDetails['ID'] = ''
		fighterDetails['name'] = ''
		fighterDetails['nickName'] = ''
		fighterDetails['association'] = ''
		fighterDetails['height'] = ''
		fighterDetails['weight'] = ''
		fighterDetails['birthDate'] = ''
		fighterDetails['city'] = ''
		fighterDetails['country'] = ''
		
		# store fighter ID in dict
		fighterDetails['ID'] = fighterID
		
		# generate fighter url
		url = self.__fighterURL__ % fighterID
		
		# retrieve html and initialise beautifulsoup object for parsing
		soup = BeautifulSoup(self.getHtml(url))

		bio = soup.find("div", {"class" : "module bio_fighter"})	
		fighterDetails['name'] = bio.h1.find(text=True)
		try:
			fighterDetails['nickName'] = bio.find("span", {"class" : "nickname"}).em.string
		except Exception:
			fighterDetails['nickName'] = ''
		try:
			fighterDetails['association'] = bio.find("span", {"class" : "item association"}).strong.string
			heightTemp = bio.find("span", {"class" : "item height"})
		except Exception:
			fighterDetails['association'] = ''
		fighterDetails['height'] = ("%s %s" % (heightTemp.strong.string, heightTemp.findAll(text=True)[3].string)).rstrip()
		weightTemp = bio.find("span", {"class" : "item weight"})
		fighterDetails['weight'] = ("%s %s" % (weightTemp.strong.string, weightTemp.findAll(text=True)[3].string)).rstrip() 
		fighterDetails['birthDate'] = bio.find("span", {"class" : "item birthday"}).findAll(text=True)[0].rsplit(":")[1].strip()
		try:
			birthpTemp =  bio.find("span", {"class" : "item birthplace"})
			fighterDetails['city'] = birthpTemp.findAll(text=True)[1].strip()
			fighterDetails['country'] = birthpTemp.strong.string
		except Exception:
			fighterDetails['city'] = ''
			fighterDetails['country'] = ''
		""" Commented
			# check if row contains 'city' and store to fighterDetails dict
			elif infoItem[0].string.rstrip(' ').rstrip('\n') == 'City':
				fighterDetails['city'] = infoItem[1].string.rstrip(' ').rstrip('\n')

			# check if row contains 'country' and store to fighterDetails dict
			elif infoItem[0].string.rstrip(' ').rstrip('\n') == 'Country':
				fighterDetails['country'] = infoItem[1].string.rstrip(' ').rstrip('\n')
			
			# find and store url for fighter image
			fighterDetails['thumbUrl'] = soup.find("span", {"id" : "fighter_picture"}).img['src']
		"""	
		# return scraped details
		return fighterDetails


	def getHtml(self, url):
		
		"""
		Retrieve and return remote resource as string
		
		Arguments:
		url -- A string containing the url of a remote page to retrieve
		
		Returns:
		data -- A string containing the contents to the remote page
		"""


		#print 'Retrieving: '+url
	
		# connect to url using urlopen
		client = urlopen(url)
		
		# read data from page
		data = client.read()
		
		# close connection to url
		client.close()

		# return the retrieved data
		return data

