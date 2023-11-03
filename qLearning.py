import subprocess
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import time
from pathlib import Path

parameter_space = {
       "vm.swappiness": {
        "min": 0,
        "max": 100
    }
}

# Q-table
q_tables = {param: np.zeros((parameter_space[param]["max"] + 1, 2)) for param in parameter_space}

# Q-learning parameters
learning_rate = 0.1
discount_factor = 0.9
exploration_prob = 0.3
num_episodes = 5 

average_tps_per_episode = []
tps_per_ep = []

# Q-learning algorithm
for episode in tqdm(range(num_episodes), desc="Training Episodes"):
    
    current_params = {param: np.random.randint(parameter_space[param]["min"], parameter_space[param]["max"] + 1)
                      for param in parameter_space}

    done = False
    episode_rewards = [] 

    while not done:
        # Exploration vs. exploitation
        if np.random.uniform(0, 1) < exploration_prob:
            action = {param: np.random.choice([-1, 1]) for param in parameter_space}  # Exploration
        else:
            action = {param: 1 if q_tables[param][current_params[param]][1] > q_tables[param][current_params[param]][0] else -1
                      for param in parameter_space}  # Exploitation

        new_params = {param: max(parameter_space[param]["min"], min(parameter_space[param]["max"], current_params[param] + action[param]))
                      for param in parameter_space}

        try:
           
            for param, value in new_params.items():
                subprocess.Popen(f"sudo sysctl {param}={value} > /dev/null 2>&1", shell=True).wait()
            subprocess.Popen("nohup ./script.sh > script_output.log 2>&1 &", shell=True).wait()
            print("1")
            file_path = Path('/home/ccbd/tuneos/mathangi/resultss/execute_execute.tsv')
            max_wait_time = 200  
            wait_interval = 5  
            waited_time = 0
            time.sleep(200)
            while not file_path.is_file():
                if waited_time >= max_wait_time:
                    print("Timeout: File not found.")
                    break
                time.sleep(wait_interval)
                waited_time += wait_interval

            cum_tps_values = []
            benchmark_files = ["/home/ccbd/tuneos/mathangi/resultss/execute_execute.tsv"]
            print("2")
            for file in benchmark_files:
                with open(file, 'r') as f:
                    lines = f.readlines()
                    if len(lines) > 1:
                     
                        for line in lines[1:]:
                            try: 
                                cum_tps = float(line.split()[1])
                            except: 
                                cum_tps = 0
                            cum_tps_values.append(cum_tps)

            if cum_tps_values:
                avg_cum_tps = sum(cum_tps_values) / len(cum_tps_values)
                reward = avg_cum_tps
            else:
                reward = 0

            episode_rewards.append(reward)
            print(reward)
            # Update Q-table
            for param in parameter_space:
                current_idx = current_params[param]
                action_idx = 1 if action[param] == 1 else 0
                q_tables[param][current_idx][action_idx] += learning_rate * (reward + discount_factor * np.max(q_tables[param][current_idx]) - q_tables[param][current_idx][action_idx])

            current_params = new_params

            if all(value == parameter_space[param]["min"] or value == parameter_space[param]["max"] for param, value in current_params.items()):
                done = True
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            reward = 0

    average_reward = sum(episode_rewards) / len(episode_rewards)
    tps_per_ep.append(average_reward)

plt.plot(range(len(tps_per_ep)), tps_per_ep, label='Average TPS')
plt.xlabel('Episodes')
plt.ylabel('Average TPS')
plt.title('Average TPS Over Episodes')
plt.legend()
plt.savefig("file.png")

optimal_params = {param: np.argmax(q_tables[param], axis=1) for param in parameter_space}

print("Optimal Parameters:")
for param, values in optimal_params.items():
    print(f"{param}: {values}")
