import os
import requests
from datetime import datetime
import c19utils

formatted_date = datetime.now().strftime("%Y-%m-%d")
directories = c19utils.establish_directories(formatted_date)

for url in c19utils.CovidURLList():
    psi_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=" + url
    print("Requesting Page Speed Insights for:", url)

    downloaded = requests.get(psi_url).text
    try:
      filename = c19utils.filter_bad_filename_chars(url)
      output_filename = os.path.join(directories['today'], ('page_speed_insights-%s.json' % filename))
      html_file = open(output_filename, "w")
      html_file.write(downloaded)
      html_file.close()
    except Exception as e:
      # For now we don't worry if it doesn't save, we just let the user know
      print(f"Failed to store PSI JSON for {url}")
