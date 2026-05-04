# General approach
I started by reading through the prompt and sending over some questions to Cody. From there I spent some time writing out my initial thoughts on architecture and design, because what's the fun in shoving the prompt as-is into Claude?

I then took these thoughts and moved them into different markdown files for Claude (and the homework reviewers) to parse. Most architectural decisions are laid out in the relevant markdown file, but I will provide the occasional high level note in this README.

Within the DATABASE.md it is noted that SQLite was chosen for simplicity of local development and for ease to the reviewers. In production I would look to PostgreSQL, as it's generally a great starting point for systems such as this.

For this homework I also chose Python for the backend as I am personally more familiar with it at this time. Were I to stand up something at Lab37 though, I would look to Go first as that's the language the team seems to be standardizing around at this time (when standing up a new project or component I always consider both the technical requirements and current team strengths).

# How to run the project

**Backend** (requires Python 3.11+ with a *virtual environment*):
```bash
python -m venv venv
source venv/bin/activate
cd backend
pip install -r requirements.txt
python seed.py        # one-time: creates recipes.db with sample data
uvicorn main:app --reload --port 8000
```

Interactive API docs available at http://localhost:8000/docs once running.

**Frontend:**
```bash
cd frontend
npm install
npm run dev           # runs on http://localhost:5173
```

**Seed credentials:**
| Username | Password  | Access |
|----------|-----------|--------|
| alice    | password1 | Acme Bakery |
| bob      | password2 | Globex Foods |
| carol    | password3 | Acme Bakery + Globex Foods |

# Testing
Stress test backend:
- python3 tests/integration/stress_test.py (backend must be running)
Stress test  →  http://localhost:8000
Duration per level: 5s  |  Concurrency levels: [1, 2, 5, 10, 20, 50]

Logging in... OK

 Concurrency    Requests    Errors         RPS
------------------------------------------------
           1        4094         0       818.7
           2        5259         0      1051.4
           5        7060         0      1411.5
          10        6945         0      1387.9
          20        6588         0      1315.3
          50        5606      1635      1114.2

================================================
Peak throughput: 1411.5 req/s  (concurrency=5)

I believe given the spec of "5,000-10,000 requests per day", which translates to about 0.1157 requests/second that this performance should be sufficient.

Ensure users can only access recipes from companies they are a part of:
```bash
pytest tests/backend/test_company_isolation.py -v
```

# Next steps / future thoughts
Given the desire to keep time spent under 4 hours, shortcuts were certainly taken. Below are some of the things I would look to implement in the future:
- Real authentication, of course. Please don't tell all of my cybersecurity friends that I did an MVP with plaintext passwords :)
- Support for images in recipes
- Automatic updating of yield information based on ingredient changes
- Don't *actually* delete any recipes within the database - this would make it easy for users to recover accidentally deleted content, and preserves data for company research and usage
- Better user management - there should be owners, supervisors, team members, etc. with appropriate permissions at each level for different actions such as deleting a recipe
- Better company management - users can belong to multiple companies in this, but it's a rudimentary setup. It should also be considered that perhaps a company would have multiple locations with disperate menus

# Claude Code Prompts Used
- [Plan] You have parsed the markdown files for different architecture decisions for the recipe management system that I am implementing. Please take me through next
  steps to setup the initial implementation of this system.
- I completed the Python dependency installation. Please proceed with scaffolding the frontend.
-  Let's make a couple minor tweaks here. Upon login, let's show the company name that the user belongs to. Given that we support a user in multiple companies,
  let's show that as a list and let them select between them.
- Let's make another tweak - the frontend should also display the username. Let's try the upperr right, close to the sign out button.
- After those changes I cannot login to the system. It's saying, "Invalid username or password."
- Please adjust the css on the DashboardView page to place the username directly underneath the "Sign out" button, like how company name is under "Recipes"
    - Note: I hated the way this looked, so I discarded the change and edited the file myself.
- I just created a high level tests directory and subdirectories for frontend, backend, and integration. Let's build an integration test which stress tests the
  backend and outputs the maximum requests per second that it can handle. This test should be easy to run locally.
- Let's add a backend test to ensure that a user cannot retrieve or submit a recipe for a company that they do not belong to.
