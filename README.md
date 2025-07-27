# GestorLaPrimera_Django

Initial Project for Web-Based Management and Invoicing System this is an initial project aimed at unifying all the phases of the company's current management and invoicing software into a web-based platform.

The initial idea is to use the same database currently used by the company. For now, HTML is being used for the frontend, but it could be replaced with a more robust framework if the client or situation requires it.

### Features:
- Can already connect to AFIP to request the latest issued invoice \
(for security reasons, the .crt and .key files that go in the "cert" folder have been removed)
- Clients and products can be searched directly from the web interface (via AJAX calls)
- When products are selected, the system also calculates TAX and the total amount



The database address should also be updated in the <ins>settings</ins> file.


### Images (Reminder: everything is still in progress):

![](https://i.imgur.com/xPmkSrt.jpeg)

![](https://i.imgur.com/TUzswWs.jpeg)

![](https://i.imgur.com/iOUBEGR.jpeg)

## License
[MIT](https://choosealicense.com/licenses/mit/)