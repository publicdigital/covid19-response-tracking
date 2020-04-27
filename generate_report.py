import os
from jinja2 import Template
import re

def filter_bad_filename_chars(filename):
    """
        Filter bad chars for any filename
    """
    # Before, just avoid triple underscore escape for the classic '://' pattern
    filename = filename.replace('://', '_')

    return re.sub('[^\w\-_\. ]', '_', filename)[0 : 100]

output_directory = "/home/james/screenshots"
list_file = os.path.join(output_directory, 'list.txt')
tmpl_file = os.path.join(output_directory, 'template.html')

with open(tmpl_file) as tmpl:
  template = Template(tmpl.read())

with open(list_file, 'r') as f:
  for url in f:
      stripped_url = url.strip()
      with open(os.path.join(output_directory, "reports", filter_bad_filename_chars(stripped_url)), "w") as report:
        report.write(template.render(site_name=url.strip()))


