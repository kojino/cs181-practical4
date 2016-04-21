# Imports.
import numpy as np
import numpy.random as npr

from SwingyMonkey import SwingyMonkey


class Learner(object):
    '''
    This agent jumps randomly.
    '''

    def __init__(self):
        self.last_state  = None
        self.last_state_id = None
        self.last_action = None
        self.last_reward = None
        self.alpha = 0.5
        self.gamma = 0.8
        self.Q = np.zeros((600000,2))

    def reset(self):
        self.last_state  = None
        self.last_action = None
        self.last_reward = None

    def action_callback(self, state):
        '''
        Implement this function to learn things and take actions.
        Return 0 if you don't want to jump and 1 if you do.
        '''
        relative_bot = state["monkey"]["bot"] - state["tree"]["bot"]
        relative_top = state["tree"]["top"] - state["monkey"]["top"]
        tree_dist = state["tree"]["dist"]
        if relative_bot < 0:
            relative_bot_bin = str(9)
        else:
            relative_bot_bin = str((relative_bot-relative_bot%40)/40)
        if relative_top < 0:
            relative_top_bin = str(9)
        else:
            relative_top_bin = str((relative_top-relative_top%40)/40)
        tree_dist_bin = (tree_dist-tree_dist%25)/25
        vel = str(state["monkey"]["vel"])
        if tree_dist_bin < 10:
            tree_dist_bin = str(0)+str(tree_dist_bin)
        else:
            tree_dist_bin = str(tree_dist_bin)

        i = int(vel+tree_dist_bin+relative_bot_bin+relative_top_bin)

        # choose the next action a' and Q[s',a']
        if self.Q[i][0] < self.Q[i][1]:
            a = 1
            Q_ = self.Q[i][1]
        elif self.Q[i][0] == self.Q[i][1]:
            a = npr.choice([0,1])
            Q_ = self.Q[i][a]
        else:
            a = 0
            Q_ = self.Q[i][0]

        # update Q[s,a]
        if self.last_state_id != None:
            print "Q is "
            print self.Q[self.last_state_id][self.last_action]
            print "Q_ is " + str(Q_)
            self.Q[self.last_state_id][self.last_action] = (1-self.alpha)*self.Q[self.last_state_id][self.last_action]+self.alpha*(self.last_reward+self.gamma*Q_)
            print "new Q is "
            print self.Q[self.last_state_id][self.last_action]

        # You might do some learning here based on the current state and the last state.

        # You'll need to select and action and return it.
        # Return 0 to swing and 1 to jump.

        new_action = a
        new_state  = state

        self.last_action = new_action
        self.last_state  = new_state
        self.last_state_id = i

        return self.last_action

    def reward_callback(self, reward):
        '''This gets called so you can see what reward you get.'''
        self.last_reward = reward

def run_games(learner, hist, iters = 100, t_len = 100):
    '''
    Driver function to simulate learning by having the agent play a sequence of games.
    '''

    for ii in range(iters):
        # Make a new monkey object.
        swing = SwingyMonkey(sound=False,                  # Don't play sounds.
                             text="Epoch %d" % (ii),       # Display the epoch on screen.
                             tick_length = t_len,          # Make game ticks super fast.
                             action_callback=learner.action_callback,
                             reward_callback=learner.reward_callback)

        # Loop until you hit something.
        while swing.game_loop():
            print learner.Q
            pass

        # Save score history.
        hist.append(swing.score)

        # Reset the state of the learner.
        learner.reset()
        print learner.Q
        print "iter is " + str(ii)

    return


if __name__ == '__main__':

	# Select agent.
	agent = Learner()

	# Empty list to save history.
	hist = []

	# Run games.
	run_games(agent, hist, 20, 10)

	# Save history.
	np.save('hist',np.array(hist))


