from random import randint


def get_random_gender():
    genders = ('♀', '♂')
    rand_int = randint(0, 1)
    return genders[rand_int]

def get_random_skin_tone():
    skin_tones = ('🏻', '🏼', '🏽', '🏾', '🏿',)
    rand_int = randint(0, 4)
    return skin_tones[rand_int]
