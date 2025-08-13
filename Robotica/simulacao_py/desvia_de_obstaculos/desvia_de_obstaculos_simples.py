import pygame
import math

# === Inicialização ===
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Robô com Sensores de Obstáculo")

# === Cores ===
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)
VERDE = (0, 150, 0)

# === Pista com paredes ===
def desenhar_pista():
    pygame.draw.rect(tela, PRETO, (100, 100, 600, 400), 10)  # retângulo externo
    pygame.draw.rect(tela, PRETO, (200, 200, 400, 200), 10)  # retângulo interno

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

        # Para simular atraso do motor
        self.velocidade_angular_real = 0
        self.velocidade_angular_desejada = 0
        self.atraso_motor = 0.2  # 0 < atraso_motor <= 1

    def atualizar(self):
        margem_frontal = self.tamanho #* 0.6
        margem_lateral = self.tamanho * 0.6

        dist_frente = self.sensor_distancia(0)
        dist_esq_diag = self.sensor_distancia(-45)
        dist_dir_diag = self.sensor_distancia(45)
        #dist_esq_lateral = self.sensor_distancia(-90)
        #dist_dir_lateral = self.sensor_distancia(90)

        # Reseta comando angular
        self.velocidade_angular_desejada = 0

        # Evitar colisão frontal
        if dist_frente < margem_frontal:
            if dist_esq_diag > dist_dir_diag:
                self.velocidade_angular_desejada = -5
            else:
                self.velocidade_angular_desejada = 5
        else:
            # Correção lateral
            if dist_esq_diag < margem_lateral:
                self.velocidade_angular_desejada = 5
            elif dist_dir_diag < margem_lateral:
                self.velocidade_angular_desejada = -5

        # Aplica atraso do motor (filtro de primeira ordem)
        self.velocidade_angular_real += self.atraso_motor * (self.velocidade_angular_desejada - self.velocidade_angular_real)
        self.angulo += self.velocidade_angular_real

        # Movimento
        self.x += self.velocidade * math.cos(math.radians(self.angulo))
        self.y += self.velocidade * math.sin(math.radians(self.angulo))

        # Trilha
        self.trilha.append((int(self.x), int(self.y)))
        if len(self.trilha) > 500:
            self.trilha.pop(0)


    def sensor_distancia(self, angulo_sensor, alcance=150):
        """Simula um sensor ultrassônico usando raycasting"""
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
        # Trilha
        for ponto in self.trilha:
            pygame.draw.circle(tela, VERDE, ponto, 2)

        ang = math.radians(self.angulo)

        # Corpo do robô (triângulo)
        ponta = (self.x + self.tamanho * 0.6 * math.cos(ang),
                 self.y + self.tamanho * 0.6 * math.sin(ang))
        traseira_esq = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi - math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi - math.pi / 6))
        traseira_dir = (self.x + self.tamanho * 0.5 * math.cos(ang + math.pi + math.pi / 6),
                        self.y + self.tamanho * 0.5 * math.sin(ang + math.pi + math.pi / 6))
        pygame.draw.polygon(tela, VERMELHO, [(int(ponta[0]), int(ponta[1])),
                                             (int(traseira_esq[0]), int(traseira_esq[1])),
                                             (int(traseira_dir[0]), int(traseira_dir[1]))])

        # Rodas traseiras
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

        # Sensores (frente, diagonais, laterais)
        #for ang_s in [0, -45, 45, -90, 90]:
        for ang_s in [0, -45, 45]:
            dist = self.sensor_distancia(ang_s)
            rad = math.radians(self.angulo + ang_s)
            sx = self.x + dist * math.cos(rad)
            sy = self.y + dist * math.sin(rad)
            pygame.draw.line(tela, AZUL, (self.x, self.y), (sx, sy), 2)
            pygame.draw.circle(tela, AZUL, (int(sx), int(sy)), 3)

def main():
    robo = Robo(150, 150)
    clock = pygame.time.Clock()
    rodando = True
    while rodando:
        tela.fill(BRANCO)
        desenhar_pista()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        robo.atualizar()
        robo.desenhar()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
