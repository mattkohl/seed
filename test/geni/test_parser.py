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
        
        # self.t4 = "\n\n[Verse 1: Luckyiam]\nAwwww man\nIt's late as fuck\nThe sun is coming out\nIt's a long-ass night, but I feel good\n\n(Yeah, yeah, yeah, yeah, yeah)\n\nI really give a fuck what you think\nYou could judge me til your face turn pink\nJust ripped the show and we did what you can't\nLuck, and I'm drunk and I'm far in the paint\nI'm in Prague, she's in awe\nNever really seen a black man with charm\nHopped in the cab and we off to the bar\nOn the other side of town where the drinks come strong\nFive in the morning, I know the night young but she yawning\nTook her to the 'tel let her feel what she wanting\nI know I did it big I could tell by her moaning\nIn the morning in the morning\n\n[Hook: Sunspot Jonz]\nI know things could get all crazy\nBut you made it from the hating\nI know, I know\n\nGirl you all up in my mind\nI just wanna see you go shine\nSo let's go, let's go\n\n[Verse 2: Eligh]\nI'm taking a long-ass flight overseas\nSleeping on the plane until I reach Germany\nTiny group of people in Berlin, they heard of me\nStepping on stage to murder shit around three\nStinky motherfuckers usually surround me\nBut I don't clown, the got love for my sound\nThey want to see a party go down\nWith a cigarette burning past the filter, degrees\nIn the club hot mic feeds, they hop like fleas\nWhen they feel the energy\nThey got the Pac white tees\nBut they love a little me\nThey love a little me, they love a little me\n\n[Verse 3: Bicasso]\n\nI'm on the west side of town\nA tiny little spot where it all goes down\nA black new world in the bottom of the village\nWith cute little girls in their black bottom, vintage\nHigh-heeled boots, and they sippin'\nTwo dollar Cabernet, juke joint spinnin'\nLate night nigga cabaret, never-endin'\nLindy hoppin to new be-boppin'\nAnd fools be stopping through fitted\nWonder where it was? Better get in\nOr holla at Diallo if you with it\nThat's my nigga\n\n[Verse 4: Murs]\nYeah, yeah, yeah, yeah, yeah, yeah, yeah\nIt was a foreign exchange like Tay and them\nEatin' Mickey D's breakfast at six AM\nAin't nothing flyer than a Japanese sunrise\nI wasn't just trying to hit it like some guys\nHash browns, hotcakes, and I cleaned my plate\nI can't count all the bullshit that I done ate\nShe told me that she spoke English and I said great\nGrabbed her hand out the club and I said let's skate\n(Let's go)\nMan this life so special\nWhen the stress and strife try to test you\nDUI and they try to arrest you\nIf you faded coming home from the club, God bless you\n\n[Hook]\n\n[Verse 5: Aesop]\nI had a party at my house tonight\nEvery girl that came through looked tight\nAll the homies had fun, there's no need to fight\nSo much drank and weed to keep us high as a kite\nNow the sun is coming out, to chase the night away\nIf you listen really close, you could still hear the DJ play\nShe was beautiful, I hung on every single word she said\nLike, let's get close there's no time to wait\nMy niggas ain't gotta go home\nBut ya'll sure can't stay\n\n[Verse 6: The Grouch]\nGood music for the grown and sexy\nMy lady and I, two of the best seats\nBut we ain't sitting down, we in step see\nBig booty up close, pressed to me\nI grab her waist and I smell her perfume\nJill Scott keeps singing her tune\nFull moon and it's feeling real now\nBabysitter, one o'clock and we still out\nBlow the joint, breath the air, hit a detour\nNo one can see us in this lot, you could be sure\nMake it hot, get the windows steamy\nCar rocking, it's great to be me\n\n[Hook]\n\n[Verse 7: Scarub]\nLet's go. Ha!\n\nWe could fly to Galapagos\nSwim in the Ivory Coast\nRoll in the sands, hand in hand\nLet me hold ya close\nSip on some wine and toast\nDown the shore lines and posts\nLivin' the dream\nKnaw' I mean\nWe be doin the most\nYou the one that I chose\nRub you down to your toes\nLet's see how far this goes\nUnder the cosmos\nTwo searching souls\nWhere it ends? Only God knows\nOne thing for sure I want you in my tomorrows\nYeah! And all them days after that\nI'll be your Romeo, you be my Juliet\nAnd if you with me holler back baby\nYeah! If you with me where you at?\n\n[Outro: Murs]\nYeah, Yeah!\nAnd I want to dedicate this to Monsignor, my main man on the boards\nAnd to everybody that's coming home and it's really to early to go to sleep\nAnd it's too late to call it a late night creep, take your ass in the house before noon!\nBecause then you're crazy, and use a condom\nAnd if you go to jail call your mama because don't nobody else give a fuck about you. Peace!\n\nOh! Oh! Oh! Oh! Oh!\nRemember the wop? And the cabbage patch?\nDid you used to do that? Like that?\nOh, oh, yeah, yeah, yeah\nUgh, ugh, ugh, ugh\n(Let's go)\n\nTo all the late night people\nDriving home from the club, you know your *** got work in the morning!\nI hope your ass don't get fired\nLiving Legends. We invented fun!\nWe the best in the world, I feel the breast on your girl\nUgh, ugh, ugh..yeah…LEGGEEEEEEEENDS\n\nThis is for when you're like six AM, it told you\nAnd he furniture is all white and plastic\nAnd you talking to a girl you have no business talking to, because she's too fine\nAnd you ain't never talked to a girl that fine before\nTell her that you know me and it'll be all good\nI'm just talking Monsignor, you can cut me off anytime\n\nPEACE! And we out\nI always wanted to say that, peace! And we out\n\nI wanna give a shout out to baby Rio\nTo Anticon…hahahahaha\nTo all the hipsters, that shirt cost $60 and you just spilled ketchup on it\nDon't that suck? Now it's really limited edition you asshole\nIf you come to my neighborhood, we'd beat your motherfucking ass\nThat's alright, you driving your mama's Lexus, what's up!\nHahahaha, suck my dick!\nThat's how it goes in the streets, I love you man\nBut we gotta clown man, we gotta have fun man\nWhat's life if it's not fun? What's he gonna do man?\nIt's 6 am you still high off cocaine man\nYou shouldn't do hard drugs man, you know what I'm saying?\nYou shouldn't do drugs that are harder than you\nIf you a soft muthafucker, you shouldn't do hard drugs!\nHow about that? Because the hangover in the morning is going to beat yo ass\nThat's the problem, shout out to everybody who was drinking Hennessey all night\nOr all you dumb motherfuckers who bought that Ace of Spades champagne\nBecause Jay-Z put it in his new video. How 'bout that?\nHow about you have a mind of your own man?\n\nAn if you get pulled over like I said before, you're going to jail, but its alright\nAnd if you downloaded this for free, you're never going to get laid again\nLike Monsignor. Monsignor, when's the last time you got some pussy?\nAnd if it's 6 AM and you just called a girl that got a baby of yours\nAnd you gonna go have sex with the baby asleep in the bed next you, you scandalous\nBut it's a way of life you know what I'm saying?\nAnd if look, look, look, look, to all the Mexican homies headed to King Taco in East LA\nI'mma see you out there. Bring your little sister 'cause I wanna get her pregnant\n\nHahahahaah\n\nI'm out though ay...vamanos!\n\n"
        self.t4 = """

[Verse 1: Luckyiam]
Awwww man
It's late as fuck
The sun is coming out
It's a long-ass night, but I feel good

(Yeah, yeah, yeah, yeah, yeah)

I really give a fuck what you think
You could judge me til your face turn pink
Just ripped the show and we did what you can't
Luck, and I'm drunk and I'm far in the paint
I'm in Prague, she's in awe
Never really seen a black man with charm
Hopped in the cab and we off to the bar
On the other side of town where the drinks come strong
Five in the morning, I know the night young but she yawning
Took her to the 'tel let her feel what she wanting
I know I did it big I could tell by her moaning
In the morning in the morning

[Hook: Sunspot Jonz]
I know things could get all crazy
But you made it from the hating
I know, I know

Girl you all up in my mind
I just wanna see you go shine
So let's go, let's go

[Verse 2: Eligh]
I'm taking a long-ass flight overseas
Sleeping on the plane until I reach Germany
Tiny group of people in Berlin, they heard of me
Stepping on stage to murder shit around three
Stinky motherfuckers usually surround me
But I don't clown, the got love for my sound
They want to see a party go down
With a cigarette burning past the filter, degrees
In the club hot mic feeds, they hop like fleas
When they feel the energy
They got the Pac white tees
But they love a little me
They love a little me, they love a little me

[Verse 3: Bicasso]

I'm on the west side of town
A tiny little spot where it all goes down
A black new world in the bottom of the village
With cute little girls in their black bottom, vintage
High-heeled boots, and they sippin'
Two dollar Cabernet, juke joint spinnin'
Late night nigga cabaret, never-endin'
Lindy hoppin to new be-boppin'
And fools be stopping through fitted
Wonder where it was? Better get in
Or holla at Diallo if you with it
That's my nigga

[Verse 4: Murs]
Yeah, yeah, yeah, yeah, yeah, yeah, yeah
It was a foreign exchange like Tay and them
Eatin' Mickey D's breakfast at six AM
Ain't nothing flyer than a Japanese sunrise
I wasn't just trying to hit it like some guys
Hash browns, hotcakes, and I cleaned my plate
I can't count all the bullshit that I done ate
She told me that she spoke English and I said great
Grabbed her hand out the club and I said let's skate
(Let's go)
Man this life so special
When the stress and strife try to test you
DUI and they try to arrest you
If you faded coming home from the club, God bless you

[Hook]

[Verse 5: Aesop]
I had a party at my house tonight
Every girl that came through looked tight
All the homies had fun, there's no need to fight
So much drank and weed to keep us high as a kite
Now the sun is coming out, to chase the night away
If you listen really close, you could still hear the DJ play
She was beautiful, I hung on every single word she said
Like, let's get close there's no time to wait
My niggas ain't gotta go home
But ya'll sure can't stay

[Verse 6: The Grouch]
Good music for the grown and sexy
My lady and I, two of the best seats
But we ain't sitting down, we in step see
Big booty up close, pressed to me
I grab her waist and I smell her perfume
Jill Scott keeps singing her tune
Full moon and it's feeling real now
Babysitter, one o'clock and we still out
Blow the joint, breath the air, hit a detour
No one can see us in this lot, you could be sure
Make it hot, get the windows steamy
Car rocking, it's great to be me

[Hook]

[Verse 7: Scarub]
Let's go. Ha!

We could fly to Galapagos
Swim in the Ivory Coast
Roll in the sands, hand in hand
Let me hold ya close
Sip on some wine and toast
Down the shore lines and posts
Livin' the dream
Knaw' I mean
We be doin the most
You the one that I chose
Rub you down to your toes
Let's see how far this goes
Under the cosmos
Two searching souls
Where it ends? Only God knows
One thing for sure I want you in my tomorrows
Yeah! And all them days after that
I'll be your Romeo, you be my Juliet
And if you with me holler back baby
Yeah! If you with me where you at?

[Outro: Murs]
Yeah, Yeah!
And I want to dedicate this to Monsignor, my main man on the boards
And to everybody that's coming home and it's really to early to go to sleep
And it's too late to call it a late night creep, take your ass in the house before noon!
Because then you're crazy, and use a condom
And if you go to jail call your mama because don't nobody else give a fuck about you. Peace!

Oh! Oh! Oh! Oh! Oh!
Remember the wop? And the cabbage patch?
Did you used to do that? Like that?
Oh, oh, yeah, yeah, yeah
Ugh, ugh, ugh, ugh
(Let's go)

To all the late night people
Driving home from the club, you know your *** got work in the morning!
I hope your ass don't get fired
Living Legends. We invented fun!
We the best in the world, I feel the breast on your girl
Ugh, ugh, ugh..yeah…LEGGEEEEEEEENDS

This is for when you're like six AM, it told you
And he furniture is all white and plastic
And you talking to a girl you have no business talking to, because she's too fine
And you ain't never talked to a girl that fine before
Tell her that you know me and it'll be all good
I'm just talking Monsignor, you can cut me off anytime

PEACE! And we out
I always wanted to say that, peace! And we out

I wanna give a shout out to baby Rio
To Anticon…hahahahaha
To all the hipsters, that shirt cost $60 and you just spilled ketchup on it
Don't that suck? Now it's really limited edition you asshole
If you come to my neighborhood, we'd beat your motherfucking ass
That's alright, you driving your mama's Lexus, what's up!
Hahahaha, suck my dick!
That's how it goes in the streets, I love you man
But we gotta clown man, we gotta have fun man
What's life if it's not fun? What's he gonna do man?
It's 6 am you still high off cocaine man
You shouldn't do hard drugs man, you know what I'm saying?
You shouldn't do drugs that are harder than you
If you a soft muthafucker, you shouldn't do hard drugs!
How about that? Because the hangover in the morning is going to beat yo ass
That's the problem, shout out to everybody who was drinking Hennessey all night
Or all you dumb motherfuckers who bought that Ace of Spades champagne
Because Jay-Z put it in his new video. How 'bout that?
How about you have a mind of your own man?

An if you get pulled over like I said before, you're going to jail, but its alright
And if you downloaded this for free, you're never going to get laid again
Like Monsignor. Monsignor, when's the last time you got some pussy?
And if it's 6 AM and you just called a girl that got a baby of yours
And you gonna go have sex with the baby asleep in the bed next you, you scandalous
But it's a way of life you know what I'm saying?
And if look, look, look, look, to all the Mexican homies headed to King Taco in East LA
I'mma see you out there. Bring your little sister 'cause I wanna get her pregnant

Hahahahaah

I'm out though ay...vamanos!
"""

    def test_extract_sections(self):
        section_tuples = GenParser.extract_sections(self.t1)
        nums = [t.number for t in section_tuples if t.number is not None]
        self.assertEqual(len(nums), 3)
        for section_tuple in section_tuples:
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is not None)
            self.assertTrue(section_tuple.text is not None)
            self.assertGreater(section_tuple.offset, 0)
            if section_tuple.type == "Verse":
                self.assertGreater(section_tuple.number, 0)

    def test_extract_sections_no_artist(self):
        section_tuples = GenParser.extract_sections(self.t3)
        nums = [t.number for t in section_tuples if t.number is not None]
        self.assertEqual(len(nums), 1)
        for section_tuple in section_tuples:
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is None)
            self.assertTrue(section_tuple.text is not None)
            self.assertGreater(section_tuple.offset, 0)
            if section_tuple.type == "Verse":
                self.assertGreater(section_tuple.number, 0)

    def test_extract_sections_t4(self):
        section_tuples = GenParser.extract_sections(self.t4)
        nums = [t.number for t in section_tuples if t.number is not None]
        self.assertEqual(len(nums), 7)
        for section_tuple in section_tuples:
            for k, v in section_tuple._asdict().items():
                print(k.upper(), ":", v)
            self.assertTrue(section_tuple.type is not None)
            self.assertTrue(section_tuple.artists is not None)
            self.assertTrue(section_tuple.text is not None)
            if section_tuple.number == 7:
                self.assertIn("Yeah! If you with me where you at?", section_tuple.text)