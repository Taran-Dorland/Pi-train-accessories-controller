#!/bin/bash

echo "Starting flask dev environment..."

export FLASK_APP=../src/train-pi-controller
export FLASK_ENV=development

flask run --host=0.0.0.0