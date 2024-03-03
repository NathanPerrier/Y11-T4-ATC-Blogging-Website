# Perrier-Digital-Blog-Y11-T3

Created by [Nathan Perrier](https://github.com/nathan-perrier23) of [Ambrose Treacy College](https://www.atc.qld.edu.au/)

This is a blogging website for ATC, created as part of the Y11 FA3 project. 

## Setup and Running the Project

Follow these steps to set up and run the project:

1. Allow the execution of scripts for the current user:

    ```sh
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force
    ```

2. then create the virtual environment using: 

    ```sh
    python -m venv venv   
    ```      

3. active the virtual environment using:

    ```sh
    .\venv\Scripts\activate 
    ```

4. install dependencies to venv, using:

    ```sh
    python3 -m pip install -r requirements.txt
    ```

5. create a file called .env and include:

    ```sh
    SECRET_KEY = 'your_secret_key'

    OPENAI_API_KEY = 'your_api_key'

    GOOGLE_API_KEY = 'your_google_key'
    ```

5. Run the website using:

    ```sh
    python3 -m run.py
    ```

### Structure

The project is structured as follows:

`backend/`: Contains the backend Python code.
`frontend/`: Contains the frontend HTML, CSS, and JavaScript code.
`requirements.txt`: Lists the Python packages that the project depends on.
`run.py`: The entry point to the application.


#### Contributing

If you want to contribute to this project, please fork the repository, make your changes, and open a pull request. 

##### License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENCE.md) file for the full license text.
