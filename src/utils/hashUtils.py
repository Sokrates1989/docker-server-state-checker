## Utilities for password/login like operations using hash algorithm.

# Import hash library to secure login-like behaviour.
import hashlib

# Get Sha512 hash of passed strings.
def getSha512(password, pepper, salt=")s(f/g?h)§j/s%§j=s$gh!r)r$"):
	stringToHash = password + pepper + salt
	hash_object = hashlib.sha512(stringToHash)
	hex_dig = hash_object.hexdigest()
	return hex_dig
