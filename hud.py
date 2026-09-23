import tkinter as tk
import math
import random
import queue


class NovaHUD:

    def __init__(self):

        # ==========================================
        # WINDOW
        # ==========================================

        self.root = tk.Tk()

        self.root.title("NOVA AI")

        self.root.geometry("1100x750")

        self.root.configure(
            bg="#02050b"
        )

        self.root.overrideredirect(True)

        self.root.attributes(
            "-alpha",
            0.97
        )

        self.width = 1100
        self.height = 750

        # ==========================================
        # CANVAS
        # ==========================================

        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#02050b",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # ==========================================
        # STATE
        # ==========================================

        self.state = "OFF"
        self.power_on = False

        self.command_queue = queue.Queue()

        # Animation
        self.rotation = 0
        self.pulse = 0
        self.star_speed = 0.8

        # ==========================================
        # 3D STAR FIELD
        # ==========================================

        self.stars = []

        for _ in range(180):

            self.stars.append(
                self.create_star()
            )

        # ==========================================
        # UI
        # ==========================================

        self.create_space_background()
        self.create_header()
        self.create_core()
        self.create_status()
        self.create_controls()

        # ==========================================
        # START ANIMATION
        # ==========================================

        self.animate()

    # ==========================================
    # CREATE STAR
    # ==========================================

    def create_star(self):

        return {
            "x": random.uniform(
                -550,
                550
            ),

            "y": random.uniform(
                -375,
                375
            ),

            "z": random.uniform(
                1,
                1000
            ),

            "speed": random.uniform(
                2,
                6
            )
        }

    # ==========================================
    # SPACE BACKGROUND
    # ==========================================

    def create_space_background(self):

        # Large subtle circles

        self.canvas.create_oval(
            40,
            40,
            330,
            330,
            outline="#071322",
            width=1
        )

        self.canvas.create_oval(
            760,
            420,
            1050,
            710,
            outline="#071322",
            width=1
        )

        # Horizontal space lines

        for y in range(
            100,
            750,
            80
        ):

            self.canvas.create_line(
                0,
                y,
                self.width,
                y,
                fill="#040b15"
            )

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        self.canvas.create_text(
            45,
            42,
            text="N O V A",
            fill="#66e6ff",
            font=(
                "Arial",
                27,
                "bold"
            ),
            anchor="w"
        )

        self.canvas.create_text(
            47,
            72,
            text="NEURAL OPERATING VIRTUAL ASSISTANT",
            fill="#526b80",
            font=(
                "Arial",
                9
            ),
            anchor="w"
        )

        self.system_text = self.canvas.create_text(
            550,
            42,
            text="● SYSTEM OFFLINE",
            fill="#ff496c",
            font=(
                "Arial",
                10,
                "bold"
            )
        )

    # ==========================================
    # CENTRAL CORE
    # ==========================================

    def create_core(self):

        self.cx = 550
        self.cy = 350

        # Outer rings

        self.ring1 = self.canvas.create_oval(
            300,
            100,
            800,
            600,
            outline="#123149",
            width=2
        )

        self.ring2 = self.canvas.create_oval(
            350,
            150,
            750,
            550,
            outline="#194b66",
            width=2
        )

        self.ring3 = self.canvas.create_oval(
            405,
            205,
            695,
            495,
            outline="#246985",
            width=2
        )

        # Inner energy ring

        self.energy_ring = self.canvas.create_oval(
            455,
            255,
            645,
            445,
            outline="#66e6ff",
            width=3
        )

        # Core

        self.core = self.canvas.create_oval(
            485,
            285,
            615,
            415,
            fill="#071522",
            outline="#66e6ff",
            width=3
        )

        # Core N

        self.canvas.create_text(
            self.cx,
            self.cy,
            text="N",
            fill="#66e6ff",
            font=(
                "Arial",
                48,
                "bold"
            )
        )

        # Orbit particles

        self.orbit_particles = []

        for i in range(12):

            particle = self.canvas.create_oval(
                0,
                0,
                0,
                0,
                fill="#66e6ff",
                outline=""
            )

            self.orbit_particles.append(
                particle
            )

    # ==========================================
    # STATUS
    # ==========================================

    def create_status(self):

        self.status_text = self.canvas.create_text(
            self.cx,
            620,
            text="NOVA // OFFLINE",
            fill="#ff496c",
            font=(
                "Arial",
                20,
                "bold"
            )
        )

        self.sub_status = self.canvas.create_text(
            self.cx,
            648,
            text="System is powered off",
            fill="#526b80",
            font=(
                "Arial",
                10
            )
        )

    # ==========================================
    # CONTROLS
    # ==========================================

    def create_controls(self):

        # Power button

        self.power_button = tk.Button(
            self.root,
            text="●  POWER ON",
            command=self.toggle_power,
            bg="#071522",
            fg="#66e6ff",
            activebackground="#10283a",
            activeforeground="#ffffff",
            border=1,
            relief="solid",
            font=(
                "Arial",
                11,
                "bold"
            ),
            cursor="hand2"
        )

        self.power_button.place(
            x=45,
            y=680,
            width=160,
            height=42
        )

        # Close button

        self.close_button = tk.Button(
            self.root,
            text="✕",
            command=self.close_window,
            bg="#02050b",
            fg="#ffffff",
            activebackground="#1a2028",
            activeforeground="#ffffff",
            border=0,
            font=(
                "Arial",
                16
            ),
            cursor="hand2"
        )

        self.close_button.place(
            x=1045,
            y=15,
            width=40,
            height=35
        )

    # ==========================================
    # POWER TOGGLE
    # ==========================================

    def toggle_power(self):

        if self.power_on:

            self.power_off()

        else:

            self.power_on_action()

    # ==========================================
    # POWER ON
    # ==========================================

    def power_on_action(self):

        self.power_on = True

        self.set_state(
            "IDLE"
        )

        self.command_queue.put(
            ("POWER", True)
        )

    # ==========================================
    # POWER OFF
    # ==========================================

    def power_off(self):

        self.power_on = False

        self.apply_state(
            "OFF"
        )

        self.command_queue.put(
            ("POWER", False)
        )

    # ==========================================
    # EXTERNAL STATE
    # ==========================================

    def set_state(self, state):

        self.command_queue.put(
            (
                "STATE",
                state.upper()
            )
        )

    # ==========================================
    # PROCESS COMMANDS
    # ==========================================

    def process_commands(self):

        try:

            while True:

                command = (
                    self.command_queue
                    .get_nowait()
                )

                action = command[0]

                if action == "STATE":

                    self.apply_state(
                        command[1]
                    )

                elif action == "POWER":

                    self.power_on = command[1]

        except queue.Empty:

            pass

        self.root.after(
            50,
            self.process_commands
        )

    # ==========================================
    # APPLY STATE
    # ==========================================

    def apply_state(self, state):

        self.state = state

        if state == "OFF":

            self.canvas.itemconfig(
                self.system_text,
                text="● SYSTEM OFFLINE",
                fill="#ff496c"
            )

            self.canvas.itemconfig(
                self.status_text,
                text="NOVA // OFFLINE",
                fill="#ff496c"
            )

            self.canvas.itemconfig(
                self.sub_status,
                text="System is powered off"
            )

            self.power_button.config(
                text="●  POWER ON",
                fg="#66e6ff"
            )

            return

        # ======================================
        # ONLINE
        # ======================================

        self.canvas.itemconfig(
            self.system_text,
            text="● SYSTEM ONLINE",
            fill="#66e6ff"
        )

        if state == "IDLE":

            self.canvas.itemconfig(
                self.status_text,
                text="NOVA // IDLE",
                fill="#66e6ff"
            )

            self.canvas.itemconfig(
                self.sub_status,
                text="Waiting for activation..."
            )

            self.power_button.config(
                text="●  POWER OFF",
                fg="#ff496c"
            )

        elif state == "LISTENING":

            self.canvas.itemconfig(
                self.status_text,
                text="NOVA // LISTENING",
                fill="#00ffcc"
            )

            self.canvas.itemconfig(
                self.sub_status,
                text="Listening for your command..."
            )

        elif state == "THINKING":

            self.canvas.itemconfig(
                self.status_text,
                text="NOVA // THINKING",
                fill="#b56cff"
            )

            self.canvas.itemconfig(
                self.sub_status,
                text="Processing neural response..."
            )

        elif state == "SPEAKING":

            self.canvas.itemconfig(
                self.status_text,
                text="NOVA // SPEAKING",
                fill="#66e6ff"
            )

            self.canvas.itemconfig(
                self.sub_status,
                text="NOVA is responding..."
            )

    # ==========================================
    # 3D STAR FIELD
    # ==========================================

    def animate_stars(self):

        # Remove old stars

        self.canvas.delete(
            "star"
        )

        for star in self.stars:

            if self.power_on:

                star["z"] -= star["speed"]

            if star["z"] <= 1:

                star["x"] = random.uniform(
                    -550,
                    550
                )

                star["y"] = random.uniform(
                    -375,
                    375
                )

                star["z"] = 1000

            # Perspective projection

            scale = (
                500 /
                star["z"]
            )

            x = (
                self.cx +
                star["x"] *
                scale
            )

            y = (
                self.cy +
                star["y"] *
                scale
            )

            size = max(
                1,
                min(
                    5,
                    int(
                        5 *
                        (1 -
                         star["z"] /
                         1000)
                    )
                )
            )

            # Only draw visible stars

            if (
                0 <= x <= self.width
                and
                0 <= y <= self.height
            ):

                brightness = max(
                    0.2,
                    1 -
                    star["z"] /
                    1000
                )

                if self.power_on:

                    fill = "#66e6ff"

                else:

                    fill = "#1a2935"

                self.canvas.create_oval(
                    x - size,
                    y - size,
                    x + size,
                    y + size,
                    fill=fill,
                    outline="",
                    tags="star"
                )

    # ==========================================
    # 3D ORBITS
    # ==========================================

    def animate_orbits(self):

        if self.power_on:

            self.rotation += 1.5

        # Three-dimensional orbit effect

        for i, particle in enumerate(
            self.orbit_particles
        ):

            angle = math.radians(
                self.rotation +
                i * 30
            )

            # Elliptical perspective

            radius_x = 245
            radius_y = 125

            x = (
                self.cx +
                math.cos(angle) *
                radius_x
            )

            y = (
                self.cy +
                math.sin(angle) *
                radius_y
            )

            depth = (
                math.sin(angle) +
                1
            ) / 2

            size = (
                3 +
                int(depth * 5)
            )

            self.canvas.coords(
                particle,
                x - size,
                y - size,
                x + size,
                y + size
            )

            if self.power_on:

                self.canvas.itemconfig(
                    particle,
                    fill="#66e6ff"
                )

            else:

                self.canvas.itemconfig(
                    particle,
                    fill="#1a2935"
                )

    # ==========================================
    # CORE ANIMATION
    # ==========================================

    def animate_core(self):

        self.pulse += 0.08

        if not self.power_on:

            self.canvas.itemconfig(
                self.energy_ring,
                outline="#24313b"
            )

            self.canvas.itemconfig(
                self.core,
                outline="#24313b"
            )

            return

        pulse = math.sin(
            self.pulse
        )

        size = int(
            7 + pulse * 5
        )

        self.canvas.coords(
            self.core,
            485 - size,
            285 - size,
            615 + size,
            415 + size
        )

        # State colors

        if self.state == "LISTENING":

            color = "#00ffcc"

        elif self.state == "THINKING":

            color = "#b56cff"

        elif self.state == "SPEAKING":

            color = "#66e6ff"

        else:

            color = "#66e6ff"

        self.canvas.itemconfig(
            self.energy_ring,
            outline=color
        )

        self.canvas.itemconfig(
            self.core,
            outline=color
        )

    # ==========================================
    # MAIN ANIMATION
    # ==========================================

    def animate(self):

        self.process_commands()

        self.animate_stars()

        self.animate_orbits()

        self.animate_core()

        self.root.after(
            30,
            self.animate
        )

    # ==========================================
    # CLOSE
    # ==========================================

    def close_window(self):

        self.power_on = False

        self.root.destroy()

    # ==========================================
    # RUN
    # ==========================================

    def run(self):

        self.root.mainloop()


# ==============================================
# TEST
# ==============================================

if __name__ == "__main__":

    hud = NovaHUD()

    hud.run()