## Getting Started

### Installing Locally
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.  


### Prerequisites
<!-- 
What things you need to install the software and how to install them -->

#### Using Conda

Install anaconda3 or miniconda3, then:<br/>

After cloning the GSA-Database repo locally, navigate to the top-level GSA-Database directory.
Activate the base conda environment then create a fresh conda environment as follows:  
```
conda create --name gresq-3.8 python=3.8
conda activate gresq-3.8
conda install --file requirements.txt
```
To support testing, install the following packages:  
```
conda install pytest factory_boy
```

#### Installing

For development, run:  
```
pip install -e .
```

## Running the tests

<!-- Explain how to run the automated tests for this system -->

After installing, run the following from the repostory root:
```
pytest -v
```
