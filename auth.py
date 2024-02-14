from flask import request
from functools import wraps
from ToDoApp.security import secretKey
import datetime
import jwt
from bson.objectid import ObjectId


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        #Get the token from authorization field
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        #Exit if token not found
        if not token:
            return {"data": "Authorization token is missing."}, 401
        else:
            resp = validate_token(token)
            #Token validated
            if resp[1] == 200:
                userID = resp[0]["data"]          
                try:
                    currUser = users.find_one({"_id": ObjectId(userID)})
                except Exception as e:
                    return {"data": "An error occured. Could not find the user."}
                if currUser is not None:
                    return f(currUser,  *args, **kwargs)
                else:
                    return {"data": "You do not have permission to access this resource."}, 401
            else:
                return resp
    return decorated


def generateToken(userId):
    """
    Generates a JWT token for authentication

    iss: Issuer of token (calender-app)
    sub: Subject (set to user ID)
    iat: Issued at time
    exp: Expiry of token (90 mins)
    """
    try:
        #"iss": https://calender-app.com
        payload = {
            "sub": str(userId),
            "iat": datetime.datetime.utcnow(),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=90)
        }
        token = jwt.encode(payload, secretKey, algorithm="HS256")
        #print(token)
        return "Success", token
    except Exception as e:
        #print(f"Error: {e}")
        return "Unable to generate JWT token for user."


def validate_token(token):
    try:
        payload = jwt.decode(token, secretKey, algorithms=["HS256"])
        return {"data": payload["sub"]}, 200
    except jwt.exceptions.ExpiredSignatureError:
        return {"data": "Token has expired."}, 403
    except jwt.exceptions.InvalidTokenError:
        return {"data": "Invalid token."}, 401
    except Exception as e:
        #print(e)
        return {"data": "Cannot validate provided token."}, 500