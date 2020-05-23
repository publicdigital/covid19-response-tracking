import re
import pathlib
import os
import errno
from datetime import timedelta, date
import csv

class CovidURLList:
  def __init__(self):
    directories = establish_directories()
    list_file = os.path.join(directories['base'], 'list.csv')
    self.f = open(list_file, newline='')
    self.reader = csv.DictReader(self.f)

  def __iter__(self):
    return self

  def __next__(self):
    row = self.reader.__next__()
    if row:
        return row['URL'].strip()
    else:
        return None

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
