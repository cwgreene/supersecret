import json
import os

class FileSystemProvider(object):
    def __init__(self, path=os.path.expanduser("~/.secrets"), creds=None):
        if creds == None:
            creds = credentials
        self.path = path
        self.creds = creds

    def scope_path(self, scope):
        return "%s/%s" % (self.path, scope)

    def getSecrets(self, scope):
        scope_path = self.scope_path(scope)
        if not os.path.exists(scope_path):
            with open(scope_path, "w") as initial:
                initial.write("{}")
        with open(scope_path) as secretFile:
            return json.loads(secretFile.read())

    def removeAllSecrets(self, scope):
        if os.path.exists(self.scope_path(scope)):
            print "Removing"
            os.remove(self.scope_path(scope))

    def getSecret(self, scope, key):
        return self.getSecrets(scope)[key]

    def storeSecret(self, scope, key, value):
        secrets = self.getSecrets(scope)
        secrets[key] = value
        # TODO: This probably isn't safe, should make separate file
        # and then swap on completion.
        with open(self.scope_path(scope), "w") as secret_file:
            json.dump(secrets, secret_file)

credentials = None
provider = FileSystemProvider()

def getSecret(scope, key):
    return provider.get(scope, key)

def removeAllSecrets(scope):
    return provider.removeAllSecrets(scope)


def setCredentials(creds):
    creds = creds
