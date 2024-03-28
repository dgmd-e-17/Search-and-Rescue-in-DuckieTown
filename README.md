# DGMD E-17 Robotics, Autonomous Vehicles, Drones and Artificial Intelligence

## Final Project 

We will build an autonomous Duckiebot equipped with NVIDIA Jetson Nano to navigate a controlled setting and recognize victims designated by unique visual signals. 

### Objective

This project aims to apply fundamental robotics principles in practical contexts by using Robotic Systems, Artificial Intelligence, and cloud computing. It emphasizes hands-on experience with autonomous navigation, computer vision, and cloud-based data processing using Duckietown as the base robotic platform.  

### Background

Duckietown is an open-source platform used for research and education in autonomous robotics.

This project builds on these foundations by focusing on a rescue simulation scenario, which, while simplified, introduces the real-world application of robotics in search and rescue operations. 

This initiative provides a comprehensive learning experience in autonomous systems, machine vision, and cloud-based analytics, showcasing how robotics can be harnessed for innovative solutions in simulated rescue operations.

----
### Clone Repository:
```bash
 git clone https://github.com/dgmd-e-17/sar_final_project.git
```


### Upload image 

script files:
    ```
    src/env_vars.sh
    src/upload_aws.py
    ```
usage:

1) move to source directory

    ```bash
    cd src
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

