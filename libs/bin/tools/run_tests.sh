set -e
cd $(dirname "$0")
cd ../..

VENV_DIR="/tmp/runner/.aos-libs-venv"
if [ ! -d "$VENV_DIR" ]; then
  virtualenv $VENV_DIR
fi
source $VENV_DIR/bin/activate

pip install -r requirements.txt -q >/dev/null 2>&1

DJANGO_SETTINGS_MODULE=tests
nosetests
