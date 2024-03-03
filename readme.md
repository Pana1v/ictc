# Project Name

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# Project Overview

The project mainly consists of the following components:

## 1. Android App and Compiled APK
- **Description:** The Android app serves as a pivotal part of the project, contributing to both testing and functionality.
- **Components:**
  - Compiled APK for testing purposes.

## 2. Server Scripts for Hive Computing
- **Description:** Server-side scripts facilitate hive computing, utilizing the phone's camera feed to compute kinematics for the robot.
- **Components:**
  - **2.a. Line Following:**
    - Scripts dedicated to implementing line-following behavior.
  - **2.b. Person Following:**
    - Modules designed for enabling the robot to follow a person.
  - **2.c. Traffic Sign Detection:**
    - Components responsible for detecting and interpreting traffic signs.

# Usage Instructions

## Testing Android App
1. Install the compiled APK on your Android device for testing.

## Hive Computing Server Setup
1. Utilize server scripts to establish hive computing functionality.
2. Implement specific scripts based on desired robot behavior:
   - **2.a. Line Following:**
     - Execute relevant scripts for line-following functionality.
   - **2.b. Person Following:**
     - Implement modules for person-following capabilities.
   - **2.c. Traffic Sign Detection:**
     - Set up components for traffic sign detection.

## Integration with Microcontroller
1. Transmit computed kinematics to the microcontroller for robot control.

## Usage Instructions

Ensure you have the necessary dependencies installed by running:

```bash
pip install -r requirements.txt

Clone Repository
Clone the repository to your local machine using the following command:

bash
Copy code
$ git clone https://github.com/YourUsername/YourRepository.git
$ cd YourRepository