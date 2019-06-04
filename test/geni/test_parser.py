from unittest import TestCase


from src.geni.parser import GenParser


class ParserTest(TestCase):

    def setUp(self) -> None:

        self.t1 = """
        [Intro: Eve]
        Uh, uh, uh, huh
        
        [Verse 1: Eve]
        Drop your glasses, shake your asses
        
        [Chorus: Gwen Stefani]
        If I had to give you more, it's only been a year
        
        [Post-Chorus: Eve]
        They wanna bank up, crank up, makes me dizzy
        
        [Verse 2: Eve]
        Now why you gritting your teeth?
        
        [Chorus: Gwen Stefani]
        If I had to give you more, it's only been a year
        
        [Verse 3: Eve]
        Let your bones crack
        
        [Chorus: Gwen Stefani]
        If I had to give you more, it's only been a year
        
        """

        self.t2 = """
        [Intro: Pharrell]
        Yeah... I just ordered one, my nigga
        Yeah...
        
        [Verse 1: Pusha T]
        I'm still a snow mover, blow harder than tuba
        
        [Chorus: Pusha T]
        When it comes to shooters, my niggas is trained to go
        
        [Verse 2: Pusha T]
        Between a renter and a homeowner
        
        [Chorus: Pusha T]
        When it comes to shooters, my niggas is trained to go
        
        [Verse 3: Ab-Liva]
        Nothing but cash here, this sweater is cashmere
        
        [Chorus: Pusha T]
        When it comes to shooters, my niggas is trained to go
        
        """

    def test_split(self):
        result = GenParser.extract_verses(self.t1)
        print(result)
