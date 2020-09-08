import c19utils
import asyncio
import pyppeteer
from datetime import datetime
import os

formatted_date = datetime.now().strftime("%Y-%m-%d")
directories = c19utils.establish_directories(formatted_date)

async def fetch_url(url):
  try:
    print("Processing " + url)
    filename = c19utils.filter_bad_filename_chars(url)
    output_filename = os.path.join(directories['today'], ('%s.png' % filename))

    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.setViewport({'width': 800, 'height': 1280})
    await page.goto(url)
    await page.screenshot({'path': output_filename})
    await browser.close()
  except pyppeteer.errors.TimeoutError:
    print("Timed out fetching " + url)
  except pyppeteer.errors.PageError:
    print("Page error for " + url)

async def main():
  for url in c19utils.CovidURLList():
    try:
      await asyncio.wait_for(fetch_url(url), timeout=15.0)
    except asyncio.TimeoutError:
      print("asyncio timeout for " + url)


asyncio.get_event_loop().run_until_complete(main())
