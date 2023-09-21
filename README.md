# Inject users & teams in CTFd

This script allows to create teams and users in an instance of CTFd. It requires:
- the base URL of the CTFd instance.
- an admin API_KEY (see how to generate one [here](https://docs.ctfd.io/docs/api/getting-started#generating-an-admin-access-token))
- a CSV file describing Teams
- a CSV file describing Users

Note that this script does not handle all the various error that can happen. Be cautious !

Tested against CTFd 3.5.0.

## Usage

Install python requirements:
```
python3 -m pip install -r requirements
```

Example of usages:

```
❯ python3 create_users\ and\ teams.py 
Syntax: create_users and teams.py <URL> <API_KEY> <CSV teams> <CSV users>

❯ python3 create_users\ and\ teams.py https://REDACTED_CTFD_URL REDACTED_API_KEY teams.csv users.csv 
[+] Injecting teams & users in CTFd :
	URL: https://REDACTED_CTFD_URL
	API_KEY: REDACTED_API_KEY
	Teams CSV: teams.csv
	Users CSV: users.csv
[+] Checking connectivity to CTFd :
[+] Connectivity ok with https://REDACTED_CTFD_URL
[+] Read teams & users...
	2 teams found.
	7 users found.
[+] Create teams...
	Team first_team created.
	Team second_team created.
[+] Retrieve all remote teams...
	4 teams found.
[+] Create users...
	User first_team1 created and added to team first_team.
	User first_team2 created and added to team first_team.
	User first_team3 created and added to team first_team.
	User first_team4 created and added to team first_team.
	User second_team1 created and added to team second_team.
	User second_team2 created and added to team second_team.
	User second_team3 created and added to team second_team.
```

## CSV format

Each record of a team in the CSV has the following entry:
- team name
- team password (note that this password is probably meaningless in our usage).

Example:
```
first_team,password
```


Each record of a user in the CSV has the following entry:
- username
- email
- password
- team name

Example:
```
first_team1,first_team1@plop.com.invalid,first_team1,first_team
```
