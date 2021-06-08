to just run the scraper: python test/scraper_tests.py
to run the flask frontend: python app.py
- you may need to define the flask app by using this command in the main park_scraper directory: set FLASK_APP=app.py
- see https://flask.palletsprojects.com/en/1.1.x/quickstart/ for more info

to develop on the react piece:
install node.js
install yarn
run 'yarn install' to install all the packages in packages.json
do your dev
run "npx webpack" at the command line
refresh the flask page

cron job setup:
0,30 0-6,12-23 * * * /apps/venv/bin/python /apps/campfinder/scraper_cron_wrapper.py >> /apps/campfinder/cron.log 2>&1
