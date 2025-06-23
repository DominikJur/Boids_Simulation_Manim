from manim import *
import numpy as np
from boids_3d import Boids3D


class Boids3DDebug(ThreeDScene):
    def construct(self):
        # Set initial camera position for better 3D view
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
        
        # Add axis labels
        x_label = Text("X", font_size=24).next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("Y", font_size=24).next_to(axes.y_axis.get_end(), UP)
        z_label = Text("Z", font_size=24).next_to(axes.z_axis.get_end(), OUT)
        
        # Make labels fixed to frame so they don't rotate
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        
        # Add axes to scene
        self.add(axes)
        self.play(Write(axes), Write(x_label), Write(y_label), Write(z_label))
        
        # Title
        title = Text("3D Boids Debug", font_size=36, color=BLUE).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Create 3D boids system with fewer boids for easier debugging
        boids_3d = Boids3D(n=10, size=30, 
                          separation_weight=1.5, 
                          alignment_weight=1.5, 
                          cohesion_weight=1.5,
                          max_speed=1.0)  # Slower for easier observation
        
        # Create cones
        cones = []
        for i in range(10):
            cone = Cone(height=0.4, base_radius=0.15, resolution=8)
            cone.set_color(BLUE)
            # Initially point cone along positive x-axis (tip direction)
            cone.rotate(PI/2, axis=UP)  # Rotate so tip points along x-axis
            cones.append(cone)
            self.add(cone)
        
        # Animate cones appearing
        self.play(*[FadeIn(cone, scale=0.5) for cone in cones], run_time=1.5)
        
        # Parameter display
        params = Text("3D Boids Parameters:\nSeparation: 1.5\nAlignment: 1.5\nCohesion: 1.5\nSpeed: 1.0", 
                     font_size=18).to_corner(UL)
        self.add_fixed_in_frame_mobjects(params)
        self.play(FadeIn(params))
        
        # Debug info
        debug_info = Text("Debug Mode:\n• Red axes for reference\n• Slower movement\n• Cone tips point forward", 
                         font_size=16, color=YELLOW).to_corner(UR)
        self.add_fixed_in_frame_mobjects(debug_info)
        self.play(FadeIn(debug_info))
        
        # Store previous orientations to track changes
        cone_orientations = [np.array([1.0, 0.0, 0.0]) for _ in range(10)]  # Initial direction vectors
        
        def update_3d_boids(mob, dt):
            boids_3d.update()
            
            for i, cone in enumerate(cones):
                # Map boid position to scene coordinates
                x = (boids_3d.pos[i, 0] / boids_3d.size) * 6 - 3
                y = (boids_3d.pos[i, 1] / boids_3d.size) * 4 - 2  
                z = (boids_3d.pos[i, 2] / boids_3d.size) * 4 - 2
                
                # Move cone to new position
                cone.move_to([x, y, z])
                
                # Orient cone to point in direction of velocity
                velocity = boids_3d.vel[i]
                if np.linalg.norm(velocity) > 0.01:
                    # Normalize velocity to get direction
                    new_direction = velocity / np.linalg.norm(velocity)
                    old_direction = cone_orientations[i]
                    
                    # Calculate rotation needed to go from old to new direction
                    # Only rotate if there's a significant change
                    dot_product = np.dot(old_direction, new_direction)
                    if dot_product < 0.999:  # Only rotate if angle > ~2.5 degrees
                        # Calculate rotation axis and angle
                        rotation_axis = np.cross(old_direction, new_direction)
                        
                        if np.linalg.norm(rotation_axis) > 0.01:
                            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
                            rotation_angle = np.arccos(np.clip(dot_product, -1, 1))
                            
                            # Apply the rotation
                            cone.rotate(rotation_angle, axis=rotation_axis)
                            
                            # Update stored orientation
                            cone_orientations[i] = new_direction
        
        # Add updater to first cone (this updates all cones)
        cones[0].add_updater(update_3d_boids)
        
        # Camera movement during simulation
        self.play(Write(Text("Starting simulation...", font_size=24).shift(DOWN*3)), run_time=1)
        self.remove(self.mobjects[-1])  # Remove the text
        
        # Slow camera rotation for better observation
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(15)  # Longer observation time
        
        # Stop rotation and show different angles
        self.stop_ambient_camera_rotation()
        
        # Show from different angles
        angle_text = Text("Viewing from different angles...", font_size=20, color=GREEN)
        self.add_fixed_in_frame_mobjects(angle_text)
        self.play(Write(angle_text))
        
        # Top view
        self.move_camera(phi=0 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.wait(3)
        
        # Side view  
        self.move_camera(phi=90 * DEGREES, theta=0 * DEGREES, run_time=2)
        self.wait(3)
        
        # Angled view
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, run_time=2)
        self.wait(3)
        
        self.play(FadeOut(angle_text))
        
        # Final notes
        final_text = Text("3D Boids Debug Complete!\nCones should point in movement direction", 
                         font_size=24, color=GOLD)
        self.add_fixed_in_frame_mobjects(final_text)
        self.play(Write(final_text))
        self.wait(2)
        
        # # Clean up
        # for cone in cones:
        #     cone.clear_updaters()
        
        # self.play(
        #     *[FadeOut(cone) for cone in cones],
        #     FadeOut(axes),
        #     FadeOut(title),
        #     FadeOut(params),
        #     FadeOut(debug_info),
        #     FadeOut(final_text),
        #     FadeOut(x_label),
        #     FadeOut(y_label), 
        #     FadeOut(z_label),
        #     run_time=2
        # )