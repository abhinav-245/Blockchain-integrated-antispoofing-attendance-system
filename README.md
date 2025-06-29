# WEB-BASED FACE RECOGNITION ATTENDANCE SYSTEM with ANTI SPOOFING and BLOCKCHAIN INTEGRATION

This repository is a modified version of the original [Face Recognition Attendance System](https://github.com/KeerthiGowdaHN/Face-recognition-attendance-with-anti-spoofing) with added blockchain integration for enhanced security and transparency.

## Original Project Credits
This project is based on the work by:
- Keerthi Gowda H N (Original Repository Owner)
- Ayu Purnama Virgiana (210040171)
- I Komang Adisaputra Gita (210040017)

## New Features Added
- **Blockchain Integration**: 
  - Smart contract-based attendance recording
  - Immutable attendance records
  - Enhanced security and transparency
  - Decentralized storage of attendance data

# Features
The application allows users to perform the following tasks:
- **Visitor Validation**: Capture an image using the camera and perform *face recognition with anti-spoof* to differentiate between real and fake faces and validate visitors. The system checks the captured face against the database of known faces and identifies the person if a match is found.
- **View Visitor History**: View the history of visitor attendance, including their ID, name, and timestamp of the visit. Additionally, the application provides an option to search and display images of specific visitors.
- **Add to Database**: Add new individuals to the database for future recognition. Users can input the person's name and either upload a picture or capture one using the camera. The system maintains 2 data storage (CSV files) for visitors information.

The demo pictures of the features are available on our **Medium** ["Web-based Face Recognition Attendance System with Anti Spoofing"](https://medium.com/@ayuvirgiana10/web-based-face-recognition-attendance-system-with-anti-spoofing-cd479d193e6b).


# System Architecture
The entire code is written in Python **this project made and tested in python 3.11.2**

**Frontend**: 
- The system utilizes **Streamlit** to create a web interface. The main UI elements include a title bar, a sidebar for navigation, and different sections for
  visitor validation, viewing visitor history, and adding to the database.

**Data Storage:**
- This project stores visitor information in:
  - Two CSV files for general user information (visitors_db.csv) and visitor history (visitors_history.csv)
  - Blockchain network for immutable attendance records

**Face Recognition:**
- Library:
  Using facenet_pytorch for [Inception Resnet (V1) models](https://github.com/davidsandberg/facenet/blob/master/src/models/inception_resnet_v1.py), pretrained on [VGGFace2](https://www.robots.ox.ac.uk/~vgg/data/vgg_face2/) and CASIA-Webface datasets. The datasets aligned with [MTCNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html).
- **WHY [MTCNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html)?**
  The Dlib face detector misses some of the hard examples (partial occlusion, silhouettes, etc). This makes the training set too "easy" which causes the model to perform worse on other benchmarks. To solve this, we use [Multi-task CNN](https://kpzhang93.github.io/MTCNN_face_detection_alignment/index.html) for face landmark detector that has proven to work very well in this setting.

**Anti-Spoofing**
- Model: [MiniFASNet](https://github.com/AyuVirgiana/face-recognition-attendance-anti-spoofing/blob/main/src/model_lib/MiniFASNet.py) supported by [Silent-Face-Anti-Spoofing](https://github.com/computervisioneng/Silent-Face-Anti-Spoofing.git) developed by (https://www.minivision.cn/).

**Blockchain Integration:**
- Smart contracts for attendance management
- Ethereum network integration
- Web3.py for blockchain interactions

**Installation Requirements**
- [requirement.txt](https://github.com/AyuVirgiana/face-recognition-attendance-anti-spoofing/blob/main/requirements.txt) consists the version of requirements we used in this app


# Training Data 
- **Face Recognition Model**

  The following models have been ported to pytorch (with links to download pytorch state_dict's):

  |Model name|LFW accuracy (as listed [here](https://github.com/davidsandberg/facenet))|Training dataset|
  | :- | :-: | -: |
  |[20180408-102900](https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180408-102900-casia-webface.pt) (111MB)|0.9905|CASIA-Webface|
  |[20180402-114759](https://github.com/timesler/facenet-pytorch/releases/download/v2.2.9/20180402-114759-vggface2.pt) (107MB)|0.9965|VGGFace2|

  There is no need to manually download the pretrained state_dict's; they are downloaded automatically on model instantiation and cached for future use in the torch cache. To use an [Inception Resnet (V1) models](https://github.com/davidsandberg/facenet/blob/master/src/models/inception_resnet_v1.py) for facial recognition/identification in pytorch, use:
  
  ```python
  from facenet_pytorch import InceptionResnetV1 
  ```
  Used in this app => [app.py](https://github.com/AyuVirgiana/face-recognition-attendance-anti-spoofing/blob/main/app.py), line 10.

  [Classifier training of inception resnet v1](https://github.com/davidsandberg/facenet/wiki/Classifier-training-of-inception-resnet-v1) page describes how to train the Inception-Resnet-v1 model as a classifier, i.e. not using Triplet Loss as was described in the Facenet paper.

- **Anti-spoofing Model**

  cited from [Silent-Face-Anti-Spoofing](https://github.com/computervisioneng/Silent-Face-Anti-Spoofing.git)
  
Visitors database (https://github.com/KeerthiGowdaHN/Face-recognition-attendance-with-anti-spoofing/tree/main/visitor_database)

visitor photo https://github.com/KeerthiGowdaHN/Face-recognition-attendance-with-anti-spoofing/blob/main/visitor_database/Keerthi%20Gowda%20H%20N.jpg


# Installation and Setup

## Prerequisites
- Python 3.11.2 (recommended)
- Git
- pip (Python package installer)
- Webcam (for face capture functionality)

## Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/abhinav-245/Blockchain-integrated-antispoofing-attendance-system.git
   cd Blockchain-integrated-antispoofing-attendance-system
   ```

2. **Create and Activate Virtual Environment** (Recommended)
   ```bash
   # For Windows
   python -m venv venv
   .\venv\Scripts\activate

   # For Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Blockchain Environment**
   - Install MetaMask or any Ethereum wallet
   - Configure your Ethereum network settings
   - Deploy the smart contract using deploy_contract.py

## Running the Application

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the Web Interface**
   - Open your web browser
   - Navigate to the URL shown in the terminal (typically http://localhost:8501)

3. **Using the Application**
   - Use the sidebar to navigate between different features:
     - Visitor Validation: Capture and validate faces
     - View Visitor History: Check attendance records
     - Add to Database: Register new visitors

4. **Troubleshooting**
   - If you encounter any issues with camera access, ensure your webcam is properly connected and accessible
   - For model loading errors, verify that all dependencies are correctly installed
   - Check the console output for any error messages


# References
- Original Project: [Face Recognition Attendance System](https://github.com/KeerthiGowdaHN/Face-recognition-attendance-with-anti-spoofing)
- This project is supported by [Silent-Face-Anti-Spoofing](https://github.com/computervisioneng/Silent-Face-Anti-Spoofing.git) belongs to [minivision technology](https://www.minivision.cn/)
- [Face Recognition using Pytorch](https://github.com/timesler/facenet-pytorch.git) by timesler
- Pytorch model weights were initialized using parameters ported from [David Sandberg's tensorflow facenet repo](https://github.com/davidsandberg/facenet.git)

# Contributors
- Original Contributors:
  - Ayu Purnama Virgiana (210040171)
  - I Komang Adisaputra Gita (210040017)
- Blockchain Integration:
  - Adla Abhinav Reddy - Blockchain Developer
  -Akhil Bommaraju - Compared with different approaches