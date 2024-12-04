import pygame
import random
import os

# Inicializar Pygame
pygame.init()

# Configurações da tela
info = pygame.display.Info()
LARGURA = info.current_w
ALTURA = info.current_h
ESCALA = min(LARGURA/800, ALTURA/600)  # Fator de escala baseado na resolução original

# Criar tela em tela cheia
tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Gato vs Relâmpagos")

# Cores
BRANCO = (255, 255, 255)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Carregar imagens
def carregar_imagem(nome):
    return pygame.image.load(os.path.join('assets', nome)).convert_alpha()

def escalar_imagem(imagem, tamanho):
    return pygame.transform.scale(imagem, (int(tamanho[0] * ESCALA), int(tamanho[1] * ESCALA)))

# Carregar assets
try:
    img_gato = escalar_imagem(carregar_imagem('cat.png'), (64, 64))  # Mantém o gato do mesmo tamanho
    img_peixe = escalar_imagem(carregar_imagem('fish.png'), (32, 32))
    img_moeda = escalar_imagem(carregar_imagem('coin.png'), (30, 30))
    img_relampago = escalar_imagem(carregar_imagem('obstaculo.png'), (25, 50))  # Relâmpago menor
    img_fundo = pygame.transform.scale(carregar_imagem('background.png'), (LARGURA, ALTURA))
    img_game_over = pygame.transform.scale(carregar_imagem('game_over.png'), (LARGURA, ALTURA))
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    print("Verifique se todas as imagens estão na pasta 'assets'")
    pygame.quit()
    exit(1)

# Classe do Gato
class Gato(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_gato
        self.rect = self.image.get_rect()
        self.reset_position()
        self.velocidade = 8 * ESCALA
        self.vivo = True

    def reset_position(self):
        self.rect.x = LARGURA // 2 - self.rect.width // 2
        self.rect.y = ALTURA - self.rect.height * 2

    def update(self):
        if self.vivo:
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.velocidade
            if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA:
                self.rect.x += self.velocidade
            if teclas[pygame.K_ESCAPE]:
                pygame.quit()
                exit()

# Classe do Peixe
class Peixe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_peixe
        self.rect = self.image.get_rect()
        self.reset_position()
        self.velocidade = random.randrange(3, 6) * ESCALA

    def reset_position(self):
        self.rect.x = random.randrange(int(LARGURA - self.rect.width))
        self.rect.y = random.randrange(int(-100 * ESCALA), int(-40 * ESCALA))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.reset_position()

# Classe da Moeda
class Moeda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_moeda
        self.rect = self.image.get_rect()
        self.reset_position()
        self.velocidade = random.randrange(4, 7) * ESCALA

    def reset_position(self):
        self.rect.x = random.randrange(int(LARGURA - self.rect.width))
        self.rect.y = random.randrange(int(-100 * ESCALA), int(-40 * ESCALA))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.reset_position()

# Classe do Relâmpago
class Relampago(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = img_relampago
        self.rect = self.image.get_rect()
        self.reset_position()
        self.velocidade = random.randrange(7, 12) * ESCALA

    def reset_position(self):
        self.rect.x = random.randrange(int(LARGURA - self.rect.width))
        self.rect.y = random.randrange(int(-150 * ESCALA), int(-40 * ESCALA))

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA:
            self.reset_position()

# Criar grupos de sprites
todos_sprites = pygame.sprite.Group()
peixes = pygame.sprite.Group()
moedas = pygame.sprite.Group()
relampagos = pygame.sprite.Group()
gato = Gato()
todos_sprites.add(gato)

# Função para criar sprites iniciais
def criar_sprites():
    # Criar peixes
    for i in range(int(4 * ESCALA)):
        peixe = Peixe()
        todos_sprites.add(peixe)
        peixes.add(peixe)

    # Criar moedas
    for i in range(int(3 * ESCALA)):
        moeda = Moeda()
        todos_sprites.add(moeda)
        moedas.add(moeda)

    # Criar relâmpagos
    for i in range(int(2 * ESCALA)):
        relampago = Relampago()
        todos_sprites.add(relampago)
        relampagos.add(relampago)

# Criar sprites iniciais
criar_sprites()

# Pontuação e estado do jogo
pontuacao = 0
melhor_pontuacao = 0
game_over = False

def reiniciar_jogo():
    global pontuacao, game_over
    pontuacao = 0
    game_over = False
    gato.vivo = True
    gato.reset_position()
    
    # Reposicionar todos os objetos
    for sprite in peixes:
        sprite.reset_position()
    for sprite in moedas:
        sprite.reset_position()
    for sprite in relampagos:
        sprite.reset_position()

# Loop principal do jogo
clock = pygame.time.Clock()
rodando = True

# Carregar fonte personalizada ou usar a padrão
fonte_padrao = pygame.font.Font(None, int(36 * ESCALA))
fonte_grande = pygame.font.Font(None, int(72 * ESCALA))

while rodando:
    # Controle de FPS
    clock.tick(60)
    
    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
            elif evento.key == pygame.K_SPACE and game_over:
                reiniciar_jogo()

    if not game_over:
        # Atualização
        todos_sprites.update()

        # Verificar colisões com peixes (10 pontos)
        hits_peixes = pygame.sprite.spritecollide(gato, peixes, False)
        for peixe in hits_peixes:
            pontuacao += 10
            peixe.reset_position()

        # Verificar colisões com moedas (5 pontos)
        hits_moedas = pygame.sprite.spritecollide(gato, moedas, False)
        for moeda in hits_moedas:
            pontuacao += 5
            moeda.reset_position()

        # Verificar colisões com relâmpagos (fim de jogo)
        if pygame.sprite.spritecollide(gato, relampagos, False):
            game_over = True
            gato.vivo = False
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao

    # Desenho do jogo
    tela.blit(img_fundo, (0, 0))
    
    if not game_over:
        todos_sprites.draw(tela)
        
        # Mostrar pontuação durante o jogo
        texto_pontuacao = fonte_padrao.render(f"Pontuação: {pontuacao}", True, BRANCO)
        texto_melhor = fonte_padrao.render(f"Melhor: {melhor_pontuacao}", True, BRANCO)
        tela.blit(texto_pontuacao, (20 * ESCALA, 20 * ESCALA))
        tela.blit(texto_melhor, (20 * ESCALA, 60 * ESCALA))
    else:
        # Tela de Game Over
        # Fundo escuro semi-transparente
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.fill(PRETO)
        overlay.set_alpha(180)
        tela.blit(overlay, (0, 0))
        
        # Criar um painel lateral para os textos
        painel_largura = LARGURA // 4
        painel = pygame.Surface((painel_largura, ALTURA))
        painel.fill(PRETO)
        painel.set_alpha(200)
        tela.blit(painel, (LARGURA - painel_largura, 0))
        
        # Imagem de Game Over redimensionada ao lado do painel
        game_over_largura = LARGURA - painel_largura
        game_over_altura = ALTURA
        img_game_over_redim = pygame.transform.scale(img_game_over, (game_over_largura, game_over_altura))
        tela.blit(img_game_over_redim, (0, 0))
        
        # Texto "GAME OVER" no painel lateral
        texto_game_over = fonte_grande.render("GAME OVER", True, VERMELHO)
        pos_game_over = (LARGURA - painel_largura + (painel_largura - texto_game_over.get_width()) // 2 - 20,  # 20 pixels mais para a esquerda
                        ALTURA // 7)
        tela.blit(texto_game_over, pos_game_over)
        
        # Pontuação final
        texto_pontuacao_final = fonte_padrao.render(f"Pontuação Final:", True, BRANCO)
        valor_pontuacao = fonte_grande.render(str(pontuacao), True, BRANCO)
        
        pos_texto_pont = (LARGURA - painel_largura + (painel_largura - texto_pontuacao_final.get_width()) // 2,
                         ALTURA // 3)
        pos_valor_pont = (LARGURA - painel_largura + (painel_largura - valor_pontuacao.get_width()) // 2,
                         ALTURA // 3 + texto_pontuacao_final.get_height() * 1.5)
        
        tela.blit(texto_pontuacao_final, pos_texto_pont)
        tela.blit(valor_pontuacao, pos_valor_pont)
        
        # Melhor pontuação
        texto_melhor = fonte_padrao.render("Melhor Pontuação:", True, AMARELO)
        valor_melhor = fonte_grande.render(str(melhor_pontuacao), True, AMARELO)
        
        pos_texto_melhor = (LARGURA - painel_largura + (painel_largura - texto_melhor.get_width()) // 2,
                           ALTURA // 2)
        pos_valor_melhor = (LARGURA - painel_largura + (painel_largura - valor_melhor.get_width()) // 2,
                           ALTURA // 2 + texto_melhor.get_height() * 1.5)
        
        tela.blit(texto_melhor, pos_texto_melhor)
        tela.blit(valor_melhor, pos_valor_melhor)
        
        # Linha separadora
        pygame.draw.line(tela, BRANCO,
                        (LARGURA - painel_largura + 20 * ESCALA, ALTURA * 0.7),
                        (LARGURA - 20 * ESCALA, ALTURA * 0.7),
                        2)
        
        # Instruções para reiniciar
        texto_reiniciar = fonte_padrao.render("Pressione", True, BRANCO)
        texto_espaco = fonte_padrao.render("ESPAÇO", True, AMARELO)
        texto_continuar = fonte_padrao.render("para continuar", True, BRANCO)
        texto_esc = fonte_padrao.render("ESC para sair", True, VERMELHO)
        
        # Posicionar instruções
        espacamento = texto_reiniciar.get_height() * 1.2
        base_y = ALTURA * 0.75
        
        for i, texto in enumerate([texto_reiniciar, texto_espaco, texto_continuar, texto_esc]):
            pos_x = LARGURA - painel_largura + (painel_largura - texto.get_width()) // 2
            pos_y = base_y + (espacamento * i)
            tela.blit(texto, (pos_x, pos_y))

    # Atualizar tela
    pygame.display.flip()

# Encerrar Pygame
pygame.quit()