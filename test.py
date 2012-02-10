#!/usr/bin/env python
from SherdogScraper import SherdogScraper 
import unittest

class testlog:

  def log(self, str):
    print str

class TestSherdogScraper(unittest.TestCase):

  def setUp(self):
    print "Setting up"
    self.l = testlog()
    self.s = SherdogScraper(self.l)

  def test_fighter(self):
    f = self.s.getFighterDetails(2326)
    self.assertEqual(f['name'], 'Mirko Filipovic')
    self.assertEqual(f['nickName'], 'Cro Cop')
    self.assertEqual(f['association'], 'Cro Cop Squad Gym')
    self.assertEqual(f['height'], '6\'2" (188cm)')
    self.assertEqual(f['weight'], '227lbs (103kg)')
    self.assertEqual(f['birthYear'], '1974')
    self.assertEqual(f['birthDay'], '10')
    self.assertEqual(f['birthMonth'], '09')
    self.assertEqual(f['city'], 'Zagreb')
    self.assertEqual(f['country'], 'Croatia')

  def test_event(self):
    e = self.s.getEventDetails(18346)
    self.assertEqual(e['title'], 'UFC 141 - Lesnar vs. Overeem')
    self.assertEqual(e['venue'], 'MGM Grand Garden Arena')
    self.assertEqual(e['city'], 'Las Vegas, Nevada, United States')
    self.assertEqual(e['date'], '2011-12-30')
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
