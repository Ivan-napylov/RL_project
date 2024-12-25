import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from collections import deque
import random

class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, action_dim)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        return self.fc3(x)

class DQNAgent:
    def __init__(self, state_dim, action_dim, learning_rate=1e-3, gamma=0.99, epsilon=0.01, batch_size=32, buffer_size=10000):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size
        self.buffer_size = buffer_size
        self.memory = deque(maxlen=buffer_size)
        
        # Create the Q-network
        self.q_network = QNetwork(state_dim, action_dim)
        self.target_network = QNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)

        # Initialize the target network weights to match Q-network
        self.target_network.load_state_dict(self.q_network.state_dict())

    def select_action(self, state):
        if np.random.rand() < self.epsilon:
            # Explore: Random action
           return random.randint(0, self.action_dim - 1)
        else:
            # Exploit: Select action with highest Q-value
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.q_network(state_tensor)
            return torch.argmax(q_values).item()

    def store_experience(self, state, action, reward, next_state, done):
        # Ensure state and next_state are numpy arrays of consistent shape and 2D
        self.memory.append((state, action, reward, next_state, done))
        # state = np.array(state).reshape(1, -1)  # Convert state to 2D (1, 274) if it's 1D
        # next_state = np.array(next_state).reshape(1, -1)  # Same for next_state

        # # Store the experience as a tuple
        # experience = (state, action, reward, next_state, done)
        
        # # Append the experience to memory
        # self.memory.append(experience)
        # if len(self.memory) > self.buffer_size:
        #     self.memory.pop(0)  # Remove the oldest experience if memory exceeds buffer size


    def sample_experience(self):
        if len(self.memory) < self.batch_size:
            return []
        # flattened_memory = np.array([np.concatenate(m) for m in self.memory])
        memory_batch = random.sample(self.memory, self.batch_size)
        # memory_batch = np.random.choice(flattened_memory, self.batch_size, replace=False)
        
        # Extract individual components from the batch
        states, actions, rewards, next_states, dones = zip(*memory_batch)

        # Convert each component into tensors
        states = torch.FloatTensor(np.vstack(states))  # Stack states into 2D tensor
        actions = torch.LongTensor(actions)
        rewards = torch.FloatTensor(rewards)
        next_states = torch.FloatTensor(np.vstack(next_states))  # Stack next_states into 2D tensor
        dones = torch.FloatTensor(dones)

        return states, actions, rewards, next_states, dones

    def train(self):
        if len(self.memory) < self.batch_size:
            return

        batch = self.sample_experience()
        states, actions, rewards, next_states, dones = batch

        states = torch.tensor(states, dtype=torch.float32)
        actions = torch.tensor(actions, dtype=torch.int64)
        rewards = torch.tensor(rewards, dtype=torch.float32)
        next_states = torch.tensor(next_states, dtype=torch.float32)
        dones = torch.tensor(dones, dtype=torch.bool)

        # Compute the Q-values using the Q-network
        q_values = self.q_network(states)
        q_value = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)

        # Compute the target Q-values using the target network
        next_q_values = self.target_network(next_states)
        next_q_value = next_q_values.max(dim=1)[0]
        target_q = rewards + (self.gamma * next_q_value * (~dones))

        # Compute the loss (Mean Squared Error)
        loss = F.mse_loss(q_value, target_q)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        print("Loss", loss)
        # Update the target network periodically
        self.update_target_network()

    def update_target_network(self):
        # Update the target network with the Q-network's weights
        self.target_network.load_state_dict(self.q_network.state_dict())
    
    def save_weights(self, filename):
        # Save the Q-network weights
        torch.save(self.q_network.state_dict(), filename)
        # Optionally save the target network weights as well
        torch.save(self.target_network.state_dict(), filename.replace('.pth', '_target.pth'))

    def load_weights(self, filename):
        # Load the Q-network weights
        self.q_network.load_state_dict(torch.load(filename))
        # Load the target network weights if available
        self.target_network.load_state_dict(torch.load(filename.replace('.pth', '_target.pth')))