def upload_score(players):
    scores = []
    for player, score in players.items():
        if player == "":
            continue
        scores.append(f"{player} {score}")
    converted = "\n".join(scores)
    with open("./scoretable.txt", "w") as f:
        f.write(converted)
    return

def download_score():
    players = {}
    with open("./scoretable.txt", "r") as f:
        scores = f.read()
    if scores == "":
        return {}
    lines = scores.split("\n")
    for line in lines:
        pair = line.split()
        players[pair[0]] = pair[1]
    return players