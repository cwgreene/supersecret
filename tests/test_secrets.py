import os
import unittest
import secrets

class TestSecrets(unittest.TestCase):
    def testFileSecret(self):
        """Tests entire lifecycle of a lifecycle secret"""
        SCOPE = "testSecrets"
        KEY = "testKey"
        KEY2 = "testKey2"
        SECRET = "Abracdabra"
        SECRET2 = "Abracdabra2"

        # Create scope
        provider = secrets.FileSystemProvider("data/secrets/")
        provider.removeAllSecrets(SCOPE)
        self.assertFalse(os.path.exists(provider.scope_path(SCOPE)))

        # Store Secret
        provider.storeSecret(SCOPE, KEY, SECRET)
        stored_secret = provider.getSecret(SCOPE, KEY)
        self.assertEqual(SECRET, stored_secret)

        # Store Another Secret, verify original
        provider.storeSecret(SCOPE, KEY2, SECRET2)
        stored_secret = provider.getSecret(SCOPE, KEY)
        self.assertEqual(SECRET, stored_secret)

        # Verify new secret
        stored_secret = provider.getSecret(SCOPE, KEY2)
        self.assertEqual(SECRET2, stored_secret)

        # Destroy Scope
        provider.removeAllSecrets(SCOPE)
        self.assertFalse(os.path.exists(provider.scope_path(SCOPE)))
