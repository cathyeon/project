We used html because it is the easiest language to use for pages.
The combination of python and flask allows us to establish a server that takes in all of the different templates for the project.
We chose python because it is easily integrated with flask and also because it is one of the simpler language in terms of syntax.
We also use CSS to add style and flair to the html pages.

We chose to make the html sites look simple yet aimed to maintain consistency, which we achieved through a standardized style code and similar implementations across the board.
We organized the code intuitively based on the progression that a user would go through (based on the route).
We also organized the errors to be at the end of each route as well as at the end of the general application.py document.

One of the major problems that we ran into was in implementing ML.  We initially wanted to use a recommendation system that uses machine learning to predict a person's music taste.
All of the code that we attempted is on the  ML trial.py file.
The first issue we ran into was that of downloading the database provided in the Medium article.  IDE did not allow for the download and merging of two large files, so I did this locally in terminal on my Macbook.
I then changed it to a pkl file (which did not work) and then a csv file, which ended up working.  However, when trying to download a package (sklearn) for the ML itself, IDE did not allow us to do so, which would make the process very difficult.

Our primary goal with this project was to focus on the user.  That is, we did not upload a preexisting database because if this app is used by a community of people, we would ideally pull suggestions for songs from the inputs of other users.
This would provide for more accountability on the part of users because just as other people's inputs inform their recommendations, their inputs inform other people's recommendations.