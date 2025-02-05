# MFA
MFA for robots

Used for MFA authentication.

# Getting started

## Requirements

- Python 3.12+
- FastAPI
- Uvicorn

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/nkAPIs/MFA.git
    cd your-repo-name
    ```

2. **Create a virtual environment**:

    - On Windows:

        ```sh
        python -m venv venv
        ```

    - On macOS/Linux:

        ```sh
        python3 -m venv venv
        ```

3. **Activate the virtual environment**:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install the dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

## Running the Application

1. **Start the FastAPI server**:

    ```sh
    uvicorn mfaAPI:app --host 0.0.0.0 --port 8000 --reload
    ```

    - `mfaAPI` is the name of the Python file (e.g., `mfaAPI.py`).
    - `app` is the name of the FastAPI instance.
    - `--host` default 0.0.0.0.
    - `--port` default is port 8000.
    - `-reload` reloads when changes is detected.

2. **Access the application**:

    Open your browser and go to `http://127.0.0.1:8000`.

3. **Interactive API documentation**:

    - Swagger UI: `http://127.0.0.1:8000/docs`

## Using

1. **Using the API from Python**:
    ```python
    import requests
    from constants import Constants
    # From Constants the user and password is retrieved
    # user and password is located in PostgreSQL database with key = mfaAPI
    constants = Constants()

    # Step 1: Get the JWT token
    token_url = "http://127.0.0.1:8000/token"
    credentials = {
        "username": constants.user,
        "password": constants.password
    }

    response = requests.post(token_url, data=credentials)

    if response.status_code == 200:
        token = response.json().get("access_token")
        print("✅ Token received:", token)
    else:
        print("❌ Failed to get token:", response.text)
        exit()

    # Step 2: Use the token to call the /getsecret endpoint
    secret = "??????????????"  # replace with actual secret key
    headers = {
        "Authorization": f"Bearer {token}"
    }

    get_secret_url = f"http://127.0.0.1:8000/getsecret?secret={secret}"
    response = requests.get(get_secret_url, headers=headers)

    if response.status_code == 200:
        print("🔑 TOTP Token:", response.json())
    else:
        print("❌ Failed to get TOTP token:", response.text)
    ```
1. **Using curl for the API **:
    ```curl
    curl -X 'POST' \
    'http://127.0.0.1:8000/token' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=password&username=<USERNAME>&password=<PASSWORD>=&client_id=string&client_secret=string'
    ```

    returns (eks):
    ```json
    {
        "access_token": "3Mzg3NjkwNTVYuV8soORBmTN8hXNYCSUvA2WeJuqUYCw",
        "token_type": "bearer"
    }
    ```
    use the token to get MFA cipher:
    ```curl
    curl -H "Authorization: Bearer YOUR_TOKEN" "http://127.0.0.1:8000/getsecret?secret=YOUR_SECRET_KEY"
    ```
# Database
### table
    public.nkinitvalues

1. **Select from table in order to username and password**:
    ```sql
    SELECT id, name, description, type_id, value, debugmode
	FROM public.nkinitvalues 
    where id = 'mfaAPI';
    ```
2. **Returns**:
    ---
    | id          | name        | value         |
    | :---        |    :----:   |          ---: |
    | mfaAPI      | user        | nkMFAAPIUser  |
    | mfaAPI      | password    | *** pw *****  |
    ---
    user and password is used for obtaining a token.

    ** NOTE token expires after 30 minutes **

# Docker

## Making the docker instance
