## Dialpad Downloader

This is a simple script to download links to all of your Dialpad recordings. It uses the Dialpad API to download a .csv of all the recordings links. 

## Requirements

* Python 3.6+

## Installation

1. Clone the repository

3. Create a file called `config.ini` in the same directory as the script. The file should look like this:

```
[dialpad]
token = <your token>
```

4. Run the script

## Output
The script will create a folder in the same directory as the script called `Recordings\users`.
Inside this folder all recordings will be stored in the format of `user_id_user_name_.csv`.

## Notes
* You must have a Dialpad account to use this script. You can get a token from the Dialpad API page.

* The script will only download the links to the recordings. It will not download the recordings themselves. You can use a download manager to download the files, or you can use a script like this one to download the files directly.

