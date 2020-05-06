import re
import pathlib
import os
import errno

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
