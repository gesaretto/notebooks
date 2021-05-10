#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fuzzywuzzy import fuzz
from fuzzywuzzy import process


# In[2]:


import pickle
import random
jeopardy_questions = pickle.load(open("jeopardy_questions.p", "rb"))
double_jeopardy_questions = pickle.load(open("double_jeopardy_questions.p", "rb"))
final_jeopardy_questions = pickle.load(open("final_jeopardy_questions.p", "rb"))
tiebreaker_questions = pickle.load(open("tiebreaker_questions.p", "rb"))


# In[117]:


class JeopardyBot:
    
    asked_questions = ["Goof?"]
    exit_commands = ["quit", "bye", "exit", "goodbye", "no"]
    yes_commands = ["yes", "y", "yeah", "yay"]
    players = {}
    quit_game = False
    
    def start_game(self):
        answer = input("""*** JEOPARDY! ***

Hello, welcome to Jeopardy! Would you like to play? (Type "yes" or "no.") \n> """)

        while answer in self.yes_commands:
            self.pick_players()
            if self.quit_game == True:
                return
            self.play_game(self.players)
            if self.quit_game == True:
                return
            answer = input("\nWould you like to play again?\n> ")
        print("\nThank you for playing!\n")
    
    def play_game(self, players):
        self.quit_game = False
        for game_round in range(4):
            for player in self.players:
                print("\nRound " + str(game_round) + " of 4 for " + self.players[player][0] + ".")
                self.play_round(player)
                if self.quit_game == True:
                    return
        print("\n*** FINAL ROUND ***\n")
        for player in self.players:
            print("\nFinal round for " + self.players[player][0] + ":\n")
            self.players[player][1] += self.ask_question(final_jeopardy_questions)
            print("\n" + self.players[player][0] + ", your final prize is: " + str(self.players[player][1]) + ".\n")            
            
    
    def play_round(self, player):
        questions_round = "0"
        while (questions_round.isdecimal() and int(questions_round) in [1, 2]) == False:
            questions_round = input("""\nPick the type of round that you would like to play by typing 1 or 2:
            
            1. Jeopardy! (regular questions, regular prizes and losses)
            2. Double Jeopardy! (harder questions, prizes and losses are doubled)

You can quit at any time by typing "quit."

> """)
            if self.make_exit(questions_round):
                return
        if questions_round == "1":
            prize = self.ask_question(jeopardy_questions)
            if self.quit_game == True:
                return
            self.players[player][1] += prize
        elif questions_round == "2":
            prize = self.ask_question(double_jeopardy_questions)
            if self.quit_game == True:
                return
            self.players[player][1] += prize            
        print("\n" + self.players[player][0] + ", your total prize is now " + str(self.players[player][1]) + ".\n")
        return   
        
    def make_exit(self, user_input):
        if str(user_input).lower() in self.exit_commands:
            print("\nThanks for playing, see you soon!\n")
            self.quit_game = True
            return True
        else:
            return False
    
    def pick_players(self):
        number_of_players = "0"
        while (number_of_players.isdecimal() and int(number_of_players) > 0) == False:
            number_of_players = input("\nPlease enter the number of players.\n> ")
            if self.make_exit(number_of_players):
                return
        for player in range(1, int(number_of_players) + 1):
            player_name = input("\nPlease enter the name of player number " + str(player) + ".\n> ")
            if self.make_exit(player_name):
                return
            self.players[player] = [player_name, 1000]
    
    def ask_question(self, questions_round):
        question = "Goof?"
        random_categories = random.choices(list(questions_round), k=3)
        choice = "0"
        while (choice.isdecimal() == False) or (int(choice) not in list(range(1, 4))):
            choice = input("""\nPick a category by typing 1, 2, or 3:
    
    1. {option_1}
    2. {option_2}
    3. {option_3}
    
    Type "quit" at any time to quit the game.
    
> """.format(
                option_1 = random_categories[0],
                option_2 = random_categories[1],
                option_3 = random_categories[2]
            ))
            if self.make_exit(choice):
                return
        while question in self.asked_questions:
            prize, question, right_answer = random.choice(questions_round[random_categories[int(choice) - 1]])
        self.asked_questions.append(question)
        answer = input(question + "\n> ")
        if self.check_answer(answer, right_answer):
            print("\nYes! The answer was " + right_answer + ". You win $" + str(int(prize)) + "!\n")
            return prize
        else:
            print("\nNo, the answer was " + right_answer + ". Sorry! You lose $" + str(int(prize)) + "!\n")
            return 0 - prize
    
    def check_answer(self, answer, right_answer):
        if fuzz.token_set_ratio(answer, right_answer) > 80:
            return True
        else:
            return False


# In[118]:


play_jeopardy = JeopardyBot()
play_jeopardy.start_game()

