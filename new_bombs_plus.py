# New Bombs Plus - BombSquad Mod
# Author: Nickeangelo
# Adds new custom bombs with unique effects.

import babase
import bascenev1 as bs
import random
import math
from typing import Any, Sequence

# -----------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------

def _make_explosion(position: Sequence[float],
                    radius: float = 3.0,
                    damage: float = 250.0,
                    scorch: bool = True):
    """Creates a powerful explosion effect."""
    activity = bs.getactivity()
    if activity is None:
        return

    bs.Blast(position=position,
            velocity=(0, 0, 0),
            blast_radius=radius,
            hit_type="explosion",
            hit_subtype="new_bomb",
            source_player=None).autoretain()

    # Optional scorch mark
    if scorch:
        try:
            bs.emitfx(position=position,
                      count=20,
                      scale=1.2,
                      spread=3.0,
                      chunk_type="spark")
        except Exception:
            pass

# -----------------------------------------------------------
# Base Class for Custom Bombs
# -----------------------------------------------------------

class CustomBomb(bs.Bomb):
    """Base class for the new bombs."""
    bomb_type = "custom"
    texture = None
    light_color = (1, 1, 1)

    def __init__(self, **k: Any):
        super().__init__(bomb_type=self.bomb_type, **k)

        # Change the bomb's appearance
        if self.texture is not None:
            m = self.node.getdelegate()
            if m is not None:
                try:
                    self.node.texture = self.texture
                except Exception:
                    pass

        # Add a light effect
        try:
            self.light = bs.newnode(
                'light',
                attrs={
                    'color': self.light_color,
                    'radius': 0.3,
                    'intensity': 0.8
                }
            )
            bs.connectattr(self.node, 'position', self.light, 'position')
        except Exception:
            self.light = None

# -----------------------------------------------------------
# Gravity Bomb
# -----------------------------------------------------------

class GravityBomb(CustomBomb):
    bomb_type = "gravity_bomb"
    light_color = (0.3, 0.3, 1.0)

    def explode(self):
        super().explode()
        
        pos = self.node.position
        activity = bs.getactivity()

        if activity:
            for obj in activity.players + activity.objects:
                try:
                    op = obj.node.position
                    dx = pos[0] - op[0]
                    dy = pos[1] - op[1]
                    dz = pos[2] - op[2]
                    dist = max(0.1, (dx*dx + dy*dy + dz*dz) ** 0.5)

                    force = 750.0 / dist
                    obj.node.applyimpulse((dx/dist * force,
                                           dy/dist * force,
                                           dz/dist * force))
                except Exception:
                    continue

        _make_explosion(pos, radius=2.5, damage=150.0, scorch=False)

# -----------------------------------------------------------
# Mini Nuke Bomb
# -----------------------------------------------------------

class MiniNukeBomb(CustomBomb):
    bomb_type = "mini_nuke"
    light_color = (1.0, 0.6, 0.2)

    def explode(self):
        super().explode()
        pos = self.node.position

        # Flash effect
        try:
            bs.emitfx(position=pos,
                      count=40,
                      scale=2.0,
                      spread=6.0,
                      chunk_type="spark")
        except Exception:
            pass

        # Powerful explosion
        _make_explosion(pos, radius=4.0, damage=400.0, scorch=True)

        # Shockwave
        activity = bs.getactivity()
        if activity:
            for obj in activity.players + activity.objects:
                try:
                    op = obj.node.position
                    dx = op[0] - pos[0]
                    dy = op[1] - pos[1]
                    dz = op[2] - pos[2]
                    dist = max(0.3, math.sqrt(dx*dx + dy*dy + dz*dz))

                    force = 1200.0 / dist
                    obj.node.applyimpulse((dx/dist * force,
                                           dy/dist * force,
                                           dz/dist * force))
                except Exception:
                    continue

# -----------------------------------------------------------
# Atomic Bomb (Large Nuke)
# -----------------------------------------------------------

class AtomicBomb(CustomBomb):
    bomb_type = "atomic_bomb"
    light_color = (1.0, 0.9, 0.4)

    def explode(self):
        super().explode()
        pos = self.node.position

        # Big flash
        try:
            bs.emitfx(position=pos,
                      count=80,
                      scale=3.5,
                      spread=9.0,
                      chunk_type="spark")
        except Exception:
            pass

        # Extremely large explosion
        _make_explosion(pos, radius=6.5, damage=800.0, scorch=True)

        # Massive knockback
        activity = bs.getactivity()
        if activity:
            for obj in activity.players + activity.objects:
                try:
                    op = obj.node.position
                    dx = op[0] - pos[0]
                    dy = op[1] - pos[1]
                    dz = op[2] - pos[2]
                    dist = max(0.3, math.sqrt(dx*dx + dy*dy + dz*dz))

                    force = 2000.0 / dist
                    obj.node.applyimpulse((-dx/dist * force,
                                           -dy/dist * force,
                                           -dz/dist * force))
                except Exception:
                    continue

# -----------------------------------------------------------
# Register Bomb Types
# -----------------------------------------------------------

def register_bombs():
    """Registers new bombs so they can spawn in-game."""
    try:
        bs.getspecialbomboffering().add_available_bomb(
            bomb_type="gravity_bomb",
            label="Gravity Bomb"
        )
        bs.getspecialbomboffering().add_available_bomb(
            bomb_type="mini_nuke",
            label="Mini Nuke"
        )
        bs.getspecialbomboffering().add_available_bomb(
            bomb_type="atomic_bomb",
            label="Atomic Bomb"
        )
    except Exception as e:
        print("Bomb registration error:", e)

# -----------------------------------------------------------
# Plugin Entry Point
# -----------------------------------------------------------

class NewBombsPlusPlugin(babase.Plugin):
    """Main plugin class."""

    def on_app_launch(self):
        # Register bombs on launch
        register_bombs()
        print("New Bombs Plus loaded successfully.")
