# Secrets.

A simple library to make it easy to store credentials, retrieve credentials,
and make it so that you don't accidentally commit said credentials to your public
git repo.

```python
# from ipython
import secrets

secrets.storeSecret("website.com", "username", "myname")
secrets.storeSecret("website.com", "password", "mypassword")

# From your application
import secrets

connect_to_website(username=secrets.getSecret("website.com", "username"),
                   password=secrets.getSecret("website.com", "password"))
```

The secrets are stored, unencrypted, in `~/.secrets`.

## Scopes The first paramter in the above examples `"website.com"`
is called a scope. Each scope will correspond to a separate file in
`~/.secrets`.

## Providers

`secrets` allows you to use a different directory than `~/.secrets`,
by using

```python
import secrets

secrets.provider = secrets.FileSystemProvider("/path/to/other/directory")
```

It is *strongly* recommended that you do not put secrets in your repo
directory, as this would allow for accidental commits of the secrets
(which is the main thing this library is attempting to avoid). It is
probably also recommended not to have multiple user access to this
directory.

Theoretically, you can create a new provider class; checkout `secrets.py`
for the required functions to be implemented. I'll probably make this
interface explicit sometime with inheritance.
