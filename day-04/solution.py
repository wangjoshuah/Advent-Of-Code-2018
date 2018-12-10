from collections import defaultdict
import datetime
import re

input_file = open("input.txt", "r")
lines = input_file.readlines()


def extract_timestamp(line):
    timestamp_pattern = r"\[(.+?)\]"
    timestamp_result = re.search(timestamp_pattern, line).group(1)
    timestamp = datetime.datetime.strptime(timestamp_result, "%Y-%m-%d %H:%M").timestamp()
    return timestamp

def extract_minute(line):
    minute_pattern = r"\:(\d\d?)\]"
    minute_result = re.search(minute_pattern, line).group(1)
    return int(minute_result)


def pre_process(unsorted_lines):
    # sort all lines by timestamp
    sorted_lines = sorted(unsorted_lines, key=lambda x: extract_timestamp(x))

    # extract all minutes where guards are asleep
    guard_sleep_array_map = {}  # key is guard ID, value is counter array of minutes asleep
    guard_sleeptime_map = defaultdict(int)  # key is guard ID, value is total time guard was asleep
    guard_id = None
    last_minute = None
    for line in sorted_lines:
        # if new guard begins shift
        guard_pattern = r"Guard #(\d+?) begins shift"
        guard_result = re.search(guard_pattern, line)
        minute = extract_minute(line)
        if guard_result is not None:
            # set new guard
            guard_id = guard_result.group(1)
        elif "wakes up" in line:
            sleep_array = guard_sleep_array_map.get(guard_id)
            if sleep_array is None:
                sleep_array = [0] * 60
            minutes_asleep = 0
            for i in range(last_minute, minute):
                minutes_asleep += 1
                sleep_array[i] += 1
            guard_sleep_array_map[guard_id] = sleep_array
            guard_sleeptime_map[guard_id] += minutes_asleep
        last_minute = minute
        # for now ignore the edge case where guard is asleep at end of shift
    return guard_sleep_array_map, guard_sleeptime_map

def part_1(unsorted_lines):
    guard_sleep_array_map, guard_sleeptime_map = pre_process(unsorted_lines)
    # find guard that was asleep the most
    max_sleep_time = 0
    sleepiest_guard = None
    for guard_id, sleeptime in guard_sleeptime_map.items():
        print("Guard {} was asleep for {} minutes", guard_id, sleeptime)
        if sleeptime > max_sleep_time:
            max_sleep_time = sleeptime
            sleepiest_guard = guard_id

    print("Sleepiest guard is {}", sleepiest_guard)

    # Find minute the guard was asleep the most
    sleep_array = guard_sleep_array_map[sleepiest_guard]
    print(sleep_array)
    sleepiest_minute = None
    most_times_asleep = 0
    for i in range(len(sleep_array)):
        times_asleep = sleep_array[i]
        if times_asleep > most_times_asleep:
            most_times_asleep = times_asleep
            sleepiest_minute = i
    print("The guard's sleepiest minute is minute {}", sleepiest_minute)
    print("Answer is {}", int(sleepiest_guard) * int(sleepiest_minute))

def part_2(unsorted_lines):
    guard_sleep_array_map, guard_sleeptime_map = pre_process(unsorted_lines)
    most_times_asleep = 0
    sleepiest_minute = None
    target_guard = None
    for guard_id, sleep_array in guard_sleep_array_map.items():
        for i in range(len(sleep_array)):
            times_asleep = sleep_array[i]
            if times_asleep > most_times_asleep:
                most_times_asleep = times_asleep
                target_guard = guard_id
                sleepiest_minute = i

    print("Guard #{} was most asleep at minute {}", target_guard, sleepiest_minute)
    print("Answer is {}", int(target_guard) * sleepiest_minute)



part_1(lines)
part_2(lines)