# Run this script using command `source setup_environment.sh`

# Export this if you are getting a message where you need to pick from couple of UTF-8 locales (In Mac I am getting this message)
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

# Install all the requirements to run the package
pip install -r requirements.txt

# Uncomment below command when you want to run the cron_job.
# The job will run after every 5 minutes (as stated in the problem statement)
python cron_job.py --username lokeshtodwal --filepath sample_data/urls.txt --output_dir_path /Users/lokeshtodwal/Downloads

# Going to the directory where all the timestamp directories will be present.
cd /Users/lokeshtodwal/Downloads

# Starting the web server with python.
python -m http.server 8081
