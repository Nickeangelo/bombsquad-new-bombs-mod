# New Bombs Plus - Mod de bombas customizadas para BombSquad
# Compatível com Plugin Manager
# Desenvolvido para uso recreativo

import babase
import bascenev1 as bs

# ---------------------------------------------------------
#   BASE DAS BOMBAS CUSTOMIZADAS
# ---------------------------------------------------------

class BaseCustomBomb(bs.Actor):
    def __init__(self, position, bomb_type, texture, color, explosion_radius):
        super().__init__()

        self.node = bs.newnode(
            'bomb',
            attrs={
                'position': position,
                'model': bs.getmodel('bomb'),
                'texture': bs.gettexture(texture),
                'light_radius': 0.5,
                'light_color': color,
                'type': bomb_type
            },
            delegate=self
        )

        self.explosion_radius = explosion_radius
        self.color = color

    def explode(self):
        pos = self.node.position

        bs.emitfx(
            position=pos,
            count=60,
            scale=1.4,
            spread=2.0,
            chunk_type='spark'
        )

        bs.newnode(
            'explosion',
            attrs={'position': pos, 'velocity': (0, 0, 0), 'radius': self.explosion_radius}
        )

        bs.play_sound(bs.getsound('explosion01'), position=pos)


# ---------------------------------------------------------
#   BOMBAS ESPECIAIS
# ---------------------------------------------------------

class GravityCoreBomb(BaseCustomBomb):
    def __init__(self, position):
        super().__init__(
            position,
            bomb_type='impact',
            texture='powerupImpactBomb',
            color=(0.3, 0.4, 1.0),
            explosion_radius=2.2
        )

    def explode(self):
        pos = self.node.position

        # Efeito de puxar objetos
        for obj in bs.getnodes():
            try:
                if hasattr(obj, 'position'):
                    ox, oy, oz = obj.position
                    px, py, pz = pos
                    dx = (px - ox) * 18
                    dy = (py - oy) * 18
                    dz = (pz - oz) * 18
                    obj.handlemessage('impulse', ox, oy, oz, dx, dy, dz)
            except:
                pass

        super().explode()


class SolarCoreBomb(BaseCustomBomb):
    def __init__(self, position):
        super().__init__(
            position,
            bomb_type='normal',
            texture='powerupStickyBomb',
            color=(1.0, 0.6, 0.0),
            explosion_radius=3.4
        )


class FusionCoreBomb(BaseCustomBomb):
    def __init__(self, position):
        super().__init__(
            position,
            bomb_type='ice',
            texture='powerupIceBomb',
            color=(0.7, 0.1, 1.0),
            explosion_radius=2.6
        )

    def explode(self):
        pos = self.node.position

        # explosão dupla
        for i in range(2):
            bs.newnode(
                'explosion',
                attrs={'position': pos, 'velocity': (0, 0, 0), 'radius': 2.0 + i}
            )

        super().explode()


# ---------------------------------------------------------
#   COMANDOS DE CHAT
# ---------------------------------------------------------

def spawn_custom_bomb(kind, position):
    if kind == "gravity":
        GravityCoreBomb(position)
    elif kind == "solar":
        SolarCoreBomb(position)
    elif kind == "fusion":
        FusionCoreBomb(position)


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


# registrar comandos
babase.register_chat_message_handler(chat_handler)
