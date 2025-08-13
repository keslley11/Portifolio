import pygame
import math

# Inicialização
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulação Robôs PID")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)
CORES = [(255, 0, 0), (0, 128, 255), (0, 200, 0), (200, 100, 0), (255, 0, 255)]

# Camada apenas da pista
surface_pista = pygame.Surface((largura, altura))
surface_pista.fill(BRANCO)

def desenhar_pista1(surface):
    ret = pygame.Rect(150, 150, 500, 300)
    pygame.draw.ellipse(surface, PRETO, ret, 10)

desenhar_pista1(surface_pista)

class Robo:
    def __init__(self, x, y, cor, kp, ki, kd):
        self.x = x
        self.y = y
        self.x0 = x
        self.y0 = y
        self.angulo = -90
        self.tamanho = 60
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

        self.trilha = []
        self.voltas = 0
        self.oscilacoes = 0
        self.ultimo_setor = False

        self.ISE = 0
        self.IAE = 0
        self.ITAE = 0
        self.cor = cor

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

    def atualizar(self, tempo_ms):
        sensor_esq, sensor_dir = self.sensores()

        cor_esq = surface_pista.get_at(sensor_esq)[:3] if 0 <= sensor_esq[0] < largura and 0 <= sensor_esq[1] < altura else BRANCO
        cor_dir = surface_pista.get_at(sensor_dir)[:3] if 0 <= sensor_dir[0] < largura and 0 <= sensor_dir[1] < altura else BRANCO

        s_esq = 1 if cor_esq == PRETO else 0
        s_dir = 1 if cor_dir == PRETO else 0
        erro = s_esq - s_dir

        # Oscilações
        if erro != self.ultimo_erro and erro != 0:
            self.oscilacoes += 1
        self.ultimo_erro = erro

        # Heurísticas
        tempo_seg = tempo_ms / 1000.0
        self.ISE += erro**2
        self.IAE += abs(erro)
        self.ITAE += tempo_seg * abs(erro)

        # PID
        self.erro_acumulado += erro
        derivada = erro - self.erro_anterior
        saida_pid = self.kp * erro + self.ki * self.erro_acumulado + self.kd * derivada
        self.erro_anterior = erro

        self.vel_esq_alvo = self.vel_base - saida_pid
        self.vel_dir_alvo = self.vel_base + saida_pid
        self.vel_esq_alvo = max(0, min(2.0, self.vel_esq_alvo))
        self.vel_dir_alvo = max(0, min(2.0, self.vel_dir_alvo))

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

        dist = math.hypot(self.x - self.x0, self.y - self.y0)
        if dist < 30:
            if not self.ultimo_setor:
                self.voltas += 1
                self.ultimo_setor = True
        else:
            self.ultimo_setor = False

    def desenhar(self):
        for ponto in self.trilha:
            pygame.draw.circle(tela, self.cor, ponto, 2)

        ang = math.radians(self.angulo)
        ponta = (self.x + self.tamanho * 0.6 * math.cos(ang),
                 self.y + self.tamanho * 0.6 * math.sin(ang))
        traseira_esq = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi - math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi - math.pi / 6))
        traseira_dir = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi + math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi + math.pi / 6))

        pygame.draw.polygon(tela, self.cor, [(int(p[0]), int(p[1])) for p in [ponta, traseira_esq, traseira_dir]])
        sensor_esq, sensor_dir = self.sensores()
        pygame.draw.circle(tela, AZUL, sensor_esq, 4)
        pygame.draw.circle(tela, AZUL, sensor_dir, 4)

def main():
    clock = pygame.time.Clock()
    tempo_inicial = pygame.time.get_ticks()
    fonte = pygame.font.SysFont(None, 22)

    robos = [
        Robo(650, 300, CORES[0], 2, 0, 0),
        Robo(650, 300, CORES[1], 2, 0.0005, 1.4),
        Robo(650, 300, CORES[2], 3.5, 0.0018, 2.01),
        Robo(650, 300, CORES[0], 3.35, 0.00257, 1.67),
        Robo(650, 300, CORES[1], 2.8, 0.0015, 2.0),
        Robo(650, 300, CORES[2], 2.5, 0.002, 1.5),
    ]

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tempo_ms = pygame.time.get_ticks() - tempo_inicial

        tela.blit(surface_pista, (0, 0))

        for robo in robos:
            robo.atualizar(tempo_ms)
            robo.desenhar()

        for idx, robo in enumerate(robos):
            base_y = 10 + idx * 90
            pygame.draw.rect(tela, robo.cor, (10, base_y, 15, 15))
            tela.blit(fonte.render(f"Robô {idx+1} - Kp={robo.kp:.2f}, Ki={robo.ki:.4f}, Kd={robo.kd:.2f}", True, (0, 0, 0)), (30, base_y))
            tela.blit(fonte.render(f"Voltas: {robo.voltas} | Oscilações: {robo.oscilacoes}", True, (0, 0, 0)), (30, base_y+20))
            tela.blit(fonte.render(f"ISE: {robo.ISE:.2f} | IAE: {robo.IAE:.2f} | ITAE: {robo.ITAE:.2f}", True, (0, 0, 0)), (30, base_y+40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
