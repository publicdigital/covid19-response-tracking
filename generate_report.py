import os
import glob
import json
from jinja2 import Template
import re
import statistics

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)[0 : 100]

def translate_to_lighthouse_key(lighthouse_keys, url):
  if url in lighthouse_keys:
    return url
  #  print(lighthouse_keys)
  return url

def get_all_scores():
  json_file_list = glob.glob('/home/james/screenshots/lighthouse-reports/*.json')

  parsed_data = {}

  for json_file in json_file_list:
    json_data = open(json_file, "r").read()
    loaded_json = json.loads(json_data)
    url = loaded_json['finalUrl']
    date = loaded_json['fetchTime'].split('T')[0]
    if not url in parsed_data:
        parsed_data[url] = {}

    parsed_data[url][date] = loaded_json['categories']
  return parsed_data

def make_score_calculations(data):
  extracted_accessibility = [item['accessibility']['score'] for item in data.values() if item['accessibility']['score']]
  extracted_performance = [item['performance']['score'] for item in data.values() if item['performance']['score']]

  calculations = {}

  try:
    if len(extracted_accessibility) > 0:
      calculations['max_accessibility'] = max(extracted_accessibility)
      calculations['average_accessibility'] = statistics.mean(extracted_accessibility)
      calculations['current_accessibility'] = extracted_accessibility[-1]
    if len(extracted_performance) > 0:
      calculations['max_performance'] = max(extracted_performance)
      calculations['average_performance'] = statistics.mean(extracted_performance)
      calculations['current_performance'] = extracted_performance[-1]
  except Exception as err:
      print(repr(err))
      print(f"Problem with {url}")
      print(extracted_accessibility)
      print(extracted_performance)
  return calculations

parsed_data = get_all_scores()

output_directory = "/home/james/screenshots"
list_file = os.path.join(output_directory, 'list.txt')
tmpl_file = os.path.join(output_directory, 'template.html')

with open(tmpl_file) as tmpl:
  template = Template(tmpl.read())

with open(list_file, 'r') as f:
  for url in f:
      stripped_url = url.strip()
      try:
        key = translate_to_lighthouse_key(parsed_data.keys(), stripped_url)
        site_data = parsed_data[key]
        scores = make_score_calculations(site_data)
      except KeyError:
          print(f"No sign of lighthouse data for {stripped_url}")

      with open(os.path.join(output_directory, "reports", filter_bad_filename_chars(stripped_url) + ".html"), "w") as report:
        scores['site_name'] = stripped_url
        scores['reading_age'] = 'tbd'
        output = template.render(scores)
        report.write(output)

