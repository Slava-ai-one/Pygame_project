def end_win(username):
    pygame.init()
    size = w, h = window_size
    screen = pygame.display.set_mode(size)
    pygame.mixer.music.load('triumf.mp3')
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
    morph = pymorphy3.MorphAnalyzer()
    worda = 'монета'
    parsed_word_coins = morph.parse(worda)[0]
    parsed_word_minut = morph.parse('минуту')[0]
    parsed_word_second = morph.parse('секунду')[0]
    result_text = [
        f"Вы собрали {coins} {parsed_word_coins.make_agree_with_number(int(coins)).word}, сделав это за {time // 60:0>2} {parsed_word_minut.make_agree_with_number(time // 60).word} и {time % 60:0>2} {parsed_word_second.make_agree_with_number(time % 60).word}"]
    finalka = pygame.sprite.Group()
    final = load_image('final_page.png')
    final_page = pygame.sprite.Sprite(finalka)
    final_page.image = final
    final_page.rect = final_page.image.get_rect()
    final_page.rect.x = 0
    final_page.rect.y = 0
    star_image = load_image('star.png', -1)
    for i in range(coins // 6):
        star = pygame.sprite.Sprite(finalka)
        star.image = pygame.transform.scale(star_image, (75, 75))
        star.rect = star.image.get_rect()
        star.rect.x = 400 + (85 * i)
        star.rect.y = 500

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
        font_result = pygame.font.Font(None, 32)
        text_result_coord = 625
        for line in result_text:
            string_rendered = font_result.render(line, 1, pygame.Color(253, 248, 111))
            result_rect = string_rendered.get_rect()
            text_result_coord += 10
            result_rect.top = text_result_coord
            result_rect.x = 250
            text_result_coord += result_rect.height
            screen.blit(string_rendered, result_rect)
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