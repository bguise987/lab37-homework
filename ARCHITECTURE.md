# Tech stack decisions

## Frontend
Vue 3
- This is already used at Lab37, and given my (lack of) depth in JavaScript frameworks, they're all more or less equal to me for something like this
- Served from a local web server

## Backend
Python and FastAPI
- Python is the programming language that I'm currently most comfortable with
- Python and FastAPI should scale appropriately for the performance metrics given in the prompt
- Served from a local web server

## Database
SQLite
- Want to utilize a simple, local database to make development easier, and also easier for the homework reviewers to run the project on their machines
- Run and called locally from the FastAPI layer
