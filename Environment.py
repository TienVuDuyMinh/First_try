class SokobanEnvironment:
    def __init__(self, level):
        self.level = level  # Gán trực tiếp bản đồ
        self.agent_pos = self.find_agent()
        self.boxes = self.find_boxes()
        self.goals = self.find_goals()

    def find_agent(self):
        for i, row in enumerate(self.level):
            for j, cell in enumerate(row):
                if cell == 'A':  # Tìm agent
                    return (i, j)
        raise ValueError("Agent not found in the level.")

    def find_boxes(self):
        return [(i, j) for i, row in enumerate(self.level) for j, cell in enumerate(row) if cell == 'B']

    def find_goals(self):
        return [(i, j) for i, row in enumerate(self.level) for j, cell in enumerate(row) if cell == 'T']

    def is_move_valid(self, new_pos):
        i, j = new_pos
        if self.level[i][j] in ['#']:  # Kiểm tra tường
            return False
        if self.level[i][j] == 'B':  # Nếu là hộp, cần kiểm tra vị trí tiếp theo
            next_pos = (i + (1 if self.agent_pos[0] < i else -1 if self.agent_pos[0] > i else 0),
                         j + (1 if self.agent_pos[1] < j else -1 if self.agent_pos[1] > j else 0))
            if self.level[next_pos[0]][next_pos[1]] in ['#', 'B']:
                return False
        return True

    def move_agent(self, direction):
        new_pos = self.calculate_new_position(direction)
        if self.is_move_valid(new_pos):
            if self.level[new_pos[0]][new_pos[1]] == 'B':  # Nếu di chuyển vào hộp
                next_pos = (new_pos[0] + (1 if self.agent_pos[0] < new_pos[0] else -1 if self.agent_pos[0] > new_pos[0] else 0),
                             new_pos[1] + (1 if self.agent_pos[1] < new_pos[1] else -1 if self.agent_pos[1] > new_pos[1] else 0))
                # Cập nhật hộp sang vị trí mới
                row = list(self.level[next_pos[0]])
                row[next_pos[1]] = 'B'
                self.level[next_pos[0]] = ''.join(row)

            # Cập nhật vị trí mới của agent
            self.agent_pos = new_pos
            self.update_level()

    def calculate_new_position(self, direction):
        i, j = self.agent_pos
        if direction == 'up':
            return (i - 1, j)
        elif direction == 'down':
            return (i + 1, j)
        elif direction == 'left':
            return (i, j - 1)
        elif direction == 'right':
            return (i, j + 1)

    def update_level(self):
        # Xóa vị trí cũ của agent
        old_row = list(self.level[self.agent_pos[0]])
        old_row[self.agent_pos[1]] = ' '
        self.level[self.agent_pos[0]] = ''.join(old_row)

        # Cập nhật vị trí mới của agent
        new_row = list(self.level[self.agent_pos[0]])
        new_row[self.agent_pos[1]] = 'A'
        self.level[self.agent_pos[0]] = ''.join(new_row)

    def display(self):
        for row in self.level:
            print(row)

    def check_win(self):
        return all(self.level[i][j] == 'T' for i, j in self.boxes)
    
    def reset(self):
        """
        Đặt lại môi trường về trạng thái ban đầu.
        Trả về trạng thái khởi tạo ban đầu của môi trường.
        """
        self.agent_pos = self.find_agent()
        self.boxes = self.find_boxes()
        return (self.agent_pos, self.boxes)  # Trả về trạng thái hiện tại

    def step(self, action):
        """
        Thực hiện hành động và cập nhật môi trường.
        Trả về: next_state, reward, done.
        """
        # Chuyển đổi hành động thành vị trí mới
        direction_map = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        direction = direction_map[action]

        # Di chuyển agent
        self.move_agent(direction)

        # Cập nhật trạng thái mới sau khi di chuyển
        next_state = self.encode_state()  # Mã hóa trạng thái mới

        # Tính phần thưởng (phần thưởng tùy theo tiêu chí bạn đặt ra)
        reward = -1  # Ví dụ: phạt -1 cho mỗi bước đi

        # Kiểm tra điều kiện kết thúc
        done = self.check_win()

        if done:
            reward = 100  # Phần thưởng lớn khi hoàn thành level

        return next_state, reward, done

    def state_space_size(self):
        """
        Trả về kích thước không gian trạng thái dựa trên kích thước level.
        Sử dụng số lượng vị trí có thể cho agent và các hộp.
        """
        # Tính toán số lượng trạng thái có thể của môi trường dựa trên kích thước level
        n = len(self.level)
        m = len(self.level[0])
        return n * m + len(self.boxes) * n * m  # Số trạng thái dựa trên vị trí agent và vị trí hộp

    def encode_state(self):
        """
        Mã hóa trạng thái thành một chỉ số duy nhất.
        """
        # Mã hóa vị trí của agent và các hộp thành một chuỗi duy nhất
        agent_pos_code = self.agent_pos[0] * len(self.level[0]) + self.agent_pos[1]  # Mã hóa vị trí của agent

        # Mã hóa vị trí của các hộp thành một chuỗi
        box_code = 0
        for (i, j) in self.boxes:
            box_code += i * len(self.level[0]) + j

        # Tổng hợp mã hóa của trạng thái
        return agent_pos_code + box_code



# Ví dụ khởi tạo
if __name__ == "__main__":
    MAPS = {
        "level_1": [
            "##########",
            "##########",
            "##########",
            "##########",
            "#A B   T #",
            "##########",
            "##########",
            "##########",
            "##########",
            "##########",
        ],
        "level_2": [
            "##########",
            "##########",
            "##########",
            "##########",
            "#  B   T #",
            "#A       #",
            "##########",
            "##########",
            "##########",
            "##########",
        ],
        "level_3": [
            "##########",
            "##########",
            "##########",
            "#      T #",
            "#  B     #",
            "#A       #",
            "##########",
            "##########",
            "##########",
            "##########",
        ],
    }

    game = SokobanEnvironment(MAPS['level_1'])  # Sử dụng bản đồ từ MAPS
    game.display()
    if game.check_win():
        print("You win!")
