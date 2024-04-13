# CISC 499
CISC499 Project: Device Fingerprinting with Peripheral Timestamps

# Installation, Requirements & Run
1. Run the command ```pip install -r requirements.txt```
2. Run ```./root.py``` or ```python3 root.py``` based on your deployment needs

# Installation Notes
## Tensorflow-addons Warnings Error
This error is inconsistent across all systems; some produce it, while others do not. If you are facing this error, open and edit the ```__init__.py``` file in the error trackeback, and comment-out lines 19 and 20 (these are the two functions that raise the warnings issue.) The issue has been reported to tensorflow-addons, however, as it is nearing EOL, we see no resolution for this past May 2024.

## Image Generation
Images do not come pre-loaded with this service apart from the two files sitting in /temp. If you are looking to generate the images, please run ```generate_images.py```. You will need to load keystroke file data from the online database presented in Monaco's paper.

## Database Salting
1. Create the database. This should be done with the database name ```cisc499```. Tables ```salted_vectors``` and ```unsualted_vectors``` should be created with the following commands:
     ```CREATE TABLE salted_vectors ( position INT, user_id VARCHAR(50), array VARCHAR(10000), PRIMARY KEY (user_id) );```
    ```CREATE TABLE unsalted_vectors ( position INT, user_id VARCHAR(50), array VARCHAR(10000), PRIMARY KEY (user_id) );```
2. Create the user in mysql using:
    ```CREATE USER 'integration'@'localhost' IDENTIFIED BY 'cisc499';```
    ``` GRANT ALL PRIVILEGES ON *.* TO 'integration'@'localhost' WITH GRANT OPTION;```
    ```FLUSH PRIVILEGES;```
3. run ```add_salted_users.py```
4. under ```data_database``` delete this file.
5. drop and recreate the table ```unsalted_vectors```

## Questions:
Please feel free to contact me with any questions.