"""
Cronjob to run the python script in every 5 minute.
Command to run this script:
        python cron_job.py --output_dir_path /Users/lokeshtodwal/Downloads
        OR
        python cron_job.py --filepath sample_data/urls.txt --output_dir_path /Users/lokeshtodwal/Downloads
        OR
        python cron_job.py --username lokeshtodwal --filepath sample_data/urls.txt --output_dir_path /Users/lokeshtodwal/Downloads


Python command that runs using this script
python /Users/lokeshtodwal/PycharmProjects/jd/image_scraper/download_image.py
               --filepath /Users/lokeshtodwal/PycharmProjects/jd/sample_data/urls.txt
               --output_dir_path /Users/lokeshtodwal/Downloads

"""

import getpass
import os

import click
from crontab import CronTab


def remove_all_previous_jobs(cron):
    """
    Removes all the previous cron jobs which are running
    :param cron: Cron object
    :return: Removes all cron jobs
    """
    cron.remove_all()


def create_new_cron_job(cron, python_file_path, text_file_path, output_dir_path):
    """
    Creates a new cron job
    :param cron: Cron object
    :param python_file_path: Location at which python file is located
    :param text_file_path: Location at which text file is located
    :param output_dir_path: Location at which image files need to be stored
    :return: A new job
    """
    remove_all_previous_jobs(cron)
    py_command = "/usr/local/bin/python3 {} --filepath {} --output_dir_path {}".format(python_file_path,
                                                                                       text_file_path,
                                                                                       output_dir_path)
    print(py_command)
    job = cron.new(command=py_command)
    job.minute.every(5)

    cron.write()

    return job


@click.command()
@click.option("--username", default=getpass.getuser(), help="Enter name of the user")
@click.option("--filepath", default='sample_data/urls.txt', help="Path of the file")
@click.option("--output_dir_path", default='.', help="Path at which all the images will be saved")
def start_job(username, filepath, output_dir_path):

    # Creating crontab object
    cron = CronTab(user=username)

    # Removing all previous jobs. Comment this if you do not want to remove previous job.
    # remove_all_previous_jobs(cron)

    # Path of this file
    this_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    # Path of python file
    python_file_path = os.path.join(this_file_path, 'image_scraper/download_image.py')
    # Path of text file
    text_file_path = os.path.join(this_file_path, filepath)

    # Check if path of python file exists
    if os.path.exists(python_file_path):
        # Creating new job
        job = create_new_cron_job(cron, python_file_path, text_file_path, output_dir_path)

        # Check if job is enabled
        if job.is_enabled():
            print('Job is running')
    else:
        print('Path of python file does not exist')


if __name__ == '__main__':
    start_job()
