# General approach
I started by reading through the prompt and sending over some questions to Cody. From there I spent some time writing out my initial thoughts on architecture and design, because what's the fun in shoving the prompt as-is into Claude?

I then took these thoughts and moved them into different markdown files for Claude (and the homework reviewers) to parse. Most architectural decisions are laid out in the relevant markdown file, but I will provide the occasional high level note in this README.

Within the DATABASE.md it is noted that SQLite was chosen for simplicity of local development and for ease to the reviewers. In production I would look to PostgreSQL, as it's generally a great starting point for systems such as this.

For this homework I also chose Python for the backend as I am personally more familiar with it at this time. Were I to stand up something at Lab37 though, I would look to Go first as that's the language the team seems to be standardizing around at this time.

# How to run the project

# Next steps / future thoughts
Given the desire to keep time spent under 4 hours, shortcuts were certainly taken. Below are some of the things I would look to implement in the future:
- Real authentication, of course. Please don't tell all of my cybersecurity friends that I did an MVP with plaintext passwords :)
- Support for images in recipes
- Automatic updating of yield information based on ingredient changes
- Don't *actually* delete any recipes within the database - this would make it easy for users to recover accidentally deleted content, and preserves data for company research and usage
- Better user management - there should be owners, supervisors, team members, etc. with appropriate permissions at each level for different actions such as deleting a recipe
- Better company management - users should be able to belong to multiple companies, and it should be considered that perhaps a company would have multiple locations with disperate menus

# Claude Code Prompts Used
-