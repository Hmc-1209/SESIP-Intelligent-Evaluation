# SESIP-Intelligent-Evaluation
The SESIP fast evaluation using a large language model to help evaluators get preliminary judgments and supporting evidence.

## Technical and tools references
React.js as frontend, FastAPI as backend, MySQL database and gpt-4o-mini LLM model.

## Setting up
There are three major applictions to set up:
1. React.js service start up
2. Database settings
3. FastAPI service config & start up

#### Database
Any SQL db is applicable. First create a user called `SESIP-app-user`, then login. In `db` directory, there's a file called `create_table.sql`, run the script and the database should be built.

#### FastAPI
To setup api, use the command `pip install -r requirements.txt` in `api` directory. Before you start the service, make sure to add a `.env` file in the root directory of this project, with the following information:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=SESIP-app-user
DB_PASS={YOUR_DB_PSASWORD}
DB_NAME=sesip-app
ACCESS_TOKEN_SECRET_KEY={YOUR_ACCESS_TOKEN_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=10
API_KEY={YOUR_LLM_API_KEY}
BASE_PATH={YOUR_BASE_PATH_FOR_SAVING_FILES}
```
the `ACCESS_TOKEN_SECRET_KEY` is for generating app user access token, it needs a HS256 random string, and the `BASE_PATH` will be where you want to store st files and eval results. In the directory, it should contain two templates (evaluation_report_template_level_1, evaluation_report_template_level_2) provided in the project root directory.

For example, mine is at "C:/Users/minchenho/Documents/SESIP-Eval", with two Microsoft Word files in it.

#### React.js
Make sure `node.js` is installed, navigate to `app` directory and type down `npm install` for installing dependencies.
Next, type `npm start` and the service would start. The web page could be found at `http://127.0.0.1:8000/`.