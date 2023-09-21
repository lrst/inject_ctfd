import requests as r
import sys, csv

if len(sys.argv) != 5:
    print(f'Syntax: {sys.argv[0]} <URL> <API_KEY> <CSV teams> <CSV users>')
    exit(1)
_, url, apikey, teams_filename, users_filename = sys.argv

print(f'[+] Injecting teams & users in CTFd :')
print(f'\tURL: {url}')
print(f'\tAPI_KEY: {apikey}')
print(f'\tTeams CSV: {teams_filename}')
print(f'\tUsers CSV: {users_filename}')

headers = {"Authorization": f"Token {apikey}", "Content-Type": "application/json"}

def _format_request_err(answer):
    return str(answer.status_code) + ' ' + answer.text.strip('\n')

# Check the connectivity
def check_ctfd():
    try:
        a = r.get(url, headers = headers)
        if a.status_code != 200:
            print(f'Err - unable to connect to CTFd: {_format_request_err(a)}')
            exit(1)
    except Exception as e:
        print(f'Err - unable to connect to CTFd:', repr(e))
        exit(1)


# Read the CSV files
def read_users_csv(filename):
    users = list()
    with open(filename, "r") as file:
        datareader = csv.reader(file)
        for row in datareader:
            user = {'name': row[0], 'email': row[1], 'password': row[2], 'team': row[3]}
            users.append(user)
    return users

def read_teams_csv(filename):
    teams = list()
    with open(filename, "r") as file:
        datareader = csv.reader(file)
        for row in datareader:
            team = {'name': row[0], 'password': row[1]}
            teams.append(team)
    return teams


# Retrieve the list of teams
def get_remote_teams():
    try:
        a = r.get(url + "/api/v1/teams", headers=headers)
        if a.status_code != 200:
            print(f'\tErr - unable to retrieve teams from Ctfd: {_format_request_err(a)}')
            exit(1)
    except Exception as e:
        print(f'\tErr - unable to retrieve teams from Ctfd:', repr(e))
        exit(1)
    teams = dict()
    results = a.json()
    for record in results['data']:
        teams[record['name']] = record['id']
    return teams


# Create teams
def create_teams(teams):
    for team in teams:
        payload = {'name': team['name'], 'password': team['password']}
        try:
            a = r.post(url + "/api/v1/teams", headers=headers, json=payload)
            if a.status_code != 200:
                print(f'\tWarn - unable to create team {team["name"]}: {_format_request_err(a)}')
                continue
            print(f'\tTeam {team["name"]} created.')
        except Exception as e:
            print(f'\tWarn - unable to create team {team["name"]}:', repr(e))
            continue


# Create users
def create_users(users, teams):
    for user in users:
        team_id = teams[user['team']]
        if not team_id:
            print(f'\tWarn - unable to create user {user["name"]}: team {user["team"]} not found.')
            continue

        # Create the user
        payload = {'name': user['name'], 'email': user['email'], 'password': user['password']}
        try:
            a = r.post(url + "/api/v1/users", headers=headers, json=payload, params={'notify': False})
            if a.status_code != 200:
                print(f'\tWarn - unable to create user {user["name"]}: {_format_request_err(a)}')
                continue
        except Exception as e:
            print(f'\tWarn - unable to create user {user["name"]}: ', repr(e))
            continue

        # Add the user to the team
        results = a.json()
        user_id = results['data']['id']
        payload = {'user_id': user_id}
        try:
            a = r.post(url + f"/api/v1/teams/{team_id}/members", headers=headers, json=payload, params={'notify': False})
            if a.status_code != 200:
                print(f'\tWarn - unable to add user {user["name"]} to team {user["team"]}: {_format_request_err(a)}')
                continue
        except Exception as e:
            print(f'\tWarn - unable to add user {user["name"]} to team {user["team"]}: ', repr(e))
            continue

        print(f'\tUser {user["name"]} created and added to team {user["team"]}.')



# Main program
if __name__ == '__main__':
    print(f'[+] Checking connectivity to CTFd :')
    check_ctfd()
    print(f'[+] Connectivity ok with {url}')

    print(f'[+] Read teams & users...')
    teams = read_teams_csv(teams_filename)
    print(f'\t{len(teams)} teams found.')
    users = read_users_csv(users_filename)
    print(f'\t{len(users)} users found.')
    
    print(f'[+] Create teams...')
    create_teams(teams)

    print(f'[+] Retrieve all remote teams...')
    teams = get_remote_teams()
    print(f'\t{len(teams)} teams found.')

    print(f'[+] Create users...')
    create_users(users, teams)