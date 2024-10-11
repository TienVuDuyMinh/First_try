import numpy as np

# Hyperparameters
learning_rate = 0.1        # Alpha - Learning rate
discount_factor = 0.95     # Gamma - Discount factor
exploration_rate = 1.0     # Epsilon - Exploration rate
epsilon_min = 0.01         # Minimum epsilon
epsilon_decay = 0.995      # Epsilon decay rate
episodes = 1000            # Total number of episodes
max_steps_per_episode = 100 # Maximum steps per episode


class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = np.zeros((state_size, action_size))

    def encode_state(self, state):
        """
        Chuyển đổi trạng thái thành chỉ số duy nhất nếu cần thiết.
        Trong trường hợp này, chỉ cần trả về state đã mã hóa mà không cần giải nén.
        """
        # Vì state đã là một số nguyên (int) nên không cần giải nén nữa
        return state  # Trả về state đã được mã hóa

    def choose_action(self, state):
        # Mã hóa state nếu cần thiết
        state_index = self.encode_state(state)

        # Chọn hành động
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # Chọn hành động ngẫu nhiên
        else:
            return np.argmax(self.q_table[state_index])  # Chọn hành động có Q-value cao nhất

    def learn(self, state, action, reward, next_state, done):
        # Mã hóa state và next_state nếu cần thiết
        state_index = self.encode_state(state)
        next_state_index = self.encode_state(next_state)

        # Tính Q-value hiện tại
        current_q = self.q_table[state_index, action]

        # Tính giá trị Q-value mục tiêu
        max_future_q = np.max(self.q_table[next_state_index])
        target_q = reward + (self.gamma * max_future_q * (1 - done))

        # Cập nhật Q-value
        self.q_table[state_index, action] = (1 - self.learning_rate) * current_q + self.learning_rate * target_q

        # Giảm epsilon (tốc độ giảm exploration)
        if done:
            self.epsilon *= self.epsilon_decay

class SarsaAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = np.zeros((state_size, action_size))

    def choose_action(self, state):
        # Chọn hành động bằng epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # Chọn hành động ngẫu nhiên
        else:
            return np.argmax(self.q_table[state])  # Chọn hành động có Q-value cao nhất

    def learn(self, state, action, reward, next_state, next_action, done):
        # SARSA cập nhật Q-value bằng cách sử dụng hành động tiếp theo đã chọn
        current_q = self.q_table[state, action]
        next_q = self.q_table[next_state, next_action]
        target_q = reward + self.gamma * next_q * (1 - done)
        self.q_table[state, action] = (1 - self.learning_rate) * current_q + self.learning_rate * target_q

        if done:
            # Giảm dần epsilon theo thời gian
            self.epsilon *= self.epsilon_decay


class MonteCarloAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.995):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.q_table = np.zeros((state_size, action_size))
        self.returns = {}  # Dictionary để lưu trữ returns cho mỗi cặp (state, action)

    def choose_action(self, state):
        # Chọn hành động bằng epsilon-greedy policy
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # Chọn hành động ngẫu nhiên
        else:
            return np.argmax(self.q_table[state])  # Chọn hành động có Q-value cao nhất

    def learn(self, episode):
        """
        Hàm học từ một tập episode.
        Mỗi episode là một danh sách các tuple (state, action, reward).
        """
        G = 0
        visited_state_action_pairs = set()
        
        # Duyệt ngược qua episode để cập nhật Q-value
        for state, action, reward in reversed(episode):
            G = self.gamma * G + reward  # Tính tổng discounted return

            # Nếu cặp (state, action) chưa từng được thêm vào trong episode này
            if (state, action) not in visited_state_action_pairs:
                # Thêm cặp (state, action) vào set đã ghé thăm
                visited_state_action_pairs.add((state, action))

                # Cập nhật danh sách returns cho cặp (state, action)
                if (state, action) not in self.returns:
                    self.returns[(state, action)] = []
                self.returns[(state, action)].append(G)

                # Cập nhật Q-value cho cặp (state, action)
                self.q_table[state, action] = np.mean(self.returns[(state, action)])

        # Giảm dần epsilon theo thời gian
        self.epsilon *= self.epsilon_decay


