#!/usr/bin/env python
from SherdogScraper import SherdogScraper 
import unittest
import datetime

class TestSherdogScraper(unittest.TestCase):

  def setUp(self):
    self.s = SherdogScraper()

#  def test_organizations(self):
#    o = self.s.getOrganizationList()
#    self.assertEqual(o[0]['ID'], '1809')
#    self.assertEqual(o[0]['name'], '10-4 Thunder')
#    self.assertEqual(o[1]['ID'], '1846')

  def test_events(self):
    e = self.s.getEventList(2)
    for event in e:
      if event['ID'] == '18346':
        self.assertEqual(event['date'], datetime.datetime(2011, 12, 30, 0, 0))
        self.assertEqual(event['name'], 'TUF 15 - The Ultimate Fighter 15 Finale')
        self.assertEqual(event['location'], 'Las Vegas, Nevada, United States')

  def test_fighterSearch(self):
    f = self.s.getFighterSearch('', 'rich+franklin')
    self.assertEqual(len(f), 1)
    self.assertEqual(f[0]['name'], 'Rich Franklin')
    f = self.s.getFighterSearch('6', 'mitchell')
    self.assertEqual(len(f), 7)
    self.assertEqual(f[0]['name'], 'Billy Mitchell')

  def test_fighter(self):
    f = self.s.getFighterDetails(2326)
    self.assertEqual(f['name'], 'Mirko Filipovic')
    self.assertEqual(f['nickName'], 'Cro Cop')
    self.assertEqual(f['association'], 'Cro Cop Squad Gym')
    self.assertEqual(f['height'], u'6\'2" (187.96 cm)')
    self.assertEqual(f['weight'], '227 lbs (102.97 kg)')
    self.assertEqual(f['birthDate'], '1974-09-10')
    self.assertEqual(f['city'], 'Zagreb')
    self.assertEqual(f['country'], 'Croatia')
    f = self.s.getFighterDetails(26498)
    self.assertEqual(f['name'], 'Deray Davis')
    self.assertEqual(f['nickName'], '')
    self.assertEqual(f['association'], 'Team Corral')
    self.assertEqual(f['height'], u'0\'0" (0 cm)')
    self.assertEqual(f['weight'], '170 lbs (77.11 kg)')
    self.assertEqual(f['birthDate'], 'N/A')
    self.assertEqual(f['city'], '')
    self.assertEqual(f['country'], '')

  def test_event(self):
    e = self.s.getEventDetails(18346)
    self.assertEqual(e['title'], u'UFC 141 - Lesnar vs. Overeem')
    self.assertEqual(e['venue'], u'MGM Grand Garden Arena')
    self.assertEqual(e['city'], 'Las Vegas, Nevada, United States')
    self.assertEqual(e['date'], datetime.datetime(2011, 12, 30, 0, 0))
    self.assertEqual(e['fights'][0]['fighter1'], '25981')
    self.assertEqual(e['fights'][0]['fighter2'], '5185')
    self.assertEqual(e['fights'][0]['fighter1'], e['fights'][0]['winner'])
    self.assertEqual(e['fights'][1]['fighter1'], '24765')
    self.assertEqual(e['fights'][1]['fighter2'], '16555')
    self.assertEqual(e['fights'][1]['fighter1'], e['fights'][1]['winner'])
    self.assertEqual(e['fights'][2]['fighter1'], '16374')
    self.assertEqual(e['fights'][2]['fighter2'], '573')
    self.assertEqual(e['fights'][2]['fighter1'], e['fights'][2]['winner'])
    self.assertEqual(e['fights'][3]['fighter1'], '26070')
    self.assertEqual(e['fights'][3]['fighter2'], '7540')
    self.assertEqual(e['fights'][3]['fighter1'], e['fights'][3]['winner'])
    self.assertEqual(e['fights'][4]['fighter1'], '11884')
    self.assertEqual(e['fights'][4]['fighter2'], '10380')
    self.assertEqual(e['fights'][4]['fighter1'], e['fights'][4]['winner'])
    self.assertEqual(e['fights'][5]['fighter1'], '48046')
    self.assertEqual(e['fights'][5]['fighter2'], '5778')
    self.assertEqual(e['fights'][5]['fighter1'], e['fights'][5]['winner'])
    self.assertEqual(e['fights'][6]['fighter1'], '26162')
    self.assertEqual(e['fights'][6]['fighter2'], '435')
    self.assertEqual(e['fights'][6]['fighter1'], e['fights'][6]['winner'])
    self.assertEqual(e['fights'][7]['fighter1'], '24539')
    self.assertEqual(e['fights'][7]['fighter2'], '4865')
    self.assertEqual(e['fights'][7]['fighter1'], e['fights'][7]['winner'])
    self.assertEqual(e['fights'][8]['fighter1'], '11451')
    self.assertEqual(e['fights'][8]['fighter2'], '15105')
    self.assertEqual(e['fights'][8]['fighter1'], e['fights'][8]['winner'])
    self.assertEqual(e['fights'][9]['fighter1'], '461')
    self.assertEqual(e['fights'][9]['fighter2'], '17522')
    self.assertEqual(e['fights'][9]['fighter1'], e['fights'][9]['winner'])

if __name__ == '__main__':
  unittest.main()
