# CSI3335 Project Virtual Environment

This repository provides a virtual environment setup with specified dependencies for student projects in the CSI3335 course. **Please use Python 3.12.7 and above**

## Description

This virtual environment contains essential Python libraries and frameworks required for the project. The `requirements.txt` file lists all the dependencies.

## Instructions


1. **Clone the Repository**:

```bash
git clone https://github.com/Findoku/Tiger-Party.git
cd Tiger-Party
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


***Web Page***
For the web page bonus features we added WAR to the tables.
We also added WAR, PA, wRC+ to the depth charts. 
We also added a page where it talks about al the players with the highest feats in baseball.
An example of a big feat would be most strikeouts in a career.
In the biggest feats page, you can click on the players names and it takes you to a page where it talks about their career stats.
In the player page where it talks about the career stats, it also mentions if they are a manager and if they are inducted in the Hall of Fame, a photo will show indicating that. 
We also added a team stats page where it talks about the team as a whole and states if the team has ever won a world series.




***Immaculate Grid***
For the Immaculate Grid Guesser we added a popularity table in the dump where it gives each player a popularity value.
The more feats and contributions the player does to their team, the higher the value. 
We gave a multiplier for each part of the statistic for the baseball game.
An example would be giving 35 times multiplier for very homerun a person did. If one person did 1 homer it would be 35 points and 70 if 2 home runs.
We designed the immaculate grid to where you can enter the data simply by adding what it says on the actual game.
After that you click the Generate players button and wait.


***Admin Page***
You can find the admin login on the first page which is the login page.

***The Admin username is 'greg'.***

***The Admin password is 'speegle'.***

You can navigate through the pages and see the team stats like everyone else.
You can also play the immaculate grid game.
There will be a button specifically for the admin to navigate back to the admin page.


***NOTE***
You might need to use python 3.12.7 or higher for the instructions to run smoothly.
