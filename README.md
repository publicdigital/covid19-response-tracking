Capturing the evolution of public sector Covid19 response sites from around
the world. Lots of governments have responded quickly and used the web to
provide essential information, and analysing how they have done will be a
useful indicator of how well they're set up for internet-era ways of working.

This was started with a list from [the Public Digital blog](https://public.digital/2020/03/18/making-things-open-is-making-things-better/)

Reports generated from this data can be found at https://covidsites.public.digital

Please send any feedback to covidsites-feedback@public.digital

## What we capture

For each site I'm capturing:

* A screenshot
* A report from [lighthouse](https://developers.google.com/web/tools/lighthouse) in both HTML and JSON
* The HTML of the site and some basic text analysis

The former will show how the sites evolve in terms of the content they prioritise and
the visual design to support it. The lighthouse score gives us a picture of speed, and
coverage of the basics of accessibility.

They're stored in a way that was convenient to me when capturing them, which
may not be the easiest structure for analysis. If you want to use this data and there's
another structure that would make it easier for you, let me know.

## How to add a site

To recommend a site for us to include please either:

* Create a pull request to add it to the list.csv file
* or email covidsites-feedback@public.digital with the URL and the government it represents


## How it works.

Every night we do four things:

* Use an open source script to take a screenshot. This was where we started
* [Take a copy of the HTML of the site](scripts/html-and-text-analysis.py)
* [Use the lighthouse tool to run analysis of the site](scripts/lighthouse.sh)
* [Query Google's PageSpeedInsights API to capture their analysis of the site.](scripts/page-speed-insights.py)

These scripts currently run on a server provided by DigitalOcean, located in the
UK. Most of the scoring is based on objective analysis, but the score is partly
influenced by the network connection. We're considering making more use of Google's
data to get a less geographically-biased result, but expect that the impact would
be very small.

Each day we manually [generate the report](scripts/generate_report.py). This pulls
in all the data we've captured and does four things:

* Extracts the current and average accessibility scores from the lighthouse data.
* Extracts the current and average speed scores from the lighthouse data.
* Generates a timelapse animated GIF from the site
* Produces a report as a website

Every now and then we also manually run a script to generate the videos. We’re
using a private copy of the excellent [webpagetest](https://webpagetest.org)
software (running on Amazon Web Services) with some hacky scripts that manage the
queueing and check when the videos are done. As we have this set up it’s really
slow. If this service turned into a reasonable tool we’d love to get some expert
help to make it faster and more reliable, and to really tune the settings to
make the simulation of phones reliable.

### Reading age and clarity

There is some controversy over whether or not it's useful to attempt to
automatically determine the complexity of a piece of text. Because of that we're
not currently showing that measure in the reports, but we do still capture some
analysis to allow further work.

The first step is to extract text from the HTML. That’s never been a straightforward
process unless you do it manually (which we’ve not had time to do). Instead we're
relying on [Trafilatura](https://pypi.org/project/trafilatura/) for that.

We then use [textstat](https://pypi.org/project/textstat/) to extract a range
of scores for text complexity/reading age.

You can see the day-by-day results of that in the [language analysis folder](language-analysis/)

## Results

Reports generated from this data can be found at https://covidsites.public.digital

Please send any feedback to covidsites-feedback@public.digital
