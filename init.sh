#!/bin/bash
echo running database init
python manage.py migrate
python manage.py loadcsv --csv catalogue/management/commands/init.csv --image_folder product_images --lorem_description True
python manage.py loadcomments --csv comments/management/commands/init.csv --lorem_text True
python manage.py loadarticles --csv articles/management/commands/init.csv --image_folder article_images