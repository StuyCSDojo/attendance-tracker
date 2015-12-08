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
$ pip install --upgrade flask google-api-python-client gspread PyOpenSSL
```

### For Development

 - https://github.com/burnash/gspread
 - http://gspread.readthedocs.org/en/latest/oauth2.html

If you are creating your own user for GSpread via the Google Developer Console, be sure to *SHARE* the spreadsheet with
your Service account, as per: https://github.com/burnash/gspread/issues/226

### Running

