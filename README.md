# GestorLaPrimera_Django

Initial Project for Web-Based Management and Invoicing System this is an initial project aimed at unifying all the phases of the company's current management and invoicing software into a web-based platform.

The initial idea is to use the same database currently used by the company. For now, HTML is being used for the frontend, but it could be replaced with a more robust framework if the client or situation requires it.

Important: The Ui is in spanish.


### Features:
- Can already connect to ARCA to request the latest issued invoice \
(for security reasons, the .crt and .key files that go in the "cert" folder have been removed)
- Clients and products can be searched directly from the web interface (via AJAX calls)
- When products are selected, the system also calculates TAX and the total amount
- Can change price and quantity (with correspondingly validators) for every selected product
- Electronic invoices can be issued directly from the application, with CAE and CAE Vto.



### Instructions:
Follow these steps to set up and run the Django project locally:
- Clone the repository
```
git clone https://github.com/juspi07/GestorLaPrimera_Django.git
cd GestorLaPrimera_Django
```
- Install dependencies
```
pip install -r requirements.txt
```
- Apply migrations
```
python manage.py migrate
```
When apply migrations, you have a initial data in database

- Run the development server
```
python manage.py runserver
```
Then visit https://localhost:8000 in your browser.


### Images (Reminder: everything is still in progress):

![](https://i.imgur.com/uIpcFQj.png)

![](https://i.imgur.com/VmQH0fP.png)

![](https://i.imgur.com/dqw5JcV.png)

![](https://i.imgur.com/dFI08xA.png)

![](https://i.imgur.com/2F6BacL.png)

![](https://i.imgur.com/Khl51oY.png)

## License
[MIT](https://choosealicense.com/licenses/mit/)