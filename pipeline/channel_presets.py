"""Channel niches: system prompt + defaults for Groq script generation.

Each preset includes a topic_pool — a list of setting/situation ideas.
One is picked randomly per run if no --topic is provided, ensuring variety.
"""

from __future__ import annotations

from typing import TypedDict


class Variant(TypedDict, total=False):
    """One output variant — same images, different audio/subs/upload target."""
    lang: str  # "en", "hi", etc. used as key in Groq response
    label: str  # human-readable for logs
    tts_voice: str  # Edge TTS voice (e.g. "hi-IN-MadhurNeural")
    tts_provider: str  # "deapi", "sfx", or legacy "edge"
    caption_font: str  # font filename inside assets/fonts/
    caption_font_name: str  # FFmpeg-visible font family name
    yt_token_env: str  # env var name for YouTube refresh token (e.g. "YT_REFRESH_TOKEN_HI")
    min_words: int  # min word count for narration validation


class ChannelPreset(TypedDict, total=False):
    id: str
    label: str
    groq_system_hint: str
    segment_count: int  # images + script beats
    topic_pool: list[str]
    image_style_suffix: str  # appended to every image prompt
    image_negative_prompt: str  # passed as negative prompt
    # Single-variant fields (backward compat — used when `variants` is absent):
    language: str
    tts_voice: str
    tts_provider: str
    caption_font: str
    caption_font_name: str
    min_words: int  # min word count for narration validation (single-variant)
    # Multi-variant mode — Groq returns translations for each lang, pipeline renders+uploads per variant.
    variants: list[Variant]
    # topic_rotation: "myth" → pipeline/myth_topics.py (IST day theme + no-repeat within theme)
    topic_rotation: str
    # Single-variant YouTube upload: which env var holds this channel's refresh token
    yt_token_env: str
    # Extra uploads: same MP4 uploaded to additional channels using these env var names
    extra_yt_token_envs: list[str]


PRESETS: dict[str, ChannelPreset] = {
    "general_stories": {
        "id": "general_stories",
        "label": "Original cinematic storytime Shorts with varied everyday themes",
        "min_words": 105,
        "tts_provider": "deapi",
        "tts_voice": "am_michael",
        "groq_system_hint": (
            "You write highly engaging original storytime Shorts for a broad general audience. "
            "Every story must feel natural, specific, and emotionally believable, with a strong opening, "
            "clear progression, and satisfying twist, realization, or payoff. Use 120-145 words total, "
            "about 35-50 seconds spoken. Vary genre and mood: emotional, funny, mysterious, inspiring, "
            "awkward, suspenseful, surprising, or thought-provoking. Horror may appear occasionally but "
            "must never dominate. Use realistic dialogue sparingly and natural human phrasing. "
            "All people, places, and events are fictional and original. Never claim a fictional story is "
            "real news or evidence. PG-13, no graphic violence, no sexual content, no hate, no dangerous "
            "instructions, and no hashtags in narration. Never use copyrighted characters, franchises, "
            "celebrity likenesses, song lyrics, famous quotes, slogans, or recognizable existing plots."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", cinematic editorial story illustration, natural human expressions, realistic proportions, "
            "rich environmental detail, subtle film lighting, modern color grading, varied camera angles, "
            "professional vertical video visual, no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "watermark, logo, text, title, signature, celebrity, copyrighted character, brand mascot, "
            "distorted face, extra limbs, broken anatomy, low quality, blurry, gore, blood, nudity"
        ),
        "topic_pool": [
            "a stranger returning a wallet with an unexpected note",
            "a quiet employee discovering why the office cleaner stayed late",
            "two passengers accidentally exchanging identical bags",
            "a missed train leading to an important friendship",
            "a delivery arriving at the wrong apartment",
            "a student finding an old message hidden inside a library book",
            "a family dinner interrupted by a surprising confession",
            "a shopkeeper recognizing a customer from twenty years ago",
            "a phone call meant for someone else changing one evening",
            "a small lie at work growing into an awkward situation",
            "a traveler helping someone without sharing a common language",
            "a forgotten birthday turning into an unexpected celebration",
            "a neighbor leaving mysterious helpful gifts",
            "a job interview taking an unusual but meaningful turn",
            "a child teaching two arguing adults a simple lesson",
            "a restaurant order revealing a long-lost connection",
            "a photographer noticing the same stranger in old pictures",
            "a broken elevator forcing rivals to finally talk",
            "a bus driver waiting for one passenger every morning",
            "a wrong number becoming a source of encouragement",
            "a wedding guest discovering an invitation mistake",
            "a street musician receiving an unforgettable request",
            "a teacher learning why one student always arrived early",
            "a tenant discovering who cared for the rooftop garden",
            "a reunion where nobody recognizes the most successful classmate",
            "a mysterious package containing only ordinary objects",
            "a commuter finding handwritten advice on a train seat",
            "a sibling keeping a harmless secret for many years",
            "a customer complaint ending with an unexpected apology",
            "a rainy-day act of kindness returning years later",
            "a harmless mystery in a hotel room",
            "a strange coincidence during a road trip",
            "a suspenseful late-night encounter with a simple explanation",
            "an old voicemail revealing a misunderstood memory",
            "a contest winner choosing a surprising prize",
            "a new employee solving a problem everyone ignored",
        ],
    },
    "facts": {
        "id": "facts",
        "label": "Mind-blowing facts Short (bilingual — Hindi + English)",
        "variants": [
            {
                "lang": "hi",
                "label": "Hindi",
                "tts_voice": "hi-IN-MadhurNeural",
                "caption_font": "NotoSansDevanagari-Bold.ttf",
                "caption_font_name": "Noto Sans Devanagari",
                "yt_token_env": "YT_REFRESH_TOKEN_HI",
                "min_words": 80,
            },
            {
                "lang": "en",
                "label": "English",
                "tts_voice": "en-US-GuyNeural",
                "caption_font": "BebasNeue-Regular.ttf",
                "caption_font_name": "Bebas Neue",
                "yt_token_env": "YT_REFRESH_TOKEN_EN",
                "min_words": 70,
            },
        ],
        "groq_system_hint": (
            "You write punchy YouTube Shorts about surprising, verified facts — in MULTIPLE languages. "
            "The same fact will be published as separate videos on different language channels. "
            "STRUCTURE: hook fact in opening, supporting facts in the middle, punchline + takeaway at end. "
            "TONE: energetic, curious, confident. No clickbait lies. "
            "Each fact must be broadly accurate; if unsure, use safer wording like "
            "'scientists believe' or 'some research suggests'. "
            "No medical advice. No hashtags inside narration. Original phrasing only. "
            "IMAGE PROMPT RULE: write image prompts in ENGLISH only. Describe real photographs or documentary stills. "
            "Use real-world subjects, real lighting, real environments. NEVER write 'cartoon', 'illustration', "
            "'anime', or 'stylized'. Examples: 'a real octopus underwater in clear blue ocean, sunlight rays', "
            "'close-up macro photo of a honeybee on a yellow flower', "
            "'wide shot of Saturn V rocket launching at night with flames'. "
            "BILINGUAL RULE: the SAME story/facts must be expressed naturally in each language — "
            "do not literally translate word-for-word; rephrase so each version sounds native and flows well. "
            "HINDI LENGTH: variants.hi.full_narration should be long-form — "
            "aim ~150 Devanagari words (acceptable band roughly 135-170) with rich detail and connective phrases "
            "so the Hindi voiceover is substantial (~55-70 seconds). "
            "ENGLISH LENGTH: variants.en.full_narration must be long-form too — "
            "aim 120-155 English words (never a short teaser); include hook, 3-4 developed beats with examples, "
            "and a strong closing line so the English voiceover is ~40-50 seconds."
        ),
        "segment_count": 5,
        "image_style_suffix": (
            ", photorealistic documentary photography, cinematic lighting, ultra detailed, "
            "8k, sharp focus, professional camera, National Geographic style, realistic textures, "
            "natural colors, depth of field, no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "cartoon, anime, illustration, painting, drawing, sketch, 3d render, cgi, "
            "stylized, flat colors, low quality, blurry, watermark, logo, text, signature, "
            "deformed, ugly, extra limbs, mutated"
        ),
        "topic_pool": [
            # Space & Universe
            "black holes", "neutron stars", "Mars mysteries", "Moon secrets", "exoplanets",
            "the Big Bang", "dark matter", "the asteroid belt", "Saturn's rings",
            "Jupiter's storms", "sounds in space", "dead stars", "parallel universes",
            "time dilation", "cosmic radiation", "space colonies", "SETI and alien signals",
            "the Voyager probe", "sun facts", "galaxy collisions", "space weather",
            "quantum physics weirdness", "multiverse theory", "wormholes",
            "the edge of the observable universe",
            # Animals & Nature
            "deep sea creatures", "parasites that control minds", "animal superpowers",
            "extinct animals", "animals that basically can't die",
            "venomous creatures of India", "crow intelligence", "the octopus brain",
            "the mantis shrimp", "tardigrades", "animal sleep habits", "migration mysteries",
            "camouflage masters", "animals that mourn their dead", "bioluminescence",
            "carnivorous plants", "fungi intelligence", "ant colonies", "whale communication",
            "spider silk science", "the immortal jellyfish", "animal self-medication",
            "dolphin language", "electric eels", "naked mole rats", "bird navigation",
            "snake facts", "insects you didn't know exist", "animals in Indian forests",
            "microorganisms living in your body",
            # Human Body & Psychology
            "brain illusions", "the science of sleep paralysis", "memory tricks",
            "the placebo effect", "pain tolerance", "human senses you didn't know about",
            "DNA secrets", "the gut-brain connection", "adrenaline effects",
            "the subconscious mind", "phobias explained", "the science of dreams",
            "body language secrets", "why we laugh", "human evolution oddities",
            "the science of aging", "near-death experiences", "hypnosis facts",
            "déjà vu explained", "emotional memory", "synesthesia", "muscle memory",
            "the fear response", "the science of addiction", "human body record breakers",
            # History & Civilizations
            "Ancient Egypt secrets", "dark facts about the Roman Empire", "lost civilizations",
            "medieval torture devices", "ancient Indian empires", "Mughal secrets",
            "forgotten inventions", "unknown facts about World War 2", "Cold War spy stories",
            "Greek myths debunked", "real Viking history", "the Aztec civilization",
            "the Indus Valley mystery", "the Maurya Empire", "the Chola naval empire",
            "the history of slavery", "ancient medicines", "the oldest cities on Earth",
            "ancient trade routes", "Genghis Khan facts", "the real Cleopatra",
            "Alexander the Great", "dark facts about British India",
            "untold partition of India stories", "ancient Chinese secrets",
            "the real life of samurai", "real pirate history", "the Byzantine Empire",
            "the Ottoman Empire", "ancient astronomy",
            # India Specific
            "India's unsolved mysteries", "cursed places in India",
            "unknown Indian inventions", "weird Indian laws",
            "dark stories from Indian mythology", "haunted forts of India",
            "untold Indian freedom fighters", "India's richest kings in history",
            "origin stories of Indian street food", "India's rarest animals",
            "Indian space program facts", "the engineering of ancient temples",
            "India's tribal cultures", "Bollywood dark secrets",
            "India's geographical oddities", "mysteries of Indian rivers",
            "Indian martial arts", "underground cities of India",
            "India's hottest and coldest places", "facts about Indian languages",
            # Money & Power
            "the richest people in history", "how billionaires think",
            "the dark side of corporations", "famous stock market crashes",
            "consequences of money printing", "heists gone wrong",
            "underground economies", "tax havens explained",
            "the richest countries in history", "failed currencies",
            "the gold standard", "dark stories from crypto", "the mafia economy",
            "war profiteering", "untold stories of India's richest businessmen",
            "how banks really work", "money psychology", "poverty traps",
            "famous economic collapses", "the dark side of diamonds",
            # Science & Tech
            "when AI went wrong", "internet dark secrets", "nuclear energy facts",
            "genetic engineering", "CRISPR experiments", "lab-grown meat",
            "deepfake technology", "social media algorithms", "dark web facts",
            "surveillance technology", "robot evolution", "battery technology secrets",
            "shocking climate science facts", "plastic in the human body",
            "microwave radiation", "5G facts vs myths", "quantum computing",
            "the history of bioweapons", "chemical reactions gone wrong",
            "future technology predictions",
            # Food & Substances
            "foods your brain is addicted to", "the dark side of sugar",
            "fast food secrets", "spices that changed history",
            "poisonous foods we eat daily", "the science of fermentation",
            "caffeine deep dive", "the science of alcohol",
            "the spiciest things on Earth", "food frauds worldwide",
            "ancient recipes still used today", "rare foods only the rich eat",
            "the history of Indian spices", "foods banned around the world",
            "GMO food facts",
            # Crime & Dark Secrets
            "unsolved murders", "serial killer psychology",
            "cults that shocked the world", "government experiments on humans",
            "corporate cover-ups", "art heists", "counterfeit economies",
            "organized crime facts", "famous prison escapes",
            "cold cases solved by DNA", "the biggest cyber crimes ever",
            "assassination plots", "whistleblower stories",
            "the dark side of Hollywood", "scams that fooled millions",
            "human trafficking networks", "drug cartel economics",
            "facts about corrupt governments", "identity theft stories",
            "history of con artists",
            # Wildcards
            "dreams that predicted the future", "coincidences too weird to be real",
            "things banned in other countries", "phobias with unpronounceable names",
            "world records that sound fake", "the science of optical illusions",
            "superstitions with real origins", "things that didn't exist 20 years ago",
            "urban legends debunked", "numbers with dark histories",
        ],
    },
    "hindi_myth": {
        "id": "hindi_myth",
        "label": "Hindi mythology & devotion Shorts (Ganesha → Shiva → … by IST day)",
        "topic_rotation": "myth",
        "language": "hi",
        "min_words": 100,
        # Edge TTS Hindi: Swara = warm female (common for katha / devotion). Override: hi-IN-MadhurNeural (male).
        "tts_voice": "hi-IN-SwaraNeural",
        "caption_font": "NotoSansDevanagari-Bold.ttf",
        "caption_font_name": "Noto Sans Devanagari",
        "yt_token_env": "YT_REFRESH_TOKEN_MYTH",
        "extra_yt_token_envs": ["YT_REFRESH_TOKEN_MYTH_2"],
        "groq_system_hint": (
            "You write respectful Hindi Shorts about Indian mythology, epics, and devotion — for a general audience. "
            "LANGUAGE: full_narration, youtube_title, youtube_description entirely in Devanagari Hindi. "
            "IMAGE PROMPTS: English only — cinematic scene descriptions (no text in image). "
            "CRITICAL LENGTH: full_narration 105-135 Devanagari words (~40-50 sec spoken). "
            "Tone: warm, storytelling, reverent — NOT mocking faith. Retell traditional narratives in your own words; "
            "do not copy long scripture passages. PG-13, no graphic gore, no hate toward any group. "
            "No hashtags in narration. The creator gives a specific story angle in the user message — stay on that topic."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", cinematic Indian mythology digital painting, golden hour lighting, rich jewel tones, "
            "detailed divine atmosphere, epic composition, respectful devotional art style, "
            "high quality illustration, no text, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "photorealistic human face close-up as real celebrity, gore, blood, horror jumpscare, "
            "disrespectful parody, political symbols, watermark, text, logo, blurry, low quality, "
            "multiple conflicting styles, broken anatomy"
        ),
        "topic_pool": [],
    },
    "kurukshetra_unboxing": {
        "id": "kurukshetra_unboxing",
        "label": "Premium mythological diorama unboxing Shorts",
        "language": "en",
        "min_words": 1,
        "tts_provider": "sfx",
        "tts_voice": "am_michael",
        "caption_font": "BebasNeue-Regular.ttf",
        "caption_font_name": "Bebas Neue",
        "yt_token_env": "YT_REFRESH_TOKEN",
        "groq_system_hint": (
            "You create original no-narration YouTube Shorts in the style of premium collectible unboxing "
            "and assembly videos. IMPORTANT: this is NOT a story video. No plot, no characters talking, "
            "no moral, no story arc, no spoken script, and no narration. The video should feel like: "
            "sealed box reveal, lid opening, foam tray close-up, parts laid out, hands assembling pieces, "
            "macro detail shots, light sweeps, transition beats, and final rotating showcase. "
            "The subject should be inspired by Indian epics, ancient warriors, battlefields, chariots, "
            "temples, divine weapons, and museum-quality miniatures, but every product, brand, set name, "
            "sculpt, and design must be fictional and original. Do not claim the collectible is real, rare, "
            "official, or available to buy. IMAGE PROMPTS must be English only and must describe vertical "
            "product/unboxing shots with no readable text. full_narration is only internal production notes "
            "for timing and sound effects; it will NOT be spoken."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", premium collectible product photography, cinematic tabletop unboxing, macro lens detail, "
            "dramatic studio lighting, realistic miniature diorama, ancient Indian epic aesthetic, "
            "rich gold and crimson accents balanced with neutral shadows, ultra detailed packaging and parts, "
            "professional vertical YouTube Shorts frame, no readable text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "real brand logo, readable text, watermark, signature, official merchandise, copied character design, "
            "celebrity likeness, gore, blood, nudity, low quality, blurry, distorted hands, broken anatomy, "
            "extra limbs, messy clutter, plastic toy cheap look"
        ),
        "topic_pool": [
            "a fictional Kurukshetra battlefield diorama with chariots, arrows, dust, and warrior standards",
            "a premium Arjuna-inspired archer miniature set with a celestial bow and battlefield base",
            "a Bhishma-inspired grand warrior diorama with silver armor, banners, and arrow details",
            "a Krishna-inspired chariot guide diorama with golden wheels and a glowing battlefield backdrop",
            "a mace-duel arena miniature inspired by epic warriors and cracked stone terrain",
            "a temple-forge collectible set showing divine weapons laid out in velvet trays",
            "a royal war-camp diorama with tents, flags, shields, and miniature oil lamps",
            "a conch-shell ceremony diorama with warriors preparing before an ancient battle",
            "a rain-soaked battlefield collector set with muddy terrain and broken chariot parts",
            "a sunrise command-table diorama with tiny maps, arrows, and carved wooden pieces",
            "a mythic elephant-armor miniature set with jeweled plates and battlefield accessories",
            "a palace training-yard diorama with bows, maces, shields, and stone archways",
            "a grand collector box containing six fictional epic-warrior miniatures",
            "a cinematic final-battle display base with dust clouds, banners, and dramatic shadows",
            "a limited-style handmade miniature set of ancient armor, helmets, and weapons",
        ],
    },
    "school_story": {
        "id": "school_story",
        "label": "School drama / storytime Short",
        "groq_system_hint": (
            "You write fictional school storytime Shorts. Tone: suspense + heart. "
            "Characters are original (no copyrighted names). Hook in line 1. "
            "Build to one memorable twist. Keep each kid-safe."
        ),
        "segment_count": 5,
        "topic_pool": [
            "the new kid nobody noticed",
            "a locker that wouldn't open",
            "a substitute teacher with a secret",
            "the lost lunchbox mystery",
            "a field trip gone strange",
            "the science fair disaster",
            "a friendship bracelet with a twist",
            "a school play that went wrong",
            "the detention room incident",
            "a letter passed in class",
        ],
    },
    "psych_tradeoff": {
        "id": "psych_tradeoff",
        "label": "Psychology / habits (non-clinical)",
        "groq_system_hint": (
            "You write Shorts about habits, motivation, and everyday psychology. "
            "Never diagnose or claim medical facts. Use 'some people' / 'research suggests' carefully. "
            "Practical tips only."
        ),
        "segment_count": 5,
        "topic_pool": [
            "why procrastination actually happens",
            "the 2-minute rule for habits",
            "why we care what strangers think",
            "how your morning sets your day",
            "the truth about motivation",
            "why boredom is good for you",
            "the psychology of saying no",
            "why small wins matter",
            "how overthinking actually hurts",
            "the real reason we scroll endlessly",
        ],
    },
    "history_micro": {
        "id": "history_micro",
        "label": "One moment in history",
        "groq_system_hint": (
            "You write one tight historical anecdote per Short. Pick public-domain or widely taught events. "
            "No graphic violence. End with why it matters in one line."
        ),
        "segment_count": 5,
        "topic_pool": [
            "a lesser-known ancient invention",
            "a moment that almost changed history",
            "an underrated figure from ancient times",
            "a coincidence that shaped a war",
            "a forgotten discovery at sea",
            "an ancient ruler's unexpected habit",
            "a medieval tradition nobody remembers",
            "a natural disaster that changed a city",
            "a lost city that was finally found",
            "an accidental scientific breakthrough",
        ],
    },
    "ghost_stories": {
        "id": "ghost_stories",
        "label": "Ghost / horror storytime Short",
        "min_words": 100,
        "tts_provider": "deapi",
        "tts_voice": "am_michael",
        "groq_system_hint": (
            "You write spooky ghost story Shorts for YouTube. "
            "CRITICAL LENGTH RULE: The TOTAL word count across ALL 6 segments MUST be 120-140 words. "
            "Each segment narration = 2-3 sentences, about 20-25 words per segment. "
            "This produces 35-45 seconds of audio when read aloud. "
            "Tone: eerie, suspenseful, creepy but NOT gory or violent. "
            "Segment 1: hook that stops scrolling. Last segment: chilling twist or unanswered question. "
            "All stories fictional. Original characters. PG-13. No hashtags in narration. "
            "Never use copyrighted characters, franchise names, celebrity likenesses, song lyrics, "
            "famous quotes, brand slogans, or recognizable plots from films, books, games, or shows. "
            "Do not present the story as a real event. Invent every name, place, object, and plot detail."
        ),
        "segment_count": 6,
        "image_style_suffix": (
            ", dark spooky cartoon illustration, eerie atmosphere, creepy stylized art, "
            "bold outlines, muted haunting colors, horror cartoon aesthetic, ghostly shadows, "
            "dramatic lighting, sinister mood, professional youtube thumbnail quality, "
            "no text, no captions, no watermark, no logos"
        ),
        "image_negative_prompt": (
            "photorealistic, photograph, happy cheerful bright, anime eyes, blurry, "
            "low quality, watermark, logo, text, title, signature, ugly, grainy, "
            "gore, blood, nudity, child-unsafe"
        ),
        "topic_pool": [
            "a ghost haunting an empty school at night",
            "a strange presence in a family home",
            "something unexplained during a picnic in the woods",
            "a ghost encounter at a friend's sleepover",
            "a haunted old cabin during a camping trip",
            "a ghost on a late-night train",
            "something wrong with the new neighbor's house",
            "a spirit in grandparents' attic",
            "an abandoned playground after dark",
            "a ghost at a roadside motel",
            "strange events at a wedding venue",
            "a haunted library after closing",
            "something watching from the forest edge",
            "a ghost during a blackout storm",
            "an eerie presence at a local hospital",
            "something in the basement nobody talks about",
            "a ghost on a deserted beach at night",
            "a haunted elevator in an old building",
            "a strange figure at a bus stop at 3 AM",
            "something whispering from an old well",
            "a ghost in a classroom after everyone left",
            "a haunted antique bought from a flea market",
            "a spirit tied to an old family photograph",
            "something in the fog on a mountain road",
            "a ghost at a summer camp",
        ],
    },
}


def list_channel_ids() -> list[str]:
    return sorted(PRESETS.keys())


def get_preset(channel_id: str) -> ChannelPreset:
    key = channel_id.strip().lower().replace("-", "_")
    if key not in PRESETS:
        raise KeyError(f"Unknown channel preset {channel_id!r}. Try: {', '.join(list_channel_ids())}")
    return PRESETS[key]
