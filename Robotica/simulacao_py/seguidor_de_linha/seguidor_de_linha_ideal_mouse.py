import pygame
import math
import random

# Inicialização
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Robô Triangular Seguidor de Linha")

# Cores
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (100, 100, 100)

# Linha (trajetória oval)
def desenhar_pista1():
    ret = pygame.Rect(150, 150, 500, 300)
    pygame.draw.ellipse(tela, PRETO, ret, 10)

def desenhar_pista2():
    random.seed(123)  # Sempre o mesmo circuito, remova para aleatório

    centro = (largura // 2, altura // 2)
    raio = 200
    num_pontos = 30
    largura_pista = 20

    # Gerar pontos ao redor de um círculo com variação
    pontos = []
    for i in range(num_pontos):
        ang = i * (2 * math.pi / num_pontos)
        var = random.randint(-30, 30)
        r = raio + var
        x = centro[0] + r * math.cos(ang)
        y = centro[1] + r * math.sin(ang)
        pontos.append((x, y))

    # Fechar a curva
    pontos += pontos[:3]  # Para suavização circular

    # Suavização com Catmull-Rom spline (interpolação)
    curva = []
    def interp(p0, p1, p2, p3, t):
        # Catmull-Rom: gera ponto entre p1 e p2 com suavidade
        t2 = t * t
        t3 = t2 * t
        x = 0.5 * ((2 * p1[0]) +
                   (-p0[0] + p2[0]) * t +
                   (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                   (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)
        y = 0.5 * ((2 * p1[1]) +
                   (-p0[1] + p2[1]) * t +
                   (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                   (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)
        return (x, y)

    # Construção da curva suave
    for i in range(len(pontos) - 3):
        for t in [j / 10.0 for j in range(10)]:
            curva.append(interp(pontos[i], pontos[i+1], pontos[i+2], pontos[i+3], t))

    # Criar bordas com offset normal (espessura constante)
    borda_esq = []
    borda_dir = []

    for i in range(len(curva)):
        p1 = curva[i]
        p2 = curva[(i + 1) % len(curva)]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dist = math.hypot(dx, dy) or 1
        nx = -dy / dist
        ny = dx / dist
        offset = largura_pista / 2
        borda_esq.append((p1[0] + nx * offset, p1[1] + ny * offset))
        borda_dir.append((p1[0] - nx * offset, p1[1] - ny * offset))

    # Desenha pista como polígono fechado entre bordas
    pista = borda_esq + borda_dir[::-1]
    pygame.draw.polygon(tela, PRETO, pista)



# Robô triangular com sensores frontais e rodas traseiras
class Robo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = -90
        self.vel_base = 2.0 
        self.vel_curva = 0 
        self.tamanho = 60  # Robô maior
        self.largura_roda = 12
        self.altura_roda = 24
        self.trilha = []

    def sensores(self):
        frente_offset = self.tamanho * 0.3#0.6
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

    def atualizar(self):
        sensor_esq, sensor_dir = self.sensores()

        cor_esq = tela.get_at(sensor_esq)[:3] if 0 <= sensor_esq[0] < largura and 0 <= sensor_esq[1] < altura else BRANCO
        cor_dir = tela.get_at(sensor_dir)[:3] if 0 <= sensor_dir[0] < largura and 0 <= sensor_dir[1] < altura else BRANCO

        if cor_esq == PRETO and cor_dir != PRETO:
            vel_esq = self.vel_curva
            vel_dir = self.vel_base
        elif cor_dir == PRETO and cor_esq != PRETO:
            vel_esq = self.vel_base
            vel_dir = self.vel_curva
        elif cor_esq == PRETO and cor_dir == PRETO:
            vel_esq = vel_dir = self.vel_base * 0.5
        else:
            vel_esq = vel_dir = self.vel_base

        wheel_base = 30
        v = (vel_esq + vel_dir) / 2
        w = (vel_dir - vel_esq) / wheel_base

        self.angulo += math.degrees(w)

        angulo_rad = math.radians(self.angulo)
        self.x += v * math.cos(angulo_rad)
        self.y += v * math.sin(angulo_rad)

        self.trilha.append((int(self.x), int(self.y)))
        if len(self.trilha) > 500:
            self.trilha.pop(0)

    def desenhar(self):
        # Desenha trilha
        for ponto in self.trilha:
            pygame.draw.circle(tela, (0, 150, 0), ponto, 2)

        ang = math.radians(self.angulo)

        # Pontos do triângulo
        ponta = (
            self.x + self.tamanho * 0.6 * math.cos(ang),
            self.y + self.tamanho * 0.6 * math.sin(ang)
        )
        traseira_esq = (
            self.x + self.tamanho * 0.5 * math.cos(ang + math.pi - math.pi / 6),
            self.y + self.tamanho * 0.5 * math.sin(ang + math.pi - math.pi / 6)
        )
        traseira_dir = (
            self.x + self.tamanho * 0.5 * math.cos(ang + math.pi + math.pi / 6),
            self.y + self.tamanho * 0.5 * math.sin(ang + math.pi + math.pi / 6)
        )

        pontos = [ponta, traseira_esq, traseira_dir]
        pygame.draw.polygon(tela, VERMELHO, [(int(x), int(y)) for x, y in pontos])

        # Desenha rodas traseiras como retângulos com bordas arredondadas
        roda_offset = self.tamanho * 0.3
        perp_ang = ang + math.pi / 2

        for direcao in [-1, 1]:  # esquerda (-1), direita (+1)
            cx = self.x + roda_offset * math.cos(perp_ang) * direcao - 4 * math.cos(ang)
            cy = self.y + roda_offset * math.sin(perp_ang) * direcao - 4 * math.sin(ang)

            # Calcula rotação do retângulo
            rect = pygame.Rect(0, 0, self.altura_roda, self.largura_roda)
            rect.center = (cx, cy)

            # Superfície temporária para roda rotacionada
            roda_surface = pygame.Surface((self.altura_roda, self.largura_roda), pygame.SRCALPHA)
            pygame.draw.rect(roda_surface, CINZA, (0, 0, self.altura_roda, self.largura_roda), border_radius=4)

            roda_rot = pygame.transform.rotate(roda_surface, -self.angulo)
            roda_rect = roda_rot.get_rect(center=(cx, cy))
            tela.blit(roda_rot, roda_rect)

        # Sensores
        sensor_esq, sensor_dir = self.sensores()
        pygame.draw.circle(tela, AZUL, sensor_esq, 4)
        pygame.draw.circle(tela, AZUL, sensor_dir, 4)

    def reposicionar(self, x, y):
        self.x = x
        self.y = y
        self.angulo = -90
        self.trilha.clear()



# Loop principal
def main():
    robo = Robo(650, 300)
    clock = pygame.time.Clock()
    rodando = True

    while rodando:
        tela.fill(BRANCO)
        desenhar_pista1()
        #desenhar_pista2()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos = pygame.mouse.get_pos()
                    robo.reposicionar(*pos)

        robo.atualizar()
        robo.desenhar()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
