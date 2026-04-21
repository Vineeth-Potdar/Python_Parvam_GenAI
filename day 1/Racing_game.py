from ursina import *
import random

# Game constants
TRACK_LENGTH = 100
LANE_WIDTH = 4
NUM_LANES = 3
NUM_OPPONENTS = 2

class Car(Entity):
    def __init__(self, position, color, is_player=False):
        super().__init__(
            model='cube',
            scale=(1, 0.5, 2),
            color=color,
            position=position,
            collider='box'
        )
        self.is_player = is_player
        self.speed = 10
        self.lane = 0 if not is_player else 1

    def update(self):
        if self.is_player:
            # Player controls
            if held_keys['a'] or held_keys['left arrow']:
                self.x -= 5 * time.dt
            if held_keys['d'] or held_keys['right arrow']:
                self.x += 5 * time.dt
            # Keep in bounds
            self.x = max(-LANE_WIDTH, min(LANE_WIDTH, self.x))
        else:
            # AI movement
            self.z += self.speed * time.dt
            # Random lane changes
            if random.random() < 0.01:  # Small chance
                self.lane = max(0, min(NUM_LANES-1, self.lane + random.choice([-1, 1])))
                self.x = (self.lane - 1) * LANE_WIDTH

        # Move forward
        self.z += self.speed * time.dt

        # Check win condition
        if self.z > TRACK_LENGTH:
            if self.is_player:
                print("You win!")
            else:
                print("Opponent wins!")
            application.quit()

def create_track():
    # Create ground
    ground = Entity(model='plane', scale=(50, 1, TRACK_LENGTH*2), texture='grass', position=(0, -0.5, TRACK_LENGTH/2))
    
    # Create road
    road = Entity(model='plane', scale=(LANE_WIDTH*NUM_LANES, 1, TRACK_LENGTH*2), color=color.gray, position=(0, 0, TRACK_LENGTH/2))
    
    # Lane dividers
    for i in range(1, NUM_LANES):
        divider = Entity(model='cube', scale=(0.1, 0.1, TRACK_LENGTH*2), color=color.yellow, position=((i-1)*LANE_WIDTH, 0.1, TRACK_LENGTH/2))

def update():
    # Update camera to follow player
    camera.position = (player.x, 5, player.z - 10)
    camera.look_at(player)

app = Ursina()

# Create track
create_track()

# Create player
player = Car(position=(0, 0, 0), color=color.red, is_player=True)

# Create opponents
opponents = []
for i in range(NUM_OPPONENTS):
    lane = 0 if i == 0 else 2
    opp = Car(position=((lane-1)*LANE_WIDTH, 0, -10 - i*5), color=color.blue if i == 0 else color.green)
    opponents.append(opp)

# Sky
sky = Sky()

app.run()