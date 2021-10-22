from service.match_service import MatchVisitTemplate
from service.match_service import MatchManager
from datatype.enums import DartMultiplier

CHECKOUTS = {
    170: "T20 T20 Bull ",
    167: "T20 T19 Bull",
    164: "T20 T18 Bull",
    161: "T20 T17 Bull",
    160: "T20 T20 D20",
    136: "T20 T20 D8",
    36: "D18",

}
STARTING_TOTAL = 501


class X01Match(MatchManager, MatchVisitTemplate):
    def __init__(self):
        super().__init__()
        self.scores = []  # list of scores remaining parallel to players
        self.averages = []  # single-dart avg (x 3 for 3-darts avg
        self.first9 = []  # avg of first 9 darts

    def post_init(self):
        for i in range(0, len(self.match.players)):
            self.scores.append(STARTING_TOTAL)
            self.first9.append(None)
            self.averages.append(None)

    def validate_visit(self, player_index, visit):
        if self.match.last_player_index is player_index:
            return False, "Player" + str(player_index + 1) + "is not the correct sequence. Visit ignored."
        if not self.match.active:
            return False, "Game has ended."
        self.match.last_player_index = player_index
        return True, None

    def check_winning_condition(self, player_index, visit):
        """ r e t u r n s 1 , 2 o r 3 f o r when a d a r t c l o s e s the game / l e g ( i . e .
        f i n i s h i n g d ouble ) o r 0 i f not c l o s e d out

        : param pl aye r_index : p o s i t i o n o f pl a y e r d e t a i l s i n v a ri o u s l i s t s
        : param v i s i t : a l i s t o f 3 Darts ( each c o n t ai ni n g m u l t i p l i e r and
        segment )
        : r e t u r n : 0 , 1 , 2 o r 3
         """
        i = 0
        for dart in visit.darts:
            i = i + 1
            if dart.multiplier == DartMultiplier.DOUBLE and self.score[player_index] - dart.get_score() == 0:
                self.scores[player_index] = 0
                self.match.active = False
                return i
            else:
                self.scores[player_index] == dart.get_score()
        return 0

    def record_statistics(self, player_index, visit, result):
        if result is not 0:
            visit.remove_trailing_darts(result)
        self.match.visits[player_index].append(visit)

        if len(self.match.visits[player_index]) == 3:
            self.first9[player_index] = (STARTING_TOTAL - self.scores[player_index]) / 3

        num_darts_thrown = (len(self.match.visits[player_index]) - 1) * 3
        num_darts_thrown += 3 if result is 0 else result

        if result is not 0:
            self.match.winning_num_darts = num_darts_thrown
            self.match.winning_player_index = player_index

        self.averages[player_index] = (STARTING_TOTAL-self.scores[player_index])/num_darts_thrown

    def format_summary(self, player_index, visit):
        summary = "Last visit was by" + self.match.players[player_index] + "with" + visit.to_string() + "\n"

        if self.match.winning_player_index is not -1:
            summary += self.match.players[self.match.winning_player_index]+ "wins in " + str(self.match.winning_num_darts) + "darts\n"
        i =0
        for player in self.match.players:
            summary = summary + player + ":" + str(str.scores[i])+ "Remaining"
            if self.scores[i] in CHECKOUTS.keys():
                summary += "(" + CHECKOUTS.get(self.scores[i]) + ")"
            if self.first9[i]:
                summary += "\n - [3-dart Avg:" + '{0:2f}'.format(self.first9[i]) + "]"
            if self.averages[i]:
                summary += "\n - [3-dart Avg:" + '{0:2f}'.format(self.averages[i])*3 + "]"
                i= i+1
                summary += "\n"
                return summary


class X01MatchBuilder:
    def __init__(self):
        pass

    def __call__(self):
        return X01Match()
