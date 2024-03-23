#!/bin/bash

# Define the virtual environment directory name
VENV_DIR="venv"

# Check if a virtual environment is already active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "No virtual environment is active."

    # Check if the virtual environment directory exists
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment..."
        # Create a virtual environment
        python3 -m venv $VENV_DIR
    fi

    # Activate the virtual environment
    echo "Activating virtual environment..."
    source $VENV_DIR/bin/activate
else
    echo "A virtual environment is already active."
fi

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Load environment variables from .env file
echo "Loading environment variables from .env file..."
if [ -f ".env" ]; then
    set -a  # Automatically export all variables
    source .env
    set +a # Stop exporting all variables
else
    echo "Warning: .env file not found."
fi

# Check for required environment variables and warn if not set
echo ""
echo "Checking for required environment variables..."
for var in GOOGLE_APPLICATION_CREDENTIALS OPENAI_API_KEY ES_URL ES_INDEX MONGO_DBNAME MONGO_URI; do
    if [ -z "${!var}" ]; then
        echo "Warning: Environment variable $var is not set."
    fi
done

# Navigate to the src directory
cd src

# if admin argument is passed, run admin tools instead
if [ "$1" = "admin" ]; then
    echo "Running user admin tools..."
    python -m app.utils.admin_tools
    exit 0
fi


# Start the FastAPI application
echo ""
echo "Starting FastAPI application..."
which python
uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level debug --log-config log_conf.yaml
