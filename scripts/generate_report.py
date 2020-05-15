import os
import glob
import json
from jinja2 import Template
import statistics
import base64
import imageio
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
import c19utils
import re

url_mappings = {
  'https://coronaviruscolombia.gov.co/': 'https://coronaviruscolombia.gov.co/Covid19/index.html',
  'https://health.ri.gov/covid': 'https://health.ri.gov/covid/',
  'https://www.health.ny.gov/diseases/communicable/coronavirus/': 'https://coronavirus.health.ny.gov/home',
  'https://www.govt.nz/covid-19-novel-coronavirus/': 'https://covid19.govt.nz/',
  'https://en.ssi.dk': 'https://en.ssi.dk/',
  'https://arkartassituacija.gov.lv': 'https://arkartassituacija.gov.lv/',
  'https://www.bahamas.gov.bs': 'https://www.bahamas.gov.bs/'
        }

# The lighthouse key isn't guaranteed to match the URL
# so allow for variance (but don't implement it yet)
def translate_to_lighthouse_key(lighthouse_keys, url):
  if url in lighthouse_keys:
    return url
  elif url_mappings[url] in lighthouse_keys:
    return url_mappings[url]
  return url

def generate_loading_gif(report, output_filename, url_stub):
  try:
    images = []
    times = []

    for item in report['audits']['screenshot-thumbnails']['details']['items']:
      if item['data'][0:4] == 'data':
        encoded_data = item['data'][23:]
      else:
        encoded_data = item['data']
      decoded = base64.b64decode(encoded_data)
      images.append(imageio.imread(decoded))
      times.append(float(item['timing']) / 1000)

    imageio.mimsave(output_filename, images, loop = 1, duration = times)
    return "/reports/loading/" + url_stub + ".gif"
  except KeyError as e:
      print(f"Couldn't generate loading gif for {url_stub}: {report['audits']['screenshot-thumbnails']['errorMessage']}")
      return ""

def get_reading_ages(language_directory):
  language_files_list = glob.glob(os.path.join(language_directory, "*.json"))
  latest_file = max(language_files_list, key=os.path.getctime)
  with open(latest_file) as lang_file:
      return json.loads(lang_file.read())

def get_map_of_lighthouse_data(lighthouse_folder):
  json_file_list = glob.glob(lighthouse_folder + '/*.json')
  combined = {}
  for json_file in json_file_list:
    try:
      json_data = open(json_file, "r").read()
      loaded_json = json.loads(json_data)
      url = loaded_json['finalUrl']
      if not url in combined.keys():
        combined[url] = []
      combined[url].append(json_file)
    except KeyError as e:
        raise e
  return combined

def get_date_indexed_lighthouse_data(json_file_list):
  parsed_data = {}

  for json_file in json_file_list:
    json_data = open(json_file, "r").read()
    loaded_json = json.loads(json_data)
    url = loaded_json['finalUrl']
    date = loaded_json['fetchTime'].split('T')[0]

    parsed_data[date] = loaded_json
  return parsed_data

# TODO: Look at how we could get x,y as a dict to avoid mismatches
# TODO: The image produced truncates the axis labels. Fix that.
def generate_graph(x, y, filename, title):
  fig = plt.figure()
  ax1 = fig.add_subplot(1, 1, 1)
  ax1.set_title(title)
  ax1.scatter(x, y, label= "stars", color= "green", marker= "*", s=30)
  ax1.set_xlabel('Date')
  ax1.set_ylabel('Score')
  ax1.set_ylim(bottom = 0, top = 1)
  for tick in ax1.get_xticklabels():
    tick.set_rotation(90)
  fig.savefig(filename)
  plt.close(fig)

def extract_scores(data, dates):
  output = {'accessibility' : [], 'performance' : []}
  for characteristic in output:
    output[characteristic] = [data[key]['categories'][characteristic]['score'] for key in dates if data[key]['categories'][characteristic]['score']]
  return output

def generate_graphs_over_time(dates, extracted, output_directory_and_stub):
  try:
    generate_graph(dates, extracted['accessibility'], output_directory_and_stub + "_accessibility.png", "Accessibility")
    generate_graph(dates, extracted['performance'], output_directory_and_stub + "_performance.png", "Performance")
  except Exception as e:
    print("Couldn't generate graphs: " + repr(e))

def calculate_scores(latest_date, extracted, data):
  calculations = {}

  try:
    if len(extracted['accessibility']) > 0:
      calculations['max_accessibility'] = max(extracted['accessibility'])
      calculations['average_accessibility'] = statistics.mean(extracted['accessibility'])
      calculations['current_accessibility'] = data[latest_date]['categories']['accessibility']['score']
    if len(extracted['performance']) > 0:
      calculations['max_performance'] = max(extracted['performance'])
      calculations['average_performance'] = statistics.mean(extracted['performance'])
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

def generate_timelapse(url_stub, root_directory, output_file):
    os.system(f"convert -loop 1 -delay 10 {root_directory}/**/{url_stub}.png {output_file}")
    return f"/reports/timelapses/{url_stub}.gif"

def identify_latest_date(site_data):
  dates_covered = list(site_data.keys())
  dates_covered.sort()
  return dates_covered[-1]

directories = c19utils.establish_directories()

list_file = os.path.join(directories['base'], 'list.txt')
page_tmpl_file = os.path.join(directories['templates'], 'site.html')
index_tmpl_file = os.path.join(directories['templates'], 'index.html')

latest_language_data = get_reading_ages(directories['languages'])
lighthouse_index = get_map_of_lighthouse_data(directories['lighthouse'])
site_list = {}

with open(page_tmpl_file) as tmpl:
  page_template = Template(tmpl.read())

with open(index_tmpl_file) as tmpl:
  index_template = Template(tmpl.read())

top_scores = {'accessibility' : {}, 'performance' : {}}
avg_scores = {'accessibility' : {}, 'performance' : {}}

with open(list_file, 'r') as f:
  for url in f:
      stripped_url = url.strip()
      scores = {}
      clean_url = c19utils.filter_bad_filename_chars(stripped_url)
      url_stub = clean_url[0:100]
      loading_gif_filename = os.path.join(directories['loading'], url_stub + ".gif")
      graph_directory_and_prefix = os.path.join(directories['graphs'], url_stub)

      try:
        key = translate_to_lighthouse_key(lighthouse_index.keys(), stripped_url)
        site_data = get_date_indexed_lighthouse_data(lighthouse_index[key])

        dates_covered = list(site_data.keys())
        dates_covered.sort()
        latest_date = dates_covered[-1]

        extracted_scores = extract_scores(site_data, dates_covered)
        scores = calculate_scores(latest_date, extracted_scores, site_data)

        top_scores['accessibility'][stripped_url] = scores.get('max_accessibility', 0)
        top_scores['speed'][stripped_url] = scores.get('max_speed', 0)
        avg_scores['accessibility'][stripped_url] = scores.get('average_accessibility', 0)
        avg_scores['speed'][stripped_url] = scores.get('average_speed', 0)

        generate_graphs_over_time(dates_covered, extracted_scores, graph_directory_and_prefix)
        scores['graph_filename'] = "/reports/graphs/" + url_stub

        output_file = os.path.join(directories['timelapses'], url_stub + ".gif")
        scores['timelapse_filename'] = generate_timelapse(clean_url, directories['base'], output_file)
        scores['loading_gif_filename'] = generate_loading_gif(site_data[latest_date], loading_gif_filename, url_stub)
      except KeyError as e:
          print(f"No sign of lighthouse data for {stripped_url}")
          print(repr(e))
          raise e

      with open(os.path.join(directories['reports'], url_stub + ".html"), "w") as report:
        scores['site_name'] = stripped_url
        try:
          scores['reading_age'] = find_reading_age(latest_language_data[stripped_url])
          if scores['reading_age']:
            extracted_numbers = re.search(r'\d+', scores['reading_age'])
            if extracted_numbers:
              score_to_use = int(extracted_numbers.group())
              top_scores['reading_age'][stripped_url] = score_to_use
              # TODO: Replace this with proper averages
              avg_scores['reading_age'][stripped_url] = score_to_use
        except KeyError:
          scores['reading_age'] = 'tbd'

        output = page_template.render(scores)
        report.write(output)
        site_list[stripped_url] = "/reports/" + url_stub + ".html"

rankings = { 'accessibility': [], 'performance' : [] }
for consideration in rankings:
  d_sorted_by_value = OrderedDict(sorted(top_scores[consideration].items(), key=lambda x: x[1],  reverse=True))
  rankings[consideration] = d_sorted_by_value

index = index_template.render(sites = site_list, considerations = rankings, avg_scores = avg_scores)
with open(os.path.join(directories['reports'], "index.html"), "w") as index_file:
  index_file.write(index)
