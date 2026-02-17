# fortnite_ping_tester_detailed_with_stop.py
import os
import subprocess
import re
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import platform
import time
from statistics import mean

SERVERS = {
    "NA-East":     "ping-nae.ds.on.epicgames.com",
    "NA-Central":  "ping-nac.ds.on.epicgames.com",
    "NA-West":     "ping-naw.ds.on.epicgames.com",
    "Europe":      "ping-eu.ds.on.epicgames.com",
    "Oceania":     "ping-oce.ds.on.epicgames.com",
    "Brazil":      "ping-br.ds.on.epicgames.com",
    "Asia":        "ping-asia.ds.on.epicgames.com",
    "Middle East": "ping-me.ds.on.epicgames.com"
}

PING_COUNT = 25

# Global control variables
stop_flag = False
current_process = None

def ping_host_and_yield(host):
    """Generator: yields ping results line-by-line, respects stop_flag"""
    global current_process, stop_flag
    
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    cmd = ["ping", param, str(PING_COUNT), host]

    times = []
    sent = 0
    received = 0

    try:
        current_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
        )

        for line in iter(current_process.stdout.readline, ''):
            if stop_flag:
                break

            line = line.strip()
            if not line:
                continue

            # Live output
            if "Reply from" in line or "time=" in line or "time<" in line:
                yield {"type": "live", "text": line}

            # Parse ping time
            match = re.search(r'time[=<](\d+)ms', line)
            if match:
                t = int(match.group(1))
                times.append(t)
                received += 1
                sent += 1
                yield {"type": "result", "ms": t}

            elif "Request timed out" in line or "timed out" in line.lower():
                sent += 1
                yield {"type": "timeout"}

            # Stats line (might appear before finish)
            if "Packets:" in line or "Lost =" in line:
                yield {"type": "stats_line", "text": line}

            time.sleep(0.01)  # small sleep to help responsiveness

        current_process.stdout.close()
        current_process.wait(timeout=3)

    except Exception as e:
        if not stop_flag:
            yield {"type": "error", "text": f"Error: {str(e)}"}

    finally:
        # Final summary if we have data
        if times and not stop_flag:
            summary = {
                "type": "summary",
                "min": min(times),
                "max": max(times),
                "avg": round(mean(times), 1),
                "sent": sent,
                "received": received,
                "loss": round((sent - received) / sent * 100, 1) if sent > 0 else 100.0
            }
            yield summary
        elif stop_flag:
            yield {"type": "stopped", "text": "→ Test stopped by user"}

    current_process = None


def start_ping_test():
    global stop_flag
    stop_flag = False

    selected = server_var.get()
    if selected == "Select a server...":
        messagebox.showwarning("Selection required", "Please choose a server!")
        return

    host = SERVERS[selected]
    btn_test.config(state="disabled")
    btn_stop.config(state="normal")
    status_label.config(text=f"Testing {selected} • {PING_COUNT} packets...")
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"→ Pinging {selected} ({host})\n\n", "header")

    def do_test():
        for update in ping_host_and_yield(host):
            if stop_flag:
                break
            root.after(0, lambda u=update: update_ui(u))

        root.after(0, finish_test)

    threading.Thread(target=do_test, daemon=True).start()


def stop_ping_test():
    global stop_flag, current_process
    stop_flag = True
    
    if current_process and current_process.poll() is None:
        try:
            current_process.terminate()
            # Give it a moment, then kill if needed
            try:
                current_process.wait(timeout=1.5)
            except subprocess.TimeoutExpired:
                current_process.kill()
        except:
            pass
    
    status_label.config(text="Stopping... please wait")
    btn_stop.config(state="disabled")


def finish_test():
    global stop_flag
    btn_test.config(state="normal")
    btn_stop.config(state="disabled")
    
    if stop_flag:
        status_label.config(text="Test stopped")
    else:
        status_label.config(text="Test finished • Ready for next test")
    stop_flag = False


def update_ui(update):
    t = update.get("type")

    if t == "live":
        result_text.insert(tk.END, update["text"] + "\n", "live")

    elif t == "result":
        result_text.insert(tk.END, f"  {update['ms']:3} ms\n", "ping_good")

    elif t == "timeout":
        result_text.insert(tk.END, "  TIMEOUT\n", "ping_bad")

    elif t == "stats_line":
        result_text.insert(tk.END, "\n" + update["text"] + "\n", "stats")

    elif t == "summary":
        result_text.insert(tk.END, "┌──────────────────────────────┐\n", "summary")
        result_text.insert(tk.END, f"│  Min: {update['min']:3} ms               │\n", "summary")
        result_text.insert(tk.END, f"│  Avg: {update['avg']:5.1f} ms             │\n", "summary")
        result_text.insert(tk.END, f"│  Max: {update['max']:3} ms               │\n", "summary")
        result_text.insert(tk.END, f"│  Packet loss: {update['loss']}%          │\n", "summary")
        result_text.insert(tk.END, "└──────────────────────────────┘\n", "summary")

    elif t in ("error", "stopped"):
        result_text.insert(tk.END, update["text"] + "\n\n", "error" if t == "error" else "stopped")

    result_text.see(tk.END)


# ── GUI ────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Fortnite Ping Tester - Detailed + Stop")
root.geometry("600x540")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10))

tk.Label(root, text="Fortnite Data Center Ping", font=("Segoe UI", 16, "bold")).pack(pady=(20, 5))
tk.Label(root, text="Detailed results with real-time packets", font=("Segoe UI", 9), fg="#555").pack()

server_var = tk.StringVar(value="Select a server...")
dropdown = ttk.Combobox(root, textvariable=server_var, values=list(SERVERS.keys()),
                        state="readonly", width=28, font=("Segoe UI", 11))
dropdown.pack(pady=15)

frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=10)

btn_test = ttk.Button(frame_buttons, text=f"Start Test ({PING_COUNT} packets)", command=start_ping_test)
btn_test.pack(side="left", padx=8)

btn_stop = ttk.Button(frame_buttons, text="STOP", command=stop_ping_test, state="disabled")
btn_stop.pack(side="left", padx=8)

status_label = tk.Label(root, text="Choose server and start testing", fg="#444", font=("Segoe UI", 9))
status_label.pack(pady=8)

result_text = tk.Text(root, height=21, width=68, font=("Consolas", 10), bg="#f8f9fa")
result_text.pack(padx=20, pady=10, fill="both")

# Tags
result_text.tag_config("header",   font=("Segoe UI", 11, "bold"), foreground="#0066cc")
result_text.tag_config("live",     foreground="#555")
result_text.tag_config("ping_good", foreground="#006600")
result_text.tag_config("ping_bad",  foreground="red", font=("Consolas", 10, "bold"))
result_text.tag_config("stats",    foreground="#444", font=("Consolas", 10, "italic"))
result_text.tag_config("summary",  foreground="#000", font=("Consolas", 11, "bold"))
result_text.tag_config("error",    foreground="darkred", font=("Segoe UI", 11, "bold"))
result_text.tag_config("stopped",  foreground="#d35400", font=("Segoe UI", 11, "italic"))

tk.Label(root, text=f"Windows only • Click STOP to interrupt at any time", 
         font=("Segoe UI", 8), fg="gray").pack(pady=6)

root.mainloop()