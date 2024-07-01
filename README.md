# Disinformation Analysis

## Project Description
This project helps to analyse disinformation spead about healthcare and 
why people believe disinformation about healthcare.


## Endpoints
- api
- api/user/<user_id>
- api/user/<user_id>/full
- api/post/<post_id>
- api/post/<post_id>/full
- api/variable/<variable_name>
- api/variable/
- api/ranked/users
- api/create/user


### Clone the Repository
```
git clone https://github.com/Aitzha/disinformation_analysis.git
cd disinformation_analysis
```

### Create and Activate a Virtual Environment for Windows
```
python -m venv myenv # Alternatively if you have virtualenv 'virtualenv myenv'
source myenv\Scripts\activate
```

### Create and Activate a Virtual Environment for Linux and MacOS
```
python3 -m venv myenv # Alternatively if you have virtualenv 'virtualenv myenv'
source myenv/bin/activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Migration
```
python manage.py migrate
$env:PROJECT_PATH="path" # on Windows PowerShell
set PROJECT_PATH=path # on Windows Command Prompt
export PROJECT_PATH=”path” # On Linux and MacOS 
python .\scripts\populate_healthcare_disinformation.py
```

### Testing
```
python manage.py test
```

### Run the Application
```
python manage.py runserver
```
