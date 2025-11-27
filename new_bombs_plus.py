# New Bombs Plus - Mod de bombas extras para BombSquad
# Criado para uso educacional e recreativo

import babase
import bascenev1 as bs
import random

# ---------------------------------------------------------
#   REGISTRO DE ÍCONES
# ---------------------------------------------------------
def get_media():
    bs.getsound('explosion01')
    bs.gettexture('powerupBomb')
    bs.gettexture('powerupIceBomb')
    bs.gettexture('powerupImpactBomb')
    bs.gettexture('powerupStickyBomb')
    bs.gettexture('powerupPunch')

get_media()

# ---------------------------------------------------------
#   BASE DE UMA BOMBA CUSTOMIZADA
# ---------------------------------------------------------
class CustomBombFactory:
    def __init__(self,
                 model='bomb',
                 texture='powerupBomb',
                 big_explosion=False,
                 gravity_force=0.0,
                 color=(1, 1, 1)):
        
        self.model = bs.getmodel(model)
        self.texture = bs.gettexture(texture)
        self.big_explosion = big_explosion
        self.gravity_force = gravity_force
        self.color = color


# ---------------------------------------------------------
#   BOMBA GRAVITY CORE (gravitacional)
# ---------------------------------------------------------
class GravityBomb(bs.Actor):

    def __init__(self, position):
        super().__init__()
        factory = CustomBombFactory(
            texture='powerupImpactBomb',
            gravity_force=1.6,
            big_explosion=False,
            color=(0.3, 0.4, 1.0)
        )

        self.node = bs.newnode(
            'bomb',
            attrs={
                'position': position,
                'model': factory.model,
                'texture': factory.texture,
                'type': 'impact',
                'color_texture': factory.texture,
                'light_radius': 0.4,
                'light_color': factory.color
            },
            delegate=self
        )

    def explode(self):
        pos = self.node.position

        bs.emitfx(
            position=pos,
            count=40,
            scale=1.2,
            spread=1.6,
            chunk_type='spark'
        )

        # EFETOS DE "GRAVIDADE"
        for obj in bs.getnodes():
            try:
                if hasattr(obj, 'position'):
                    ox, oy, oz = obj.position
                    px, py, pz = pos
                    dx = (px - ox) * 16
                    dy = (py - oy) * 16
                    dz = (pz - oz) * 16
                    obj.handlemessage('impulse', ox, oy, oz, dx, dy, dz)
            except:
                pass

        bs.play_sound(bs.getsound('explosion01'), position=pos)
        bs.newnode('light', attrs={'color': (0.3, 0.4, 1.0), 'radius': 0.6, 'intensity': 1.8}).delete()


# ---------------------------------------------------------
#   BOMBA SOLAR CORE (explosão intensa)
# ---------------------------------------------------------
class SolarBomb(bs.Actor):

    def __init__(self, position):
        super().__init__()
        factory = CustomBombFactory(
            texture='powerupStickyBomb',
            big_explosion=True,
            color=(1.0, 0.6, 0.0)
        )

        self.node = bs.newnode(
            'bomb',
            attrs={
                'position': position,
                'model': factory.model,
                'texture': factory.texture,
                'type': 'normal',
                'light_radius': 0.7,
                'light_color': factory.color
            },
            delegate=self
        )

    def explode(self):
        pos = self.node.position

        bs.emitfx(
            position=pos,
            count=80,
            scale=1.5,
            spread=2.5,
            chunk_type='spark'
        )

        # Explosão forte
        bs.newnode(
            'explosion',
            attrs={'position': pos, 'velocity': (0, 0, 0), 'radius': 3.2}
        )

        bs.play_sound(bs.getsound('explosion01'), position=pos)


# ---------------------------------------------------------
#   BOMBA FUSION CORE (mistura instável)
# ---------------------------------------------------------
class FusionBomb(bs.Actor):

    def __init__(self, position):
        super().__init__()
        factory = CustomBombFactory(
            texture='powerupIceBomb',
            big_explosion=True,
            color=(0.7, 0.1, 1.0)
        )

        self.node = bs.newnode(
            'bomb',
            attrs={
                'position': position,
                'model': factory.model,
                'texture': factory.texture,
                'type': 'ice',
                'light_radius': 0.5,
                'light_color': factory.color
            },
            delegate=self
        )

    def explode(self):
        pos = self.node.position

        bs.emitfx(position=pos, count=60, scale=1.3, chunk_type='spark', spread=2.0)

        # explosão dupla
        for i in range(2):
            bs.newnode('explosion',
                attrs={'position': pos, 'velocity': (0, 0, 0), 'radius': 2.0 + i})

        bs.play_sound(bs.getsound('explosion01'), position=pos)


# ---------------------------------------------------------
#   SPAWN VIA CHAT
# ---------------------------------------------------------
def spawn_custom_bomb(bomb_type, position):
    if bomb_type == "gravity":
        GravityBomb(position)
    elif bomb_type == "solar":
        SolarBomb(position)
    elif bomb_type == "fusion":
        FusionBomb(position)


# Comandos
def chat_handler(msg):
    if not isinstance(msg, babase.ChatMessage):
        return

    text = msg.text.lower().strip()
    player = msg.source_player

    if text.startswith('/gravity'):
        spawn_custom_bomb("gravity", player.actor.node.position)
        return

    if text.startswith('/solar'):
        spawn_custom_bomb("solar", player.actor.node.position)
        return

    if text.startswith('/fusion'):
        spawn_custom_bomb("fusion", player.actor.node.position)
        return

babase.register_chat_message_handler(chat_handler)
