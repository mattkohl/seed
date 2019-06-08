from unittest import TestCase, skip


from src.geni.parser import GenParser


class ParserTest(TestCase):

    def setUp(self) -> None:

        self.t1 = """
        [Intro: Eve]
        Uh, uh, uh, huh
        
        [Verse 1: Eve]
        Drop your glasses, shake your asses
        Face screwed up like you having hot flashes
        Which one? Pick one, this one, classic
        Red from blonde, yeah, bitch, I'm drastic
        Why this, why that, lips stop askin'
        Listen to me, baby, relax and start passin'
        Expressway, hair back, weaving through the traffic
        This one strong, should be labeled as a hazard
        Some of y'all niggas hot, psych, I'm gassin'
        Clowns, I spot 'em and I can't stop laughin'
        Easy come, easy go, E-V gon' be lastin'
        Jealousy, let it go, results could be tragic
        Some of y'all ain't writing well, too concerned with fashion
        None of you ain't Giselle, cat walk and imagine
        A lot of y'all Hollywood, drama, casted
        Cut bitch, camera off, real shit, blast it
        
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
        [Intro]
        Uh, uh, uh, uh
        Uh, uh, uh, check the rhyme
        
        [Verse 1: Q-Tip & (<a about="http://dbpedia.org/resource/Phife_Dawg" typeof="http://dbpedia.org/ontology/Agent" href="http://dbpedia.org/resource/Phife_Dawg" title="http://dbpedia.org/resource/Phife_Dawg">Phife Dawg</a>)]
        Back in the days on the boulevard of Linden
        We used to kick routines and the presence was fittin'
        It was I, The Abstract
        (And me, the Five Footer)
        
        [Verse 2: <a about="http://dbpedia.org/resource/Phife_Dawg" typeof="http://dbpedia.org/ontology/Agent" href="http://dbpedia.org/resource/Phife_Dawg" title="http://dbpedia.org/resource/Phife_Dawg">Phife Dawg</a>]
        Now here's a funky introduction of how nice I am
        Tell your mother, tell your father, send a telegram
        I'm like an <a about="http://dbpedia.org/resource/Energizer" typeof="http://dbpedia.org/ontology/Agent" href="http://dbpedia.org/resource/Energizer" title="http://dbpedia.org/resource/Energizer">energizer</a> 'cause, you see, I last long
        
        [Chorus: Q-Tip]
        Check the rhyme y'all, check the rhyme y'all
        Check the rhyme y'all, check the rhyme y'all
        Check the rhyme y'all, check the rhyme y'all
        Check it out, check it out
        
        [Verse 3: <a about="http://dbpedia.org/resource/Phife_Dawg" typeof="http://dbpedia.org/ontology/Agent" href="http://dbpedia.org/resource/Phife_Dawg" title="http://dbpedia.org/resource/Phife_Dawg">Phife Dawg</a> & (Q-Tip)]
        Back in the days on the boulevard of Linden
        We used to kick routines and the presence was fittin'
        It was I, the Phifer (And me, the Abstract)
        (The rhymes were so rumpin' that the brothers rode the 'zack)
        
        [Verse 4: Q-Tip]
        Okay, if knowledge is the key then just show me the lock
        Got the scrawny legs but I move just like <a about="http://dbpedia.org/resource/Lou_Brock" typeof="http://dbpedia.org/ontology/Agent" href="http://dbpedia.org/resource/Lou_Brock" title="http://dbpedia.org/resource/Lou_Brock">Lou Brock</a>
        With speed, I'm agile plus I'm worth your while
        One hundred percent intelligent black child
        My optic presentation sizzles the retina
        How far must you go to gain respect? Umm...
        
        [Outro: Q-Tip]
        NC, y'all check the rhyme y'all
        <a about="http://dbpedia.org/resource/South_Carolina" typeof="http://dbpedia.org/ontology/AdministrativeRegion" href="http://dbpedia.org/resource/South_Carolina" title="http://dbpedia.org/resource/South_Carolina">SC</a>, y'all check it out y'all
        <a about="http://dbpedia.org/resource/Virginia" typeof="http://dbpedia.org/ontology/AdministrativeRegion" href="http://dbpedia.org/resource/Virginia" title="http://dbpedia.org/resource/Virginia">Virginia</a>, check the rhyme y'all
        Check it out, check it out
        In <a about="http://dbpedia.org/resource/London" typeof="http://dbpedia.org/ontology/Location" href="http://dbpedia.org/resource/London" title="http://dbpedia.org/resource/London">London</a>, check the rhyme, y'all
        
        """
        
        self.t3 = """
        [Intro]
        Somebody shoulda told me it would be like this
        Be like this, be like this
        Somebody shoulda told me it would be like this
        
        [Verse 1]
        Yeah, life is a balance
        You lose your grip, you can slip into an abyss
        No doubt, you see these niggas trippin'
        Ego in charge of every move, he's a star
        And we can't look away due to the days that he caught our hearts
        He's fallin' apart, but we deny it
        Justifying that half ass shit he dropped, we always buy it
        When he tell us he a genius but it's clearer lately
        It's been hard for him to look into the mirror lately
        There was a time when this nigga was my hero, maybe
        That's the reason why his fall from grace is hard to take
        'Cause I believed him when he said his shit was purer and he
        The type of nigga swear he real but all around him's fake
        The women, the dickriders, you know, the yes men
        Nobody with the balls to say somethin' to contest him
        So he grows out of control
        Into the person that he truly was all along, it's startin' to show
        Damn, wonder what happened
        Maybe it's my fault for idolizin' niggas
        Based off the words they be rappin'
        But come to find out, these niggas don't even write they shit
        Hear some new style bubblin' up, then they bite this shit
        Damn, that's what I get for lyin' to myself
        Well, fuck it, what's more important is he's cryin' out for help
        While the world's eggin' him on, I'm beggin' him to stop it
        Playin' his old shit, knowin' he won't top it
        False prophets        
        """        

    def test_extract_verses(self):
        results = GenParser.extract_verses(self.t1)
        for verse_tuple in results:
            self.assertTrue(verse_tuple.type is not None)
            self.assertTrue(verse_tuple.artists is not None)
            self.assertTrue(verse_tuple.text is not None)
            self.assertGreater(verse_tuple.offset, 0)
            if verse_tuple.type == "Verse":
                self.assertGreater(verse_tuple.number, 0)

    @skip
    def test_extract_annotated_verses(self):
        results = GenParser.extract_verses(self.t2)
        for verse_tuple in results:
            self.assertTrue(verse_tuple.type is not None)
            self.assertTrue(verse_tuple.artists is not None)
            self.assertTrue(verse_tuple.text is not None)
            self.assertGreater(verse_tuple.offset, 0)
            if verse_tuple.type == "Verse":
                self.assertGreater(verse_tuple.number, 0)

    def test_extract_verses_no_artist(self):
        for verse_tuple in GenParser.extract_verses(self.t3):
            self.assertTrue(verse_tuple.type is not None)
            self.assertTrue(verse_tuple.artists is None)
            self.assertTrue(verse_tuple.text is not None)
            self.assertGreater(verse_tuple.offset, 0)
            if verse_tuple.type == "Verse":
                self.assertGreater(verse_tuple.number, 0)
