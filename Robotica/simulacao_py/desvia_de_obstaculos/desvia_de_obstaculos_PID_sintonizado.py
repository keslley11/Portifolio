import pygame
import math

# === Inicialização ===
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Robô PID com Sensores")
fonte = pygame.font.SysFont(None, 30)

# === Cores ===
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)
VERDE = (0, 150, 0)
AMARELO = (255, 255, 0)

# === Pista com paredes ===
def desenhar_pista():
    pygame.draw.rect(tela, PRETO, (100, 100, 600, 400), 10)  # externo
    pygame.draw.rect(tela, PRETO, (200, 200, 400, 200), 10)  # interno

# === Classes ===
class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.erro_anterior = 0

    def calcular(self, erro, dt):
        self.integral += erro * dt
        derivada = (erro - self.erro_anterior) / dt if dt > 0 else 0
        saida = self.kp * erro + self.ki * self.integral + self.kd * derivada
        self.erro_anterior = erro
        return max(min(saida, 1), -1)

class Robo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = -90
        self.velocidade = 2.0
        self.tamanho = 60
        self.largura_roda = 12
        self.altura_roda = 24
        self.trilha = []
        self.margem_segura = self.tamanho * 0.5
        self.velocidade_angular_real = 0
        self.velocidade_angular_desejada = 0
        self.atraso_motor = 0.04
        self.pid = PID(kp=1, ki=0, kd=0.5) #kp=1, ki=0, kd=0.5
        self.colidiu = False  # Flag de colisão

    def atualizar(self, dt):
        if self.colidiu:
            return  # Para movimento se colidiu

        dist_esq_diag = self.sensor_distancia(-45) /150  # 0-150  -> 0-1
        dist_dir_diag = self.sensor_distancia(45)  /150  # 0-150  -> 0-1

        
        erro =  dist_dir_diag - dist_esq_diag
        self.velocidade_angular_desejada = self.pid.calcular(erro, dt) *5
        print(f"Erro: {erro:.5f}| Saída_PID: {self.velocidade_angular_desejada/5*100:.3f}%")

        self.velocidade_angular_real += self.atraso_motor * (self.velocidade_angular_desejada - self.velocidade_angular_real)
        self.angulo += self.velocidade_angular_real

        self.x += self.velocidade * math.cos(math.radians(self.angulo))
        self.y += self.velocidade * math.sin(math.radians(self.angulo))

        self.trilha.append((int(self.x), int(self.y)))
        if len(self.trilha) > 500:
            self.trilha.pop(0)

        # --- Verificar colisão com paredes ---
        if self.sensor_distancia(0) < 5:  # sensor frontal
            self.colidiu = True

    def sensor_distancia(self, angulo_sensor, alcance=150):
        angulo_total = math.radians(self.angulo + angulo_sensor)
        for d in range(0, alcance, 2):
            px = int(self.x + d * math.cos(angulo_total))
            py = int(self.y + d * math.sin(angulo_total))
            if 0 <= px < largura and 0 <= py < altura:
                cor = tela.get_at((px, py))[:3]
                if cor == PRETO:
                    return d
            else:
                return d
        return alcance

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
        pygame.draw.polygon(tela, VERMELHO, [(int(ponta[0]), int(ponta[1])),
                                             (int(traseira_esq[0]), int(traseira_esq[1])),
                                             (int(traseira_dir[0]), int(traseira_dir[1]))])

        roda_offset = self.tamanho * 0.3
        perp_ang = ang + math.pi / 2
        for direcao in [-1, 1]:
            cx = self.x + roda_offset * math.cos(perp_ang) * direcao - 4 * math.cos(ang)
            cy = self.y + roda_offset * math.sin(perp_ang) * direcao - 4 * math.sin(ang)
            roda_surface = pygame.Surface((self.altura_roda, self.largura_roda), pygame.SRCALPHA)
            pygame.draw.rect(roda_surface, CINZA, (0, 0, self.altura_roda, self.largura_roda), border_radius=4)
            roda_rot = pygame.transform.rotate(roda_surface, -self.angulo)
            roda_rect = roda_rot.get_rect(center=(cx, cy))
            tela.blit(roda_rot, roda_rect)

        for ang_s in [-45, 45]:
            dist = self.sensor_distancia(ang_s)
            rad = math.radians(self.angulo + ang_s)
            sx = self.x + dist * math.cos(rad)
            sy = self.y + dist * math.sin(rad)
            pygame.draw.line(tela, AZUL, (self.x, self.y), (sx, sy), 2)
            pygame.draw.circle(tela, AZUL, (int(sx), int(sy)), 3)

# === Função principal ===
def main():
    robo = Robo(150, 250)
    clock = pygame.time.Clock()
    rodando = True
    tempo_inicio = pygame.time.get_ticks()
    reiniciar_btn = pygame.Rect(650, 20, 120, 40)

    while rodando:
        dt = clock.tick(60) / 1000.0
        tela.fill(BRANCO)
        desenhar_pista()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if reiniciar_btn.collidepoint(evento.pos):
                    robo = Robo(150, 250)
                    tempo_inicio = pygame.time.get_ticks()

        # Atualizar e desenhar robô
        robo.atualizar(dt)
        robo.desenhar()

        # --- Cronômetro ---
        tempo_corrente = (pygame.time.get_ticks() - tempo_inicio) / 1000
        texto_tempo = fonte.render(f"Tempo: {tempo_corrente:.2f}s", True, PRETO)
        tela.blit(texto_tempo, (20, 20))

        # --- Botão reiniciar ---
        pygame.draw.rect(tela, CINZA, reiniciar_btn)
        texto_btn = fonte.render("Reiniciar", True, PRETO)
        tela.blit(texto_btn, (reiniciar_btn.x + 10, reiniciar_btn.y + 5))

        # --- Mensagem de colisão ---
        if robo.colidiu:
            aviso = fonte.render("Colidiu! Clique em Reiniciar.", True, VERMELHO)
            tela.blit(aviso, (250, 550))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
