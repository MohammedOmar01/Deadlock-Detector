import csv

def read_csv(filename, has_process_id=False):
    with open(filename, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        data = []
        for row in reader:
            if has_process_id:
                data.append([row[0]] + list(map(int, row[1:])))
            else:
                data.append(list(map(int, row)))
        return data if has_process_id else data[0]

def validate_data(available, allocation, request):
    r_len = len(available)
    p_len = len(allocation)

    if not (r_len == len(allocation[0]) - 1 == len(request[0]) - 1):
        raise ValueError("Mismatch in number of resources between files.")
    if not (p_len == len(request)):
        raise ValueError("Mismatch in number of processes between allocation and request.")
    
    print(f"\n System has {r_len} resources and {p_len} processes.\n")

def deadlock_detection(available, allocation, request):
    num_processes = len(allocation)
    work = available[:]
    finish = [sum(row[1:]) == 0 for row in allocation]
    finished = []
    deadlocked = []

    while True:
        progress = False
        for i in range(num_processes):
            if not finish[i]:
                can_proceed = all(work[j] >= request[i][j+1] for j in range(len(work)))
                if can_proceed:
                    print(f" Process {allocation[i][0]} can proceed.")
                    work = [work[j] + allocation[i][j+1] for j in range(len(work))]
                    finish[i] = True
                    finished.append(allocation[i][0])
                    progress = True
                    break
        if not progress:
            break

    deadlocked = [allocation[i][0] for i in range(num_processes) if not finish[i]]
    return finished, deadlocked

def print_result(finished, deadlocked):
    print("\n Result:")
    if deadlocked and not finished:
        print(" Deadlock detected. No process could finish.")
        print(" Deadlocked processes:", ", ".join(deadlocked))
    elif deadlocked:
        print(" Partial deadlock detected.")
        print(" Deadlocked processes:", ", ".join(deadlocked))
        print(" Finished processes   :", ", ".join(finished))
    else:
        print(" No deadlock detected.")
        print(" All processes finished:", ", ".join(finished))

def main():
    try:
        available = read_csv("Available.csv")
        allocation = read_csv("Allocation.csv", has_process_id=True)
        request = read_csv("Request.csv", has_process_id=True)

        print("📥 Inputs successfully loaded.")
        validate_data(available, allocation, request)

        finished, deadlocked = deadlock_detection(available, allocation, request)
        print_result(finished, deadlocked)

    except Exception as e:
        print(f"❗ Error: {e}")

if __name__ == "__main__":
    main()
