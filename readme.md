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

Person Following

https://github.com/Pana1v/ictc/assets/63401208/06f4ab7f-1f70-42eb-adc3-db73597a3067

Line Following

https://github.com/Pana1v/ictc/assets/63401208/e3c35637-c9e8-484b-8647-13adae28dffa

IP Feed from Android -> PC Over WiFi -> Microcontroller for generating transmitted analog signals
![WhatsApp Image 2024-03-01 at 14 17 49_1c7e3cf5](https://github.com/Pana1v/ictc/assets/63401208/cf725798-0a5f-4a4f-ae2e-bd12c38871b8)

Traffic Sign Detection

Object Detection 

![WhatsApp Image 2024-03-01 at 07 11 43_a9450384](https://github.com/Pana1v/ictc/assets/63401208/d2166b8a-04e5-49f0-b7de-a0d10abf122e)

IP Feed from Android -> PC Over WiFi -> Microcontroller for generating transmitted analog signals

[WhatsApp Image 2024-03-01 at 12 40 58_5377dfaa](https://github.com/Pana1v/ictc/assets/63401208/65a9f68b-1472-4193-a1f6-f22ac8050d16)

Customised App!

![WhatsApp Image 2024-03-01 at 07 04 59_f48552ad](https://github.com/Pana1v/ictc/assets/63401208/00f813e2-d4c3-480e-b479-9fd1bd4ef31b)


## Test![WhatsApp Image 2024-03-02 at 12 14 48_86a6848a](https://github.com/Pana1v/ictc/assets/63401208/b17356ed-fb88-4738-8a00-439f6b86f8b1)
ing Android App
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
