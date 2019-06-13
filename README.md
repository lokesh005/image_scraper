# Problem Statement
Given a plaintext file containing URLs, one per line, e.g.:
    
    http://mywebserver.com/images/271947.jpg
    http://mywebserver.com/images/24174.jpg
    http://somewebsrv.com/img/992147.jpg

Write a script that takes this plaintext file as an argument and downloads all images, storing them on the local hard disk. Also write unittest.

In a deployment scenario this script needs to be deployed to multiple Debian machines, scheduled to run every five minutes. The downloaded images should be served via http on each server.

__________

1. Clone this repo.
2. Run setup_environment.sh using command: `source setup_environment.sh`.
The script contains following things:\
   a) Selects some export statements to pick some of UTF-8 supporting locales.\
   b) Installs packages from `requirements.txt` file, using command `pip install -r requirements.txt`.\
   c) Run the cron_job script which will run the python script in every 5 minutes. Right now this is commented but when you are in a machine you can just uncomment it, so as to start the whole script by just one click.
   d) Starts the web server
3. File Hierarchy:\
   * image_scraper: This directory contains all the code needed to scrape the images from URL and save at some assigned directory.
      * `download_image.py`: This scripts downloads the images using urls from a plain text files.
      * `utils.py`: This script pre-process the url list assigned to it.
      * `utils_url_validator.py`: This script validates the URL.
      
   * sample_data: This directory contains the text file which contains the URLs of the image.
   * tests: This directory contains unittest for all the scripts present in `image_scraper` directory.
      * `test_download_image.py`: Unittest for script available at ../image_scraper/download_image.py
      * `test_url_validator.py`: Unittest for script available at ../image_scraper/utils_url_validator.py
      * `test_utils.py`: Unittest for script available at ../image_scraper/utils.py
   
   * `cron_job.py`: Cronjob to run the python script in every 5 minute.
   * `requirements.py`: Install all the requirements to run the package.
   * `setup_environment.sh`: Make system compatible with the script, starts the cron_job and starts a server at the location where all the timestamp directories will be saved.
  
4. How to run the script without using cron_job:
   * Save a file inside `sample_data` directory.
   * Check the present working directory. It should be the root directory (i.e. if you do `ls` then result will contains [Readme.md, cron_job.py, image_scraper, requirements.txt, sample_data, setup_environment.sh, tests])
   * Run the download_image script using command: `python -m image_scraper.download_image --filepath sample_data/urls.txt
                                                --output_dir_path /Users/lokeshtodwal/Downloads`
   * If the above command runs successfully then you will see a directory at the location specified at `output_dir_path` in the above command. The directory name will be the timestamp at which the script ran. Inside timestamp directory you will see the images along with the log file (which will brief you about the script).
   * To run unittest use following commands:
      * `python -m unittest tests.test_download_image`
      * `python -m unittest tests.test_utils`
      * `python -m unittest tests.test_url_validator`\
   The above commands should run successfully.
    
    
    
#### Note:
* Right now I am considering that the text file will either contain URL with extensions like 'jpg', 'png', 'gif', 'bmp', 'jpeg', 'webp' or the URL that is extracted from Google Image search([sample image](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQVAKOMUULIBcWwo1e1Ci6sJnn1PfoKVEfXjSYUnSuGV61WWk9)). Also for URL like mentioned above does not have any basename, so I will be saving the file in the name of `images(\d).png`.  
* The image files and the log file will be saved inside a directory, where the directory name will be the timestamp at which the python script was called.