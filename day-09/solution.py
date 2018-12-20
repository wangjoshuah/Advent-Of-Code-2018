class Game:

    def __init__(self, players) -> None:
        super().__init__()
        self.players = list()
        self.num_players = players
        for i in range(players):
            self.players.append(Player(i + 1))
        self.circle = Circle()

    def play_until(self, last_marble):
        for i in range(last_marble + 1):
            player = self.players[i % self.num_players]
            score = self.circle.add_marble(i + 1)
            player.score += score
        print(self.circle)
        return self.print_high_score()

    def print_high_score(self):
        high_score = 0
        highest_scoring_player = None
        for player in self.players:
            if player.score > high_score:
                high_score = player.score
                highest_scoring_player = player
        print(f"Player {highest_scoring_player.number} won with a high score of {high_score}")
        return high_score


class Circle:

    def __init__(self) -> None:
        super().__init__()
        self.current = Marble(0)
        self.current.clockwise = self.current
        self.current.counter_clockwise = self.current
        self.zero = self.current

    def add_marble(self, value):
        new_marble = Marble(value)
        if value % 23 == 0:
            points = new_marble.value
            marble_to_remove = self.current
            for j in range(7):
                marble_to_remove = marble_to_remove.counter_clockwise
            points += marble_to_remove.value
            marble_to_remove.clockwise.counter_clockwise = marble_to_remove.counter_clockwise
            marble_to_remove.counter_clockwise.clockwise = marble_to_remove.clockwise
            self.current = marble_to_remove.clockwise
            return points
        else:
            clockwise1 = self.current.clockwise
            clockwise2 = clockwise1.clockwise
            new_marble.clockwise = clockwise2
            new_marble.counter_clockwise = clockwise1
            clockwise1.clockwise = new_marble
            clockwise2.counter_clockwise = new_marble
            self.current = new_marble
            return 0

    def __str__(self) -> str:
        values = list()
        values.append(self.zero.value)
        next_marble = self.zero.clockwise
        while next_marble is not self.zero:
            values.append(next_marble.value)
            next_marble = next_marble.clockwise
        return values.__str__()


class Marble:

    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
        self.counter_clockwise = None
        self.clockwise = None


class Player:

    def __init__(self, number) -> None:
        super().__init__()
        self.number = number
        self.score = 0

