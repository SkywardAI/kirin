## Regular Setup

1. Before setting up the backend app, please create a new directory called `coverage` for the testing report purpose:

   ```shell
   cd backend && mkdir coverage
   ```

2. Backend app setup:

    ```shell
    # Creating VENV
    pyenv virtualenv 3.11.0 any_venv_name
    pyenv local any_venv_name

    # Install dependencies
    pip3 install -r https://raw.githubusercontent.com/SkywardAI/containers/main/requirements.txt

    # Test run your backend server
    uvicorn src.main:backend_app --reload
    ```

3. Testing with `PyTest`:
   Make sure that you are in the `backend/` directory.

   ```shell
   # For testing without Docker
   pytest
   
   # For testing within Docker
   docker exec backend_app pytest
   ```

4. `Pre-Commit` setup:

    ```shell
    # Make sure you are in the ROOT project directory
    pre-commit install
    pre-commit autoupdate
    ```

5. Backend app credentials setup:
    If you are not used to VIM or Linux CLI, then ignore the `echo` command and do it manually. All the secret variables for this template are located in `.env.example`.

    If you want to have another name for the secret variables, don't forget to change them also in:

    * `backend/src/config/base.py`
    * `docker-compose.yaml`

    ```shell
    # Make sure you are in the ROOT project directory
    touch .env

    echo "SECRET_VARIABLE=SECRET_VARIABLE_VALUE" >> .env
    ```

    For test usage , you can simplely use .env.example

    ```shell
    cp .env.example .env
    ```

