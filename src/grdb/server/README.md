# Web API Documentation

## QUERY from version 1

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

## Current API

Pass filter as query string into data/expriments endpoint.

If filtering a text field, pass the text as the query string value.

ex) ```experiments/data?rcs=CH4```

If filtering a numerical filed, pass the inequality sign as well as the numeric value as the query string value.

ex) ```experiments/data?rbp=lt40```

You can chain the filters.

ex) ```experiments/data?rcs=CH4&rbp=lt40```

#### Query String Keys

- rcs : carbon source (text)
- rbp : base pressure (numeric)
- sc : catalyst (text)
- st : thickness (numeric)
- sd : diameter (numeric
- sl : length (numeric)
- ssa : surface area (numeric)
- edp : dew point (numeric)
- eat : ambient temperature (numeric)
- ftd : tube diameter (numeric)
- fcsa : cross sectional area (numeric)
- ftl : tube length (numeric)
- flhr : length of heated region (numeric)
- patg : average thickness of growth (numeric)
- psdg : standard deviation of growth (numeric)
- pnl : number of layers (numeric)
- pgc : growth coverage (numeric)
- pds : domain size (numeric)
- ps : shape (text)

#### Inequality Codes
- eq : eqaul to
- ne : not equal to
- lt : less than
- le : less than or equal to
- gt : greater than
- ge : greater than or equal to

#### Query String Values:
- For text fields: <value>
- For numerical fields: <inequality code><value>

### TODO:
Experiment data submission will be handled by csv file submission. (Probably there should be some kind of protocol to be able to parse the file) 
