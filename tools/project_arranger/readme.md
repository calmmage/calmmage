- project 3: project organization
  role: Automatic scripts, configured with yaml rules.

# Idea
1) Main idea: put the projects into the right places

2) components
   component 1: pulling the repos from github and putting them into the right places
   component 2: analyzer tool
   a thing for
- baseline version: see projects with no code and filter them out
  - group 1: just empty
  - group 2: empty, but might be worth revisiting, keep close.
    component 3: daily / monthly job?

# Instructions
Todo: change this to typer application

When done, run like that:
```bash
typer cli.py run sort
```

Main command:
- sort projects

Secondary commands (research):
- View
    - dump current project groups
    - dump generated project groups
- Analyze (detect projects worth attention)

# Main ideas:
- clone all repos
- sort all local repos with config
- remove banned repos

# More ideas:

- All the auto-jobs I wanted
    - auto-commit all repos
    - daily job?
    - weekly/monthly job? (seasonal dir refresh)
