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
        
        self.t4 = "\n\n[Verse 1: Luckyiam]\nAwwww man\nIt's late as fuck\nThe sun is coming out\nIt's a long-ass night, but I feel good\n\n(Yeah, yeah, yeah, yeah, yeah)\n\nI really give a fuck what you think\nYou could judge me til your face turn pink\nJust ripped the show and we did what you can't\nLuck, and I'm drunk and I'm far in the paint\nI'm in Prague, she's in awe\nNever really seen a black man with charm\nHopped in the cab and we off to the bar\nOn the other side of town where the drinks come strong\nFive in the morning, I know the night young but she yawning\nTook her to the 'tel let her feel what she wanting\nI know I did it big I could tell by her moaning\nIn the morning in the morning\n\n[Hook: Sunspot Jonz]\nI know things could get all crazy\nBut you made it from the hating\nI know, I know\n\nGirl you all up in my mind\nI just wanna see you go shine\nSo let's go, let's go\n\n[Verse 2: Eligh]\nI'm taking a long-ass flight overseas\nSleeping on the plane until I reach Germany\nTiny group of people in Berlin, they heard of me\nStepping on stage to murder shit around three\nStinky motherfuckers usually surround me\nBut I don't clown, the got love for my sound\nThey want to see a party go down\nWith a cigarette burning past the filter, degrees\nIn the club hot mic feeds, they hop like fleas\nWhen they feel the energy\nThey got the Pac white tees\nBut they love a little me\nThey love a little me, they love a little me\n\n[Verse 3: Bicasso]\n\nI'm on the west side of town\nA tiny little spot where it all goes down\nA black new world in the bottom of the village\nWith cute little girls in their black bottom, vintage\nHigh-heeled boots, and they sippin'\nTwo dollar Cabernet, juke joint spinnin'\nLate night nigga cabaret, never-endin'\nLindy hoppin to new be-boppin'\nAnd fools be stopping through fitted\nWonder where it was? Better get in\nOr holla at Diallo if you with it\nThat's my nigga\n\n[Verse 4: Murs]\nYeah, yeah, yeah, yeah, yeah, yeah, yeah\nIt was a foreign exchange like Tay and them\nEatin' Mickey D's breakfast at six AM\nAin't nothing flyer than a Japanese sunrise\nI wasn't just trying to hit it like some guys\nHash browns, hotcakes, and I cleaned my plate\nI can't count all the bullshit that I done ate\nShe told me that she spoke English and I said great\nGrabbed her hand out the club and I said let's skate\n(Let's go)\nMan this life so special\nWhen the stress and strife try to test you\nDUI and they try to arrest you\nIf you faded coming home from the club, God bless you\n\n[Hook]\n\n[Verse 5: Aesop]\nI had a party at my house tonight\nEvery girl that came through looked tight\nAll the homies had fun, there's no need to fight\nSo much drank and weed to keep us high as a kite\nNow the sun is coming out, to chase the night away\nIf you listen really close, you could still hear the DJ play\nShe was beautiful, I hung on every single word she said\nLike, let's get close there's no time to wait\nMy niggas ain't gotta go home\nBut ya'll sure can't stay\n\n[Verse 6: The Grouch]\nGood music for the grown and sexy\nMy lady and I, two of the best seats\nBut we ain't sitting down, we in step see\nBig booty up close, pressed to me\nI grab her waist and I smell her perfume\nJill Scott keeps singing her tune\nFull moon and it's feeling real now\nBabysitter, one o'clock and we still out\nBlow the joint, breath the air, hit a detour\nNo one can see us in this lot, you could be sure\nMake it hot, get the windows steamy\nCar rocking, it's great to be me\n\n[Hook]\n\n[Verse 7: Scarub]\nLet's go. Ha!\n\nWe could fly to Galapagos\nSwim in the Ivory Coast\nRoll in the sands, hand in hand\nLet me hold ya close\nSip on some wine and toast\nDown the shore lines and posts\nLivin' the dream\nKnaw' I mean\nWe be doin the most\nYou the one that I chose\nRub you down to your toes\nLet's see how far this goes\nUnder the cosmos\nTwo searching souls\nWhere it ends? Only God knows\nOne thing for sure I want you in my tomorrows\nYeah! And all them days after that\nI'll be your Romeo, you be my Juliet\nAnd if you with me holler back baby\nYeah! If you with me where you at?\n\n[Outro: Murs]\nYeah, Yeah!\nAnd I want to dedicate this to Monsignor, my main man on the boards\nAnd to everybody that's coming home and it's really to early to go to sleep\nAnd it's too late to call it a late night creep, take your ass in the house before noon!\nBecause then you're crazy, and use a condom\nAnd if you go to jail call your mama because don't nobody else give a fuck about you. Peace!\n\nOh! Oh! Oh! Oh! Oh!\nRemember the wop? And the cabbage patch?\nDid you used to do that? Like that?\nOh, oh, yeah, yeah, yeah\nUgh, ugh, ugh, ugh\n(Let's go)\n\nTo all the late night people\nDriving home from the club, you know your *** got work in the morning!\nI hope your ass don't get fired\nLiving Legends. We invented fun!\nWe the best in the world, I feel the breast on your girl\nUgh, ugh, ugh..yeah…LEGGEEEEEEEENDS\n\nThis is for when you're like six AM, it told you\nAnd he furniture is all white and plastic\nAnd you talking to a girl you have no business talking to, because she's too fine\nAnd you ain't never talked to a girl that fine before\nTell her that you know me and it'll be all good\nI'm just talking Monsignor, you can cut me off anytime\n\nPEACE! And we out\nI always wanted to say that, peace! And we out\n\nI wanna give a shout out to baby Rio\nTo Anticon…hahahahaha\nTo all the hipsters, that shirt cost $60 and you just spilled ketchup on it\nDon't that suck? Now it's really limited edition you asshole\nIf you come to my neighborhood, we'd beat your motherfucking ass\nThat's alright, you driving your mama's Lexus, what's up!\nHahahaha, suck my dick!\nThat's how it goes in the streets, I love you man\nBut we gotta clown man, we gotta have fun man\nWhat's life if it's not fun? What's he gonna do man?\nIt's 6 am you still high off cocaine man\nYou shouldn't do hard drugs man, you know what I'm saying?\nYou shouldn't do drugs that are harder than you\nIf you a soft muthafucker, you shouldn't do hard drugs!\nHow about that? Because the hangover in the morning is going to beat yo ass\nThat's the problem, shout out to everybody who was drinking Hennessey all night\nOr all you dumb motherfuckers who bought that Ace of Spades champagne\nBecause Jay-Z put it in his new video. How 'bout that?\nHow about you have a mind of your own man?\n\nAn if you get pulled over like I said before, you're going to jail, but its alright\nAnd if you downloaded this for free, you're never going to get laid again\nLike Monsignor. Monsignor, when's the last time you got some pussy?\nAnd if it's 6 AM and you just called a girl that got a baby of yours\nAnd you gonna go have sex with the baby asleep in the bed next you, you scandalous\nBut it's a way of life you know what I'm saying?\nAnd if look, look, look, look, to all the Mexican homies headed to King Taco in East LA\nI'mma see you out there. Bring your little sister 'cause I wanna get her pregnant\n\nHahahahaah\n\nI'm out though ay...vamanos!\n\n"

    def test_extract_sections(self):
        results = GenParser.extract_sections(self.t1)
        for section_tuple in results:
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is not None)
            self.assertTrue(section_tuple.text is not None)
            self.assertGreater(section_tuple.offset, 0)
            if section_tuple.type == "Verse":
                self.assertGreater(section_tuple.number, 0)

    @skip
    def test_extract_annotated_sections(self):
        results = GenParser.extract_sections(self.t2)
        for section_tuple in results:
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is not None)
            self.assertTrue(section_tuple.text is not None)
            self.assertGreater(section_tuple.offset, 0)
            if section_tuple.type == "Verse":
                self.assertGreater(section_tuple.number, 0)

    def test_extract_sections_no_artist(self):
        for section_tuple in GenParser.extract_sections(self.t3):
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is None)
            self.assertTrue(section_tuple.text is not None)
            self.assertGreater(section_tuple.offset, 0)
            if section_tuple.type == "Verse":
                self.assertGreater(section_tuple.number, 0)

    def test_extract_sections_t4(self):
        section_tuples = GenParser.extract_sections(self.t4)
        print(len(section_tuples))
        print(section_tuples)