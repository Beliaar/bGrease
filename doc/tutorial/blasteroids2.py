import math
import random
import pyglet
import grease
from grease import component, controller, renderer, geometry
from pyglet.window import key
from grease.pygletsys import KeyControls


class PlayerShip(grease.Entity):
    """Thrust ship piloted by the player"""

    THRUST_ACCEL = 75
    TURN_RATE = 240
    SHAPE_VERTS = [
        (-8, -12), (-4, -10), (0, -8), (4, -10), (8, -12), # flame
        (0, 12), (-8, -12), (0, -8), (8, -12)]
    COLOR = "#7f7"

    def __init__(self, world, invincible=False):
        self.position.position = (0, 0)
        self.position.angle = 0
        self.movement.velocity = (0, 0)
        self.movement.rotation = 0
        self.shape.verts = self.SHAPE_VERTS
        self.shape.closed = False
        self.renderable.color = self.COLOR

    def turn(self, direction):
        self.movement.rotation = self.TURN_RATE * direction
    
    def thrust_on(self):
        thrust_vec = geometry.Vec2d(0, self.THRUST_ACCEL)
        thrust_vec.rotate(self.position.angle)
        self.movement.accel = thrust_vec
        self.shape.verts[2] = (0, -16 - random.random() * 16)        

    def thrust_off(self):
        self.movement.accel = (0, 0)
        self.shape.verts[2] = (0, -8)


class Asteroid(grease.Entity):
    """Big floating space rock"""

    UNIT_CIRCLE = [(math.sin(math.radians(a)), math.cos(math.radians(a))) 
        for a in range(0, 360, 18)]

    def __init__(self, world, radius=45):
        self.position.position = (
            random.choice([-1, 1]) * random.randint(50, window.width / 2), 
            random.choice([-1, 1]) * random.randint(50, window.height / 2))
        self.movement.velocity = (random.gauss(0, 700 / radius), random.gauss(0, 700 / radius))
        self.movement.rotation = random.gauss(0, 15)
        verts = [(random.gauss(x * radius, radius / 7), random.gauss(y * radius, radius / 7))
            for x, y in self.UNIT_CIRCLE]
        self.shape.verts = verts
        self.renderable.color = "#aaa"


class GameSystem(KeyControls):
    """Main game logic system

    This subclass KeyControls so that the controls can be bound
    directly to the game logic here
    """

    def set_world(self, world):
        KeyControls.set_world(self, world)
        self.player_ship = PlayerShip(self.world)

    @KeyControls.key_press(key.LEFT)
    @KeyControls.key_press(key.A)
    def start_turn_left(self):
        if self.player_ship.exists:
            self.player_ship.turn(-1)

    @KeyControls.key_release(key.LEFT)
    @KeyControls.key_release(key.A)
    def stop_turn_left(self):
        if self.player_ship.exists and self.player_ship.movement.rotation < 0:
            self.player_ship.turn(0)

    @KeyControls.key_press(key.RIGHT)
    @KeyControls.key_press(key.D)
    def start_turn_right(self):
        if self.player_ship.exists:
            self.player_ship.turn(1)

    @KeyControls.key_release(key.RIGHT)
    @KeyControls.key_release(key.D)
    def stop_turn_right(self):
        if self.player_ship.exists and self.player_ship.movement.rotation > 0:
            self.player_ship.turn(0)
    
    @KeyControls.key_hold(key.UP)
    @KeyControls.key_hold(key.W)
    def thrust(self, dt):
        if self.player_ship.exists:
            self.player_ship.thrust_on()
        
    @KeyControls.key_release(key.UP)
    @KeyControls.key_release(key.W)
    def stop_thrust(self):
        if self.player_ship.exists:
            self.player_ship.thrust_off()
            
    @KeyControls.key_press(key.SPACE)
    def start_firing(self):
        if self.player_ship.exists:
            self.player_ship.gun.firing = True

    @KeyControls.key_release(key.SPACE)
    def stop_firing(self):
        if self.player_ship.exists:
            self.player_ship.gun.firing = False
    
    @KeyControls.key_press(key.P)
    def pause(self):
        self.world.running = not self.world.running 


class GameWorld(grease.World):

    def configure(self):
        """Configure the game world's components, systems and renderers"""
        self.components.position = component.Position()
        self.components.movement = component.Movement()
        self.components.shape = component.Shape()
        self.components.renderable = component.Renderable()
        self.components.collision = component.Collision()        

        self.systems.movement = controller.EulerMovement()
        self.systems.game = GameSystem()
        self.systems.collision = collision.Circular(
            handlers=[collision.dispatch_events])

        self.renderers.camera = renderer.Camera(
            position=(window.width / 2, window.height / 2))
        self.renderers.vector = renderer.Vector(line_width=1.5)


def main():
    """Initialize and run the game"""
    global window
    window = pyglet.window.Window()
    world = GameWorld()
    pyglet.clock.schedule(world.tick)
    window.push_handlers(world)
    window.push_handlers(world.systems.game)
    for i in range(8):
        Asteroid(world)
    pyglet.app.run()

if __name__ == '__main__':
    main()


# vim: ai ts=4 sts=4 et sw=4

