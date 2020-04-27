import os
import glob
import json
from jinja2 import Template
import re
import statistics
import base64
import imageio
import matplotlib.pyplot as plt

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)[0 : 100]

# The lighthouse key isn't guaranteed to match the URL
# so allow for variance (but don't implement it yet)
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

# TODO: The image produced truncates the axis labels. Fix that.
def generate_graph(x, y, filename, title):
  fig = plt.figure()
  ax1 = fig.add_subplot(1, 1, 1)
  ax1.set_title(title)
  ax1.scatter(x, y, label= "stars", color= "green", marker= "*", s=30)
  ax1.set_xlabel('Date')
  ax1.set_ylabel('Score')
  for tick in ax1.get_xticklabels():
    tick.set_rotation(90)
  fig.savefig(filename)
  plt.close(fig)

def make_score_calculations(data, latest_date, output_folder_and_stub):
  calculations = {}

  dates = list(data.keys())
  dates.sort()
  extracted_accessibility = [data[key]['categories']['accessibility']['score'] for key in dates if data[key]['categories']['accessibility']['score']]
  extracted_performance = [data[key]['categories']['performance']['score'] for key in dates if data[key]['categories']['performance']['score']]
  try:
    generate_graph(dates, extracted_accessibility, output_folder_and_stub + "_accessibility.png", "Accessibility")
    generate_graph(dates, extracted_performance, output_folder_and_stub + "_performance.png", "Performance")
  except Exception as e:
    print("Couldn't generate graphs: " + repr(e))

  try:
    if len(extracted_accessibility) > 0:
      calculations['max_accessibility'] = max(extracted_accessibility)
      calculations['average_accessibility'] = statistics.mean(extracted_accessibility)
      calculations['current_accessibility'] = data[latest_date]['categories']['accessibility']['score']
    if len(extracted_performance) > 0:
      calculations['max_performance'] = max(extracted_performance)
      calculations['average_performance'] = statistics.mean(extracted_performance)
      calculations['current_performance'] = data[latest_date]['categories']['performance']['score']
  except Exception as err:
      print(repr(err))
      print(f"Problem with {url}")
  return calculations

def find_reading_age(language_data):
  try:
    reading_age = language_data['dragnet']['standard']
  except KeyError:
    try:
      reading_age = language_data['trafilatura']['standard']
    except KeyError:
      reading_age = 'tbd'
  if reading_age == '-1th and 0th grade':
     reading_age = 'tbd'
  return reading_age

def generate_timelapse(url_stub, root_folder):
    output_file = os.path.join(root_folder, "reports", "timelapses", url_stub + ".gif")
    os.system(f"convert -loop 1 -delay 10 {root_folder}/**/{url_stub}.png {output_file}")
    return f"/reports/timelapses/{url_stub}.png"

output_directory = "/home/james/screenshots"
language_directory = os.path.join(output_directory, 'language-analysis')
list_file = os.path.join(output_directory, 'list.txt')
page_tmpl_file = os.path.join(output_directory, 'template.html')
index_tmpl_file = os.path.join(output_directory, 'index_template.html')

latest_language_data = get_reading_ages(language_directory)
parsed_data = get_all_scores()
site_list = []

with open(page_tmpl_file) as tmpl:
  page_template = Template(tmpl.read())

with open(index_tmpl_file) as tmpl:
  index_template = Template(tmpl.read())

with open(list_file, 'r') as f:
  for url in f:
      stripped_url = url.strip()
      scores = {}
      url_stub = filter_bad_filename_chars(stripped_url)

      try:
        key = translate_to_lighthouse_key(parsed_data.keys(), stripped_url)
        site_data = parsed_data[key]
        dates_covered = list(site_data.keys())
        dates_covered.sort()
        latest_date = dates_covered[-1]
        graph_folder_and_prefix = os.path.join(output_directory, "reports", "graphs", url_stub)
        scores = make_score_calculations(site_data, latest_date, graph_folder_and_prefix)
        scores['timelapse_filename'] = generate_timelapse(url_stub, output_directory)
        scores['graph_filename'] = "/reports/graphs/" + url_stub
      except KeyError as e:
          print(f"No sign of lighthouse data for {stripped_url}")
          print(repr(e))

      with open(os.path.join(output_directory, "reports", url_stub + ".html"), "w") as report:
        scores['site_name'] = stripped_url
        try:
          scores['reading_age'] = find_reading_age(latest_language_data[stripped_url])
        except KeyError:
          scores['reading_age'] = 'tbd'
        loading_gif_filename = os.path.join(output_directory, "reports", "loading", url_stub + ".gif")

        generate_loading_gif(site_data[latest_date], loading_gif_filename)
        scores['loading_gif_filename'] = "/reports/loading/" + url_stub + ".gif"

        output = page_template.render(scores)
        report.write(output)
        site_list.append({'name': stripped_url, 'path': "/reports/" + url_stub + ".html"})

  index = index_template.render(sites = site_list)
  with open(os.path.join(output_directory, "reports", "index.html"), "w") as index_file:
      index_file.write(index)

