# Recruiter Tools
A set of tools to visualize information from Greenhouse.

Currently supports:
1. Showing the interview counts of selected interviewers within a hardcoded time span

## Installing
1. Clone this repository
1. Create a virtualenv
1. Install the necessary packages
    ```
    pip install -r requirements.txt
    ```
1. Set up your config secrets:
    1. `cp example_config_file.cfg config_file.cfg`
    1. Edit this config file to add a random `SECRET_KEY`, `GREENHOUSE_KEY` [(details)](https://support.greenhouse.io/hc/en-us/articles/115000521723-How-do-I-manage-Harvest-API-key-permissions-), and `SQLALCHEMY_DATABASE_URI` (the current one is ok for development).
1. run `flask run`
1. Navigate to `localhost:5000/admin/` and add the names of which interviewers you want to track data for. 
1. Open `localhost:5000` to see the results (this can take a moment while it fetched data from Greenhouse's API)
