# data/scraper

Generates JSON data in [data/](../) to populate a database.

## Setup
1. Create virtualenv (not covered)
2. Install requirements
3. Generate `iata.json` file.

```bash
$ pip3 install -r requirements.txt
$ ./generate.py
# Check iata.json exists
$ file ../iata.json
```

## Files
We're generating two files at the top of the [data/](../) directory.
1. [iata.json](../iata.json) - This contains the majority of the data, all the IATA airport codes.
2. [metropolitan.json](../metropolitan.json) - The contains a subset of IATA codes like CHI or LON. Metropolitan area codes that don't necessarily have an airport associated with them
