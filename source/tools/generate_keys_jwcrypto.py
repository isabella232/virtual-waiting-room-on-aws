# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import json
import random
import time
import uuid
from jwcrypto import jwk, jwt, jws

# key id
kid = uuid.uuid4().hex

# create JWK format keys
keypair = jwk.JWK.generate(kid=kid, kty='RSA', size=2048)

# get the private and public JWK from the pair
private_jwk = keypair.export_private(as_dict=True)
public_jwk = keypair.export_public(as_dict=True)

# print the JWKs
print(f"{json.dumps(private_jwk, indent=4)}")
print()
print(f"{json.dumps(public_jwk, indent=4)}")

# issuer (iss) can be URL of waiting room instance web endpoint
iss = 'https://ixulut9y89.execute-api.us-east-1.amazonaws.com/api/'

# audience (aud) is the unique event ID for the waiting room
aud = 'DBF95F82-4C93-4E4F-B27B-225529C6AFCD'

# subject (sub) is the unique device/client ID requesting a position
sub = '03C16C5A-8607-4489-B744-1525183A6738'

# issued-at and not-before can be the same time (epoch seconds)
iat = int(time.time())
nbf = iat

# expiration (exp) is a time after iat and nbf, like 1 hour (epoch seconds)
exp = iat + 3600

# waiting room specific claims
# generate a random position
# Bandit B311: not used for cryptographic purposes
waiting_room = {'position': random.randint(1, 25000)} # nosec

# create token claims
claims = {
    'aud': aud,
    'sub': sub,
    'waiting_room': waiting_room,
    'token_use': 'access',
    'iat': iat,
    'nbf': nbf,
    'exp': exp,
    'iss': iss
}

token = jwt.JWT(header={"alg": "RS256", "typ": "JWT"}, claims=claims)
token.make_signed_token(keypair)

# print the token
print(f"{token.serialize()}")
