#!/usr/bin/env python
from SherdogScraper import SherdogScraper 


class testlog:
  def log(self, str):
    print str

t = testlog()

x = SherdogScraper(t)

print dir(x)
print x
event = x.getEventDetails(18346)
print event
