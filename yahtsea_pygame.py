import random
import pygame
from datetime import date, datetime
from dice.dice_ui import DiceUI
from history.history import History

pygame.init()

WIDTH = 600
HEIGHT = 310
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('YahtSea')
timer = pygame.time.Clock()
fps = 60
huge_font = pygame.font.Font('freesansbold.ttf', 30)
large_font = pygame.font.Font('freesansbold.ttf', 24)
font = pygame.font.Font('freesansbold.ttf', 22)
small_font = pygame.font.Font('freesansbold.ttf', 16)

class Label:
    def __init__(self, x_pos, y_pos, text, my_score):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.score = my_score

    def draw(self):
        name_text = font.render(self.text, True, (0, 0, 0))
        screen.blit(name_text, (self.x_pos + 20, self.y_pos + 10))
        score_text = font.render(str(self.score), True, (0, 0, 255))
        screen.blit(score_text, (self.x_pos + 130, self.y_pos + 10))


def draw_game(username):
    current_date = date.today().strftime("%Y-%m-%d")

    turns_text = large_font.render(f"{username}", True, (255, 255, 255))
    screen.blit(turns_text, (10, 15))
#     but_text = font.render(username, True, (0, 0, 0))
#     screen.blit(but_text, (100, 15))

    # Draw a box for the daily and all time leaders
    pygame.draw.rect(screen, (255, 255, 255), [10, 170, 160, 130], 100, 6)
    pygame.draw.rect(screen, (255, 255, 255), [180, 170, 410, 130], 65, 6)
#     pygame.draw.rect(screen, (0, 0, 0), [15, 175, 150, 120], 2, 10)

    score_text = font.render('Daily Leaders', True, (0, 0, 0))
    screen.blit(score_text, (190, 180))

    if current_date in history.data['top']['daily'] and len(history.data['top']['daily'][current_date]) > 0:
        # loop through the daily winners
        position = 220
        for user, score in history.data['top']['daily'][current_date].items():
            user = (user[:16] + '..') if len(user) > 18 else user
            score_text = small_font.render(f"{user} - {score}", True, (0, 0, 0))
            screen.blit(score_text, (190, position))
            position = position + 25

    high_score_text = font.render('All Time Leaders', True, (0, 0, 0))
    screen.blit(high_score_text, (390, 180))

    if len(history.data['top']['all']['users']) > 0:
        # loop through the daily winners
        position = 220
        for user, score in history.data['top']['all']['users'].items():
            user = (user[:16] + '..') if len(user) > 18 else user
            score_text = small_font.render(f"{user} - {score}", True, (0, 0, 0))
            screen.blit(score_text, (390, position))
            position = position + 25

running = True
while running:
    timer.tick(fps)
    screen.fill((128, 128, 128))

    history = History()
    username = None

    users = history.get_active_game_users()
    if len(users) > 0:
        user_data_time, username = next(iter(users.items()))

    if username != None and history.data[username]['current']['updated'] == "":
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history.data[username]['current']['updated'] = date_time
        history.save_file()

    pygame.draw.rect(screen, (0, 255, 0), [0, 0, WIDTH, HEIGHT])

    if username != None:
        if len(history.data[username]['current']['roundScores']) == 3 and history.data[username]['current']['remainingRolls'] == 0:
            pygame.draw.rect(screen, (255, 255, 255), [100, 100, WIDTH - 200, HEIGHT - 180])
            pygame.draw.rect(screen, (0, 0, 0), [95, 95, WIDTH - 190, HEIGHT - 170], 5, 8)

            # Game Over
            game_over_text = large_font.render(f"Game Over", True, (0, 0, 0))
            rect = game_over_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) - 28))
            screen.blit(game_over_text, rect)

            game_over_text = huge_font.render(f"Final Score", True, (0, 0, 0))
            rect = game_over_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 10))
            screen.blit(game_over_text, rect)

            game_over_text = huge_font.render(f"{sum(history.data[username]['current']['roundScores'])}", True, (0, 0, 0))
            rect = game_over_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 48))
            screen.blit(game_over_text, rect)
        elif history.data[username]['current']['remainingRolls'] == 3:
            pygame.draw.rect(screen, (255, 255, 255), [100, 100, WIDTH - 200, HEIGHT - 180])
            pygame.draw.rect(screen, (0, 0, 0), [95, 95, WIDTH - 190, HEIGHT - 170], 5, 8)

            game_over_text = large_font.render(f"Round {len(history.data[username]['current']['roundScores'])} completed", True, (0, 0, 0))
            rect = game_over_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) - 28))
            screen.blit(game_over_text, rect)

            game_over_text = huge_font.render(f"{sum(history.data[username]['current']['roundScores'])} Points Scored", True, (0, 0, 0))
            rect = game_over_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 10))
            screen.blit(game_over_text, rect)

            instruction_text = font.render(f"Roll to start next round", True, (0, 0, 0))
            rect = instruction_text.get_rect(center=(WIDTH / 2, (HEIGHT / 2) + 48))
            screen.blit(instruction_text, rect)
        else:
            die1 = DiceUI(10, 50, 1, 0, screen)
            die2 = DiceUI(130, 50, 1, 1, screen)
            die3 = DiceUI(250, 50, 1, 2, screen)
            die4 = DiceUI(370, 50, 1, 3, screen)
            die5 = DiceUI(490, 50, 1, 4, screen)

            die1.update_number(history.data[username]['current']['dice'][0])
            die1.update_active(True if 1 in history.data[username]['current']['diceHeld'] else False)

            die2.update_number(history.data[username]['current']['dice'][1])
            die2.update_active(True if 2 in history.data[username]['current']['diceHeld'] else False)

            die3.update_number(history.data[username]['current']['dice'][2])
            die3.update_active(True if 3 in history.data[username]['current']['diceHeld'] else False)

            die4.update_number(history.data[username]['current']['dice'][3])
            die4.update_active(True if 4 in history.data[username]['current']['diceHeld'] else False)

            die5.update_number(history.data[username]['current']['dice'][4])
            die5.update_active(True if 5 in history.data[username]['current']['diceHeld'] else False)

            ### Round 1
            round_one_score = 0
            round_one_score_label = ''
            if len(history.data[username]['current']['roundScores']) > 0:
                round_one_score = history.data[username]['current']['roundScores'][0]
                round_one_score_label = round_one_score
            round_1 = Label(0, 170, 'Round 1', round_one_score_label)

            ### Round 2
            round_two_score = 0
            round_two_score_label = ''
            if len(history.data[username]['current']['roundScores']) > 1:
                round_two_score = history.data[username]['current']['roundScores'][1]
                round_two_score_label = round_two_score
            round_2 = Label(0, 200, 'Round 2', round_two_score_label)

            ### Round 3
            round_three_score = 0
            round_three_score_label = ''
            if len(history.data[username]['current']['roundScores']) > 2:
                round_three_score = history.data[username]['current']['roundScores'][2]
                round_three_score_label = round_three_score
            round_3 = Label(0, 230, 'Round 3', round_three_score_label)

            ### Total
            total_score = 0
            if len(history.data[username]['current']['roundScores']) > 0:
                total_score = sum([round_one_score, round_two_score, round_three_score])
            grand_total = Label(0, 260, 'Total', total_score)

            draw_game(username)
            die1.draw()
            die2.draw()
            die3.draw()
            die4.draw()
            die5.draw()

            round_1.draw()
            round_2.draw()
            round_3.draw()
            grand_total.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()
