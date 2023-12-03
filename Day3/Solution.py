from SolverBase import SolverBase


class EnginePartNumber:
    def __init__(self, value, start_index, end_index):
        self.value = value
        self.start_index = start_index
        self.end_index = end_index


class EngineInstructionLine:
    def __init__(self, string_raw):
        self.current_digit = None
        self.prev_instruction_line = None
        self.next_instruction_line = None
        self.symbol_indices = []
        self.part_number_values = []

        self.init_digit_tracking()
        for counter in range(0, len(string_raw)):
            if string_raw[counter] == ".":
                if self.prev_is_digit:
                    self.update_digit_tracking(counter)

            elif string_raw[counter].isdigit():
                self.digit_start = counter if not self.prev_is_digit else self.digit_start
                self.current_digit += string_raw[counter]
                self.prev_is_digit = True
                continue

            elif self.prev_is_digit:
                self.update_digit_tracking(counter)
                self.symbol_indices.append(counter)

            else:
                self.symbol_indices.append(counter)

        if self.prev_is_digit:
            self.update_digit_tracking(len(string_raw))

    def update_digit_tracking(self, current_index):
        self.part_number_values.append(EnginePartNumber(self.current_digit, self.digit_start, current_index - 1))
        self.init_digit_tracking()

    def init_digit_tracking(self):
        self.current_digit = ''
        self.prev_is_digit = False
        self.digit_start = 0

    def get_valid_part_numbers(self):
        return [num for num in self.part_number_values if self.has_adjacent_symbols(num) or
                EngineInstructionLine.has_adjacent_neighbor_symbols(num, self.prev_instruction_line) or
                EngineInstructionLine.has_adjacent_neighbor_symbols(num, self.next_instruction_line)]

    def has_adjacent_symbols(self, number):
        if number.start_index - 1 in self.symbol_indices or number.end_index + 1 in self.symbol_indices:
            return True
        else:
            return False

    @staticmethod
    def has_adjacent_neighbor_symbols(number, adjacent_instruction_line):
        if adjacent_instruction_line is None:
            return False

        for counter in range(number.start_index - 1, number.end_index + 2):
            if counter in adjacent_instruction_line.symbol_indices:
                return True

        return False


class EngineInstruction:

    def __init__(self, instruction_lines):
        for counter in range(0, len(instruction_lines)):
            if counter != 0:
                instruction_lines[counter].prev_instruction_line = instruction_lines[counter - 1]
            if counter != len(instruction_lines) - 1:
                instruction_lines[counter].next_instruction_line = instruction_lines[counter + 1]

        self.instruction_lines = instruction_lines

    def get_valid_instruction_numbers(self):
        return [num for line in self.instruction_lines for num in line.get_valid_part_numbers()]


class Day3Problem1(SolverBase):

    def solve(self):
        instruction_lines = list(map(lambda line: EngineInstructionLine(line), self.input_data))
        engine_instructions = EngineInstruction(instruction_lines)
        result = [int(num.value) for num in engine_instructions.get_valid_instruction_numbers()]
        print(sum(result))

test = Day3Problem1("Input.txt")
test.solve()
