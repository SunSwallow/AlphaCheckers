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
                    """
                    评估，待写
                    """
                    # 恢复棋盘以进入下一个for
                    board[action_round3[0]] = player
                    board[action_round3[1]] = 0
                board[action_round2[0]] = opponent_player
                board[action_round2[1]] = 0
            board[action[0]] = player
            board[action[1]] = 0



        ### START CODE HERE ###

    def stimulation_max(self, state, legal_actions):
        player = state[0]
        board = state[1]
        # 按照纵向最大跳跃距离排序
        max_actions = sorted(legal_actions, key=lambda x: x[0][0] - x[1][0], reverse=True if player == 1 else False)
        return max_actions

    def actions(self, state):
        action_list = []
        player = state[0]
        board = state[1]
        player_piece_pos_list = board.getPlayerPiecePositions(player)
        for pos in player_piece_pos_list:
            for adj_pos in board.adjacentPositions(pos):
                if board.isEmptyPosition(adj_pos):
                    action_list.append((pos, adj_pos))

        for pos in player_piece_pos_list:
            boardCopy = copy.deepcopy(board)
            boardCopy.board_status[pos] = 0
            for new_pos in boardCopy.getAllHopPositions(pos):
                if (
                        pos, new_pos) not in action_list:
                    action_list.append((pos, new_pos))

        return action_list

    def h(self, player, board):
        pass
        ### END CODE HERE ###
