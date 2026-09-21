import csv

def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a new user"""
    try:
        if username in sn:
            return False

        sn[username] = (fullname, [])
        return True

    except Exception as error:
        print("Error adding user.")
        print(error)
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    try:
        if user1 not in sn or user2 not in sn:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)

        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)

        return True

    except Exception as error:
        print("Error adding friend.")
        print(error)
        raise

def get_friends(sn: dict, user1: str, distance: int) -> list:
    try:
        if user1 not in sn:
            return []

        friends = []
        visited = [user1]
        current = [user1]

        for i in range(distance):
            next_group = []

            for user in current:
                for friend in sn[user][1]:
                    if friend not in visited:
                        visited.append(friend)
                        friends.append(friend)
                        next_group.append(friend)

            current =next_group

        return friends

    except Exception as error:
        print("Error getting friends.")
        print(error)
        raise

def save_network(filename: str, sn: dict) -> None:
    try:
        file = open(filename, "w", newline="", encoding="utf-8")
        writer = csv.writer(file)

        for username in sn:
            fullname = sn[username][0]
            friends = sn[username][1]

            row = [username, fullname]

            for friend in friends:
                row.append(friend)

            writer.writerow(row)

        file.close()

    except OSError as error:
        print("Error saving network.")
        print(error)
        raise


def load_network(filename: str) -> dict:
    try:
        sn = {}

        file = open(filename, "r", encoding="utf-8")
        reader = csv.reader(file)

        for row in reader:
            username = row[0]
            fullname = row[1]
            friends = row[2:]

            sn[username] = (fullname, friends)

        file.close()

        return sn

    except OSError as error:
        print("Error loading network.")
        print(error)
        raise


def main() -> None:
    print("Veljko Stojanovic")

    sn = {
        "alice": ("Alice Smith", ["maria"]),
        "maria": ("Maria Cortez", ["alice", "joe", "david"]),
        "joe": ("Joseph Adams", ["maria", "eve"]),
        "eve": ("Evelyn Cooper", ["joe"]),
        "david": ("David Benson", ["maria"])
    }

    print("\nPart a")
    print(add_user(sn, "john", "John Smith"))

    print("\nPart b")
    print(add_friend(sn, "john", "alice"))

    print("\nPart c")
    print(get_friends(sn, "alice", 1))
    print(get_friends(sn, "alice", 2))

    print("\nPart d")
    save_network("social_network.csv", sn)
    print("Network saved.")

    print("\nPart e")
    loaded_network = load_network("social_network.csv")
    print(loaded_network)


main()