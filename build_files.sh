echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python3.9 -m venv venv


# activate the virtual environment
source venv/bin/activate


# install all deps in the venv
pip install -r requirements.txt
python3.9 manage.py runserver


echo "BUILD END"

# [optional] Start the application here 
# python manage.py runserver

#2012 6 months renew $150    2019 950 + 250 = 1200