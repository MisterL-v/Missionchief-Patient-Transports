# Missionchief-Patient-Transports
This script automatically processes patient transports on the website "www.leitstellenspiel.de" or "www.missionchief.com".

## :file_folder: Versions
[#1.0](https://github.com/MisterL-v/Missionchief-Patient-Transports/releases/tag/%23version_1.0) `[Latest]`

## :heavy_check_mark: Functions
First of all, after the registration, the script searches for possible patient transports that have not yet been processed.
In the event that one or more patient transports are required, the script primarily alerts patient transport vehicles.
If there is no patient transport vehicle is available, an mobile intensive car unit of the same value is automatically alerted.

## :heavy_exclamation_mark: Requirements
The script has been tested in Python version 3.8 and higher.
To work it needs the python extension Selenium.

Google Chrome must be installed and the Chromedriver has to be downloaded.

Finally, the login information and the path to the downloaded Chromedriver must be changed at the beginning of the script.
