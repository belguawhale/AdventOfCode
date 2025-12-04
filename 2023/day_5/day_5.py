import re

def lookup(mapping, source):
    for dest_range_start, source_range_start, range_len in mapping:
        if source_range_start <= source < source_range_start + range_len:
            return dest_range_start - source_range_start + source
    return source

def lookup_range(mapping, input_range):
    # apply mapping to input_range and return a list of dest_ranges.
    dest_ranges = []

    input_range_start = input_range[0]
    input_range_end = input_range[0] + input_range[1] - 1

    while input_range_start <= input_range_end:
        print(input_range_start, input_range_end, dest_ranges)
        for dest_range_start, source_range_start, range_len in mapping:
            if source_range_start <= input_range_start < source_range_start + range_len:
                # Case 1: We're inside a mapped range. We want the mapped dest range to go until the end of the mapped range or end of input range
                end_of_mapped_input_range = min(input_range_end, source_range_start + range_len - 1)
                start_of_mapped_dest_range = dest_range_start - source_range_start + input_range_start
                break
        else:
            # Case 2: start of input range is not mapped. We want the dest range to go until the first mapped range or end of input range
            start_of_mapped_dest_range = input_range_start
            smallest_source_range_start_greater_than_input_range_start = min(
                filter(lambda n: n > input_range_start,
                       (source_range_start for _, source_range_start, _ in mapping)), default=10000000000000)
            end_of_mapped_input_range = min(smallest_source_range_start_greater_than_input_range_start - 1, input_range_end)

        dest_ranges.append([start_of_mapped_dest_range, end_of_mapped_input_range - input_range_start + 1])
        input_range_start = end_of_mapped_input_range + 1

    return dest_ranges

def lookup_ranges(mapping, input_ranges):
    output = []
    for input_range in input_ranges:
        output.extend(lookup_range(mapping, input_range))
    return output

def part_1(inp):
    seeds, seed_to_soil_map, soil_to_fertilizer_map, fertilizer_to_water_map, water_to_light_map, light_to_temperature_map, temperature_to_humidity_map, humidity_to_location_map = inp

    return min(lookup(humidity_to_location_map,
               lookup(temperature_to_humidity_map,
               lookup(light_to_temperature_map,
               lookup(water_to_light_map,
               lookup(fertilizer_to_water_map,
               lookup(soil_to_fertilizer_map,
               lookup(seed_to_soil_map, seed)))))))
               for seed in seeds)

def part_2(inp):
    seeds, seed_to_soil_map, soil_to_fertilizer_map, fertilizer_to_water_map, water_to_light_map, light_to_temperature_map, temperature_to_humidity_map, humidity_to_location_map = inp

    # brute force did not work lol

    # min_location_number = 10000000000000000
    #
    # for i in range(0, len(seed_ranges), 2):
    #     for seed in range(seed_ranges[i], seed_ranges[i] + seed_ranges[i+1]):
    #         location = lookup(humidity_to_location_map,
    #            lookup(temperature_to_humidity_map,
    #            lookup(light_to_temperature_map,
    #            lookup(water_to_light_map,
    #            lookup(fertilizer_to_water_map,
    #            lookup(soil_to_fertilizer_map,
    #            lookup(seed_to_soil_map, seed)))))))
    #         min_location_number = min(location, min_location_number)

    # idea: given seed ranges, output the resulting soil ranges, and so forth
    seed_ranges = []

    for i in range(0, len(seeds), 2):
        seed_ranges.append([seeds[i], seeds[i] + seeds[i+1] - 1])

    print("seed_ranges", seed_ranges)
    soil_ranges = lookup_ranges(seed_to_soil_map, seed_ranges)
    print("soil_ranges", soil_ranges)
    fertilizer_ranges = lookup_ranges(soil_to_fertilizer_map, soil_ranges)
    print("fertilizer_ranges", fertilizer_ranges)
    water_ranges = lookup_ranges(fertilizer_to_water_map, fertilizer_ranges)
    print("water_ranges", water_ranges)
    light_ranges = lookup_ranges(water_to_light_map, water_ranges)
    print("light_ranges",light_ranges)
    temperature_ranges = lookup_ranges(light_to_temperature_map, light_ranges)
    print("temperature_ranges", temperature_ranges)
    humidity_ranges = lookup_ranges(temperature_to_humidity_map, temperature_ranges)
    print("humidity_ranges", humidity_ranges)
    location_ranges = lookup_ranges(humidity_to_location_map, humidity_ranges)
    print("location_ranges", location_ranges)
    
    return min(start for start, _ in location_ranges)

def parse_file(file):
    with open(file, "r") as f:
        seeds = list(map(int, f.readline().split("seeds: ")[1].strip().split(" ")))
        f.readline()

        seed_to_soil_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            seed_to_soil_map.append(list(map(int, line.strip().split(" "))))

        soil_to_fertilizer_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            soil_to_fertilizer_map.append(list(map(int, line.strip().split(" "))))

        fertilizer_to_water_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            fertilizer_to_water_map.append(list(map(int, line.strip().split(" "))))

        water_to_light_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            water_to_light_map.append(list(map(int, line.strip().split(" "))))

        light_to_temperature_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            light_to_temperature_map.append(list(map(int, line.strip().split(" "))))

        temperature_to_humidity_map = []
        f.readline()
        while (line := f.readline()) != "\n":
            temperature_to_humidity_map.append(list(map(int, line.strip().split(" "))))

        humidity_to_location_map = []
        f.readline()
        while (line := f.readline()) not in ("\n", ""):
            humidity_to_location_map.append(list(map(int, line.strip().split(" "))))

    return [seeds, seed_to_soil_map, soil_to_fertilizer_map, fertilizer_to_water_map,
            water_to_light_map, light_to_temperature_map, temperature_to_humidity_map,
            humidity_to_location_map]


inp_example = parse_file("input_example.txt")
print(inp_example)
print(part_1(inp_example))

inp = parse_file("input.txt")
print(part_1(inp))

print("assert", lookup_range(inp_example[1], [0, 100]), [[0, 50], [52, 48], [50, 2]])
inp_example2 = parse_file("input_example2.txt")
print(part_2(inp_example2))

# print(part_2(inp))
