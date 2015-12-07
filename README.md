# Secrets.

A simple library to make it easy to store credentials, retrieve credentials,
and make it so that you don't accidentally commit said credentials to your public
git repo.

    # from ipython
    import secrets

    secrets.storeSecret("website.com", "username", "myname")
    secrets.storeSecret("website.com", "password", "mypassword")

    # From your application
    import secrets

    connect_to_website(username=secrets.getSecret("website.com", "username"),
                       password=scretes.getSecret("website.com", "password"))

The secrets are stored, unencrypted, in ~/.secrets
