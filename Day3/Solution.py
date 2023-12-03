from SolverBase import SolverBase


class Gear:
    def __init__(self, index):
        self.index = index
        self.adjacent_parts = []


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
        self.part_numbers = []
        self.gears = []

        self.init_digit_tracking()
        for counter in range(0, len(string_raw)):
            if string_raw[counter] == "*":
                self.gears.append(Gear(counter))

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

        # don't forget end of the line in case the previous was a digit
        if self.prev_is_digit:
            self.update_digit_tracking(len(string_raw))

    def update_digit_tracking(self, current_index):
        self.part_numbers.append(EnginePartNumber(self.current_digit, self.digit_start, current_index - 1))
        self.init_digit_tracking()

    def init_digit_tracking(self):
        self.current_digit = ''
        self.prev_is_digit = False
        self.digit_start = 0

    def get_valid_part_numbers(self):
        return [part for part in self.part_numbers if self.has_adjacent_symbols(part) or
                EngineInstructionLine.has_adjacent_neighbor_symbols(part, self.prev_instruction_line) or
                EngineInstructionLine.has_adjacent_neighbor_symbols(part, self.next_instruction_line)]

    def has_adjacent_symbols(self, part):
        if part.start_index - 1 in self.symbol_indices or part.end_index + 1 in self.symbol_indices:
            return True
        else:
            return False

    @staticmethod
    def has_adjacent_neighbor_symbols(part, adjacent_instruction_line):
        if adjacent_instruction_line is None:
            return False

        for counter in range(part.start_index - 1, part.end_index + 2):
            if counter in adjacent_instruction_line.symbol_indices:
                return True

        return False

    def get_valid_gears(self):
        valid_parts = self.get_valid_part_numbers()
        for gear in self.gears:
            for part in valid_parts:
                if gear.index + 1 == part.start_index or gear.index - 1 == part.end_index:
                    gear.adjacent_parts.append(part)

            EngineInstructionLine.update_gear_with_adjacent_parts(gear, self.prev_instruction_line)
            EngineInstructionLine.update_gear_with_adjacent_parts(gear, self.next_instruction_line)

        return [gear for gear in self.gears if len(gear.adjacent_parts) == 2]

    @staticmethod
    def update_gear_with_adjacent_parts(gear, adjacent_instruction_line):
        valid_parts = adjacent_instruction_line.get_valid_part_numbers() if adjacent_instruction_line is not None else []
        for part in valid_parts:
            if gear.index in range(part.start_index - 1, part.end_index + 2):
                gear.adjacent_parts.append(part)


class EngineInstruction:

    def __init__(self, instruction_lines):
        for counter in range(0, len(instruction_lines)):
            if counter != 0:
                instruction_lines[counter].prev_instruction_line = instruction_lines[counter - 1]
            if counter != len(instruction_lines) - 1:
                instruction_lines[counter].next_instruction_line = instruction_lines[counter + 1]

        self.instruction_lines = instruction_lines

    def get_valid_part_numbers(self):
        return [part for line in self.instruction_lines for part in line.get_valid_part_numbers()]

    def get_valid_gears(self):
        return [gear for line in self.instruction_lines for gear in line.get_valid_gears()]


class Day3Problem1(SolverBase):

    def solve(self):
        instruction_lines = list(map(lambda line: EngineInstructionLine(line), self.input_data))
        engine_instructions = EngineInstruction(instruction_lines)
        result = [int(num.value) for num in engine_instructions.get_valid_part_numbers()]
        print(sum(result))


class Day3Problem2(SolverBase):

    def solve(self):
        instruction_lines = list(map(lambda line: EngineInstructionLine(line), self.input_data))
        engine_instructions = EngineInstruction(instruction_lines)
        result = [int(gear.adjacent_parts[0].value) * int(gear.adjacent_parts[1].value) for gear in
                  engine_instructions.get_valid_gears()]
        print(sum(result))


problem1 = Day3Problem1("Input.txt")
problem1.solve()

problem2 = Day3Problem2("Input.txt")
problem2.solve()
