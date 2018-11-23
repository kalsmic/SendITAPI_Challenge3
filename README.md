# SendIT API
SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

**prerequisites for using the project**
- PostgresSQL - a powerful, open source object-relational database system.
- Python -  an interpreted high-level programming language for general-purpose programming.
- Postman - a tool used to send requests and receive responses through our REST API
 


**SENDIT API ENDPOINTS**

| EndPoint                                | Functionality                                                   |
| ----------------------------------------| --------------------------------------------------------------- |
| GET api/v1/parcels                      | Fetch all parcel delivery orders                                |
| GET api/v1/parcels/<parcelId>           | Fetch a specific parcel delivery order                          |
| GET api/v1/users/<userId>/parcels       | Fetch all parcel delivery orders by a specific user             |
| PUT api/v1/parcels/<parcelId>/cancel    | Cancel the specific parcel delivery order                       |
| POST api/v1/parcels                     | Create a parcel delivery order                                  |
| POST /auth/signup                       | Register a user                                                 |
| POST /auth/login                        | Login a user                                                    |
| PUT /parcels/<parcelId>/destination     | Change the location of a specific parcel delivery order         | 
| PUT /parcels/<parcelId>/status          | Change the status of a specific parcel delivery order           |
| PUT /parcels/<parcelId>/presentLocation | Change the present location of a specific parcel delivery order |

How to set up the project
Open the terminal and run the following commands
```bash

    $ > git clone https://github.com/kalsmic/SendITAPI_Challenge3.git
    $ > cd SendITAPI_Challenge3
    $ > git checkout develop
    $ > python3 -m venv venv
    $ > source venv/bin.activate
    $ > pip3 install -r requirements.txt
    $ > EXPORT FLASK_APP
    $ > flask run
    Open http://127.0.0.1:5000/  in your web browser.
   ```
### How to run tests
- Open terminal from root folder of the project.
- Enter the command below in the terminal to run the tests
```bash
  $ > pytest
  ```
