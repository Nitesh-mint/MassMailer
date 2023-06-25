# Mass Mailer
This project built on <strong>DJANGO</strong>  aims to send emails to multiple user at once to save time. This app can send mails to large amounts of emails from JSON file.
# Features 
<li>Send Mails to any email from any email.</li>
<li>Send mails to multiple emails at the same time.</li>
<li>Send mail using JSON file.</li>

# Setup
<li><b>Fork</b> this repo or download <b>zip</b>, open termial inside the project folder and follow:</li>

```
python -m venv .venv
source .venv/bin/activate
```
<li>Install requirements:</li>

`
python -m pip install -r requirements.txt 
`
<li>Go to the <a href="https://app.brevo.com/settings/keys/api">Sendinblue</a> and copy the API key.</li>
<li>Inside project folder go to:</li> 

` massmailer/settings.py`

<li>In line number 138 replace with your API</li>

```

EMAIL_BACKEND = 'anymail.backends.sendinblue.EmailBackend'
ANYMAIL = {
    "SENDINBLUE_API_KEY": "replace-with-your-api",
    "SEND_DEFAULTS": {
        "tags": ["app"]
    },
    "DEBUG_API_REQUESTS": DEBUG,
}

```
<li>Run the server</li>

`python manage.py runserver`


