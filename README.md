# Getting Started
You will want to make sure you create a virtual environment. If you are not
sure how to do this, please ask. On a Mac, it is a command like the following:
```angular2html
python -m venv .venv
```

You will then enter the virtual environment (most IDEs will do this automatically,
so this is only needed from the command line). On a Mac, this is:
```angular2html
source .venv/bin/activate
```
while on Windows, it is:
```angular2html
.venv\Scripts\activate
```

Now, install any requirements using `pip`. This will just install the requirements
into the local directories:
```angular2html
pip install -r requirements.txt
```

# Creating the Database

To start, you should create a database and add sample data. To do this, you
should run python (while in the virtual environment) and run the script
which does this (note that, on the first line, `$` is the prompt, not part
of the command you type, similarly `>>>` is the prompt inside the Python
interpreter). Note that you need to create the `db` directory first since
Python will not do this for you:
```angular2html
$ mkdir db
$ python
Python 3.9.13 (main, Aug 25 2022, 18:29:29) 
[Clang 12.0.0 ] :: Anaconda, Inc. on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import build_database
Run build_database.create_and_load_db() to create the DB schema and load sample data
>>> build_database.create_and_load_db()
```

Note that this will _not_ be used directly in production, since this uses
SQLite and loads sample data. A script for production will be provided later.

# Exploring the Database

If you have the sqlite tool, you can load the database and look at the contents:

```angular2html
$ sqlite3 db/lingo.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> .tables
meaning      reflection   team_member  word       
project      team         user       
sqlite> select * from word;
1|co-creation of knowledge|1|2024-01-03 19:37:22.257080|2024-01-03 19:37:22.257083
2|Co-production|1|2024-01-03 19:37:22.262213|2024-01-03 19:37:22.262217
3|Convergence|1|2024-01-03 19:37:22.266115|2024-01-03 19:37:22.266117
4|Data|1|2024-01-03 19:37:22.268860|2024-01-03 19:37:22.268861
5|data twinning|1|2024-01-03 19:37:22.272429|2024-01-03 19:37:22.272430
6|digital twinning|1|2024-01-03 19:37:22.273329|2024-01-03 19:37:22.273330
7|epistemic humility|1|2024-01-03 19:37:22.274251|2024-01-03 19:37:22.274252
8|extension|1|2024-01-03 19:37:22.277284|2024-01-03 19:37:22.277285
9|farmer|1|2024-01-03 19:37:22.279305|2024-01-03 19:37:22.279306
sqlite> select * from meaning where word_id = 9;
53|9|Someone who is responsible for growing food, fiber, fuel, or other natural products consumed or used by people or animals|2024-01-03 19:37:22.280484|2024-01-03 19:37:22.280485
54|9|I tend to think of the word "farmer" to refer specifically to a group of people who are directly involved in agricultural production. I distinguish farmer from farmworker to indicate variation in labor relations, and also recognize that "farmer" can be a cultural category that is associated with rurality. Corporations (e.g. Cargill, Tyson, Perdue) are not farmers, but landowners who hire farmworkers can be farmers. I associate the term "farmer" with someone for whom agriculture is a major occupation, but in reality I know that is often not the case, many people who identify as farmers also engage in off-farm work, and many people who work on farms might not call themselves farmers. The meaning of this term also varies widely depending on geographic location.|2024-01-03 19:37:22.280485|2024-01-03 19:37:22.280486
55|9|Farmers are individuals who produce food, including vegetables, grains, and meat. Emphasis on "individual."|2024-01-03 19:37:22.280486|2024-01-03 19:37:22.280487
56|9|agricultural steward|2024-01-03 19:37:22.280487|2024-01-03 19:37:22.280487
sqlite>
```

# Starting the API Server

To start the API server, run the command `python server.py`. You should see something like
the following:
```angular2html
$ python server.py
 * Serving Flask app 'config'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.1.147:8000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 123-456-789
```

# Accessing the API

There are several ways to access the API. We are still adding JWT support for security,
so the API is open for now. The easiest way to access the API is using a browser if
you are just retrieving information. For instance, if you navigate 
to [http://localhost:8000/api/words](http://localhost:8000/api/words),
you will see the list of words, in JSON form. You can also navigate
to [http://localhost:8000/api/words/1](http://localhost:8000/api/words/1) to
get just the individual word with ID of 1.

A second option is to use the CURL command. This is more flexible, since you can
make other forms of requests. The equivalent commands using CURL for the above
would be `curl http://localhost:8000/api/words` and `curl http://localhost:8000/api/words/1`.

A third option is to use a tool like [Postman](https://www.postman.com/). Postman
includes a web interface as well as a tool that you can install and use locally.

A final option is to use the built-in API explorer which will _not_ be enabled in
production, but is available for development. You can find this
at [http://localhost:8000/api/ui/](http://localhost:8000/api/ui/) when the API server
is running. This will let you see the existing API and try calling it directly.
For instance, if you go to the above URL and navigate to the GET option under Words,
you can click the "Try it out" button to make an API call. Then, click Execute. You will
see the JSON result on the page. We are in the process of improving this since it does
not yet handle parameters well.
