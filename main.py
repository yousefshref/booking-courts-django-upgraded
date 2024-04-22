from datetime import datetime, timedelta

def time_slots_between(start_time_str, end_time_str):
    # Convert input strings to datetime objects
    start_time = datetime.strptime(start_time_str, "%H:%M")
    end_time = datetime.strptime(end_time_str, "%H:%M")

    if start_time == end_time:
        # Return a 24-hour cycle starting from the given time
        time_slots = []
        current_time = start_time
        for _ in range(48):  # 24 hours * 2 slots per hour
            time_slots.append(current_time.strftime("%H:%M"))
            current_time += timedelta(minutes=30)  # Increment by 30 minutes
        return time_slots

    # Initialize list to hold time slots
    time_slots = []

    # Increment time in slots and append to list until end time is reached
    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.strftime("%H:%M"))
        current_time += timedelta(minutes=60)  # Increment by 30 minutes

    return time_slots

# Example usage
start_time = "02:30"
end_time = "02:30"
slots = time_slots_between(start_time, end_time)
print(slots)
