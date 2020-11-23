mkdir log
mkdir instance
pip install virtualenv
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=flaskr
export FLASK_ENV=development
flask init-db
flask run
