import re
import glob
import pathlib
import os
import errno
from datetime import timedelta, date
import csv
import orjson

class CovidSiteList:
  def __init__(self):
    directories = establish_directories()
    list_file = os.path.join(directories['base'], 'list.csv')
    self.f = open(list_file, newline='')
    self.reader = csv.DictReader(self.f)

  def __iter__(self):
    return self

  def __next__(self):
    return self.reader.__next__()

class CovidURLList(CovidSiteList):
  def __next__(self):
    row = self.reader.__next__()
    if row:
      return row['URL'].strip()
    else:
      return None

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)

def establish_directories(formatted_date = None):
    base_directory = pathlib.Path(__file__).parent.parent.absolute()

    directories = {
      'base': base_directory,
      'reports': os.path.join(base_directory, "reports"),
      'lighthouse': os.path.join(base_directory, "lighthouse-reports"),
      'languages': os.path.join(base_directory, 'language-analysis'),
      'graphs': os.path.join(base_directory, "reports", "graphs"),
      'timelapses': os.path.join(base_directory, "reports", "timelapses"),
      'loading': os.path.join(base_directory, "reports", "loading"),
      'templates': os.path.join(base_directory, "templates")
    }

    if formatted_date:
      directories['today'] = os.path.join(base_directory, formatted_date)

    for directory in directories:
        # Ensure output folders exist
        try:
            os.makedirs(directories[directory])
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    return directories

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)

def get_map_of_lighthouse_data(lighthouse_folder):
  json_file_list = glob.glob(lighthouse_folder + '/*.json')
  combined = {}
  for json_file in json_file_list:
    try:
      json_data = open(json_file, "r").read()
      loaded_json = orjson.loads(json_data)
      url = loaded_json['finalUrl']
      if not url in combined.keys():
        combined[url] = []
      combined[url].append(json_file)
    except KeyError as e:
      raise e
  return combined

url_mappings = {
  'https://coronaviruscolombia.gov.co/': 'https://coronaviruscolombia.gov.co/Covid19/index.html',
  'https://health.ri.gov/covid': 'https://health.ri.gov/covid/',
  'https://www.health.ny.gov/diseases/communicable/coronavirus/': 'https://coronavirus.health.ny.gov/home',
  'https://www.govt.nz/covid-19-novel-coronavirus/': 'https://covid19.govt.nz/',
  'https://en.ssi.dk': 'https://en.ssi.dk/',
  'https://arkartassituacija.gov.lv': 'https://arkartassituacija.gov.lv/',
  'https://www.bahamas.gov.bs': 'https://www.bahamas.gov.bs/',
  'https://www.mspas.gob.gt/index.php/noticias/coronavirus-2019-ncov': 'https://www.mspas.gob.gt/index.php/noticias/covid-19/coronavirus-2019-ncov',
  'https://www.mspas.gob.gt/index.php/noticias/covid-19/coronavirus-2019-ncov': 'https://www.mspas.gob.gt/index.php/noticias/coronavirus-2019-ncov',
  'https://www.ontario.ca/page/2019-novel-coronavirus': 'https://covid-19.ontario.ca',
  'https://coronavirusecuador.com': 'https://www.coronavirusecuador.com/',
  'https://yukon.ca/covid-19': 'https://yukon.ca/en/covid-19-information'
}
