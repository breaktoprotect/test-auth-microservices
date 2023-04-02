from fastapi import FastAPI, Header, HTTPException
from keycloak import KeycloakOpenID

app = FastAPI()

# Initialize Keycloak OpenID client
keycloak_openid = KeycloakOpenID(server_url="http://localhost:8080/auth/",
                                 client_id="testclient",
                                 realm_name="sample",
                                 client_secret_key="")

# Define protected endpoint
@app.get("/protected")
async def protected_endpoint(authorization: str = Header(...)):
    try:
        # Validate access token
        token_info = keycloak_openid.decode_token(authorization, verify=True)
        
        # Check user role
        if "admin" not in token_info.get("realm_access").get("roles"):
            raise HTTPException(status_code=403, detail="User not authorized")
            
        # Return protected data
        return {"data": "This is protected data"}
        
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

# Define public endpoint
@app.get("/public")
async def public_endpoint():
    return {"data": "This is public data"}