import numpy as np


class Boids3D:
    def __init__(self, 
                 n=50, 
                 size=100,
                 max_speed=2.0,
                 max_force=0.1,
                 separation_radius=3.0,
                 alignment_radius=10.0,
                 cohesion_radius=10.0,
                 separation_weight=1.5,
                 alignment_weight=1.0,
                 cohesion_weight=1.0):
        self.n = n
        self.size = size
        self.max_speed = max_speed
        self.max_force = max_force
        self.separation_radius = separation_radius
        self.alignment_radius = alignment_radius
        self.cohesion_radius = cohesion_radius
        self.separation_weight = separation_weight
        self.alignment_weight = alignment_weight
        self.cohesion_weight = cohesion_weight
        
        # Random positions and velocities in 3D
        self.pos = np.random.random((n, 3)) * size
        self.vel = (np.random.random((n, 3)) - 0.5) * max_speed
        
        # Normalize initial velocities
        speeds = np.linalg.norm(self.vel, axis=1)
        speeds = np.where(speeds == 0, 1, speeds)
        self.vel = self.vel / speeds[:, np.newaxis] * max_speed
    
    def limit_force(self, force):
        magnitude = np.linalg.norm(force)
        if magnitude > self.max_force:
            return force / magnitude * self.max_force
        return force
    
    def boundary_force(self, position, velocity):
        force = np.zeros(3)
        margin = 10
        
        if position[0] < margin:
            force[0] = self.max_speed
        elif position[0] > self.size - margin:
            force[0] = -self.max_speed
            
        if position[1] < margin:
            force[1] = self.max_speed
        elif position[1] > self.size - margin:
            force[1] = -self.max_speed
            
        if position[2] < margin:
            force[2] = self.max_speed
        elif position[2] > self.size - margin:
            force[2] = -self.max_speed
        
        if np.linalg.norm(force) > 0:
            force = force / np.linalg.norm(force) * self.max_speed
            force = force - velocity
            force = self.limit_force(force)
        
        return force
    
    def update(self):
        accelerations = np.zeros_like(self.vel)
        
        for i in range(self.n):
            distances = np.sqrt(np.sum((self.pos - self.pos[i])**2, axis=1))
            
            sep_neighbors = (distances < self.separation_radius) & (distances > 0)
            align_neighbors = (distances < self.alignment_radius) & (distances > 0)
            coh_neighbors = (distances < self.cohesion_radius) & (distances > 0)
            
            # Separation
            sep_force = np.zeros(3)
            if np.any(sep_neighbors):
                for j in range(self.n):
                    if sep_neighbors[j]:
                        diff = self.pos[i] - self.pos[j]
                        distance = distances[j]
                        if distance > 0:
                            sep_force += diff / (distance ** 2)
                
                if np.linalg.norm(sep_force) > 0:
                    sep_force = sep_force / np.linalg.norm(sep_force) * self.max_speed
                    sep_force = sep_force - self.vel[i]
                    sep_force = self.limit_force(sep_force)
            
            # Alignment
            align_force = np.zeros(3)
            if np.any(align_neighbors):
                avg_velocity = np.mean(self.vel[align_neighbors], axis=0)
                if np.linalg.norm(avg_velocity) > 0:
                    desired = avg_velocity / np.linalg.norm(avg_velocity) * self.max_speed
                    align_force = desired - self.vel[i]
                    align_force = self.limit_force(align_force)
            
            # Cohesion
            coh_force = np.zeros(3)
            if np.any(coh_neighbors):
                center_of_mass = np.mean(self.pos[coh_neighbors], axis=0)
                desired = center_of_mass - self.pos[i]
                if np.linalg.norm(desired) > 0:
                    desired = desired / np.linalg.norm(desired) * self.max_speed
                    coh_force = desired - self.vel[i]
                    coh_force = self.limit_force(coh_force)
            
            boundary_force = self.boundary_force(self.pos[i], self.vel[i])
            
            total_force = (sep_force * self.separation_weight + 
                          align_force * self.alignment_weight + 
                          coh_force * self.cohesion_weight +
                          boundary_force * 2.0)
            
            accelerations[i] = total_force
        
        self.vel += accelerations
        speeds = np.linalg.norm(self.vel, axis=1)
        speed_limiters = np.minimum(speeds, self.max_speed) / np.maximum(speeds, 1e-8)
        self.vel *= speed_limiters[:, np.newaxis]
        self.pos += self.vel
        self.pos = np.clip(self.pos, 0, self.size)