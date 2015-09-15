class TagType:

    ANIME = 'anime'
    COMMON = 'common'
    SEASON = 'season'

    choices = (
        (ANIME, 'Anime'),
        (COMMON, 'Common'),
        (SEASON, 'Season'),
    )

    d = dict(choices)
