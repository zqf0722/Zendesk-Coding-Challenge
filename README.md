# Zendesk-Coding-Challenge

## ----IMPORTANT----
### Unzip the `env.rar` file which I attached in the email and get `.env` file
### Put the `.env` file in the top-level directory before running the application. It has all the parameters and authentication needed to request tickets from API and run the application.
### Then type `pip install -r requirements.txt` to install all the python packages needed for the application.

### After putting the `.env` in the top-level directory and installing the needed packages.
### Type `python test.py` to run the unittest.
### Type `flask run` to start the web viewer on your localhost. Use the url showed on your terminal to access the web viewer.
## ----Personalize----
You can change the environment argument in `.env` to personalize the application.

For instance: change `SUB_DOMAIN, EMAIL_ADDRESS, API_TOKEN` to request for the tickets of your own account or change `TICKETS_PER_PAGE` to set up how many tickets are showing in one page.

## If you DO NOT want to use `.env`, please make sure that there is NO `.env` in the top-level directory. Then manually input the environment variable, they are as followed:
`EMAIL_ADDRESS`: `{email_address}` of your Zendesk account if you are using basic authentication to request for tickets OR the `{email_address}/token` if you are using API token to request for tickets

`API_TOKEN`: `{password}`  of your Zendesk account if you are using basic authentication to request for tickets OR the `{apitoken}` if you are using API token to request for tickets

`SUB_DOMAIN`: `https://{subdomain}.zendesk.com/` is the url of your Zendesk account

`TICKETS_PER_PAGE`: `{number of tickets per page}` number of tickets showing in one page, default value is 25, maximum value is 100

### The default authentication method is using API token to request for tickets. If you want to use your own account, change **only** the email address and **keep** the `/token` suffix in `EMAIL_ADDRESS`, then change the `API_TOKEN` to your own token. If you want to use basic authentication. Please change the `EMAIL_ADDRESS` to your email address **without** the `/token` suffix and change the `API_TOKEN` to the password of your account.
## Just to remind you again, please unzip `env.rar` which I attached in the email when submitting the challenge and put `.env` under the top-level directory (which is the same level as this README file) of the project.
## Thank you!
