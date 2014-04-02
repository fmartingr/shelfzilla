shelfzilla
==========

## Prepare environment for local development

```
# Check that everything is installed
fab doctor

# Setup NPM/Virtualenv/Database
fab setup_environment

# Executes the server
fab runserver
```

## Dependencies

- Nodejs
- Python 2.7 with virtualenv and pip
- grunt-cli installed as global resource
- bower installed as a global resource

# First install

The first time you use `fab setup_environment` django will ask for a initial superadmin user, be sure to enter **an email address as username** or the login form won't allow you to access the site. You can enter anything since this is a local environment.

