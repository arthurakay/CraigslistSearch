# Craiglist Quick Search

I've got a lot of Craigslist searches, and I can save time by having this Python script get me the latest results.

### Installation

Requires Python >= 3.7.0

    pip install -r requirements.txt
    
### Configuration

Create a file at the project root named `creds.json`, and include the following:

    {
        "smtp_server": "smtp.domain.com",
        "smtp_port": 25,
        "smtp_username": "user@domain.com",
        "smtp_password": "password123",
    
        "email_from": "user@domain.com",
        "email_to": "your@email.com"
    }
    
### Run the script

    python craigslist.py
    
That will create an HTML file `results.html` allowing you to click the individual search results.