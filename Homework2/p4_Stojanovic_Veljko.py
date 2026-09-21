import csv
def load_casts(filename: str) -> dict:
    movies = {}

    file = open(filename, "r", encoding="utf-8")
    reader = csv.reader(file)

    for row in reader:
        title = row[0]
        year = row[1]
        director = row[2]
        actors = row[3:]

        movies[(title, year)] = (director, actors)

    file.close()

    return movies

def display_top_collaborations(rated_filename: str,
                               casts_filename: str) -> None:
    rated_movies = []

    file = open(rated_filename, "r", encoding="utf-8")
    reader = csv.reader(file)

    next(reader)

    for row in reader:
        title = row[1]
        year = row[2]

        rated_movies.append((title, year))

    file.close()

    casts = load_casts(casts_filename)

    collaborations = {}

    for movie in rated_movies:
        if movie in casts:
            director = casts[movie][0]
            actors = casts[movie][1]

            for actor in actors:
                pair = (director, actor)

                if pair in collaborations:
                    collaborations[pair] += 1
                else:
                    collaborations[pair] = 1

    ranking = []

    for pair in collaborations:
        director = pair[0]
        actor = pair[1]
        count = collaborations[pair]

        ranking.append((count, director, actor))

    ranking.sort(reverse=True)

    print("Top Collaborations:")

    count = 0

    for item in ranking:
        if count == 10:
            break

        print((item[1], item[2], item[0]))
        count += 1

def display_top_actors(grossing_filename: str,
                       casts_filename: str) -> None:
    casts = load_casts(casts_filename)

    actor_totals = {}

    file = open(grossing_filename, "r", encoding="utf-8")
    reader = csv.reader(file)

    next(reader)

    for row in reader:
        title = row[1]
        year = row[2]

        money = row[3]
        money = money.replace("$", "")
        money = money.replace(",", "")
        money = int(money)

        movie = (title, year)

        if movie in casts:
            actors = casts[movie][1]

            for actor in actors:
                if actor in actor_totals:
                    actor_totals[actor] += money
                else:
                    actor_totals[actor] = money

    file.close()

    ranking = []

    for actor in actor_totals:
        ranking.append((actor_totals[actor], actor))

    ranking.sort(reverse=True)

    print("Top Actors:")

    count = 0

    for item in ranking:
        if count == 10:
            break

        print((item[1], item[0]))
        count += 1

def main() -> None:
    print("Veljko Stojanovic")

    print()
    display_top_collaborations(
        "imdb-top-rated.csv",
        "imdb-top-casts.csv"
    )

    print()
    display_top_actors(
        "imdb-top-grossing.csv",
        "imdb-top-casts.csv"
    )

main()