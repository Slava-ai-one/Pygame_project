def start_screen():
    pygame.init()
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    intro_text = ["Правила игры",
                  "Задача игрока: пройти три зала и выбраться   ",
                  "из подземелья, собирая монеты. При встрече  ",
                  "с противником нужно выбрать: жизнь или кошелек"]


    fon = pygame.transform.scale(load_image('begin_page.png'), (w, h))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 24)
    text_coord = 845
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color(253, 248, 111))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 280
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()