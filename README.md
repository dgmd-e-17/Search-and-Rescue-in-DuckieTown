# <img style="float: left; padding-right: 30px; width: 45px" src="./images/harvard-logo.png">  DGMD E-17 Robotics, Autonomous Vehicles, Drones and Artificial Intelligence

## Final Project - Search and Rescue in Duckietown

**Harvard University, Spring 2024**<br/>
**Instructor:** Nabib Ahmed <br/>
**Teaching Assistant:** Marwah Aman<br/>

**Team: The Killer Robots**:

* Artemio Mendoza
* Natheniel Roe 
* Sidharta Roy

Welcome to our project to design and construct an autonomous Duckiebot capable of navigating through a simulated environment known as Duckietown. Our Duckiebot's mission is to identify and report the locations of "victims" marked by distinct visual cues, such as colored shapes or QR codes. This endeavor showcases core robotics principles, including autonomous navigation and object recognition, all within a simulated search and rescue scenario.

<a id="contents"></a>
## Table of Contents

1. [Project Summary](#summary)
2. [Technologies and Methods](#technologies-and-methods)
3. [Solution Architecture](#solution-architecture)
4. [Project Components](#project-components)
    - 4.1 [Clone Repository](#clone-repo)
    - 4.2 [Project Proposal](#proposal)
    - 4.3 [Ethics Concerns](#ethics)
    - 4.4 [Initial Demo](#initial-demo)
    - 4.5 [Software Components](#software-components)
5. [References](#references)


<a id="summary"></a>
## Project Summary
[Return to Table of Contents](#contents)

This project involves the design and construction of an autonomous Duckiebot that is capable of navigating a simplified Duckietown environment. The primary objective is for the Duckiebot to locate and report the locations of "victims" identified by distinct visual cues, such as colored shapes or QR codes. Utilizing LLaVA, an OpenSource Multimodal Large Language Model (LLM), the Duckiebot will also be able to identify hazardous situations potentially involving human victims. 

The adquired data is uploaded to AWS S3 for further analysis.

This project aims to demonstrate essential robotics principles, including autonomous navigation and object recognition, within a simulated search and rescue scenario. 

### Objective

This project aims to apply fundamental robotics principles in practical contexts by using Robotic Systems, Artificial Intelligence, and cloud computing. It emphasizes hands-on experience with autonomous navigation, computer vision, and cloud-based data processing using Duckietown as the base robotic platform.  

This initiative provides a comprehensive learning experience in autonomous systems, machine vision, and cloud-based analytics, showcasing how robotics can be harnessed for innovative solutions in simulated rescue operations.

### Background

Duckietown is an open-source platform used for research and education in autonomous robotics.

This project builds on these foundations by focusing on a rescue simulation scenario, which, while simplified, introduces the real-world application of robotics in search and rescue operations. 

This initiative provides a comprehensive learning experience in autonomous systems, machine vision, and cloud-based analytics, showcasing how robotics can be harnessed for innovative solutions in simulated rescue operations.

<a id="technologies-and-methods"></a>
## Technologies and Methods
[Return to Table of Contents](#contents)

#### Hardware

* NVIDIA Jetson Nano 4GB with GPU (CUDA)
* Video cam
* Differential Driver, 2-wheeled robot, with encoders.
* Customized Duckietown setup, modified to for search and rescue

#### Software

* Python for programming control scripts, and interacting with AWS
* LLaVA, a Multimodal LLM model; designed to identify dangerous scenarios
* OpenCV for computer vision and image processing functions
* ROS for coordinating sensor data and actuator commands
* AWS Services  - Cloud integration for AI advanced Image processing
* Docker - to access Duckietown image with basic commands

#### Methods

* Implement algorithms for navigationg around obstacles 
* Deep Learning/Computer Vision techniques for victim identification
* Data logging and visual indication for reporting
* Image capture and transference to AWS cloud 
* Use of advanced image processing and data management via AWS

<a id="solution-architecture"></a>
## Solution Architecture
[Return to Table of Contents](#contents)

* Our SAR system employs an autonomous Duckiebot with NVIDIA Jetson Nano, using MobileNet CNN for real-time victim detection. 

* We use a State of The Art (SOTA) Large Language Model, LLaVA, to identify possible hazardous situations via image capture. The image is not only classified, but also, the potentially dangerous situation is described, so the rescue team could have context.

* The images clasified as dangerous are uploaded to AWS for advanced analysis and logging.

<img src="./images/architecture.png"> </img>

<a id="project-components"></a>
## Project Components
[Return to Table of Contents](#contents)



<a id="clone-repo"></a>
### Clone Repository:
```bash
 git clone https://github.com/dgmd-e-17/sar_final_project.git
```

<a id="proposal"></a>
### Proposal presentation



<a id="ethics"></a>
### Ethical concerns

<a id="initial-demo"></a>
### Initial Demo

<a id="software-components"></a>
### Software Components
[Return to Table of Contents](#contents)

#### Building Instructions

- [🚧] **TODO** add description
- [🚧] **TODO** add link to duckiebot building manual

#### RobotSoftware Platform installation

- [🚧] **TODO** add description
- [🚧] **TODO** add link to duckiebot software manual

#### MLL Implementatation - LLaVA Component

We decided to use a novel approach to classify the situation. Instead of training and deploying a classical Convolutional Neural Network to label the image, we decided to locally implement a SOTA LLM, that will not only classify the images, but provide a description of the situation. 

Gitub Repository: https://github.com/haotian-liu/LLaVA

- [🚧] **TODO** add installation instructions

#### AWS Components

- [🚧] **TODO** add description

#### Usage:  upload image 

script files:
    ```
    src/env_vars.sh
    src/upload_aws.py
    ```
usage:

1) move to source directory

    ```bash
    cd aws_components\src
    ```

2) load env variable by running shell script

    ```bash
    $ source ./env_vars.sh
    ```

3) execute CLI command

    ```bash
    └─ $ ▶ python upload_aws.py ./data/test_file_1.txt 
    File was uploaded successfully.
    ```

<a id="references"></a>
## 5. References
[Return to Table of Contents](#contents)

* Duckietown Project Documentation and Resources. The official Duckietown documentation offers comprehensive guides on setting up Duckiebots, programming them, and understanding the Duckietown environment: https://docs.duckietown.org/

* Visual Instruction Tuning. *Haotian Liu, et al*. https://arxiv.org/html/2304.08485v2

* LLaVA: Large Language and Vision Assistant. Visual Instruction Tuning. NeuriIPS 2023 (Oral). Haotian Liu, et al. https://llava-vl.github.io/

* OpenCV Documentation.  The OpenCV library is crucial for computer vision tasks. The official documentation provides tutorials, guides, and API references for implementing various computer vision algorithms, essential for object recognition in robotics:  https://docs.opencv.org/master/

* Robot Operating System (ROS). Provides tools and libraries to help software developers create robot applications, from simple robots to complex autonomous systems. https://www.ros.org

* AWS AI Services. AI cloud-based ML and DL-based services. These services enable developers to add intelligence to their applications without requiring deep expertise in AI. https://aws.amazon.com/machine-learning/ai-services/