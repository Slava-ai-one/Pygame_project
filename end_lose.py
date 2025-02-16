def end_lose(username):
    pygame.init()
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('sad_fanfar.mp3')
    pygame.mixer.music.play(1)
    pygame.mixer.music.set_volume(0.3)
    intro_text = ["Если хотите увидеть таблицу лидеров, нажмите Space.",
                  "Если хотите закрыть, нажмите Escape"]
    con = sqlite3.connect('users_db.sqlite')
    cur = con.cursor()
    coins, time = map(int, (
        cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone()))
    print(coins, time,
          cur.execute(f"""select points, time from users_points where username in ('{username}')""").fetchone(),
          sep='\n')
    finalka = pygame.sprite.Group()
    final = load_image('final_page_lose.png')
    final_page = pygame.sprite.Sprite(finalka)
    final_page.image = final
    final_page.rect = final_page.image.get_rect()
    final_page.rect.x = 0
    final_page.rect.y = 0
    screen = pygame.display.set_mode(size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # terminate()
                pygame.quit()
                return 'close'
            # elif event.type == pygame.KEYDOWN or \
            #        event.type == pygame.MOUSEBUTTONDOWN:
            #    return  # начинаем игру
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # terminate()
                pygame.quit()
                return 'table'
        finalka.draw(screen)
        font = pygame.font.Font(None, 30)
        text_coord = 775
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color(253, 248, 111))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 250
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()