# Craiglist Quick Search

I've got a lot of Craigslist searches, and I can save time by having this Python script get me the latest results.

### Installation

Requires Python >= 3.7.0

    pip install -r requirements.txt
    
### Configuration

You'll need the following environment variables set:

    "smtp_server": "smtp.domain.com"
    "smtp_port": 25
    "smtp_username": "user@domain.com"
    "smtp_password": "password123"
    "email_from": "user@domain.com"
    "email_to": "your@email.com"
    
### Run the script

    python craigslist.py > results.html
    
That will create an HTML file `results.html` allowing you to click the individual search results.

### Deployment on Heroku

Create a new app on Heroku (free dynos), and connect the repo; enable automated deployments when changes are detected.

Next, install `Heroku Scheduler`. Heroku should detect `Procfile`, and you can configure `Heroku Scheduler` to run that command.

Finally, add the necessary environment variables (see above).

The result will be an email sent once per day containing your Craigslist search results!