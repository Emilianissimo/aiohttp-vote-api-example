# AioHttp Fullstack, Api and Parser Example

Getting started
-
Before start, please, install PostgreSQL:

Ubuntu 20.04 LTS Focal Fossa (focal):

```bash
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    sudo -u postgres psql # enter to db
```
Change password, by default I'm using 'postgres':
```sql
    ALTER USER postgres PASSWORD 'postgres';
```
It should show you <b>ALTER ROLE</b>. If that so, everything is done.

Install dependencies:

```bash
    pip3 install -r requirements.txt
```

Use configuration/init_db.py file to create tables and migrate fake data:

```bash
    python3 init_db.py
```

Run app:

```bash
    python3 main.py
```

Project map
-
- app
- - api # logic
- - - api.py # api (json) controller
- - - parser.py
- - - views.py # views (templates) controller
- - models
- - routes
- templates # for html code
- configuration
- - settings.py # configuration
- init_db.py # migrations
- main.py
