# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\bin\activate

# create a requirements.txt file with the installed packages
pip freeze > requirements.txt

#pip show list | grep <package_name>
pip show list | grep request

# Install the required packages
pip install -r requirements.txt

# Update the packages
pip install --upgrade -r requirements.txt
