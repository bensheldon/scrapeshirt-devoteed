Scrapeshirt
===========

This script, `scrapeshirt.py`, scrapes some daily t-shirt websites then posts it to [Devoteed](http://we.shirtsonsale.info/), the crowdsourced daily t-shirt site that came out of shirtsonsale.info, RIP.

Devoteed is built on top of Shoutem, whose API is an near clone of Twitter's API (pre-OAuth). So this basically "tweets" (shoutems?) one tweet per shirt and even uploads the image of the shirt.

Instructions
------------

1. Create an account on http://we.shirtsonsale.info/
2. Edit `scraepshirt.py` to to set your `USERNAME` and `PASSWORD`
3. Run `python scrapeshirt.py` every day.