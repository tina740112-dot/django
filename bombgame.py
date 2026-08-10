import random
import tkinter as tk
from tkinter import messagebox


BOARD_SIZE = 12
BOMB_COUNT = 20


def in_bounds(r, c, size):
    return 0 <= r < size and 0 <= c < size


def neighbors(r, c, size):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if in_bounds(nr, nc, size):
                yield nr, nc


class BombDefusalGame:
    def __init__(self, root, size=BOARD_SIZE, bomb_count=BOMB_COUNT):
        self.root = root
        self.size = size
        self.bomb_count = bomb_count

        self.root.title("拆炸彈遊戲 12x12")
        self.root.resizable(False, False)

        self.status_var = tk.StringVar()
        self.flag_var = tk.StringVar()
        self.timer_var = tk.StringVar()
        self.click_var = tk.StringVar()

        self.top_frame = tk.Frame(root, padx=10, pady=8)
        self.top_frame.pack(fill="x")

        self.status_label = tk.Label(
            self.top_frame,
            textvariable=self.status_var,
            anchor="w",
            font=("Microsoft JhengHei", 11, "bold"),
        )
        self.status_label.pack(side="left")

        self.flag_label = tk.Label(
            self.top_frame,
            textvariable=self.flag_var,
            anchor="e",
            font=("Microsoft JhengHei", 10),
        )
        self.flag_label.pack(side="right")

        self.stats_frame = tk.Frame(root, padx=10)
        self.stats_frame.pack(fill="x", pady=(0, 6))

        self.timer_label = tk.Label(
            self.stats_frame,
            textvariable=self.timer_var,
            anchor="w",
            font=("Microsoft JhengHei", 10),
        )
        self.timer_label.pack(side="left")

        self.click_label = tk.Label(
            self.stats_frame,
            textvariable=self.click_var,
            anchor="w",
            font=("Microsoft JhengHei", 10),
        )
        self.click_label.pack(side="left", padx=(16, 0))

        self.control_frame = tk.Frame(root)
        self.control_frame.pack(pady=(0, 8))

        self.reset_button = tk.Button(
            self.control_frame,
            text="重新開始",
            command=self.reset_game,
            font=("Microsoft JhengHei", 10),
            padx=8,
            pady=4,
        )

        self.pause_button = tk.Button(
            self.control_frame,
            text="暫停遊戲",
            command=self.toggle_pause,
            font=("Microsoft JhengHei", 10),
            padx=8,
            pady=4,
        )
        self.reset_button.pack(side="left", padx=(0, 8))
        self.pause_button.pack(side="left")

        self.board_frame = tk.Frame(root, padx=10, pady=10, bg="#d9d9d9")
        self.board_frame.pack()

        self.buttons = []
        self._build_board_ui()
        self.reset_game()

    def _build_board_ui(self):
        for r in range(self.size):
            row = []
            for c in range(self.size):
                btn = tk.Button(
                    self.board_frame,
                    width=3,
                    height=1,
                    relief="raised",
                    font=("Consolas", 10, "bold"),
                    bg="#f0f0f0",
                    activebackground="#e6e6e6",
                )
                btn.grid(row=r, column=c, padx=1, pady=1)
                btn.bind("<Button-1>", lambda e, rr=r, cc=c: self.open_cell(rr, cc))
                btn.bind("<Button-3>", lambda e, rr=r, cc=c: self.toggle_flag(rr, cc))
                row.append(btn)
            self.buttons.append(row)

    def reset_game(self):
        self.revealed = [[False] * self.size for _ in range(self.size)]
        self.flagged = [[False] * self.size for _ in range(self.size)]
        self.numbers = [[0] * self.size for _ in range(self.size)]
        self.bombs = set()
        self.first_move = True
        self.game_over = False
        self.paused = False
        self.elapsed_seconds = 0
        self.left_click_count = 0
        self.timer_running = False
        if hasattr(self, "timer_job") and self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
        self.timer_job = None

        for r in range(self.size):
            for c in range(self.size):
                btn = self.buttons[r][c]
                btn.config(text="", state="normal", relief="raised", bg="#f0f0f0", fg="black")

        self.status_var.set("狀態：進行中（左鍵開格，右鍵插旗）")
        self.pause_button.config(text="暫停遊戲")
        self._update_flag_text()
        self._update_stats_text()

    def toggle_pause(self):
        if self.game_over:
            return

        if not self.paused:
            self.paused = True
            self._stop_timer()
            self.pause_button.config(text="繼續遊戲")
            self.status_var.set("狀態：遊戲暫停中")
            return

        self.paused = False
        self.pause_button.config(text="暫停遊戲")
        self.status_var.set("狀態：進行中（左鍵開格，右鍵插旗）")
        if not self.first_move:
            self._start_timer()

    def _update_stats_text(self):
        self.timer_var.set(f"計時：{self.elapsed_seconds} 秒")
        self.click_var.set(f"左鍵次數：{self.left_click_count}")

    def _start_timer(self):
        if self.timer_running:
            return
        self.timer_running = True
        self._tick_timer()

    def _tick_timer(self):
        if not self.timer_running:
            return
        self.elapsed_seconds += 1
        self._update_stats_text()
        self.timer_job = self.root.after(1000, self._tick_timer)

    def _stop_timer(self):
        self.timer_running = False
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def _update_flag_text(self):
        flags = sum(sum(1 for x in row if x) for row in self.flagged)
        self.flag_var.set(f"旗標：{flags}/{self.bomb_count}")

    def _place_bombs(self, safe_r, safe_c):
        all_cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        blocked = {(safe_r, safe_c)}
        blocked.update(neighbors(safe_r, safe_c, self.size))

        candidates = [cell for cell in all_cells if cell not in blocked]
        self.bombs = set(random.sample(candidates, self.bomb_count))

    def _count_adjacent_bombs(self, r, c):
        return sum((nr, nc) in self.bombs for nr, nc in neighbors(r, c, self.size))

    def _reveal_area(self, r, c):
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if self.revealed[cr][cc] or self.flagged[cr][cc]:
                continue

            self.revealed[cr][cc] = True
            count = self._count_adjacent_bombs(cr, cc)
            self.numbers[cr][cc] = count
            self._render_open_cell(cr, cc)

            if count == 0:
                for nr, nc in neighbors(cr, cc, self.size):
                    if not self.revealed[nr][nc] and (nr, nc) not in self.bombs:
                        stack.append((nr, nc))

    def _render_open_cell(self, r, c):
        btn = self.buttons[r][c]
        count = self.numbers[r][c]

        color_map = {
            1: "#0b57d0",
            2: "#2e7d32",
            3: "#c62828",
            4: "#6a1b9a",
            5: "#8d6e63",
            6: "#00838f",
            7: "#37474f",
            8: "#000000",
        }

        btn.config(
            text=str(count) if count > 0 else "",
            relief="sunken",
            state="disabled",
            bg="#ffffff",
            disabledforeground=color_map.get(count, "black"),
        )

    def _reveal_all_bombs(self, exploded=None):
        for r, c in self.bombs:
            btn = self.buttons[r][c]
            if exploded == (r, c):
                btn.config(text="X", bg="#ff8a80", fg="black", relief="sunken")
            else:
                btn.config(text="*", bg="#ffd54f", fg="black", relief="sunken")

    def _all_safe_revealed(self):
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in self.bombs and not self.revealed[r][c]:
                    return False
        return True

    def open_cell(self, r, c):
        if self.game_over or self.paused or self.flagged[r][c] or self.revealed[r][c]:
            return

        self.left_click_count += 1
        self._update_stats_text()

        if self.first_move:
            self._place_bombs(r, c)
            self.first_move = False
            self._start_timer()

        if (r, c) in self.bombs:
            self.game_over = True
            self._stop_timer()
            self._reveal_all_bombs(exploded=(r, c))
            self.status_var.set("狀態：挑戰失敗，你踩到炸彈了")
            messagebox.showinfo(
                "挑戰失敗",
                f"你踩到炸彈了，挑戰失敗。\n耗時：{self.elapsed_seconds} 秒\n左鍵次數：{self.left_click_count}",
            )
            return

        self._reveal_area(r, c)

        if self._all_safe_revealed():
            self.game_over = True
            self._stop_timer()
            self._reveal_all_bombs()
            self.status_var.set("狀態：挑戰成功，全部安全格已拆除")
            messagebox.showinfo(
                "挑戰成功",
                f"成功拆除所有危險區域！\n耗時：{self.elapsed_seconds} 秒\n左鍵次數：{self.left_click_count}",
            )

    def toggle_flag(self, r, c):
        if self.game_over or self.paused or self.revealed[r][c]:
            return

        self.flagged[r][c] = not self.flagged[r][c]
        btn = self.buttons[r][c]
        if self.flagged[r][c]:
            btn.config(text="🚩", fg="#d32f2f")
        else:
            btn.config(text="", fg="black")

        self._update_flag_text()


def main():
    root = tk.Tk()
    BombDefusalGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()