## Attendance Tracker for Stuy CS Dojo

The Attendance Tracker is a Python Flask application to upload, store, and pull
attendance logs from Google Spreadsheets to and from either CSV files or
one-line texts lines.

This Flask Application is meant to be used in line with the CS Dojo Scanner
application, but it can also be called manually.

### Installing Dependencies

The Attendance Tracker is built on Python 2.7.6 and requires Flask and the
Google API.

```
$ sudo apt-get install python-dev libssl-dev libffi-dev
$ pip install --upgrade flask google-api-python-client gspread PyOpenSSL
```

### For Development

 - https://github.com/burnash/gspread
 - http://gspread.readthedocs.org/en/latest/oauth2.html

If you are creating your own user for GSpread via the Google Developer Console, be sure to *SHARE* the spreadsheet with
your Service account, as per: https://github.com/burnash/gspread/issues/226

### Running

To run the application, you must first create admin credentials for the app. Do this via `console.py`:

```
$ python console.py
>> add username password
>> list
[A LIST WILL APPEAR HERE]
>> exit
```

Next, you must obtain a JSON file for a Google API Service account. See the links provided in the 'For Development' section
to learn how. Save the JSON file in the *SAME* folder as `app.py` (i.e. the project root folder) as `gcreds.json`. The name *MUST*
be `gcreds.json`.

To run the application, simply start the server using:

```
$ python app.py
```

### Contacting the Server via CURL

You can contact the server via a web browser, `wget` request, or `curl` request as shown below:

```
$ curl -s -X GET "${SERVER_ADDR}?username=${ADMIN_NAME}&pword=${ADMIN_PWORD}&osis=${barcode}&date=${DATE}"
```

The 'osis' is a New York City school ID. For users not implementing this app for non-NYC schools, you can browse through the source
to change the variable name to something else, such as `data`.

Possible responses:

 - `OK` - Server executed successfuly
 - `no_creds` - `gcreds.json` was not found or was not loaded successfully
 - `bad_login` - The `${ADMIN_NAME}` and `${ADMIN_PWORD}` variables were not recognized. Add them via `console.py`
 - `no_osis` - No data was sent to the server. Nothing to execute.

### Troubleshooting

I ran into an issue where a valid `gcreds.json` was not being authorized. It turned out the issue is
that the machine running the server must maintain proper system time. On Linux systems, you can update
the system time via:

```
$ sudo ntpdate time.nist.gov
```

