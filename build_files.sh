echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.12 -m venv venv

# activate the virtual environment
source venv/bin/activate


#pip install --upgrade pip
## install all deps in the venv
pip install --upgrade -r requirements.txt

## collect static files using the Python interpreter from venv
#python manage.py collectstatic --noinput

echo "BUILD END"

# [optional] Start the application here 
# python manage.py runserver