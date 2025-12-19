"""
Railway Timetable Conflict Detection and Resolution
"""


# CONFIGURATION

TEST_MODE = False   # Set True only for developer testing


# DATA MODEL

class TrainSchedule:
    def __init__(self, train_id, platform, start_time, end_time, priority):
        self.train_id = train_id
        self.platform = platform
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority

    def __repr__(self):
        return (
            f"Train {self.train_id} | "
            f"Platform: {self.platform} | "
            f"Start: {self.start_time} | "
            f"End: {self.end_time} | "
            f"Priority: {self.priority}"
        )


# INTERVAL LOGIC

def intervals_overlap(a, b):
    """Returns True if two time intervals overlap"""
    return a.start_time < b.end_time and b.start_time < a.end_time


# PLATFORM AVAILABILITY CHECK

def is_platform_free(timetable, platform, start, end, current_train):
    """Checks whether a platform is free for the given time interval"""
    for train in timetable:
        if train == current_train:
            continue
        if train.platform == platform:
            if start < train.end_time and train.start_time < end:
                return False
    return True


# CONFLICT DETECTION

def detect_conflicts(timetable):
    conflicts = []
    for i in range(len(timetable)):
        for j in range(i + 1, len(timetable)):
            t1 = timetable[i]
            t2 = timetable[j]
            if t1.platform == t2.platform and intervals_overlap(t1, t2):
                conflicts.append((t1, t2))
    return conflicts


# CONFLICT RESOLUTION

def resolve_conflicts(timetable, platforms):
    """
    Resolution Strategy:
    1. Try platform reassignment
    2. If not possible, apply minimal delay
    """
    timetable.sort(key=lambda x: x.start_time)

    for train in timetable:
        while True:
            conflicts = [
                t for t in timetable
                if t != train
                and t.platform == train.platform
                and intervals_overlap(train, t)
            ]

            if not conflicts:
                break

            highest_priority_train = min(
                [train] + conflicts, key=lambda x: x.priority
            )

            if highest_priority_train != train:
                break

            latest_end = max(t.end_time for t in conflicts)
            delay_needed = latest_end - train.start_time

            best_platform = train.platform
            best_platform_delay = delay_needed

            for p in platforms:
                if p == train.platform:
                    continue

                blocking = [
                    t for t in timetable
                    if t.platform == p and intervals_overlap(train, t)
                ]

                if not blocking:
                    best_platform = p
                    best_platform_delay = 0
                    break

                p_latest_end = max(t.end_time for t in blocking)
                p_delay = p_latest_end - train.start_time

                if p_delay < best_platform_delay:
                    best_platform = p
                    best_platform_delay = p_delay

            train.platform = best_platform
            train.start_time += best_platform_delay
            train.end_time += best_platform_delay

    return timetable


# MAIN EXECUTION

def main():
    print("\nRAILWAY TIMETABLE CONFLICT DETECTION SYSTEM")
    print("------------------------------------------")

    timetable = []
    platforms = []

    #  TEST MODE (For Developer Only) 
    if TEST_MODE:
        print("Running in TEST MODE\n")
        platforms = ["P1", "P2", "P3"]
        timetable = [
            TrainSchedule("T1", "P1", 10, 20, 1),
            TrainSchedule("T2", "P1", 12, 18, 3),
            TrainSchedule("T3", "P2", 15, 25, 2),
        ]

    #  REAL USER INPUT MODE
    else:
        p_count = int(input("Enter number of platforms: "))
        for i in range(p_count):
            platforms.append(input(f"Platform {i + 1} ID: "))

        n = int(input("\nEnter number of trains: "))
        for i in range(n):
            print(f"\nEnter details for Train {i + 1}")
            train_id = input("Train ID: ")
            platform = input("Assigned Platform: ")
            start_time = float(input("Start Time: "))
            end_time = float(input("End Time: "))
            priority = int(input("Priority (lower number = higher priority): "))

            timetable.append(
                TrainSchedule(train_id, platform, start_time, end_time, priority)
            )

    #  CONFLICT DETECTION 
    conflicts = detect_conflicts(timetable)

    print("\nDETECTED CONFLICTS")
    print("-----------------")
    if not conflicts:
        print("No conflicts detected.")
    else:
        for a, b in conflicts:
            print(
                f"Train {a.train_id} conflicts with "
                f"Train {b.train_id} on Platform {a.platform}"
            )

    # CONFLICT RESOLUTION 
    resolve_conflicts(timetable, platforms)

    print("\nUPDATED TIMETABLE (Resolved)")
    print("----------------------------")
    for train in timetable:
        print(train)


# ENTRY POINT

if __name__ == "__main__":
    main()
