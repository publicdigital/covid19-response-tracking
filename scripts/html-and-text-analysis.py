import textstat
import trafilatura
import requests
#import dragnet
from lxml import html
import json
from datetime import datetime
import os
import c19utils
import langdetect

formatted_date = datetime.now().strftime("%Y-%m-%d")
directories = c19utils.establish_directories(formatted_date)

output_for_json = {}

def process_trafilatura(downloaded):
  downloaded = html.fromstring(downloaded)
  return trafilatura.extract(downloaded)

def process_dragnet(downloaded):
  return dragnet.extract_content(downloaded)

def get_scores(text, language):
  scores = {}
  try:
    textstat.set_lang(language)
    scores['flesch_reading_ease'] = textstat.flesch_reading_ease(text)
    scores['smog'] = textstat.smog_index(text)
    scores['flesch_kincaid_grade'] = textstat.flesch_kincaid_grade(text)
    scores['coleman_liau'] = textstat.coleman_liau_index(text)
    scores['automated_readability'] = textstat.automated_readability_index(text)
    scores['dale_chall_readability'] = textstat.dale_chall_readability_score(text)
    scores['difficult_words'] = textstat.difficult_words(text)
    scores['linsear_write_formula'] = textstat.linsear_write_formula(text)
    scores['gunning_fog'] = textstat.gunning_fog(text)
    scores['standard'] = textstat.text_standard(text)
    return scores
  except Exception as e:
      return repr(e)

for url in c19utils.CovidURLList():
    output_for_json[url] = {'dragnet' : {}, 'trafilatura': {}}

    try:
      downloaded = requests.get(url).text
    except Exception as e:
      traf_msg = repr(e)
      output_for_json[url]['error'] = traf_msg
      continue

    # First thing we do is capture the HTML
    try:
      output_filename = os.path.join(directories['today'], ('%s.html' % c19utils.filter_bad_filename_chars(url)))
      html_file = open(output_filename, "w")
      html_file.write(downloaded)
      html_file.close()
    except:
      # For now we don't worry if it doesn't save, we just let the user know
      print(f"Failed to store HTML for {url}")

    try:
      traf_text = process_trafilatura(downloaded)
      output_for_json[url]['language'] = langdetect.detect(traf_text)
      output_for_json[url]['wordcount'] = len(traf_text.split(' ')) # Very crude, but I just want a rough sense
      output_for_json[url]['trafilatura'] = get_scores(traf_text, output_for_json[url]['language'])
      traf_msg = output_for_json[url]['trafilatura']['standard']
    except Exception as e:
      output_for_json[url]['trafilatura'] = {'error' : repr(e)}

#  try:
#    dragnet_text = process_dragnet(downloaded)
#    output_for_json[url]['dragnet'] = get_scores(dragnet_text)
#    dragnet_msg = output_for_json[url]['dragnet']['standard']
#  except Exception as e:
#    output_for_json[url]['dragnet'] = {'error' : repr(e)}
    dragnet_msg = ""

json_filename = os.path.join(directories['languages'], ('%s.json' % formatted_date))
json_file = open(json_filename, "w")
json_file.write(json.dumps(output_for_json, indent=2, sort_keys=True))
json_file.close()
