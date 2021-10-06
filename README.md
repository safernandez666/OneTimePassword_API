# One Time Password API

## Create the database

On database folder run the following command.

```
sqlite3 users.db < init.sql
```
## Request

1. http://localhost:5000/v1/init [GET]
2. http://localhost:5000/v1/validate [POST]

Check with the user's email.

<p align="center">
<img src="screenshots/imagen_1.png" width="800" >
</p>

If the user is in the database, an email will be sent with the OTP code.

<p align="center">
<img src="screenshots/imagen_2.png" width="800" >
</p>

The user must perform the POST with their email and code. The time that the code is alive depends on the variable ***timeToLease***

<p align="center">
<img src="screenshots/imagen_3.png" width="800" >
</p>