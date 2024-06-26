import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'dev-ys2gjmv8t2h7h16t.us'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'http://localhost:5000'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header
# Done - tested, but server only returns 500 errors and not status code
'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
   # raise Exception('Not Implemented')
   # if "Authorization" not in request.headers:
    # abort(401)

    # auth_header = request.headers['Authorization']
    

    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'no_auth_header',
            'description': 'Expected Auth Header'
            }, 401)
    

    header_parts = auth_header.split(' ')
    
    # if len(header_parts) != 2:
    #     raise AuthError({
    #         'code': 'malformed_header',
    #         'description': 'No token'
    #         }, 401)
    
    if header_parts[0].lower() != 'bearer':
        
        raise AuthError({
            'code': 'invalid header',
            'description': 'No bearer'
            }, 401)
    elif len(header_parts)==1:
        raise AuthError({
            'code': 'invalid header',
            'description': 'Token not found'
            }, 401)
    elif len(header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'header must be bearer token'
            }, 401) 

    token = header_parts[1]
    return token


'''
start here
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
# def check_permissions(permission, payload):
#     if 'permissions' not in payload:
#         raise AuthError({
#             'code': 'invalid_claims',
#             'description': 'Permissions not included in JWT.'
#             }, 400)

#     if permission not in payload['permissions']:
#         raise AuthError({
#             'code': 'unauthorized',
#             'description': 'Permission not found.'
#         }, 401)
#     return True

def check_permissions(permission, payload):
    # if 'permissions' is None:
        # abort(400)

    if 'permissions' not in payload:
        abort(400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission Not found',
        }, 401)
    return True

    # raise Exception('Not Implemented')

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
# Validation code from Auth0
# https://auth0.com/docs/quickstart/backend/python/01-authorization
def verify_decode_jwt(token):
    # raise Exception('Not Implemented')
    def requires_auth(f):
    # """Determines if the Access Token is valid"""
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            jsonurl = urlopen("https://"+AUTH0_DOMAIN+".auth0.com/.well-known/jwks.json")
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            
              # Auth0 token should have a key id
            if 'kid' not in unverified_header:
                raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed'
            }, 401)

            rsa_key = {}
            for key in jwks["keys"]:
                if key["kid"] == unverified_header["kid"]:
                    rsa_key = {
                        "kty": key["kty"],
                        "kid": key["kid"],
                        "use": key["use"],
                        "n": key["n"],
                        "e": key["e"]
                    }
            ptint('rsa_key')
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer="https://"+AUTH0_DOMAIN+"/"
                    )
                    return payload

                except jwt.ExpiredSignatureError:
                    raise AuthError({
                        "code": "token_expired",
                        "description": "token is expired"
                        }, 401)

                except jwt.JWTClaimsError:
                    raise AuthError({
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        "please check the audience and issuer"\
                        }, 401)

                except Exception:
                    raise AuthError({
                        "code": "invalid_header",
                        "description": "Unable to parse authentication token."
                        }, 400)

                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
            raise AuthError({
                "code": "invalid_header",
                "description": "Unable to find appropriate key"
            }, 401)
        return decorated

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator

    # Had issues with permissions not being iterable. switched to code from https://github.com/kalsmic/Coffee_Shop_Full_Stack/blob/master/backend/src/auth/auth.py