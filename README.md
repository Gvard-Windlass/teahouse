# Teahouse

Practice project written with django 4.1.1, styled using bootstrap 5.2.2

Images generated using [Craiyon](https://www.craiyon.com/) and [Stable Diffusion
Online](https://stablediffusionweb.com/).

To initialize project, load catalogue, comment and article data with following commands:
```
python manage.py loadcsv --csv catalogue/management/commands/init.csv --image_folder product_images --lorem_description True
python manage.py loadcomments --csv comments/management/commands/init.csv --lorem_text True
python manage.py loadarticles --csv articles/management/commands/init.csv --image_folder article_images
```

## Screenshots
![Home page](screenshots/home.png?raw=true "Home page")
![Article page](screenshots/articles.png?raw=true "Article page")
![Products page](screenshots/products.png?raw=true "Products page")
![Product detail page](screenshots/product-detail.png?raw=true "Product detail page")
![Cart page](screenshots/cart.png?raw=true "Cart page")
![Profile page](screenshots/profile.png?raw=true "Profile page")
