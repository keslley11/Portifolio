import pygame
import math
import random

# Inicialização
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Robô Seguidor de Linha")

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

class Robo:
    def __init__(self, x, y):
        self.inicial_x = x
        self.inicial_y = y
        self.x = x
        self.y = y
        self.angulo = -90
        self.vel_base = 2.0 # 2.0 --> 100%
        self.vel_curva = 0
        self.vel_esq = 0
        self.vel_dir = 0
        self.vel_esq_alvo = 0
        self.vel_dir_alvo = 0
        self.resposta_lenta = 0.06 # fator de suavização (quanto menor, mais lento)

        #Sem PID --> 20s ; 2 voltas
        
        # self.kp = 2  # 2.0 --> 100% da velocidade --> controle on/off
        # self.ki = 0 
        # self.kd = 0 
    
    
        # PID (tune: trial&error) --> +100s ; +20voltas ; apartir de 1min e 20 fica bom
        
        # self.kp = 2  # 2.0 --> 100% da velocidade
        # self.ki = 0.0005 #0.0005 --> erro acumulado
        # self.kd = 1.4 #1.4  --> erro instantaneo
        
        
        # PID (tune: alg_genetico) --> começa bem e fica ruim
        
        # self.kp = 2.62  # 2.0 --> 100% da velocidade
        # self.ki = 0.00902 # --> erro acumulado
        # self.kd = 5.41 # --> erro instantaneo
        
        # PID (tune: alg_genetico) --> tambem começa bem e fica ruim (penalidade oscilações: 0.1)
        
        # self.kp = 1.39  # 2.0 --> 100% da velocidade
        # self.ki = 0.00017 # --> erro acumulado
        # self.kd = 2.83  # --> erro instantaneo
        
        # PID (tune: alg_genetico) --> tambem começa bem e fica ruim (penalidade oscilações: 0.2)
        
        # self.kp = 3.55  # 2.0 --> 100% da velocidade
        # self.ki = 0.00325 # --> erro acumulado
        # self.kd = 1.74  # --> erro instantaneo
        
        # PID (tune: alg_genetico) --> bom! (ganhos limitados)
        
        # self.kp = 3.5  # 2.0 --> 100% da velocidade
        # self.ki = 0.0018 # --> erro acumulado
        # self.kd = 2.01  # --> erro instantaneo
        
        # # PID (tune: alg_genetico) --> tambem começa bem e fica ruim (ganhos limitados)
        # 
        # self.kp = 2.26  # 2.0 --> 100% da velocidade
        # self.ki = 0.00502 # --> erro acumulado
        # self.kd = 3.72  # --> erro instantaneo
        
        # PID (tune: alg_genetico) --> bom! (ganhos limitados)
        
        self.kp = 3.35
        self.ki = 0.00257
        self.kd = 1.67

        self.erro_anterior = 0
        self.erro_acumulado = 0

        self.tamanho = 60
        self.largura_roda = 12
        self.altura_roda = 24
        self.trilha = []

        self.voltas = 0
        self.ultimo_setor = None
        self.oscilacoes = 0
        self.ultimo_erro = 0

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

    def atualizar(self):
        sensor_esq, sensor_dir = self.sensores()

        cor_esq = tela.get_at(sensor_esq)[:3] if 0 <= sensor_esq[0] < largura and 0 <= sensor_esq[1] < altura else BRANCO
        cor_dir = tela.get_at(sensor_dir)[:3] if 0 <= sensor_dir[0] < largura and 0 <= sensor_dir[1] < altura else BRANCO

        # Sensor detecta linha (1 = linha, 0 = fora)
        s_esq = 1 if cor_esq == PRETO else 0
        s_dir = 1 if cor_dir == PRETO else 0
        # Erro: sensor esquerdo - sensor direito
        erro = s_esq - s_dir

        # Contagem de oscilações
        if erro != self.ultimo_erro and erro != 0:
            self.oscilacoes += 1
        self.ultimo_erro = erro

        '''     #Sem PID
        # Define as velocidades alvo com base na leitura dos sensores
        if cor_esq == PRETO and cor_dir != PRETO:
            self.vel_esq_alvo = self.vel_curva
            self.vel_dir_alvo = self.vel_base
        elif cor_dir == PRETO and cor_esq != PRETO:
            self.vel_esq_alvo = self.vel_base
            self.vel_dir_alvo = self.vel_curva
        elif cor_esq == PRETO and cor_dir == PRETO:
            self.vel_esq_alvo = self.vel_dir_alvo = self.vel_base * 0.5
        else:
            self.vel_esq_alvo = self.vel_dir_alvo = self.vel_base
        '''
        
        #PID
        self.erro_acumulado += erro
        derivada = erro - self.erro_anterior
        saida_pid = self.kp * erro + self.ki * self.erro_acumulado + self.kd * derivada
        self.erro_anterior = erro

        self.vel_esq_alvo = self.vel_base - saida_pid
        self.vel_dir_alvo = self.vel_base + saida_pid
        #Limitando a velocidade: 0 - 2
        self.vel_esq_alvo = max(0, min(2.0, self.vel_esq_alvo))
        self.vel_dir_alvo = max(0, min(2.0, self.vel_dir_alvo))

        # Aplica atraso (filtro) para simular resposta real lenta
        self.vel_esq += (self.vel_esq_alvo - self.vel_esq) * self.resposta_lenta
        self.vel_dir += (self.vel_dir_alvo - self.vel_dir) * self.resposta_lenta

        # Monitorar
        print(
            f" S_Esq: {s_esq} | S_Dir: {s_dir} | Erro: {erro:2d} | Kp: {self.kp:2.2f} | Ki: {self.ki:1.5f} | Kd: {self.kd:2.2f} | PID: {saida_pid:5.2f} | Vel_Esq: {self.vel_esq_alvo:5.2f} | Vel_Dir: {self.vel_dir_alvo:5.2f}"
            )

        # Cinemática diferencial (animação)
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
            if self.ultimo_setor == False:
                self.voltas += 1
                self.ultimo_setor = True
        else:
            self.ultimo_setor = False

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

            rect = pygame.Rect(0, 0, self.altura_roda, self.largura_roda)
            rect.center = (cx, cy)

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
        self.inicial_x = x
        self.inicial_y = y
        self.angulo = -90
        self.trilha.clear()
        self.voltas = 0
        self.oscilacoes = 0
        self.ultimo_erro = 0


def desenhar_botao_reiniciar():
    fonte = pygame.font.SysFont(None, 36)
    texto = fonte.render("REINICIAR", True, (255, 255, 255))
    botao_rect = pygame.Rect(largura // 2 - 80, altura // 2 - 25, 160, 50)
    pygame.draw.rect(tela, (100, 100, 100), botao_rect)
    tela.blit(texto, (botao_rect.x + 20, botao_rect.y + 10))
    return botao_rect

def main():
    robo = Robo(650, 300)
    clock = pygame.time.Clock()

    tempo_inicial = pygame.time.get_ticks()
    fonte_tempo = pygame.font.SysFont(None, 28)
    tempo_pausado = 0
    momento_colisao = None

    colidiu = False
    botao_rect = None

    rodando = True
    while rodando:
        tela.fill(BRANCO)
        desenhar_pista1()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    pos = pygame.mouse.get_pos()
                    if colidiu and botao_rect and botao_rect.collidepoint(pos):
                        robo = Robo(650, 300)
                        colidiu = False
                        tempo_pausado += pygame.time.get_ticks() - momento_colisao
                        momento_colisao = None
                        tempo_inicial = pygame.time.get_ticks() - tempo_pausado
                    elif not colidiu:
                        robo.reposicionar(*pos)

        if not colidiu:
            robo.atualizar()
            tempo_atual = pygame.time.get_ticks()

            # Verifica se o robô saiu da tela
            if not (0 <= robo.x < largura and 0 <= robo.y < altura):
                colidiu = True
                momento_colisao = pygame.time.get_ticks()

        robo.desenhar()

        # Se colidiu, exibe botão
        if colidiu:
            tempo_atual = momento_colisao # pausa o tempo no momento da colisão
            botao_rect = desenhar_botao_reiniciar()

        # Cronômetro
        tempo_decorrido = (tempo_atual - tempo_inicial - tempo_pausado) // 1000
        minutos = tempo_decorrido // 60
        segundos = tempo_decorrido % 60
        fonte = pygame.font.SysFont(None, 36)
        texto_tempo = fonte.render(f"Tempo: {minutos:02d}:{segundos:02d}", True, (0, 0, 0))
        tela.blit(texto_tempo, (10, 10))
        # voltas
        texto_voltas = fonte.render(f"Voltas: {robo.voltas}", True, (0, 0, 0))
        tela.blit(texto_voltas, (10, 40))
        # oscilações
        texto_oscilacoes = fonte.render(f"Oscilações: {robo.oscilacoes}", True, (0, 0, 0))
        tela.blit(texto_oscilacoes, (10, 70))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
