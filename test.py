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

  def test_event(self):
    e = self.s.getEventDetails(18346)
    self.assertEqual(e['title'], 'UFC 141 - Lesnar vs. Overeem')

if __name__ == '__main__':
  unittest.main()
