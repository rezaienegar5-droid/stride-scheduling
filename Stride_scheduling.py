
# Stride Scheduling Algorithm

BIG = 10000

n = int(input("Number of processes: "))
processes = []

for i in range(n):
    print("\nProcess", i + 1)

    pid = input("Process name: ")
    arrival = int(input("Arrival time: "))
    burst = int(input("Burst time: "))
    tickets = int(input("Tickets: "))

    processes.append({
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "remaining": burst,
        "tickets": tickets,
        "stride": BIG // tickets,
        "pass": 0,
        "start": -1,
        "finish": 0
    })

time = 0
gantt = []

while any(p["remaining"] > 0 for p in processes):

    ready = [
        p for p in processes
        if p["arrival"] <= time and p["remaining"] > 0
    ]

    if not ready:
        time += 1
        continue

    current = min(ready, key=lambda p: p["pass"])

    if current["start"] == -1:
        current["start"] = time

    gantt.append((current["pid"], time, time + 1))

    current["remaining"] -= 1
    current["pass"] += current["stride"]
    time += 1

    if current["remaining"] == 0:
        current["finish"] = time

print("\n--- GANTT CHART ---")
for pid, start, end in gantt:
    print(f"{start} - {end}: {pid}")

total_wait = 0
total_turnaround = 0
total_response = 0

print("\n--- RESULTS ---")

for p in processes:
    turnaround = p["finish"] - p["arrival"]
    waiting = turnaround - p["burst"]
    response = p["start"] - p["arrival"]
    runtime = p["finish"] - p["start"]

    total_wait += waiting
    total_turnaround += turnaround
    total_response += response

    print(
        p["pid"],
        "| Start:", p["start"],
        "| Finish:", p["finish"],
        "| Runtime:", runtime,
        "| Turnaround:", turnaround,
        "| Waiting:", waiting,
        "| Response:", response
    )

print("\n--- AVERAGES ---")
print("Average waiting:", round(total_wait / n, 2))
print("Average turnaround:", round(total_turnaround / n, 2))
print("Average response:", round(total_response / n, 2))
print("Total elapsed time:", time)