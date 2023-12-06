from SolverBase import SolverBase


class SparceMapEntry:
    def __init__(self, string_raw):
        split_string = string_raw.split()
        self.destination_start = int(split_string[0])
        self.source_start = int(split_string[1])
        self.length = int(split_string[2])

        self.destination_end_exclusive = self.destination_start + self.length
        self.source_end_exclusive = self.source_start + self.length


class SparseMap:
    def __init__(self, map_entries, name="none"):
        self.map_entries = sorted(map_entries, key=lambda entry: entry.source_start)
        self.name = name

    def get_destination(self, source):
        for entry in self.map_entries:
            if entry.source_start <= source < entry.source_start + entry.length:
                return entry.destination_start + (source - entry.source_start)

        return source

    def get_destination_ranges_for_list(self, source_list):
        destination_ranges = []
        for (source_start, source_end_exclusive) in source_list:
            destination_ranges.extend(self.get_destination_ranges(source_start, source_end_exclusive))

        return destination_ranges

    def get_destination_ranges(self, source_start, source_end_exclusive):
        destination_ranges = []
        print("Source Start : {} Source End Exclusive {}".format(source_start, source_end_exclusive))
        for entry in self.map_entries:
            if entry.source_start <= source_start:
                offset = (source_start - entry.source_start)
                destination_start = entry.destination_start + offset
                # we are happy entry range contains full lookup range
                if entry.source_end_exclusive >= source_end_exclusive:
                    destination_end_exclusive = destination_start + source_end_exclusive - source_start
                    print("Destination Start {} Destination End Exclusive {}".format(destination_start,
                                                                                     destination_end_exclusive))
                    destination_ranges.append((destination_start, destination_end_exclusive))
                    source_start = source_end_exclusive
                    break
                elif entry.source_end_exclusive > source_start:
                    destination_end_exclusive = entry.destination_end_exclusive
                    source_start = entry.source_end_exclusive
                    if destination_end_exclusive - destination_start > 0:
                        print("Destination Start {} Destination End Exclusive {}".format(destination_start,
                                                                                         destination_end_exclusive))
                        destination_ranges.append((destination_start, destination_end_exclusive))
                    continue
            elif entry.source_start < source_end_exclusive:
                destination_start = entry.destination_start
                if entry.source_end_exclusive >= source_end_exclusive:
                    destination_end_exclusive = destination_start + source_end_exclusive - entry.source_start
                    print("Destination Start {} Destination End Exclusive {}".format(destination_start,
                                                                                     destination_end_exclusive))
                    destination_ranges.append((destination_start, destination_end_exclusive))
                    source_end_exclusive = entry.source_start
                    break
                else:
                    destination_end_exclusive = entry.destination_end_exclusive

                    if destination_end_exclusive - destination_start > 0:
                        print("Destination Start {} Destination End Exclusive {}".format(destination_start,
                                                                                         destination_end_exclusive))
                        destination_ranges.append((destination_start, destination_end_exclusive))

                    source_start = entry.source_end_exclusive
                    continue

        if source_end_exclusive - source_start >= 1:
            print("Destination Start {} Destination End Exclusive {}".format(source_start,
                                                                             source_end_exclusive))
            destination_ranges.append((source_start, source_end_exclusive))

        return destination_ranges


class SeedsMapper:

    def __init__(self, input_lines, seeds_parser=None):
        self.seeds = []
        self.seed_to_soil = None
        self.soil_to_fertilizer = None
        self.fertilizer_to_water = None
        self.water_to_light = None
        self.light_to_temperature = None
        self.temperature_to_humidity = None
        self.humidity_to_location = None
        self.all_maps = []

        seeds_parser = seeds_parser if seeds_parser is not None else lambda current_seeds: [int(seed) for seed in
                                                                                            current_seeds]
        self.parse_input([line for line in input_lines if line.strip()], seeds_parser)

    def parse_input(self, input_lines, seeds_parser):
        counter = 0
        while counter < len(input_lines):
            current_line = input_lines[counter]

            if current_line.startswith("seeds"):
                current_seeds = current_line.split(":")[1].strip().split()
                self.seeds.extend(seeds_parser(current_seeds))
                counter += 1

            elif current_line.startswith("seed-to-soil map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.seed_to_soil = self.create_map(input_lines[counter + 1:end_index])
                self.seed_to_soil.name = "seed to soil"
                self.all_maps.append(self.seed_to_soil)
                counter = end_index

            elif current_line.startswith("soil-to-fertilizer map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.soil_to_fertilizer = self.create_map(input_lines[counter + 1:end_index])
                self.soil_to_fertilizer.name = "soil to fert"
                self.all_maps.append(self.soil_to_fertilizer)
                counter = end_index

            elif current_line.startswith("fertilizer-to-water map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.fertilizer_to_water = self.create_map(input_lines[counter + 1:end_index])
                self.fertilizer_to_water.name = "fert to water"
                self.all_maps.append(self.fertilizer_to_water)
                counter = end_index

            elif current_line.startswith("water-to-light map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.water_to_light = SeedsMapper.create_map(input_lines[counter + 1:end_index])
                self.water_to_light.name = "water to light"
                self.all_maps.append(self.water_to_light)
                counter = end_index

            elif current_line.startswith("light-to-temperature map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.light_to_temperature = SeedsMapper.create_map(input_lines[counter + 1:end_index])
                self.light_to_temperature.name = "light to temp"
                self.all_maps.append(self.light_to_temperature)
                counter = end_index

            elif current_line.startswith("temperature-to-humidity map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.temperature_to_humidity = SeedsMapper.create_map(input_lines[counter + 1:end_index])
                self.temperature_to_humidity.name = "temp to humidity"
                self.all_maps.append(self.temperature_to_humidity)
                counter = end_index

            elif current_line.startswith("humidity-to-location map"):
                end_index = SeedsMapper.get_end_of_section(input_lines, counter)
                self.humidity_to_location = SeedsMapper.create_map(input_lines[counter + 1:end_index])
                self.humidity_to_location.name = "humidity to location"
                self.all_maps.append(self.humidity_to_location)
                counter = end_index

    @staticmethod
    def create_map(lines):
        return SparseMap([SparceMapEntry(line) for line in lines])

    @staticmethod
    def get_end_of_section(input_lines, start_of_section):
        for counter in range(start_of_section + 1, len(input_lines)):
            if input_lines[counter].endswith("map:"):
                return counter

        return len(input_lines)

    def get_location(self, seed):
        destination = seed
        for current_map in self.all_maps:
            destination = current_map.get_destination(destination)
        return destination

    def get_all_locations(self):
        return [self.get_location(seed) for seed in self.seeds]

    def get_location_by_range(self, seed_list):
        destinations = seed_list
        for current_map in self.all_maps:
            print("***" + current_map.name)
            destinations = current_map.get_destination_ranges_for_list(destinations)

        return destinations


class Problem1(SolverBase):

    def solve(self):
        input_lines = self.input_data
        seeds_mapper = SeedsMapper(input_lines)
        print(min(seeds_mapper.get_all_locations()))


class Problem2(SolverBase):

    def solve(self):
        input_lines = self.input_data
        seeds_mapper = SeedsMapper(input_lines, seeds_parser=lambda seeds: [])

        current_seeds = self.input_data[0].split(":")[1].strip().split()
        counter = 0
        seed_ranges = []
        while counter < len(current_seeds):
            seed_start = int(current_seeds[counter])
            length = int(current_seeds[counter + 1])
            seed_ranges.append((seed_start, seed_start + length))
            counter += 2

        all_destination_ranges = seeds_mapper.get_location_by_range(seed_ranges)
        print(all_destination_ranges)
        print(min([start for (start, end) in all_destination_ranges]))

    # brute force standard calculation which does not work
    @staticmethod
    def parse_seed_ranges(current_seeds):
        all_seeds = []

        counter = 0
        while counter < len(current_seeds):
            seed_start = int(current_seeds[counter])
            length = int(current_seeds[counter + 1])
            for seed in range(seed_start, seed_start + length):
                all_seeds.append(seed)

            counter += 2

        return all_seeds


problem1 = Problem1("Input.txt")
problem1.solve()

problem2 = Problem2("Input.txt")
problem2.solve()
