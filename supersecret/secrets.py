import json
import os
import tempfile
import shutil

class NoSuchSecret(Exception):
    def __init__(self, scope, key):
        self.scope = scope
        self.key = key
    def __str__(self):
        return "'%s' is not a secret in scope '%s'" % (self.key, self.scope)

class FileSystemProvider(object):
    def __init__(self, path=os.path.expanduser("~/.supersecret"), creds=None):
        if not os.path.exists(path):
            os.makedirs(path)
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

    def hasSecret(self, scope):
        return key in self.getSecrets(scope)

    def removeAllSecrets(self, scope):
        if os.path.exists(self.scope_path(scope)):
            os.remove(self.scope_path(scope))

    def getSecret(self, scope, key):
        try:
            return self.getSecrets(scope)[key]
        except KeyError:
            raise NoSuchSecret(scope, key)

    def storeSecret(self, scope, key, value):
        secrets = self.getSecrets(scope)
        secrets[key] = value
        # File swap
        print(secrets)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_secret_file:
            json.dump(secrets, temp_secret_file)
        shutil.move(temp_secret_file.name, self.scope_path(scope))

    def getScopes(self):
        result = []
        for file in os.listdir(self.path):
            result.append(file)
        return result

    def dumpScope(self, scope):
        print(self.getSecrets(scope))

    def dumpSecrets(self):
        for scope in self.getScopes():
            print(scope)
            self.dumpScope(scope)

credentials = None
provider = FileSystemProvider()

def hasSecret(scope, key):
    return provider.hasSecret(scope, key)

def getSecret(scope, key):
    return provider.getSecret(scope, key)

def removeAllSecrets(scope):
    return provider.removeAllSecrets(scope)

def storeSecret(scope, key, value):
    return provider.storeSecret(scope, key, value)

def setCredentials(creds):
    creds = creds

def dumpSecrets():
    provider.dumpSecrets()

def listScopes():
    for scope in provider.getScopes():
        print(scope)

def dumpScope(scope):
    provider.dumpScope(scope)

def require(secrets):
    for scope in secrets:
        scope_secrets = secrets.getSecrets(scope)
        for key in scope:
            if key not in scope_secrets:
                raise NoSuchSecret(scope, key)
