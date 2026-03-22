### **a. About the Module**
FloorNet is a neural network framework designed to transform RGBD videos of indoor spaces into vector-graphics floorplans. The network architecture consists of three distinct branches: a PointNet branch, a Floorplan branch, and an Image branch. The module also includes an integrated, free Integer Programming (IP) solver (`IP.py`) for users who do not have a Gurobi license. 

### **b. URL / Source for Dataset**
* **Pre-processed `tfrecords` files (155 residential scans):** Download [here](https://drive.google.com/open?id=16lyX_xTiALUzKyst86WJHlhpTDr8XPF_) (or via [Mega](https://mega.nz/#F!5yQy0b5T!ykkR4dqwGO9J5EwnKT_GBw) as a backup). These files must be placed under the `data/` folder.
* **Raw Data Components:** * [Point Clouds](https://drive.google.com/open?id=1JJlD0qsgMpiU5Jq9TNm3uDPjvqi88aZn)
    * [Annotations](https://drive.google.com/open?id=1hYDE2SXLA8Cq7LEK67xO-UMeTSPJ5rcB)
    * [Associations](https://drive.google.com/open?id=125TAmYWk22EyzCdlbGIfX4Z4DRMhru_V)
* **Custom Data Example:** An example of raw data before processing can be found [here](https://mega.nz/#!dnohjKZa!I3NJZ806vNK-UYp-ap7OynGnS5E-E5AK_z5WsX8n1Ls).

### **c. Software and Hardware Requirements**
* **Language:** Python 2.7
* **Core Frameworks & Libraries:** TensorFlow (>= 1.3), NumPy, OpenCV 3
* **Hardware Acceleration:** CUDA (>= 8.0)
* **Solvers:** Gurobi (optional) or the included free IP solver (`IP.py`).

### **d. Detailed Instructions to Execute the Source Code**

**1. Data Preparation**
Before training or evaluating, data must be formatted into `tfrecords`. Use `RecordWriterTango.py` (for the provided dataset) or the template `RecordWriterCustom.py` (for custom data source pipelines) to convert raw data and annotations.

Every custom data sample (`tf.train.Example`) must contain the following components:
* **Inputs:**
    * A point cloud (randomly sampled 50,000 points).
    * A mapping from the point cloud's 3D space to the 2D space of a 256x256 top-view density image (contains 50,000 indices, one for each point). 
    * *(Optional)* Image features of the RGB video stream, if the image branch is enabled.
* **Labels:**
    * Corners and their corresponding types.
    * Total number of corners.
    * A ground-truth icon segmentation map.
    * A ground-truth room segmentation map.

**2. Training the Network**
To train the network from scratch, run the following command in your terminal:
```bash
python train.py --restore=0
```

**3. Evaluating the Model**
To evaluate the performance of the trained model, execute:
```bash
python train.py --task=evaluate --separateIconLoss
```