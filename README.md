# Othello Game

Othello.py can be run to play a human vs greedy algorithm (computer) game.

The Othello game is further trained using Reinforcement Learning using PPO and A2C models. 

The notebooks PPO.ipynb and A2C.ipynb contain code for both training and evaluating the Othello game using the respective algorithms.

Run the Othello_PPO_human.ipynb file to play against the PPO model, and Othello_A2C_human.ipynb file to play against the A2C model. 
Run Othello_PPO_vs_A2C_human.ipynb file to watch the PPO and A2C models play aginst each other. Both the models have nearly the same performance.

### Installations

Install the following packages to run the code.

```bash
pip3 install pygame gym glob2 stable-baselines3 sb3-contrib numpy pettingzoo typing torch torchvision
```
