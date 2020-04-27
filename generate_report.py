import os
import glob
import json
from jinja2 import Template
import re
import statistics
import base64
import imageio

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
  return url

def generate_loading_gif(report, output_filename):
  try:
    images = []
    times = []

    for item in report['audits']['screenshot-thumbnails']['details']['items']:
      decoded = base64.b64decode(item['data'])
      images.append(imageio.imread(decoded))
      times.append(float(item['timing']) / 1000)

    imageio.mimsave(output_filename, images, loop = 1, duration = times)
  except KeyError as e:
      print(repr(e))

def get_reading_ages(language_directory):
  language_files_list = glob.glob(os.path.join(language_directory, "*.json"))
  latest_file = max(language_files_list, key=os.path.getctime)
  with open(latest_file) as lang_file:
      return json.loads(lang_file.read())

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

    parsed_data[url][date] = loaded_json
  return parsed_data

def make_score_calculations(data):
  extracted_accessibility = [item['categories']['accessibility']['score'] for item in data.values() if item['categories']['accessibility']['score']]
  extracted_performance = [item['categories']['performance']['score'] for item in data.values() if item['categories']['performance']['score']]

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
  return calculations

output_directory = "/home/james/screenshots"
language_directory = os.path.join(output_directory, 'language-analysis')
list_file = os.path.join(output_directory, 'list.txt')
tmpl_file = os.path.join(output_directory, 'template.html')

latest_language_data = get_reading_ages(language_directory)
parsed_data = get_all_scores()

with open(tmpl_file) as tmpl:
  template = Template(tmpl.read())

with open(list_file, 'r') as f:
  for url in f:
      stripped_url = url.strip()
      scores = {}

      try:
        key = translate_to_lighthouse_key(parsed_data.keys(), stripped_url)
        site_data = parsed_data[key]
        dates_covered = list(site_data.keys())
        dates_covered.sort()
        latest_date = dates_covered[-1]
        scores = make_score_calculations(site_data)
      except KeyError as e:
          print(f"No sign of lighthouse data for {stripped_url}")
          print(repr(e))

      with open(os.path.join(output_directory, "reports", filter_bad_filename_chars(stripped_url) + ".html"), "w") as report:
        scores['site_name'] = stripped_url
        try:
          scores['reading_age'] = latest_language_data[stripped_url]['dragnet']['standard']
        except KeyError:
          try:
            scores['reading_age'] = latest_language_data[stripped_url]['trafilatura']['standard']
          except KeyError:
            scores['reading_age'] = 'tbd'

        if scores['reading_age'] == '-1th and 0th grade':
            scores['reading_age'] = 'tbd'

        loading_gif_filename = os.path.join(output_directory, "reports", "loading", filter_bad_filename_chars(stripped_url) + ".gif")

        generate_loading_gif(site_data[latest_date], loading_gif_filename)
        scores['loading_gif_filename'] = "/reports/loading/" + filter_bad_filename_chars(stripped_url) + ".gif"

        output = template.render(scores)
        report.write(output)

