Our project is essentially a recommendation algorithm that utilizes python.
In application.py, which is our main document, we imported SQL functions from the cs50 database to make tables (with the song, artist, and genre) as well as flask functions from the flask database to run the website.
We also import os as well as other functions which will be explained later.  Finally, we import apology and login_required from helpers, which is another python file that we wrote.
We imported warnings as well to show warnings when something goes wrong with the html sites.

Using flask and python, we used the function @app.route to route the user to different pages based on the command the user puts in.
First, we check that the templates are loaded.  Then we input the headers and define this as reponse.
We control the cache and make sure the request for the page is not expired.  We then run a session of the app.
Without any input from the user (notated by /), the homepage (after registering and logging in) displays the list of songs.  We then render a template of this list of songs

For the "register" route, if the button is not pressed at this stage, then there is a default screen that prompts the user to login with their username and password.  If the user does not have an account already, they can register.
To do so, the user presses the register button, which renders the template for register.html.
One more caveat is that if the username or password does not exist or do not match up when still on the login page, we return 0 which exits.
When registering, the user's usename and password goes into a hash table.  If we cannot insert the username (which is the result of someone else having the same user name), then we return an apology saying the username already exists.
Once the user is registered, they are redirected to the homepage in a logged-in state.

The next route is input.  This allows for song input.  We first request and render the template and then ask the user to input title, artist, tags, and rating.
These values are then put into the initial database so that they can later be displayed when requested.

For the login route, we prompt the user for their username and password and return an apology if there is no value provided in those boxes.
If the length of the string called rows (on username) is not equal to 1, we consider this an invalid username and/or password.
We also redirect back to the original page (/ once again) once the user is logged in.

The logout route clears the session with session.clear and redirects to a logged out version of the original page.

The recommend route is the heart of this project.  For songs, we db.execute from the list of songs and produce a list of songs that may be recommended.  The same goes for tags and personaltags.
After that, we return the render_template of recommend.html which gives the list of recommended songs.

The last route is browse.  This renders a template for browse.html which produces a list of songs that were inputted by users.

The errorhandler function provides an internal server error if there is an issue with the html site.


helpers.py also uses flask and decorates routes to require login.  The decorated function sets up a session and redirects to the login page in case the user_id is "None" or invalid.
It also provides an escape route in case of error and spits out an apology.
