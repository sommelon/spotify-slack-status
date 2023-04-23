# Display the current song as yout status on Slack without adding an app to your workspace

# WARNING
### USE AT YOUR OWN RISK. IF THE WRONG PERSON GETS ACCESS TO YOUR COMPUTER WHILE THIS SCRIPT IS RUNNING, THEY COULD ALSO GET ACCESS YOUR SLACK (AND SPOTIFY) ACCOUNT.


## Usage
1. Run `python3 main.py`
3. Log in to Spotify (a window in your default browser should automatically open)
4. Enter the Slack credentials (see [Get Slack credentials](#get-slack-credentials))
5. Listen to songs

Conditions for updating status:
- Don't update status if the current status emoji does not match the one that's configured.
- Clear status if there is no song playing and the status emoji matches the one that's configured'.

## Setup
1. Run `pip install -r requirements.txt`
3. Create a Spotify app at https://developer.spotify.com/dashboard
4. Update the variables in `.env` (look below for more info)

### Get Slack credentials
1. Log in to Slack
2. Press F12
3. Go to the `Network` tab
4. Refresh the page
5. Find `users.interactions.list?` (or some other entry which contains the following info)

#### Get the workspace domain
1. Click on the `Headers` tab
2. Under the `General` section, find `Request URL` and copy the subdomain of the URL
(eg. from this: `https://test-qpv0000.slack.com/api/`, copy the `test-qpv0000` part.)


#### Get the token
1. Click on the `Payload` tab (if not already active)
2. Copy the value of the `token` key (**without** quotes)

#### Get the d-cookie
1. Click on the `Headers` tab
2. Under `Request Headers` section, find `cookie:` and copy the value of the `d` key
(text between the `=` and `;` symbols)



## Persist credentials (WARNING - INSECURE)
You don't have to login to Spotify and enter the token and d-cookie on each start.

If you want to persist the Spotify credentials, use the `--spotify-use-file-cache` switch.

If you want to persist the Slack credentials, you can put the values into `.env` via `TOKEN` and `D_COOKIE` variables.
This is not recommended, as anyone who has access to your unencrypted disk can access these values.
