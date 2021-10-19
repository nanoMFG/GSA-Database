# Web API Documentation

## QUERY

### Expermimental Conditions

- Catalyst (?)
- Tube Diameter*
- Cross Sectional Area* 
- Tube Length*
- Base Pressure*
- Thickness*
- Diameter*
- Length*
- Sample Surface Area* 
- Dew Point*

### Preparation

- Name (?)
- Duration*
- Furnace Temperature*
- Furnace Pressure*
- Sample Location*
- Helium Flow Rate*
- Hydrogen Flow Rate*
- Carbon Source (?)
- Carbon Source Flow Rate*
- Argon Flow Rate*
- Cooling Rate*

### Properties

- Shape (dropdown?)
- Average Thickness of Growth*
- St. Dev. of Growth*
- Number of Layers*
- Domain Size*

### Provenance Information

- Last Name (textbox?)
- First Name (textbox?)
- Institution (textbox?)

"*" means the field is filtered by inequality (less than, greather than equal to, etc)
## Submission

### ???

- Catalyst (?)
- Tube Diameter#
- Corss Sectional Area#
- Tube Length#
- Base Pressure#
- Thickness#
- Diameter#
- Length#
- Sample Surface Area#
- Dew Point

### Steps

There can be multiple steps

One step consists of

- Name (Annealing, Growing, Cooling, Other)
- Duration# (min/sec/hrs)
- Furnace Temperature# (C)
- Furnace Pressure# (Torr/Pa/mbar/mTorr)
- Sample Location# (inches/mm)
- Helium Flow Rate# (sccm)
- Hydrogen Flow Rate# (sccm)
- Argon Flow Rate# (sccm)
- Carbon Source# (CH4/C2H4/C2H2/C6H6/Other)
- Carbon Source Flow Rate# (sccm)
- Cooling Rate# (C/min)

"#" means it is a numeric field

### TODO:
1. Create api endpoint to get experiment data with query strings(?) <br>
ex. nanomfg.org/api/experiments?tube-diameter=<10&thickness=!=10 <br>
Downside: too many query parameter. This endpoint might not be able to be used by api calls without frontend application.<br>
Is there any better approach?


2. Experiment data submission will be handled by csv file submission. (Probably there should be some kind of protocol to be able to parse the file) 


4. Frontend App