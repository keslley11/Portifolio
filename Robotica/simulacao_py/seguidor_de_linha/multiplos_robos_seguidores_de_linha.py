import pygame
import math
import random

# Inicialização
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Múltiplos Robôs Seguidores de Linha")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)
VERDE = (0, 150, 0)

# Linha (trajetória oval)
def desenhar_pista(surface):
    ret = pygame.Rect(150, 150, 500, 300)
    pygame.draw.ellipse(surface, PRETO, ret, 10)

# Robo
class Robo:
    def __init__(self, x, y, kp, ki, kd, id=1):
        self.x = x
        self.y = y
        self.inicial_x = x
        self.inicial_y = y
        self.angulo = -90
        self.vel_base = 2.0
        self.vel_esq = 0
        self.vel_dir = 0
        self.vel_esq_alvo = 0
        self.vel_dir_alvo = 0
        self.resposta_lenta = 0.06

        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.erro_anterior = 0
        self.erro_acumulado = 0
        self.ultimo_erro = 0

        self.voltas = 0
        self.oscilacoes = 0
        self.ultimo_setor = False
        self.trilha = []
        self.tamanho = 60
        self.id = id

    def sensores(self):
        frente_offset = self.tamanho * 0.3
        lado_offset = self.tamanho * 0.3
        angulo_rad = math.radians(self.angulo)

        frente_x = self.x + frente_offset * math.cos(angulo_rad)
        frente_y = self.y + frente_offset * math.sin(angulo_rad)

        perp_rad = angulo_rad + math.pi / 2

        sensor_esq = (
            int(frente_x + lado_offset * math.cos(perp_rad)),
            int(frente_y + lado_offset * math.sin(perp_rad))
        )
        sensor_dir = (
            int(frente_x - lado_offset * math.cos(perp_rad)),
            int(frente_y - lado_offset * math.sin(perp_rad))
        )
        return sensor_esq, sensor_dir

    def atualizar(self, pista_surface):
        sensor_esq, sensor_dir = self.sensores()

        cor_esq = pista_surface.get_at(sensor_esq)[:3] if 0 <= sensor_esq[0] < largura and 0 <= sensor_esq[1] < altura else BRANCO
        cor_dir = pista_surface.get_at(sensor_dir)[:3] if 0 <= sensor_dir[0] < largura and 0 <= sensor_dir[1] < altura else BRANCO

        s_esq = 1 if cor_esq == PRETO else 0
        s_dir = 1 if cor_dir == PRETO else 0
        erro = s_esq - s_dir

        if erro != self.ultimo_erro and erro != 0:
            self.oscilacoes += 1
        self.ultimo_erro = erro

        self.erro_acumulado += erro
        derivada = erro - self.erro_anterior
        saida_pid = self.kp * erro + self.ki * self.erro_acumulado + self.kd * derivada
        self.erro_anterior = erro

        self.vel_esq_alvo = max(0, min(2.0, self.vel_base - saida_pid))
        self.vel_dir_alvo = max(0, min(2.0, self.vel_base + saida_pid))

        self.vel_esq += (self.vel_esq_alvo - self.vel_esq) * self.resposta_lenta
        self.vel_dir += (self.vel_dir_alvo - self.vel_dir) * self.resposta_lenta

        # Cinemática diferencial
        wheel_base = 30
        v = (self.vel_esq + self.vel_dir) / 2
        w = (self.vel_dir - self.vel_esq) / wheel_base

        self.angulo += math.degrees(w)
        angulo_rad = math.radians(self.angulo)
        self.x += v * math.cos(angulo_rad)
        self.y += v * math.sin(angulo_rad)

        self.trilha.append((int(self.x), int(self.y)))
        if len(self.trilha) > 500:
            self.trilha.pop(0)

        # Contador de voltas
        dx = self.x - self.inicial_x
        dy = self.y - self.inicial_y
        dist = math.hypot(dx, dy)
        if dist < 30:
            if not self.ultimo_setor:
                self.voltas += 1
                self.ultimo_setor = True
        else:
            self.ultimo_setor = False

    def desenhar(self):
        for ponto in self.trilha:
            pygame.draw.circle(tela, VERDE, ponto, 2)

        ang = math.radians(self.angulo)
        ponta = (self.x + self.tamanho * 0.6 * math.cos(ang),
                 self.y + self.tamanho * 0.6 * math.sin(ang))
        traseira_esq = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi - math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi - math.pi / 6))
        traseira_dir = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi + math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi + math.pi / 6))

        pygame.draw.polygon(tela, VERMELHO, [ponta, traseira_esq, traseira_dir])
        fonte = pygame.font.SysFont(None, 20)
        texto_id = fonte.render(f"#{self.id}", True, BRANCO)
        tela.blit(texto_id, (self.x - 10, self.y - 10))

        sensor_esq, sensor_dir = self.sensores()
        pygame.draw.circle(tela, AZUL, sensor_esq, 4)
        pygame.draw.circle(tela, AZUL, sensor_dir, 4)


def main():
    clock = pygame.time.Clock()
    tempo_inicial = pygame.time.get_ticks()
    fonte = pygame.font.SysFont(None, 24)

    # Criar superfície de pista separada
    pista_surface = pygame.Surface((largura, altura))
    pista_surface.fill(BRANCO)
    desenhar_pista(pista_surface)

    # Robôs com diferentes PID (id, kp, ki, kd)
    parametros = [
        (1, 2, 0, 0),
        (2, 2, 0.0005, 1.4),
        (3, 3.5, 0.0018, 2.01),
        (4, 3.35, 0.00257, 1.67),
        (5, 2.8, 0.0015, 2.0)
    ]
    robos = [Robo(650, 300, kp, ki, kd, id=n) for n, kp, ki, kd in parametros]

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.blit(pista_surface, (0, 0))

        for robo in robos:
            robo.atualizar(pista_surface)
            robo.desenhar()

        # Cronômetro
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - tempo_inicial) // 1000
        minutos = tempo_decorrido // 60
        segundos = tempo_decorrido % 60
        texto_tempo = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, (0, 0, 0))
        tela.blit(texto_tempo, (10, 10))

        # Info de cada robô
        for i, robo in enumerate(robos):
            texto = fonte.render(
                f"R#{robo.id} | Voltas: {robo.voltas} | Osc: {robo.oscilacoes}", True, (0, 0, 0))
            tela.blit(texto, (10, 40 + i * 20))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
