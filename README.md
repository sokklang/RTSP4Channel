# Video Streaming Application User Guide

## Introduction

This user guide provides instructions for using the Python video streaming application developed using the PyQt5 and OpenCV libraries. The application allows you to load a configuration file with RTSP streaming settings and display multiple video streams in a grid layout.

## Table of Contents

- [Requirements](#requirements)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Loading Configuration](#loading-configuration)
  - [Starting Video Streams](#starting-video-streams)
  - [Exiting the Application](#exiting-the-application)


## Requirements

Before using the video streaming application, ensure you have the following prerequisites installed on your system:

- Python 3.x
- PyQt5 library
- OpenCV library

You can install these dependencies using the following commands:

```bash
pip install PyQt5 opencv-python
```

## Usage

### Running the Application
1. Clone or download the repository containing the source code.

2. Open a terminal or command prompt and navigate to the directory containing the source code files.

3. Run the application by executing the following command:
    ```bash
    python main.py
    ```

4. The application window will open, showing a grid layout with four video widgets.

5. If you prefer to distribute the application as an executable, you can use PyInstaller to create a standalone executable file for your platform. You can download the pre-built executable from [this link](https://github.com/sokklang/RTSP4Channel/tree/main/dist).

### Loading Configuration

1. Click the "Load Config" button to open a file dialog.

2. Choose a JSON configuration file (*.json) that specifies the RTSP streaming settings for each video channel.

    ```json
    {
    "channels": [
        {
        "username": "your_username",
        "password": "your_password",
        "xvr_ip": "xvr_ip_address",
        "channel": 1,
        "stream_type": 0
        },
        {
        "username": "your_username",
        "password": "your_password",
        "xvr_ip": "xvr_ip_address",
        "channel": 2,
        "stream_type": 1
        },
        ...
    ]
    }
    ```

    `username`: The username for authentication to access the RTSP stream.

    `password`: The password for authentication (will be URL-encoded in the application).

    `xvr_ip`: The IP address of the XVR (DVR/NVR) device.

    `channel`: The channel number of the camera feed.

    `stream_type`: The stream type (0 for main stream, 1 for sub-stream, etc.).

    `Note`: The application supports up to four video widgets in a 2x2 grid layout. You can adjust the layout and number of video widgets in the source code if needed.

3. After loading the configuration, the file path will be displayed in the text field.


### Starting Video Streams

1. Click the "Start Stream" button to initiate the video streaming based on the loaded configuration.

2. The video streams from the specified RTSP URLs will be displayed in the video widgets. The streams will update at a set interval.

### Exiting the Application

To exit the application: Press the 'q' key on your keyboard.
