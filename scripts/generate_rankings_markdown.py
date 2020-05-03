import glob
import json
import statistics
from collections import OrderedDict

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

parsed_data = get_all_scores()
top_scores = {'accessibility' : {}, 'performance' : {}}
avg_scores = {'accessibility' : {}, 'performance' : {}}
for url, data in parsed_data.items():
    extracted_accessibility = [item['accessibility']['score'] for item in data.values() if item['accessibility']['score']]
    extracted_performance = [item['performance']['score'] for item in data.values() if item['performance']['score']]
    try:
        top_scores['accessibility'][url] = max(extracted_accessibility)
        top_scores['performance'][url] = max(extracted_performance)
        avg_scores['accessibility'][url] = statistics.mean(extracted_accessibility)
        avg_scores['performance'][url] = statistics.mean(extracted_performance)
    except:
        print("Problem with %s", url)
        print(extracted_accessibility)
        print(extracted_performance)

for consideration in ['accessibility', 'performance']:
  d_sorted_by_value = OrderedDict(sorted(top_scores[consideration].items(), key=lambda x: x[1],  reverse=True))
  print "## Test rankings for consideration"
  print "| URL | Highest score | Average score |"
  print "| --- | --- | --- |"
  for url, high_score in d_sorted_by_value.items():
      try:
        print "| ", url, " | ", high_score, " | ", avg_scores[consideration][url], " |"
      except:
        print "| ", url, " | ", high_score, " | - |"

