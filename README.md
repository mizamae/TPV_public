<!-- This file is part of Tiny TPV environment.

Tiny TPV is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Tiny TPV is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Tiny TPV. If not, see <https://www.gnu.org/licenses/>. -->

# Tiny TPV
[![en](https://img.shields.io/badge/lang-en-red.svg)](README.md)
[![es](https://img.shields.io/badge/lang-es-yellow.svg)](README.es.md)

This creates a web application (connected to Tiny TPV) that can be used as commerce web-site. It includes the following features:
- Resposive design to comfortable view on any device
- Automatic product updates from Tiny TPV (requires minor configuration in Tiny TPV application)

## Installation

Create a virtual environment based on Python 3.11 or newer.
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Tiny TPV.

```
pip install -r requirements.txt
```

The web server should be configured as required depending on the software used. In this repo, an exemplary application using Nginx and Gunicorn is delivered.
The default configuration for Nginx is detailed in the file ![Nginx configuration](/customerPortal.conf).
The files to configure the services for Gunicorn and Celery are provided in ![Gunicorn configuration](/gunicorn.service) and ![Celery configuration](/celery_worker.service) respectively.

## Appearance

Once up and running, reaching at the predefined endpoint (webpage-endpoint.com in Nginx configuration file) the default webpage appears.
![default page](/assets/images/default_page.png)
The page is structured in sections that can be easily reached by scrolling down or hitting in the navigation bar titles. Needless to say this page can be fully customizable in appearance and form.

The cool side of this is that a Django application is running behind the scenes (on a Postgresql database) with the following models available:

- Product family: this serves as container to group products that share a similar feature such as dog food, cat food, etc...
- Product: is every single product that you can offer to the visitors.

If the commerce sells books, one product family may be Comics. Through its Tiny TPV interface will create such family and it will automagically create it in the public web page to make it accessible for online customers.
![product families](/assets/images/familias.png)
By clicking in the family picture, all the products belonging to that family (and created through the Tiny TPV interface) will appear showing its actual price and stock.
![product families](/assets/images/productos.png)

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

Tiny TPV is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Tiny TPV is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Tiny TPV (see [license](gpl-3.txt)).
