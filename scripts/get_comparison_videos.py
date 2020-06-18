import requests
from urllib import parse
import c19utils
import os
import time
import getopt
import sys

def generate_request_url(wpt_server, this_site, top_site):
  return f"{wpt_server}m/video/docompare.php?url[1]={this_site}&url[2]={top_site}&label[1]=This+site&label[2]=Top+performer"

def generate_video_request_url(wpt_server, test_id):
  return f"{wpt_server}/video/create.php?tests={test_id}&end=visual&bg=000000&fg=ffffff"

def process_video_for(wpt_server, result_page, site_url):
  print("Moving on to getting video for",site_url)

  o = parse.urlparse(result_page.url)
  test_id = parse.parse_qs(o.query)['tests'][0]

  video_request_url = generate_video_request_url(wpt_server, test_id)
  res = requests.get(video_request_url)

  # requests will automatically follow a 301
  p = parse.urlparse(res.url)
  video_id = parse.parse_qs(p.query)['id'][0]

  # Let's give it a moment...
  time.sleep(5)

  video_filename = f"{wpt_server}/video/download.php?id={video_id}"
  print("Getting video",video_filename)
  output_name = c19utils.filter_bad_filename_chars(site_url) + ".mp4"

  try:
    os.system(f"curl -o {output_name} {video_filename}")
    if os.stat(output_name).st_size == 5336:
      print("Failed to get video (suspicious filesize)", video_filename)
  except OSError as e:
      print(repr(e))
      print("While processing",site_url)

help_string = "get_comparison_videos.py -t <top_site_url> -s <webpage_test_server> -l <list_file> -o <output_folder>"

try:
    opts, args = getopt.getopt(sys.argv[1:],"ht:s:", ["topsite=","wptserver="])
except getopt.GetoptError:
  print(help_string)
  sys.exit(2)

# TODO: Get this from real data
for opt, arg in opts:
  if opt == '-h':
    print(help_string)
    sys.exit()
  elif opt in ['-t', '--topsite']:
    top_site = arg
  elif opt in ['-s', '--wptserver']:
    wpt_server = arg
  elif opt in ['-l', '--listfile']:
    list_file = arg
  elif opt in ['-o', '--output']:
    output_folder = arg

successes = {}
directories = c19utils.establish_directories("2020-05-04")

for url in c19utils.CovidURLList():
  comparison_url = generate_request_url(wpt_server, url, top_site)
  abc = requests.get(comparison_url)

  # The URL should return a 301, but requests follows
  # that by default and gives us the following page
  if abc.status_code == 200:
    print("Triggered comparison for " + url)
    successes[url] = abc.url

iterable = list(successes.keys())

while len(iterable) > 0:
  print("Running a check with", str(len(iterable)), "items in queue")
  for site_url in iterable:
    check = requests.get(successes[site_url])
    if "Tested From" in check.text:
      process_video_for(wpt_server, check, site_url)
      iterable.remove(site_url)
  time.sleep(5)

