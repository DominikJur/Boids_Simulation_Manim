from manim import *
import numpy as np
from boids_2d import Boids2D
from boids_3d import Boids3D


class BoidsAnimation(ThreeDScene):
    def construct(self):
        self.N = 30
        
        # INTRO SCENE
        self.intro_scene()
        
        # Main title for simulation
        self.title = Text("Boids Flocking Behavior", font_size=36).to_edge(UP)
        self.play(Write(self.title))
        self.wait(1)
        
        # Run each phase with built-in transitions
        self.run_boids_phase("Default Behavior", 1.5, 1.0, 1.0, duration=15)
        self.run_boids_phase("High Cohesion", 1.5, 1.0, 2.25, duration=15)
        self.run_boids_phase("High Separation", 3.5, 1.0, 1.0, duration=15) 
        self.run_boids_phase("High Alignment", 2.0, 3.0, 1.0, duration=15)
        
        # Final fade out
        final_text = Text("End of Simulation", font_size=32, color=BLUE)
        self.play(Write(final_text))
        self.wait(2)
        self.play(FadeOut(final_text), FadeOut(self.title))
        
        # 3D TRANSITION
        self.transition_to_3d()
        
    def intro_scene(self):
        # Main title
        main_title = Text("BOIDS SIMULATION", font_size=48, color=BLUE)
        self.play(Write(main_title))
        self.wait(2)
        
        # Authors section
        authors_title = Text("Authors:", font_size=24, color=YELLOW).shift(DOWN*0.5)
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
            *[FadeOut(obj, shift=DOWN) for obj in [main_title, authors_title] + author_objects],
            run_time=1.5
        )
        
    def transition_to_3d(self):
        # Transition announcement
        transition_title = Text("Transitioning to 3D", font_size=40, color=GOLD)
        self.play(Write(transition_title))
        self.wait(1)
        self.play(FadeOut(transition_title))
        
        # Set up 3D scene
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1], 
            z_range=[-3, 3, 1],
            x_length=8,
            y_length=6,
            z_length=6,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        self.add(axes)
        self.play(Write(axes), run_time=1)
        
        # Main title for 3D simulation
        title_3d = Text("3D Boids Simulation", font_size=36, color=BLUE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title_3d)
        self.play(Write(title_3d))
        self.wait(1)
        
        # Run 3D phases with different parameters
        self.run_3d_boids_phase("3D Default Behavior", 1.5, 1.0, 1.0, axes, duration=12)
        self.run_3d_boids_phase("3D High Cohesion", 1.5, 1.0, 2.25, axes, duration=12)
        self.run_3d_boids_phase("3D High Separation", 3.5, 1.0, 1.0, axes, duration=12)
        self.run_3d_boids_phase("3D High Alignment", 2.0, 3.0, 1.0, axes, duration=12)
        
        # Final 3D outro - positioned lower
        outro_3d = Text("3D Boids Complete!", font_size=32, color=GOLD).shift(DOWN*2)
        self.add_fixed_in_frame_mobjects(outro_3d)
        self.play(Write(outro_3d))
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(axes),
            FadeOut(title_3d),
            FadeOut(outro_3d),
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
        
    def run_3d_boids_phase(self, name, sep_weight=1.5, align_weight=1.0, coh_weight=1.0, axes=None, duration=12):
        # Transition in effect
        transition_text = Text("Switching to...", font_size=24, color=GRAY)
        self.add_fixed_in_frame_mobjects(transition_text)
        self.play(FadeIn(transition_text))
        self.play(FadeOut(transition_text), run_time=0.5)
        
        # Create fresh 3D boids system
        boids_3d = Boids3D(n=25, size=100, 
                          separation_weight=sep_weight,
                          alignment_weight=align_weight, 
                          cohesion_weight=coh_weight)
        
        # Create cones
        cones = []
        cone_orientations = [np.array([1.0, 0.0, 0.0]) for _ in range(25)]  # Track orientations
        
        for i in range(25):
            cone = Cone(height=0.25, base_radius=0.08, resolution=8).set_color(BLUE)
            # Initially point cone along positive x-axis
            cone.rotate(PI/2, axis=UP)
            cones.append(cone)
            self.add(cone)
        
        # Animate cones appearing
        self.play(*[FadeIn(cone, scale=0.5) for cone in cones], run_time=1)
        
        # Phase label with animation
        phase_text = Text(name, font_size=32, color=YELLOW).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(phase_text)
        self.play(Write(phase_text))
        
        # Parameter displays with staggered animation
        sep_text = Text(f"Separation: {sep_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*2)
        align_text = Text(f"Alignment: {align_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*1.5)
        coh_text = Text(f"Cohesion: {coh_weight:.1f}", font_size=24).to_edge(LEFT).shift(UP*1)
        
        self.add_fixed_in_frame_mobjects(sep_text, align_text, coh_text)
        self.play(
            FadeIn(sep_text, shift=RIGHT),
            FadeIn(align_text, shift=RIGHT),
            FadeIn(coh_text, shift=RIGHT),
            lag_ratio=0.3,
            run_time=1.5
        )
        
        def update_3d(mob, dt):
            boids_3d.update()
            for i, cone in enumerate(cones):
                # Position mapping from 3D boids space to scene space
                x = (boids_3d.pos[i, 0] / boids_3d.size) * 5 - 2.5
                y = (boids_3d.pos[i, 1] / boids_3d.size) * 3.5 - 1.75
                z = (boids_3d.pos[i, 2] / boids_3d.size) * 3.5 - 1.75
                
                # Move cone to new position
                cone.move_to([x, y, z])
                
                # Orient cone to point in direction of velocity
                velocity = boids_3d.vel[i]
                if np.linalg.norm(velocity) > 0.01:
                    # Normalize velocity to get direction
                    new_direction = velocity / np.linalg.norm(velocity)
                    old_direction = cone_orientations[i]
                    
                    # Calculate rotation needed to go from old to new direction
                    dot_product = np.dot(old_direction, new_direction)
                    if dot_product < 0.999:  # Only rotate if significant change
                        # Calculate rotation axis and angle
                        rotation_axis = np.cross(old_direction, new_direction)
                        
                        if np.linalg.norm(rotation_axis) > 0.01:
                            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
                            rotation_angle = np.arccos(np.clip(dot_product, -1, 1))
                            
                            # Apply the rotation
                            cone.rotate(rotation_angle, axis=rotation_axis)
                            
                            # Update stored orientation
                            cone_orientations[i] = new_direction
        
        cones[0].add_updater(update_3d)
        self.wait(duration)
        
        # Clean up with transitions
        for cone in cones:
            cone.clear_updaters()
        
        # Fade out everything smoothly
        self.play(
            *[FadeOut(cone, scale=0.5) for cone in cones],
            FadeOut(phase_text, shift=DOWN),
            FadeOut(sep_text, shift=LEFT),
            FadeOut(align_text, shift=LEFT), 
            FadeOut(coh_text, shift=LEFT),
            run_time=1.5
        )