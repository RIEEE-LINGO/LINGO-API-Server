# About Us
interLINGO was developed by researchers at Appalachian State University (App State). Funding for this project came from the Research Institute for Environment, Energy, and Economics at App State as well as the Science and Technologies for Phosphorus Sustainability (STEPS) Center. interLINGO provides a collaborative space for teams to surface, discuss, and resolve differences in philosophies across disciplines by using language as a boundary object. 

If you are interested in using interLINGO, please contact Dr. Mark Hills (hillsma@appstate.edu) and Dr. Kim Bourne (bournekd@appstate.edu).

Contributors to this program include:
Elle Russell
Dr. Mark Hills
Christian Hart
Dr. Kimberly Bourne
Dr. Christine Hendren


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

To start, you should create a database and add sample data. The easiest way to
do this is just to run `server.py`. By default, this will be run in debug mode.
When it starts, it looks for a `db` directory and, if it does not find one, it
creates the sample database and loads sample data automatically. Note that this
should _not_ be done in production, which is using a different kind of database
(MySQL vs SQLite). If you delete the `db` directory, the application will create
it again the next time it is run.

# Exploring the Database

If you have the sqlite tool, you can load the database and look at the contents:

```angular2html
$ sqlite3 db/lingo.db
SQLite version 3.39.3 2022-09-05 11:02:23
Enter ".help" for usage hints.
sqlite> .tables
meaning      reflection   team         team_member  user         word       
sqlite> select * from word;
1|1|co-creation of knowledge|1|2024-12-19 20:29:04.915818|2024-12-19 20:29:04.915819
2|1|Co-production|1|2024-12-19 20:29:04.919654|2024-12-19 20:29:04.919655
3|1|Convergence|1|2024-12-19 20:29:04.923630|2024-12-19 20:29:04.923631
4|1|Data|1|2024-12-19 20:29:04.925530|2024-12-19 20:29:04.925531
5|1|data twinning|1|2024-12-19 20:29:04.928799|2024-12-19 20:29:04.928800
6|1|digital twinning|1|2024-12-19 20:29:04.929823|2024-12-19 20:29:04.929825
7|1|epistemic humility|1|2024-12-19 20:29:04.930827|2024-12-19 20:29:04.930829
8|1|extension|1|2024-12-19 20:29:04.934912|2024-12-19 20:29:04.934914
9|1|farmer|1|2024-12-19 20:29:04.937254|2024-12-19 20:29:04.937258
sqlite> select * from meaning where word_id = 9;
53|9|Someone who is responsible for growing food, fiber, fuel, or other natural products consumed or used by people or animals|2024-01-03 19:37:22.280484|2024-01-03 19:37:22.280485
54|9|I tend to think of the word "farmer" to refer specifically to a group of people who are directly involved in agricultural production. I distinguish farmer from farmworker to indicate variation in labor relations, and also recognize that "farmer" can be a cultural category that is associated with rurality. Corporations (e.g. Cargill, Tyson, Perdue) are not farmers, but landowners who hire farmworkers can be farmers. I associate the term "farmer" with someone for whom agriculture is a major occupation, but in reality I know that is often not the case, many people who identify as farmers also engage in off-farm work, and many people who work on farms might not call themselves farmers. The meaning of this term also varies widely depending on geographic location.|2024-01-03 19:37:22.280485|2024-01-03 19:37:22.280486
55|9|Farmers are individuals who produce food, including vegetables, grains, and meat. Emphasis on "individual."|2024-01-03 19:37:22.280486|2024-01-03 19:37:22.280487
56|9|agricultural steward|2024-01-03 19:37:22.280487|2024-01-03 19:37:22.280487
sqlite>
```

# Starting the API Server

To start the API server, you first need to set the environment variable
used by the server to find the database. If this is not done, the system
will fall back on the SQLite debug database mentioned above.

On Windows, you would set
this using the `SET` command, while you would use the `export` command
on a Mac or Linux machine:
```
# On Windows
SET DATABASE_URL=mysql+pymysql://lingo:password@host-ip/lingo

# On Mac or Linux
export DATABASE_URL=mysql+pymysql://lingo:password@host-ip/lingo
```

For testing, you can also set the `ENABLE_SECURITY` flag to `NO` to
disable security checks, but this should not be set at all for
production environments or if you are testing with security enabled.
By default, security is enabled.

For testing, you can also set the `DEFAULT_USER_ID` flag to the ID
of the default user. This is _only_ for testing purposes where
`ENABLE_SECURITY` is also set to `NO`. Normally, the current user is
based on the security token generated as part of the authentication
process. This provides a default user for when authentication is not
done. The default is `1` in cases where security is disabled and this
is not set.

Now, to run the server, you can run the command `python server.py`. 
You should see something like the following:
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

To run in production mode, you can instead run the `run.sh` script found in
the `bin` directory. This will _NOT_ start the server in debug mode, so you
should not do this for development. Finally, note that, on Mac or Linux
machines, you can combine setting the location of the database and starting
the server as a single command:

```
$ DATABASE_URL=mysql+pymysql://lingo:password@host-ip/lingo python server.py
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

# Bundling the Server

To create a Docker image for the server, you use the `Docker build`
command (note that `0.0.2` is just a sample version number, the
actual version number should be included):
```
docker build -t lingo-api-server:0.0.2
```
If you are on a Mac with Apple silicone then you need to include
a flag to build an image that runs on Intel and AMD processors:
```
docker build --platform linux/amd64 -t lingo-api-server:0.0.2
```
If you don't do this, you may get errors when you try to create
a running container, depending on the processor used on the
server.
