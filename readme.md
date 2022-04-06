# Backend Developer Challenge

A service exposed through a REST API that lets users publish bonds for sale and buy bonds published by other users.
Django is used to create REST APIs.

Starting URL: http://127.0.0.1:8000/api/

Basic authentication(Username and password required)

## Endpoints created:

##### 1) Get all profiles :

Request-type: GET

This endpoint would return all the existing profiles.

##### 2) Get all bonds :

Request-type: GET

API: `http://127.0.0.1:8000/api/bonds`

This endpoint would return all the existing bonds.

##### 3) Get specific bond with id :

Request-type: GET

API: `http://127.0.0.1:8000/api/bonds/{uuid: bond_id}`

This endpoint would require a bond id, and returns a specific bond matching that id.

##### 4) Publish a bond:

Request-type: POST

API: `http://127.0.0.1:8000/api/create-bond`

Required payload in JSON format:

```sh
{
"name": string(3-40 alphanumeric characters);
"numberOfBonds": integer(value between 1-10,000);
"price": decimal(value between 0-100,000,000 Upto 4 decimals);
}
```

This endpoint would create a bond, and return the bond itself as response.

##### 5) Edit a Bond:

Request-type: PATCH

API: `http://127.0.0.1:8000/api/edit-bond/{uuid: bond_id}`

Required payload in JSON format(All fields are optional)

```sh
{
"name": string(3-40 alphanumeric characters);
"numberOfBonds": integer(value between 1-10,000);
"price": decimal(value between 0-100,000,000 Upto 4 decimals);
}
```

This endpoint would edit the bond with given id, if provided data are valid

##### 6) Delete a bond :

Request-type: DELETE

API: `http://127.0.0.1:8000/api/delete-bond/{uuid: bond_id}`

This endpoint would delete the bond with given id and return the bond as response

##### 7) Buy a bond :

Request-type: PATCH

API: `http://127.0.0.1:8000/api/buy-bond/{uuid: bond_id}`

This endpoint requires the id of the bond which the user wants to purchase and if it is available, the user can purchase it, otherwise Invalid Operation error is returned.

##### 8) View prices of bonds in USD :

Request-type: GET

API: `http://127.0.0.1:8000/api/view-in-usd`

This endpoint enables the user to view the price of all the bonds in USD. The exchange rate is obtained from the following API. "SieAPIRest" is Series id provided.
https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno
