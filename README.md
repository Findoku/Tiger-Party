# CSI3335 Project Virtual Environment

This repository provides a virtual environment setup with specified dependencies for student projects in the CSI3335 course. **Please use Python 3.10 and above**

## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions


1. **Clone the Repository**:

```bash
git clone https://github.com/sanjelarun/csi3335-project-venv.git
cd csi3335-project-venv
```

2. **Create a Virtual Environment**

**For Windows**
```bash
python -m venv project_env
```
**For Linux/MacOs**
```bash
python3 -m venv project_env

```
3. **Activate the Virtual Environment**

**For Windows**
```bash
.\project_env\Scripts\activate
```
**For Linux/MacOs**
```bash
source project_env/bin/activate
```

4. **Install the dependencies**
```bash
pip install -r requirements.txt
```

## Usage

Once the virtual environment is activated and dependencies are installed, you can start working on your project within this environment. Remember to deactivate the virtual environment once you're done:

```bash
deactivate
```


## Bonus Features
**dunlfar Example,**
During the late 19th century, professional baseball was still evolving, with frequent managerial changes within teams. It wasn’t uncommon for teams to shuffle managers even multiple times in a single season, especially in cases of financial instability or poor team performance.
-Added Unique Keys to ensure its physically possible to change managers even during a season.

**Edward Hanlon Example Split seasons,**
-Long ago there used to be split seasons within in a season this data does not continue to be sorted in this mannor today but I preserved it alongside the full sets for people who want to see data by split season

**Shohei's Big Bucks**
-Added in Salaries manually From Online as salaries have not been updated since 2016 Most large scale database structures were behind a paywall but there are still salaries from every year since 2016 to update the data with the top grossers.

**Automation**
Added in Custom Pythhon Script Within The Dump that with tweaking (Or as long as the CSVs retains the same descriptors - This is easily configurable with mappings) Can automatically update any database with baseball data.

```
Input For Automation
Host Name: <USER INPUT>
USER: <USERNAME>
PASSWORD: <PASSWORD>
DATABASE NAME: <DB NAME>
LOCALITY: <YES / NO>    (For optimal use store Scripts in TigerScripts and CSVs in CSV file)
```
