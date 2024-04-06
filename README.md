# MarketSquare

To run the project locally:

Install all dependencies

*`poetry install`*

Create a new instance of the database, initialize, run and apply database migrations

*`poetry run quart --app marketsquare db init`*

*`poetry run quart --app marketsquare db migrate`*

*`poetry run quart --app marketsquare db upgrade`*

Then seed the database with the hard-coded products (i.e. put data into the database)

*`poetry run seed`*

Then start the application by running:

*`poetry run start`*

Open browser to view on http://localhost:4332

