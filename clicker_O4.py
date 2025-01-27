import pyautogui
import time
import random
from pynput import mouse, keyboard
import threading

# Variables for managing groups
group_data = []  # Stores reload points and click points for each group
paused = False
stopped = False
click_counts = []  # To store click counts for each group

# Function to capture mouse click points
def capture_points(group_num):
    print(f"Setting points for Group {group_num}.")
    reload_point = None
    click_points = []

    def on_click(x, y, button, pressed):
        nonlocal reload_point, click_points
        if pressed:
            print(f"Point captured: ({x}, {y})")
            if reload_point is None:
                reload_point = (x, y)
                print("Reload point set.")
            elif len(click_points) < 10:
                click_points.append((x, y))
                print(f"Click point {len(click_points)} set.")

            if reload_point and len(click_points) == 10:
                return False

    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    if not reload_point or len(click_points) != 10:
        print("Error: Points input invalid. Please re-enter points for this group.")
        return capture_points(group_num)

    return reload_point, click_points

# Function to handle keyboard events
def on_press(key):
    global paused, stopped
    try:
        if key == keyboard.Key.f9:  # Pause/Resume on F9
            paused = not paused
            state = "paused" if paused else "resumed"
            print(f"Execution {state}.")
        elif key == keyboard.Key.f11:  # Stop on F11
            stopped = True
            print("Execution stopped.")
            return False
    except AttributeError:
        pass

# Worker function for each group
def group_worker(group_num, reload_point, click_points):
    global paused, stopped
    total_clicks = 0
    clicks_per_cycle = random.randint(1100, 1300)

    while total_clicks < 20000 and not stopped:
        if not paused:
            for _ in range(clicks_per_cycle):
                if stopped or paused:
                    break

                point = random.choice(click_points)
                pyautogui.click(point)
                total_clicks += 1
                click_counts[group_num - 1] = total_clicks

                # Clear the output and update click counts for all groups
                print("\033[H\033[J", end="")  # ANSI escape code to clear the terminal
                for i, count in enumerate(click_counts, start=1):
                    print(f"Group {i}: {count} clicks")

                time.sleep(random.uniform(0.2, 0.42))

                if total_clicks >= 20000 or stopped or paused:
                    break

            if not stopped and not paused:
                # Reload action
                pyautogui.click(reload_point)
                print(f"Group {group_num}: Reloading... Pausing for 15 seconds.")
                for _ in range(15):
                    if stopped or paused:
                        break
                    time.sleep(1)

                clicks_per_cycle = random.randint(1100, 1300)  # Recalculate clicks per cycle

# Main script
if __name__ == "__main__":
    # Step 1: Ask for number of groups
    while True:
        try:
            num_groups = int(input("Enter the number of groups (1-4): "))
            if 1 <= num_groups <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")

    # Step 2: Capture points for each group
    for i in range(1, num_groups + 1):
        reload_point, click_points = capture_points(i)
        group_data.append((reload_point, click_points))
        click_counts.append(0)  # Initialize click count for this group

    # Step 3: Start keyboard listener
    keyboard_listener = keyboard.Listener(on_press=on_press)
    keyboard_listener.start()

    # Step 4: Start threads for each group
    threads = []
    for i, (reload_point, click_points) in enumerate(group_data, start=1):
        thread = threading.Thread(target=group_worker, args=(i, reload_point, click_points))
        threads.append(thread)
        thread.start()

    # Step 5: Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Task completed.")
