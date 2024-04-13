# CISC 499
CISC499 Project: Device Fingerprinting with Peripheral Timestamps

# Installation, Requirements & Run
1. Run the command ```pip install -r requirements.txt```
2. Run ```./root.py``` or ```python3 root.py``` based on your deployment needs

# Installation Notes
## Tensorflow-addons Warnings Error
This error is inconsistent across all systems; some produce it, while others do not. If you are facing this error, open and edit the ```__init__.py``` file in the error trackeback, and comment-out lines 19 and 20 (these are the two functions that raise the warnings issue.) The issue has been reported to tensorflow-addons, however, as it is nearing EOL, we see no resolution for this past May 2024.

## Image Generation
Images do not come pre-loaded with this service apart from the two files sitting in /temp. If you are looking to 