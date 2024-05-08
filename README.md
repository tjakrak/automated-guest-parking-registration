Automated Guest Parking Form Submission
===
![downloads](https://img.shields.io/github/downloads/atom/atom/total.svg)

## Table of Contents

[TOC]

[](https://imgur.com/a/Sp45UhY)
## Introduction
In the Boulevard housing area, parking on the street is permitted only if vehicles are registered for guest parking. Traditionally, this registration process has been manual. To streamline this, our repository introduces a Python script that automates the process using Selenium.

Key Features:

* Automation: The script fills out and submits the parking registration web form available at [Boulevard Parking](https://boulevard.parkingattendant.com/1hchtwjdt95fd4zyxvqmdmeve0/permits/temporary/new?policy=k10g06m5yd15n7bbep5x0qncmm).
* Scheduling: Registration is set to automatically repeat daily using GitHub Actions, ensuring that it occurs without manual intervention at 9 PM each day.

This solution aims to save time and reduce the hassle associated with manual entry, providing a seamless parking experience for residents and their guests.

## Requirements
* Python 3.x
* Selenium WebDriver
* Google Chrome
* ChromeDriver
* A GitHub account for deploying the script with GitHub Actions

1. Clone the repository
```
git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name
```
2. Setup Python environment
```
python -m venv venv
source venv/bin/activate 
# On Windows use `venv\Scripts\activate`
```

3. Install required packages
```
pip install -r requirements.txt
```

4. Configure Environment Variables:
* Update config.json file. Replace the placeholder text within the angle brackets (<>) with your actual data:
``` 
    {
        "vehicle": "<license_plate>",
        "tenant": "<home_address>",
        "token": "<token>",
        "space": "<parking_area>",
        "notes": "<car_make>, <car_model>, <car_color>",
        "name": "<your_name>",
        "email": "<email_address>",
        "tel": "<phone_number>",
        "duration": "<parking_duration>"
    }
```
* Alternatively, set up **TOKEN**, **EMAIL**, **TEL**  environment variables in GitHub Secrets for deployment using GitHub Actions.
    * **Settings > Secrets and variables > Actions**
>Notes: Make sure **tenant** and **space** are in capital letters, follow the exact words on the [website](https://boulevard.parkingattendant.com/1hchtwjdt95fd4zyxvqmdmeve0/permits/temporary/new?policy=k10g06m5yd15n7bbep5x0qncmm).

## Usage
*  Local execution
    * To run the script locally, execute:
    `python automation_script.py`
* Github Actions Deployment<br>
The **.github/workflows/automation.yml** file contains the configuration for GitHub Actions. This workflow is scheduled to run the script daily at a specified time.
    * Push your changes to GitHub repository
    `git add .`
    `git commit -m "Set up automation script"`
    `git push origin main`
    * The GitHub Actions workflow will automatically run at the next scheduled time. You can view the action results in the "Actions" tab of your GitHub repository.

#### Configuring the Scheduler
* Edit the Cron Schedule:
In the **.github/workflows/automation.yml**, adjust the cron schedule to suit your needs:
```
on:
  schedule:
    - cron: '0 7 * * *'  # Runs at 07:00 UTC every day
```