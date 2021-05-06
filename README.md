# GSA-Database

## About The Project
A Flask app
More details will be added later

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python3 
  ```sh
  brew install python
  ```
* Flask 
  ```sh
  pip3 install Flask 
  ```
 

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/nanoMFG/GSA-Database.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```
   
### Running the application

python3 app.py 

### Description of Gr-ResQ Data Model 

![overview of data model](https://github.com/nanoMFG/GSA-Database/blob/master/data_model.png)

The main entry is an experiment.  Each experiment consists of the following components: 

#### authors 

name and affiliation of contributors.

#### recipe 

base pressure. 
carbon source.
preparation step
  - step name 
  - duration 
  - temperature 
  - furnace pressure 
  - sample locatioon 
  - helium flow rate 
  - H2 flow rate 
  - C flow rate 
  - cooling rate 

#### furnace 

tube diameter 
cross sectional area 
tube length 
length of heated region 

#### environmental conditions 

dew point 
ambient temperature 

#### substrate 

catalyst 
thickness 
diameter 
length 
surface area 

#### properties 

#### results

SEM images 
raman spectra 



