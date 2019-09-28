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
        _, self.action = self.MiniMax_pruned_version(state=(state[0], board), value_of_last_state=10000, depth=0)

    def MiniMax(self, state, depth, Depth=2):  # MiniMax递归算法
        if depth != Depth:
            evaluation_value = -10000
            selected_action = None
            legal_actions = self.game.actions(state)
            player = state[0]
            for action in self.stimulation_max(state, legal_actions):
                board = copy.deepcopy(state[1])
                board.board_status[action[0]] = 0
                board.board_status[action[1]] = player
                value, next_action = self.MiniMax((3 - player, board), depth + 1)
                if value * ((-1) ** depth) > evaluation_value:  # 这里整合了MAX和MIN两种情况：对于MIN，取最小值即是取其相反数的MAX
                    evaluation_value = value
                    selected_action = action
            return evaluation_value, selected_action
        else:
            evaluation_value = self.evaluation(state, p=1, i=5, d=0)  # hahaha
            return evaluation_value, None

    def MiniMax_pruned_version(self, state, value_of_last_state, depth, Depth=2):
        if depth != Depth:
            evaluation_value = -10000
            value_of_last_state = value_of_last_state  # alpha-beta pruning需要参考前一层的值，因此需添加这个参数
            selected_action = None
            legal_actions = self.game.actions(state)
            player = state[0]
            for action in self.stimulation_max(state, legal_actions):
                board = state[1]
                board.board_status[action[0]] = 0
                board.board_status[action[1]] = player
                value, next_action = self.MiniMax_pruned_version((3 - player, board), evaluation_value, depth + 1)
                board.board_status[action[0]] = player
                board.board_status[action[1]] = 0
                if value * ((-1) ** depth) > evaluation_value:
                    evaluation_value = value
                    selected_action = action
                if value * ((-1) ** depth) > value_of_last_state * (
                        (-1) ** depth):  # alpha-beta pruning的判断条件，同样将MAX与MIN整合在了一起
                    return evaluation_value, selected_action
            return evaluation_value, selected_action
        else:
            evaluation_value = self.evaluation(state, p=1, i=10, d=2)
            return evaluation_value, None

    def stimulation_max(self, state, legal_actions):
        player = state[0]
        # board = state[1]
        # 按照纵向最大跳跃距离排序
        max_actions = sorted(legal_actions, key=lambda x: x[0][0] - x[1][0], reverse=True if player == 1 else False)
        return max_actions

    def evaluation(self, state, p, i, d):  # 目前判断因子包括垂直距离、水平距离、最后一个棋子的距离
        player = state[0]
        board = state[1]

        if player == 1:
            ver_positions = [position[0] for position in board.getPlayerPiecePositions(player)]
            hor_positions = [abs(position[1] - board.getColNum(position[0]) / 2 + 1) / board.getColNum(position[0]) for
                             position in board.getPlayerPiecePositions(player)]
            ver_displacement = sum(ver_positions)
            print(hor_positions)
            lagger = 2 * board.size - 1 - max(ver_positions)
            hor_displacement = sum(hor_positions)

        else:
            ver_positions = [2 * board.size - position[0] for position in board.getPlayerPiecePositions(player)]
            hor_positions = [abs(position[1] - board.getColNum(position[0]) / 2 + 1) / board.getColNum(position[0]) for
                             position in board.getPlayerPiecePositions(player)]
            ver_displacement = sum(ver_positions)
            lagger = min(ver_positions)
            hor_displacement = sum(hor_positions)
        return -p * ver_displacement + i * lagger - d * hor_displacement

        ### END CODE HERE ###
        '''
        第一版代码
        player = self.game.player(state)
        opponent_player = 3 - player
        board = copy.deepcopy(state[1])
        # get max actions for the player:
        # 向前跳一步
        for action in self.stimulation_max((player, board), legal_actions):
            board[action[0]] = 0
            board[action[1]] = player
            # 进入对手的遍历
            # 获得下一步对手的所有合法移动
            legal_actions_of_opponent = self.action((opponent_player, board))
            for action_round2 in self.stimulation_max((opponent_player, board), legal_actions_of_opponent):
                board[action_round2[0]] = 0
                board[action_round2[1]] = opponent_player

                # 进入自己的回合，round3
                legal_actions_of_round3 = self.action((player, board))
                for action_round3 in self.stimulation_max((player, board), legal_actions_of_round3):
                    board[action_round3[0]] = 0
                    board[action_round3[1]] = player
                    #评估，待写
                    # 恢复棋盘以进入下一个for
                    board[action_round3[0]] = player
                    board[action_round3[1]] = 0
                board[action_round2[0]] = opponent_player
                board[action_round2[1]] = 0
            board[action[0]] = player
            board[action[1]] = 0
        '''

    def h(self, player, board):
        pass
