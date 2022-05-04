from PIL import Image, ImageDraw, ImageFilter, ImageFont
import constants

CARD_POSITIONS = {
    "board": [(235, 160), (265, 160), (295, 160), (325, 160), (355, 160)], 
    0: [(185, 240), (215, 240)],
    1: [(80, 190), (110, 190)], 
    2: [(80, 130), (110, 130)], 
    3: [(185, 80), (215, 80)], 
    4: [(280, 80), (310, 80)], 
    5: [(375, 80), (405, 80)],
    6: [(480, 130), (510, 130)],
    7: [(480, 190), (510, 190)],
    8: [(375, 240), (405, 240)]
    }

CHIP_POSITIONS = {
    "pot": (280, 230),
    0: (200, 210),
    1: (140, 195),
    2: (140, 135),
    3: (200, 120),
    4: (295, 120),
    5: (390, 120),
    6: (450, 135),
    7: (450, 195),
    8: (390, 210)
}

SUITS_DICT = {
    "s": "spades",
    "c": "clubs",
    "h": "hearts",
    "d": "diamonds"
}

RANKS_DICT = {
    "A": "ace",
    "T": "10",
    "J": "jack",
    "Q": "queen",
    "K": "king", 
}

class Renderer:

    def __init__(self, hole_cards_str, num_players, dealer_pos):
        pot = Image.open('poker_bot/images/chips/chip.png')
        self.pot = pot.resize((50,50))
        self.chip = pot.resize((25,25))

        self.pot_mask = Image.new("L", self.pot.size, 0)
        draw = ImageDraw.Draw(self.pot_mask)
        mask_width, mask_height = self.pot_mask.size
        draw.ellipse((0, 0, mask_width, mask_height), fill=255)
        # self.pot_mask.save('poker_bot/images/chips/pot_mask.jpg', quality=95)

        self.chip_mask = Image.new("L", self.chip.size, 0)
        draw = ImageDraw.Draw(self.chip_mask)
        mask_width, mask_height = self.chip_mask.size
        draw.ellipse((0, 0, mask_width, mask_height), fill=255)
        
        self.setup(hole_cards_str, num_players, dealer_pos)

    def setup(self, hole_cards_str, num_players, dealer_pos, init: bool = True):
        self.background = Image.open('poker_bot/images/poker_table.jpg')
        self.dealer_pos = dealer_pos
        self.num_players = num_players

        dealer = ImageDraw.Draw(self.background)
        dealer_font = ImageFont.truetype("poker_bot/images/Montserrat-Regular.ttf", 24)
        dealer.text((CHIP_POSITIONS["pot"][0]-25, CHIP_POSITIONS["pot"][1]-35), f'Dealer: {dealer_pos}', font=dealer_font, fill=(255, 0, 0))
        dealer.text((CARD_POSITIONS[0][0][0], CARD_POSITIONS[0][0][1]+40), "Pos 0", font=dealer_font, fill=(255, 0, 0))

        for key in CARD_POSITIONS:
            for i in range(len(CARD_POSITIONS[key])):
                if key == 0:
                    self.load_card(hole_cards_str[i], CARD_POSITIONS[key][i])
                else:
                    if type(key) == int and key not in list(range(num_players)):
                        pass
                    else:
                        self.load_card("", CARD_POSITIONS[key][i], True)

        for key in CHIP_POSITIONS:
            if key == "pot":
                self.update_pot("0", key, "pot")
            else:
                if key not in list(range(num_players)):
                    pass
                else:
                    self.update_pot("0", key, "chip")

        self.background.save('poker_bot/images/screen.jpg', quality=95)

    def load_card(self, card_str, position, blank: bool = False):
        if blank:
            lookup_query = 'poker_bot/images/cards/red_joker.png'
        else:
            lookup_value = [0, 0]
            if card_str[0] in RANKS_DICT:
                lookup_value[0] = RANKS_DICT[card_str[0]]
            else:
                lookup_value[0] = card_str[0]
            lookup_value[1] = SUITS_DICT[card_str[1]]
            
            lookup_query = f'poker_bot/images/cards/{"_of_".join(lookup_value)}.png'

        card = Image.open(lookup_query)
        card_size = list(card.size)
        card = card.resize((int(size/20) for size in card_size))
        self.background.paste(card, position)
        self.background.save('poker_bot/images/screen.jpg', quality=95)

    def update_pot(self, value, key, img):
        if img == "pot":
            self.background.paste(self.pot, CHIP_POSITIONS[key], self.pot_mask)
            pot_size = ImageDraw.Draw(self.background)
            pot_font = ImageFont.truetype("poker_bot/images/Montserrat-Regular.ttf", 24)
            pot_size.text((CHIP_POSITIONS[key][0]+17, CHIP_POSITIONS[key][1]+10), value, font=pot_font, fill=(255, 0, 0))
        else:
            self.background.paste(self.chip, CHIP_POSITIONS[key], self.chip_mask)
            chip_size = ImageDraw.Draw(self.background)
            chip_font = ImageFont.truetype("poker_bot/images/Montserrat-Regular.ttf", 14)
            chip_size.text((CHIP_POSITIONS[key][0]+7, CHIP_POSITIONS[key][1]+4), value, font=chip_font, fill=(255, 0, 0))
        self.background.save('poker_bot/images/screen.jpg', quality=95)

    def eliminate_player(self):
        self.num_players -= 1
    
    def peek_dealer_pos(self):
        return self.dealer_pos

# test_renderer = Renderer(("5s", "6c"), 5)