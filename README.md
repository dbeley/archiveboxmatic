# ArchiveBoxMatic

**Work in progress. Don't expect every features to work.**

ArchiveBoxMatic lets you configure ArchiveBox archives in a yaml file.

## Installation

```
git clone https://github.com/dbeley/archiveboxmatic
cd archiveboxmatic
python install setup.py
```

You can also use pipenv to install your virtual environment

```
git clone https://github.com/dbeley/archiveboxmatic
cd archiveboxmatic
pipenv install '-e .'
```

### ArchiveBox installation

#### Docker install (recommended)

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

#### Python install

```
pip install archivebox
mkdir data
cd data
archivebox init
archivebox manage createsuperuser
cd ..
```

Use `python` method in your config file.

## Configuration

See [`config.example.yaml`](https://github.com/dbeley/archiveboxmatic/blob/master/config.example.yaml) for a default config file. By default, archiveboxmatic will search for a config.yaml file in the directory from where it has been launched.

## Usage

```
usage: archiveboxmatic [-h] [--debug] [-c CONFIG_FILE] [-s SCHEDULE]
                       [--dry-run]

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
  --dry-run             Run the script without starting the archive process.
                        Can be used to validate the config file.
```

## Schedule

You can automatically run archiveboxmatic with the provided systemd service file.

You will have to change the WorkingDirectory option in the systemd file to the directory containing archiveboxmatic.

```
cp systemd-service/* ~/.config/systemd/user
systemctl --user daemon-reload
systemctl --user enable --now archiveboxmatic
systemctl --user status archiveboxmatic
```
