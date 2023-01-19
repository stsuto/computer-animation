import time
import random

from euclid import Vector3
from pyglet.gl import *

window = pyglet.window.Window()

texture = pyglet.image.load('particles/snow.bmp').get_texture()


class Particle:

    position_x_change_interval = (-400, 400)
    position_y_change_interval = (-300, 300)
    falling_direction = Vector3(10, 200, 0)
    life_duration = 100
    size_decrease = 5

    def __init__(self, position):
        self.position = position.copy()
        self.position[0] += random.uniform(*Particle.position_x_change_interval)
        self.position[1] += random.uniform(*Particle.position_y_change_interval)
        self.direction = Particle.falling_direction + Vector3(random.randint(-100, 100), random.randint(-100, 100), 0)
        # print(self.direction)
        self.time_of_death = time.time() + Particle.life_duration
        self.size = 20

    def update(self, dtime):
        self.position -= self.direction * dtime
        self.size -= Particle.size_decrease * dtime


class ParticleSystem:

    source = Vector3(300, 500, 0)

    def __init__(self, num_of_particles: int = 1):
        self.particles = []
        self.addParticles(num_of_particles)

    def addParticles(self, num_of_particles: int):
        for i in range(num_of_particles):
            self.particles.append(Particle(ParticleSystem.source))

    def update(self, dtime: time.time):
        for p in self.particles:
            p.update(dtime)

        t = time.time()

        for i in range(len(self.particles) - 1, -1, -1):
            if (self.particles[i].time_of_death <= t) or (self.particles[i].position[1] < -100):
                del self.particles[i]
                if random.choice([True, False]):
                    self.addParticles(1)


system = ParticleSystem(300)


@window.event
def on_draw():
    glClearColor(0, 0.4, 0.6, 0)
    glClear(GL_COLOR_BUFFER_BIT)

    glColor3f(1, 1, 1)
    glEnable(texture.target)
    glBindTexture(texture.target, texture.id)
    glEnable(GL_BLEND)
    glBlendFunc(GL_ONE, GL_ONE)
    glBegin(GL_QUADS)

    for p in system.particles:
        size = p.size
        glTexCoord2f(0, 0)
        glVertex3f(p.position[0] - size, p.position[1] - size, p.position[2])
        glTexCoord2f(1, 0)
        glVertex3f(p.position[0] + size, p.position[1] - size, p.position[2])
        glTexCoord2f(1, 1)
        glVertex3f(p.position[0] + size, p.position[1] + size, p.position[2])
        glTexCoord2f(0, 1)
        glVertex3f(p.position[0] - size, p.position[1] + size, p.position[2])

    glEnd()
    glDisable(GL_BLEND)
    glDisable(texture.target)


def update(dtime):
    system.update(dtime)


pyglet.clock.schedule_interval(update, 1 / 1000.0)
pyglet.app.run()
