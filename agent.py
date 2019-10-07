import random, re, datetime
import copy


class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


class TeamNameMinimaxAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)

        ### START CODE HERE ###
        board = copy.deepcopy(state[1])
        if max([position[0] for position in board.getPlayerPiecePositions(1)]) > min(
                [position[0] for position in board.getPlayerPiecePositions(2)]):
            _, self.action = self.MiniMax_pruned_version(state=(state[0], board), al=-10000, be=10000, depth=0)
        else:
            _, self.action = self.selfMax(state=(state[0], board), depth=0)

    def MiniMax_pruned_version(self, state, depth, al, be, Depth=2):
        if depth != Depth:
            alpha = al
            beta = be
            # print('\t'*depth + "第{}层节点生成，alpha = {}，beta = {}".format(depth, alpha, beta))
            if depth % 2 == 0:  # max layer
                evaluation = -10000
            else:
                evaluation = 10000
            selected_action = None
            legal_actions = self.game.actions(state)
            player = state[0]
            for action in self.stimulation_max(state, legal_actions):
                if action[1][0] * (-1) ** player < action[0][0] * (-1) ** player:
                    continue
                board = state[1]
                board.board_status[action[0]] = 0
                board.board_status[action[1]] = player
                value, next_action = self.MiniMax_pruned_version((3 - player, board), depth + 1, al=alpha, be=beta)
                board.board_status[action[0]] = player
                board.board_status[action[1]] = 0
                if depth % 2 == 0:  # max layer
                    if value > evaluation:
                        evaluation = value
                        selected_action = action
                        alpha = value
                else:  # min layer
                    if value < evaluation:
                        evaluation = value
                        selected_action = action
                        beta = value
                if alpha >= beta:
                    # print('\t'*depth + "Pruned in layer",depth)
                    return evaluation, selected_action
            return evaluation, selected_action
        else:
            evaluation_value = self.evaluation(state, p=2, i=10, d=5)
            return evaluation_value, None

    def selfMax(self, state, depth, Depth=2):
        if depth != Depth:
            evaluation = -10000
            selected_action = None
            legal_actions = self.game.actions(state)
            player = state[0]
            for action in self.stimulation_max(state, legal_actions):
                if action[1][0] * (-1) ** player < action[0][0] * (-1) ** player:
                    continue
                board = state[1]
                board.board_status[action[0]] = 0
                board.board_status[action[1]] = player
                ver_positions = [position[0] for position in board.getPlayerPiecePositions(player)]
                if sum(ver_positions) == (2 - player) * 30 + (player - 1) * 170:
                    board.board_status[action[0]] = player
                    board.board_status[action[1]] = 0
                    return 10000, action
                value, next_action = self.selfMax((player, board), depth + 1)
                board.board_status[action[0]] = player
                board.board_status[action[1]] = 0
                if value > evaluation:
                    evaluation = value
                    selected_action = action
            return evaluation, selected_action
        else:
            evaluation = self.evaluation(state, p=1, i=5, d=0)
            return evaluation, None

    def stimulation_max(self, state, legal_actions):
        player = state[0]
        # board = state[1]
        # 按照纵向最大跳跃距离排序
        max_actions = sorted(legal_actions, key=lambda x: x[0][0] - x[1][0], reverse=True if player == 1 else False)
        return max_actions

    def evaluation(self, state, p, i, d):
        player = state[0]
        board = state[1]

        if player == 1:
            ver_positions = [position[0] for position in board.getPlayerPiecePositions(player)]
            op_p = [position[0] for position in board.getPlayerPiecePositions(3 - player)]
            hor_positions = [abs(position[1] - board.getColNum(position[0]) / 2) / board.getColNum(position[0]) for
                             position in board.getPlayerPiecePositions(player) if position[0] % 2 == 0]

            ver_displacement = sum(ver_positions)
            lagger = 2 * board.size - 1 - max(ver_positions)
            hor_displacement = sum(hor_positions)
        else:
            ver_positions = [2 * board.size - 1 - position[0] for position in board.getPlayerPiecePositions(player)]
            op_p = [2 * board.size - 1 - position[0] for position in board.getPlayerPiecePositions(3 - player)]
            hor_positions = [abs(position[1] - board.getColNum(position[0]) / 2) / board.getColNum(position[0]) for
                             position in board.getPlayerPiecePositions(player) if position[0] % 2 == 0]
            ver_displacement = sum(ver_positions)
            lagger = 2 * board.size - 1 - max(ver_positions)
            hor_displacement = sum(hor_positions)

        return - p * ver_displacement + i * lagger - d * hor_displacement - p * sum(op_p)

        ### END CODE HERE ###

    def h(self, player, board):
        pass
