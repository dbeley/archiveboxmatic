# ArchiveBoxMatic

**Work in progress. Don't expect every features to work.**

ArchiveBoxMatic lets you configure ArchiveBox archives in a yaml file.

## Installation

```
git clone https://github.com/beley/archiveboxmatic
cd archiveboxmatic
python install setup.py
```

You can also use pipenv to install your virtual environment

```
git clone https://github.com/beley/archiveboxmatic
cd archiveboxmatic
pipenv install '-e .'
```

### ArchiveBox installation

#### Classic install

```
pip install archivebox
mkdir data
cd data
archivebox init
archivebox manage createsuperuser
cd ..
```

Use `python` method in your config file.

#### Docker install

For an archivebox data folder named data and placed in the repo folder, create a file named `.env` containing this content
```
DATA_FOLDER=~/data_folder
```

You can then initiate an archivebox archive with the following commands

```
docker-compose pull archivebox
docker-compose run archivebox init
docker-compose run archivebox manage createsuperuser
docker-compose up -d
```

Use `docker-compose` method in your config file.

## Configuration

See `config.example.yaml` for a default config file. By default, archiveboxmatic search for a config.yaml file in the directory where it has been launched.

```
archivebox:
    # method: docker-compose, python.
    method: docker-compose
    # path containing archivebox data. When using docker-compose method, must be the path of the docker-compose file (the path will be the one in the .env file).
    path: ./
    # environment variables to be used when running archivebox (see archivebox docs).
    environment:
        - USE_COLOR=True
        - SHOW_PROGRESS=False
        - TIMEOUT=120
        - MEDIA_TIMEOUT=300
configuration:
    timezone: Europe/Paris
archives:
    # - name: name of the archive
    #   depth: depth of archive (0 or 1).
    #   sources: files containing urls.
    #       text_files: files containing one urls by line.
    #       shaarli: html files exported by shaarli.
    #       reddit_saved: files containing one urls by line (same as text_files).
    #       firefox_bookmarks: html files containing firefox bookmarks.
    #       firefox_history: json files exported with the export_browser_history.sh script in archivebox repository.
    #   schedule: optional. Possible values are daily, weekly, monthly or yearly. See README.md for more informations.
    - name: example
      depth: 0
      sources:
          text_files:
              - text1.txt
              - text2.txt
          shaarli:
              - shaarli.html
          reddit_saved:
              - reddit_saved.html
          firefox_bookmarks:
              - firefox_bookmarks.html
          firefox_history:
              - firefox_history.html
    - name: daily
      depth: 0
      sources:
          text_files:
              - URLs/daily.txt
      schedule: daily
    - name: weekly
      depth: 0
      sources:
          text_files:
              - URLs/weekly.txt
      schedule: weekly
    - name: monthly
      depth: 0
      sources:
          text_files:
              - URLs/monthly.txt
      schedule: monthly
    - name: yearly
      depth: 0
      sources:
          text_files:
              - URLs/yearly.txt
      schedule: yearly
    - name: shaarli
      depth: 0
      sources:
          shaarli_files:
              - bookmarks_shaarli.html
    - name: reddit-saved
      depth: 0
      sources:
          reddit_saved:
              - reddit_saved_user1.txt
              - reddit_saved_user2.txt
    - name: firefox
      depth: 0
      sources:
          firefox_bookmarks:
              - bookmarks_firefox.html
          firefox_history:
                - history_firefox.html
```

## Usage

```
usage: archiveboxmatic [-h] [--debug] [-c CONFIG_FILE] [-s SCHEDULE]

ArchiveBoxMatic: configure ArchiveBox with the simplicity of a yaml file.

optional arguments:
  -h, --help            show this help message and exit
  --debug               Display debugging information.
  -c CONFIG_FILE, --config_file CONFIG_FILE
                        Config file (default: ./config.yaml).
  -s SCHEDULE, --schedule SCHEDULE
                        Only run scheduled tasks for a specific timeframe
                        (Choices: daily, weekly, monthly, yearly, all.
                        Default: all).
```

## Schedule

Periodic runs can be set up with the help of systemd timers.

You might have to change the contents of systemd services in the systemd-service folder (specially the WorkingDirectory option and the ExecStart command, if you used pipenv for installing for example).

```
cp systemd-service/* ~/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable --now archiveboxmatic_daily.timer
systemctl --user enable --now archiveboxmatic_weekly.timer
systemctl --user enable --now archiveboxmatic_monthly.timer
systemctl --user enable --now archiveboxmatic_yearly.timer
systemctl --user list-timers --all
```

```
systemctl --user start archiveboxmatic_all.service
```

By default the schedule are the following (you can change it in the OnCalendar option in the systemd timer files).

- daily : every day at 12am
- weekly : every monday at 10am
- monthly : every first day of the month at 5am
- yearly : every first day of the year at 1am
