from manim import *
import numpy as np
from boids import Boids2D

class BoidsAnimation(Scene):
    def construct(self):
        self.N = 30
        
        # INTRO SCENE
        self.intro_scene()
        
        # Main title for simulation
        self.title = Text("Boids Flocking Behavior", font_size=36).to_edge(UP)
        self.play(Write(self.title))
        self.wait(1)
        
        # Run each phase with built-in transitions
        self.run_boids_phase("Default Behavior", 1.5, 1.0, 1.0)
        self.run_boids_phase("High Cohesion", 1.5, 1.0, 3.0)
        self.run_boids_phase("High Separation", 3.0, 1.0, 1.0) 
        self.run_boids_phase("High Alignment", 1.5, 3.0, 1.0)
        
        # Final fade out
        final_text = Text("End of Simulation", font_size=32, color=BLUE)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text), FadeOut(self.title))
        
    def intro_scene(self):
        # Main title
        main_title = Text("BOIDS SIMULATION", font_size=48, color=BLUE)
        self.play(Write(main_title))
        self.wait(1.5)
        
        # Subtitle
        subtitle = Text("Emergent Flocking Behavior", font_size=28, color=WHITE).next_to(main_title, DOWN, buff=0.5)
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        
        # Authors section
        authors_title = Text("Authors:", font_size=24, color=YELLOW).shift(DOWN*1)
        self.play(Write(authors_title))
        
        authors = [
            "Dominik Jur",
            "Szymon Klim", 
            "Kacper Samulaki",
            "Albert Janik"
        ]
        
        author_objects = []
        for i, author in enumerate(authors):
            author_text = Text(author, font_size=22).next_to(authors_title, DOWN, buff=0.3 + i*0.4)
            author_objects.append(author_text)
            self.play(FadeIn(author_text, shift=LEFT), run_time=0.6)
        
        self.wait(2)
        
        # Fade out intro
        self.play(
            *[FadeOut(obj, shift=DOWN) for obj in [main_title, subtitle, authors_title] + author_objects],
            run_time=1.5
        )
        
    def run_boids_phase(self, name, sep_weight=1.5, align_weight=1.0, coh_weight=1.0, duration=12):
        # Transition in effect
        transition_text = Text("Switching to...", font_size=24, color=GRAY)
        self.play(FadeIn(transition_text))
        self.play(FadeOut(transition_text), run_time=0.5)
        
        # Create fresh boids system
        boids = Boids2D(n=self.N, size=50, 
                       separation_weight=sep_weight,
                       alignment_weight=align_weight, 
                       cohesion_weight=coh_weight)
        
        # Create triangles
        triangles = []
        triangle_angles = [0.0 for _ in range(self.N)]
        
        for i in range(self.N):
            triangle = Triangle().scale(0.15).set_color(BLUE)
            triangles.append(triangle)
        
        # Animate triangles appearing
        self.play(*[FadeIn(triangle, scale=0.5) for triangle in triangles], run_time=1)
        
        # Phase label with animation
        phase_text = Text(name, font_size=32, color=YELLOW).to_edge(DOWN)
        self.play(Write(phase_text))
        
        # Parameter displays with staggered animation
        sep_text = Text(f"Separation: {sep_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*2)
        align_text = Text(f"Alignment: {align_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*1.5)
        coh_text = Text(f"Cohesion: {coh_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*1)
        
        self.play(
            FadeIn(sep_text, shift=RIGHT),
            FadeIn(align_text, shift=RIGHT),
            FadeIn(coh_text, shift=RIGHT),
            lag_ratio=0.3,
            run_time=1.5
        )
        
        def update(mob, dt):
            boids.update()
            for i, triangle in enumerate(triangles):
                # Position
                x = (boids.pos[i, 0] / boids.size) * 10 - 5
                y = (boids.pos[i, 1] / boids.size) * 6 - 3
                triangle.move_to([x, y, 0])
                
                # Rotation
                velocity = boids.vel[i]
                if np.linalg.norm(velocity) > 0.01:
                    new_angle = np.arctan2(velocity[1], velocity[0])
                    angle_diff = new_angle - triangle_angles[i]
                    triangle.rotate(angle_diff)
                    triangle_angles[i] = new_angle
        
        triangles[0].add_updater(update)
        self.wait(duration)
        
        # Clean up with transitions
        for triangle in triangles:
            triangle.clear_updaters()
        
        # Fade out everything smoothly
        self.play(
            *[FadeOut(triangle, scale=0.5) for triangle in triangles],
            FadeOut(phase_text, shift=DOWN),
            FadeOut(sep_text, shift=LEFT),
            FadeOut(align_text, shift=LEFT), 
            FadeOut(coh_text, shift=LEFT),
            run_time=1.5
        )