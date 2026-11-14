#!/usr/bin/env python3
"""Course content + generator.

Writes site/content.js for the website and the lesson/reference notes into the
Obsidian vault. Existing notes are left alone unless --force is passed, so your
own edits in Obsidian are safe.

    python3 build.py           # build site content, create missing notes
    python3 build.py --force   # also overwrite lesson/reference notes
"""
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VAULT = HERE.parent / "Spanish"  # the Obsidian vault sits next to this folder

# The course is told through gossip: you're becoming the biggest chismoso/chismosa on the block, so every
# lesson is about people (who's here, who left, who's coming) and food (who ate what). Weeks are numbered
# by their order in COURSE; "id" is the stable key for PHOTOS, GRAMMAR and CYBER.
# Worksheet item: q = prompt, a = accepted answers, h = optional hint
# Quiz item: q = question, o = options, a = index of correct option, x = explanation
# chisme: (Spanish, English) gossip lines using the week's grammar; shown in the lesson and used for speaking practice.
COURSE = [
    {
        "id": "nouns", "phase": 1, "title": "People, Food & Gender",
        "goal": "Name the people and the food around you: the/a + noun + adjective, plurals, and subject pronouns.",
        "lesson": """
## Meet the neighbors — el barrio
Every lesson is gossip about the same people. Your job: become **el más chismoso** (or **la más chismosa**) del barrio — the one who knows everything.

| | |
|---|---|
| *doña Rosa* | the neighbor next door. She sees everything from her window. |
| *Marco y Lucía* | the couple in 3B. Are they fine? Nobody's sure. |
| *el tío Beto* | always eating. Always. |
| *Valeria* | used to live upstairs. Now… she's gone. Why? |
| *Javi* | the new guy. Nobody knows anything about him — yet. |

## Every noun has a gender
Spanish nouns are **masculine** or **feminine**, and the article (the/a) has to match.

| | Masculine | Feminine |
|---|---|---|
| the (singular) | el taco | la tortilla |
| the (plural) | los tacos | las tortillas |
| a / some | un vecino / unos vecinos | una vecina / unas vecinas |

**Rules of thumb:**
- Ending in **-o** → usually masculine: *el pollo, el queso, el hermano*
- Ending in **-a, -ción, -dad** → usually feminine: *la sopa, la fruta, la canción, la ciudad*
- Common exceptions: *el día, el mapa, el problema* (masculine) · *la mano, la foto* (feminine)
- Feminine words starting with a stressed **a-** take *el* in the singular: *el agua fría* (still feminine — note *fría*)

## People come in pairs
| | Man | Woman |
|---|---|---|
| neighbor | el vecino | la vecina |
| friend | el amigo | la amiga |
| boyfriend / girlfriend | el novio | la novia |
| brother / sister | el hermano | la hermana |
| uncle / aunt | el tío | la tía |
| gossip | el chismoso | la chismosa |

A mixed group uses the masculine plural: *los vecinos* = the neighbors (men and women).

## Making plurals
- Ends in a vowel → add **-s**: *taco → tacos*
- Ends in a consonant → add **-es**: *pan → panes*, *ciudad → ciudades*
- Ends in **-z** → change to **-ces**: *lápiz → lápices*, *pez → peces*

## Adjectives go after the noun and match it
*la sopa caliente* · *los tacos picantes* · *un vecino curioso* · *unas vecinas chismosas*

Adjectives ending in **-e** or a consonant only change for number: *el café grande, las tortillas grandes*.

## Subject pronouns (Latin American set)
| Singular | Plural |
|---|---|
| yo — I | nosotros / nosotras — we |
| tú — you (informal) | ustedes — you all (always, formal or not) |
| usted — you (formal) | ellos / ellas — they |
| él / ella — he / she | |

> In Latin America **ustedes** is used for every "you all." If a book or flashcard shows vosotros, skip it — it isn't used in Latin America.
""",
        "chisme": [("el chisme", "the gossip"), ("la vecina chismosa", "the gossipy neighbor"),
                   ("el novio nuevo", "the new boyfriend"), ("los tacos del tío Beto", "tío Beto's tacos"),
                   ("una pareja feliz… ¿o no?", "a happy couple… or not?")],
        "worksheet": [
            {"q": "___ tortilla (the)", "a": ["la"]},
            {"q": "___ pollo (the)", "a": ["el"]},
            {"q": "___ día (the) — careful, exception!", "a": ["el"]},
            {"q": "___ agua (the) — careful!", "a": ["el"]},
            {"q": "Make plural: el pan", "a": ["los panes"]},
            {"q": "Make plural: la vecina", "a": ["las vecinas"]},
            {"q": "Translate: the hot soup", "a": ["la sopa caliente"]},
            {"q": "Translate: a curious neighbor (man)", "a": ["un vecino curioso"]},
            {"q": "Translate: the girlfriend", "a": ["la novia"]},
            {"q": "Pronoun for \"you all\" in Latin America", "a": ["ustedes"]},
        ],
        "quiz": [
            {"q": "Which is correct?", "o": ["el problema", "la problema"], "a": 0,
             "x": "Many words ending in -ma come from Greek and are masculine: el problema, el sistema, el idioma."},
            {"q": "Where do most adjectives go?", "o": ["After the noun", "Before the noun"], "a": 0,
             "x": "la sopa caliente — the noun comes first, then the adjective."},
            {"q": "\"los vecinos\" can mean…", "o": ["the neighbors (a mixed group)", "only women neighbors", "one neighbor"], "a": 0,
             "x": "A mixed group uses the masculine plural."},
            {"q": "\"la chismosa\" is…", "o": ["the gossip (a woman)", "the gossip (a man)", "the story"], "a": 0,
             "x": "el chismoso / la chismosa = a person who gossips. el chisme = the gossip itself."},
            {"q": "\"unas tortillas\" means…", "o": ["some tortillas", "one tortilla", "the tortillas"], "a": 0,
             "x": "unos/unas = some."},
            {"q": "Plural of \"el pez\" (fish)", "o": ["los peces", "los pezes", "los pez"], "a": 0,
             "x": "Words ending in -z change the z to c before adding -es."},
            {"q": "\"___ agua está fría\"", "o": ["El", "La", "Los"], "a": 0,
             "x": "agua is feminine, but starts with a stressed a-, so it takes el in the singular. The adjective stays feminine: fría."},
            {"q": "\"los tacos picantes\" means…", "o": ["the spicy tacos", "the taco is spicy", "some spicy tacos"], "a": 0,
             "x": "los = the (masc. plural), and picantes matches tacos."},
        ],
        "practice": "Write 5 food phrases from your kitchen with article + adjective (*el queso blanco, las tortillas calientes…*) and describe 5 people you know with *el/la* + noun + adjective (*mi vecina curiosa, el tío simpático…*).",
    },
    {
        "id": "ser-estar", "phase": 1, "title": "Ser vs Estar — Who's Here, Who's Gone",
        "goal": "Choose between the two verbs for \"to be,\" and say who is here, there, or not here anymore.",
        "lesson": """
## Two verbs for "to be"
| Ser | Estar |
|---|---|
| yo **soy** | yo **estoy** |
| tú **eres** | tú **estás** |
| él/ella/usted **es** | él/ella/usted **está** |
| nosotros **somos** | nosotros **estamos** |
| ellos/ustedes **son** | ellos/ustedes **están** |

## SER — what someone IS
Think **DOCTOR**: **D**escription, **O**ccupation, **C**haracteristics, **T**ime, **O**rigin, **R**elationship.
- *Doña Rosa es muy chismosa.* — characteristic
- *Javi es de Colombia.* — origin
- *Lucía es doctora.* — occupation
- *Son las tres. Hoy es lunes.* — time & dates
- *Marco es el novio de Lucía.* — relationship
- *La fiesta es en mi casa.* — where an **event** takes place

## ESTAR — where someone is and how they are
Think **PLACE**: **P**osition, **L**ocation, **A**ction (-ando), **C**ondition, **E**motion.
- *¿Dónde está Marco?* — location
- *Lucía está enojada.* — emotion right now
- *El tío Beto está lleno.* — condition (full!)
- *La sopa está fría.* — condition

## Here, there, and over there
| | |
|---|---|
| *aquí* / *acá* | here (acá is very common in Latin America) |
| *ahí* | there (near you) |
| *allí* / *allá* | over there (far from both of us) |

- *Estoy aquí.* — I'm here.
- *¿Está Marco? — No, no está.* — Is Marco here? — No, he isn't. (Just *no está* = he's not in.)
- *Lucía está en casa.* — at home · *Javi está en el trabajo.* — at work
- *Valeria ya no está.* — Valeria isn't here anymore. (*ya no* = not anymore)
- *Todos están allá.* — Everyone's over there.

## Hay vs está
- **hay** = there is / there are (something exists): *Hay un chico nuevo en el edificio.*
- **está** = it's located (a specific, known thing): *El chico nuevo está en el 4A.*

## Same adjective, different meaning — food edition
| ser | estar |
|---|---|
| es rico — is rich (a person) | está rico — is tasty (food you're eating) |
| es aburrido — is boring | está aburrido — is bored |
| es listo — is clever | está listo — is ready |
| es malo — is bad (a bad person) | está malo — is sick / has gone bad |
""",
        "chisme": [("¿Dónde está Valeria? — Ya no está aquí.", "Where's Valeria? — She's not here anymore."),
                   ("Marco está aquí, pero Lucía no está.", "Marco is here, but Lucía isn't."),
                   ("Hay un chico nuevo en el edificio.", "There's a new guy in the building."),
                   ("Doña Rosa es muy chismosa.", "Doña Rosa is a big gossip."),
                   ("Lucía está enojada. ¿Por qué?", "Lucía is angry. Why?")],
        "worksheet": [
            {"q": "Yo ___ de Colombia.", "a": ["soy"]},
            {"q": "¿Dónde ___ Marco?", "a": ["está"]},
            {"q": "Doña Rosa ___ muy chismosa.", "a": ["es"]},
            {"q": "Lucía ___ enojada hoy.", "a": ["está"]},
            {"q": "Translate: She isn't here.", "a": ["no está", "ella no está", "no está aquí", "ella no está aquí", "no está acá", "ella no está acá"]},
            {"q": "Translate: Valeria isn't here anymore.", "a": ["valeria ya no está", "valeria ya no está aquí", "valeria ya no está acá"]},
            {"q": "___ un chico nuevo en el edificio. (there is)", "a": ["hay"]},
            {"q": "La sopa ___ fría.", "a": ["está"], "h": "temporary condition"},
            {"q": "Los tacos ___ ricos. (taste good)", "a": ["están"]},
            {"q": "Translate: over there (two ways)", "a": ["allá", "allí"]},
        ],
        "quiz": [
            {"q": "\"¿Está Marco?\" on the phone means…", "o": ["Is Marco there?", "Is Marco okay?", "Is it Marco?"], "a": 0,
             "x": "estar = location. No está = he's not in."},
            {"q": "\"Valeria ya no está\" means…", "o": ["Valeria isn't here anymore", "Valeria isn't ready", "Valeria is here already"], "a": 0,
             "x": "ya no = not anymore."},
            {"q": "\"There's a new neighbor\"", "o": ["Hay un vecino nuevo", "Está un vecino nuevo", "Es un vecino nuevo"], "a": 0,
             "x": "hay = there is (something exists)."},
            {"q": "\"The party is at my house\"", "o": ["La fiesta es en mi casa", "La fiesta está en mi casa"], "a": 0,
             "x": "Locations of EVENTS use ser. Locations of people and things use estar."},
            {"q": "\"La comida está rica\" means…", "o": ["The food is tasty", "The food is rich", "The food is expensive"], "a": 0,
             "x": "estar rico = tasty; ser rico = rich."},
            {"q": "\"acá\" means…", "o": ["here", "there", "over there"], "a": 0, "x": "acá = aquí, very common in Latin America."},
            {"q": "\"She's a gossip\" (a trait)", "o": ["Es chismosa", "Está chismosa"], "a": 0, "x": "Characteristics → ser."},
            {"q": "\"It's three o'clock\"", "o": ["Son las tres", "Están las tres", "Es las tres"], "a": 0,
             "x": "Time uses ser, and plural hours use son: son las tres (but es la una)."},
        ],
        "practice": "Write a roll call of 8 people you know: where each one **is** right now (*Mi mamá está en casa, mi amigo está allá…*), one with *ya no está*, and one thing each person **is** like (*es simpático, es chismosa…*).",
    },
    {
        "id": "present-regular", "phase": 1, "title": "Present Tense — Who Eats What",
        "goal": "Conjugate regular -ar, -er and -ir verbs, talk about meals, and make sentences negative.",
        "lesson": """
## Three verb families
Every infinitive ends in **-ar**, **-er** or **-ir**. Drop the ending, add the new one.

| | cocinar (cook) | comer (eat) | compartir (share) |
|---|---|---|---|
| yo | cocin**o** | com**o** | compart**o** |
| tú | cocin**as** | com**es** | compart**es** |
| él/ella/usted | cocin**a** | com**e** | compart**e** |
| nosotros | cocin**amos** | com**emos** | compart**imos** |
| ellos/ustedes | cocin**an** | com**en** | compart**en** |

> -er and -ir are identical except **nosotros**: comemos vs compartimos.

## The meals
| | noun | verb |
|---|---|---|
| breakfast | el desayuno | desayunar — *Desayuno a las siete.* |
| lunch | la comida / el almuerzo | comer — *Comemos a las dos.* |
| dinner | la cena | cenar — *Cenan muy tarde.* |
| snack | la merienda / el antojito | merendar |

## The present tense covers a lot
*Como* = I eat / I'm eating / I do eat. You don't need a separate "-ing" for most everyday sentences.

## Drop the pronoun
The ending already tells you who: *Cocino los domingos* is more natural than *Yo cocino los domingos*. Use the pronoun to point a finger — perfect for gossip: ***Él** no paga, **ella** paga.*

## Negatives
Put **no** right before the verb: *No como carne. Javi no cocina nunca.*

## Food and people verbs (all regular)
- **-ar:** cocinar, desayunar, cenar, tomar (to drink/take), preparar, comprar, pagar, probar*, llegar, hablar, llamar, esperar, mirar, escuchar
- **-er:** comer, beber, vender, leer, aprender, deber (should), creer (to believe)
- **-ir:** vivir, compartir, abrir, escribir, recibir, subir (to go up)

\\* *probar* changes its stem — that's week 5.
""",
        "chisme": [("El tío Beto come tres veces al día… y cena otra vez.", "Tío Beto eats three times a day… and has dinner again."),
                   ("Marco cocina, pero Lucía no come.", "Marco cooks, but Lucía doesn't eat."),
                   ("Javi vive solo y no cocina nunca.", "Javi lives alone and never cooks."),
                   ("¿Ellos comparten la comida? ¡Qué raro!", "They share their food? How weird!"),
                   ("Doña Rosa mira todo desde la ventana.", "Doña Rosa watches everything from the window.")],
        "worksheet": [
            {"q": "cocinar → yo", "a": ["cocino"]},
            {"q": "comer → tú", "a": ["comes"]},
            {"q": "compartir → nosotros", "a": ["compartimos"]},
            {"q": "cenar → ellos", "a": ["cenan"]},
            {"q": "beber → ella", "a": ["bebe"]},
            {"q": "vivir → ustedes", "a": ["viven"]},
            {"q": "Translate: I don't eat meat", "a": ["no como carne", "yo no como carne"]},
            {"q": "desayunar → nosotros", "a": ["desayunamos"]},
            {"q": "tomar → yo", "a": ["tomo"]},
            {"q": "Translate: Javi never cooks (\"Javi no ___ nunca\")", "a": ["cocina"]},
        ],
        "quiz": [
            {"q": "nosotros ending for -ir verbs", "o": ["-imos", "-emos", "-amos"], "a": 0, "x": "vivimos, compartimos."},
            {"q": "\"Cenamos tarde\" means…", "o": ["We have dinner late", "They have dinner late", "I had dinner late"], "a": 0, "x": "-amos = nosotros."},
            {"q": "\"Como tacos\" can mean…", "o": ["I eat / I'm eating tacos", "Only: I ate tacos"], "a": 0,
             "x": "The simple present covers ongoing actions too."},
            {"q": "¿Tú ___ en el 3B?", "o": ["vives", "vive", "vivo"], "a": 0, "x": "tú → -es for -ir verbs."},
            {"q": "\"Lucía doesn't eat\"", "o": ["Lucía no come", "Lucía come no", "No Lucía come"], "a": 0,
             "x": "no goes directly before the verb."},
            {"q": "\"el desayuno\" is…", "o": ["breakfast", "dinner", "dessert"], "a": 0, "x": "desayunar = to have breakfast (to \"un-fast\")."},
            {"q": "\"Ellos beben café\" means…", "o": ["They drink coffee", "You drink coffee", "He drinks coffee"], "a": 0, "x": "-en = ellos/ustedes."},
            {"q": "ustedes form of \"pagar\"", "o": ["pagan", "paguen", "pagamos"], "a": 0, "x": "-ar verbs: ustedes -an."},
        ],
        "practice": "Write 8–10 sentences about who eats what in your house or on your street: who cooks, who never cooks, who eats too much, who drinks coffee at night. Include at least two negative sentences.",
    },
    {
        "id": "irregulars", "phase": 1, "title": "Questions & Key Irregulars — Dicen que…",
        "goal": "Ask any gossip question and use tener, ir, venir, hacer and decir.",
        "lesson": """
## Question words (always with an accent)
| | |
|---|---|
| ¿Qué? — what | ¿Quién? / ¿Quiénes? — who |
| ¿Dónde? — where | ¿Adónde? — to where |
| ¿Cuándo? — when | ¿Por qué? — why |
| ¿Cómo? — how | ¿Cuál? / ¿Cuáles? — which / what |
| ¿Cuánto/a? — how much | ¿Cuántos/as? — how many |

- **¿Por qué?** (why) vs **porque** (because): *¿Por qué está enojada? — Porque Marco no cocina.*
- **¿Qué?** asks for a definition; **¿Cuál?** picks from options: *¿Cuál es su número?*
- The gossip's favorite: *¿Con quién?* — With whom?

## Five irregular verbs you'll use every day
| | tener | ir | venir | hacer | decir |
|---|---|---|---|---|---|
| yo | tengo | voy | vengo | hago | digo |
| tú | tienes | vas | vienes | haces | dices |
| él/ella/usted | tiene | va | viene | hace | dice |
| nosotros | tenemos | vamos | venimos | hacemos | decimos |
| ellos/ustedes | tienen | van | vienen | hacen | dicen |

## Coming and going: ir vs venir
- **ir** = to go (away from here): *Marco va al mercado.*
- **venir** = to come (toward here): *¿Viene Javi a la fiesta?*
- *ir a* + place: *Voy a la tienda.* · *a + el = al*: *Va al trabajo.*

## The gossip's verb: decir
- *Dicen que…* — They say that… / Word is…
- *¿Qué dice doña Rosa?* — What's doña Rosa saying?
- *No digo nada.* — I'm not saying anything.

## Tener expressions (where English uses "to be")
- *tengo hambre / sed* — I'm hungry / thirsty
- *tengo frío / calor* — I'm cold / hot
- *tengo sueño / miedo* — I'm sleepy / afraid
- *tiene razón* — she's right
- *tengo 30 años* — I'm 30 · *¿Cuántos años tiene Javi?*
- *tengo que* + infinitive — I have to: *Tengo que contarte algo.* (I have to tell you something.)
""",
        "chisme": [("Dicen que Javi tiene novia.", "Word is Javi has a girlfriend."),
                   ("¿Con quién va Lucía al cine?", "Who is Lucía going to the movies with?"),
                   ("¿Viene Valeria a la fiesta? — No, no viene.", "Is Valeria coming to the party? — No, she isn't."),
                   ("Tengo que contarte algo.", "I have to tell you something."),
                   ("¿Por qué no viene? — Porque tiene miedo.", "Why isn't she coming? — Because she's scared.")],
        "worksheet": [
            {"q": "tener → yo", "a": ["tengo"]},
            {"q": "venir → él", "a": ["viene"]},
            {"q": "decir → ellos", "a": ["dicen"]},
            {"q": "hacer → yo", "a": ["hago"]},
            {"q": "ir → nosotros", "a": ["vamos"]},
            {"q": "Translate: Word is… / They say that…", "a": ["dicen que"]},
            {"q": "Translate: I'm hungry", "a": ["tengo hambre", "yo tengo hambre"]},
            {"q": "Translate: With whom?", "a": ["con quién"]},
            {"q": "Translate: I have to tell you something", "a": ["tengo que contarte algo", "te tengo que contar algo"]},
            {"q": "venir → yo", "a": ["vengo"]},
        ],
        "quiz": [
            {"q": "\"Dicen que…\" means…", "o": ["They say that… / Word is…", "Tell me that…", "I said that…"], "a": 0,
             "x": "decir → dicen (ellos). The most useful gossip opener."},
            {"q": "Javi is coming here. Which verb?", "o": ["Viene", "Va"], "a": 0, "x": "venir = toward the speaker; ir = away."},
            {"q": "\"Tiene razón\" means…", "o": ["She's right", "She has a reason", "She's reasonable"], "a": 0, "x": "tener razón = to be right."},
            {"q": "\"because\" is…", "o": ["porque", "por qué", "porqué"], "a": 0, "x": "porque (one word, no accent) = because."},
            {"q": "decir → yo", "o": ["digo", "dico", "dizo"], "a": 0, "x": "Irregular yo: digo."},
            {"q": "\"Va al mercado\": why al?", "o": ["a + el = al", "It's a typo", "al means \"the\""], "a": 0, "x": "a + el always contracts to al."},
            {"q": "\"¿Cuántos años tiene?\" asks…", "o": ["How old is he/she?", "How many years has it been?", "What year is it?"], "a": 0,
             "x": "Age uses tener."},
            {"q": "\"How many cousins?\"", "o": ["¿Cuántas primas?", "¿Cuántos primas?", "¿Cuánta primas?"], "a": 0,
             "x": "cuánto matches the noun: primas is feminine plural → cuántas."},
        ],
        "practice": "Write 8 gossip questions about someone new on your street (use 6 different question words: *¿Quién es? ¿De dónde viene? ¿Con quién vive?…*). Then answer them with *Dicen que…*.",
    },
    {
        "id": "stem-changers", "phase": 1, "title": "Stem-Changers — At the Restaurant",
        "goal": "Recognize and conjugate e→ie, o→ue and e→i verbs while ordering, eating and paying.",
        "lesson": """
## The \"boot\" verbs
Some verbs change a vowel in the stem — in every form **except nosotros**. Draw the table and the changing forms make a boot shape.

| | e → ie: querer | o → ue: almorzar | e → i: pedir |
|---|---|---|---|
| yo | qu**ie**ro | alm**ue**rzo | p**i**do |
| tú | qu**ie**res | alm**ue**rzas | p**i**des |
| él/ella/usted | qu**ie**re | alm**ue**rza | p**i**de |
| nosotros | queremos | almorzamos | pedimos |
| ellos/ustedes | qu**ie**ren | alm**ue**rzan | p**i**den |

## At the restaurant
- **e → ie:** querer, preferir, pensar, empezar, entender, cerrar
- **o → ue:** poder, almorzar, probar (to taste/try), costar, volver (to come back), dormir, recordar
- **e → i:** pedir (to order), servir (to serve), repetir (to have seconds!), seguir
- **u → ue:** jugar (the only one): *juego, juegas, juega, jugamos, juegan*

## Phrases
- *¿Qué pides?* — What are you ordering?
- *Quiero los tacos, por favor.* — I'd like the tacos, please.
- *¿Puedo probar?* — Can I try some?
- *¿Cuánto cuesta?* — How much is it?
- *La cuenta, por favor.* — The check, please.
- *Siempre pide lo mismo.* — She always orders the same thing.

## Watch these
- **pedir** = to ask *for* / order · **preguntar** = to ask a question
- **volver** = to come back: *Marco vuelve a las diez.*
""",
        "chisme": [("Lucía siempre pide lo mismo.", "Lucía always orders the same thing."),
                   ("El tío Beto repite tres veces.", "Tío Beto goes back for seconds three times."),
                   ("Marco no puede pagar. ¡Otra vez!", "Marco can't pay. Again!"),
                   ("Javi prefiere comer solo. ¿Por qué será?", "Javi prefers to eat alone. Why could that be?"),
                   ("Ellos vuelven muy tarde.", "They come back really late.")],
        "worksheet": [
            {"q": "querer → yo", "a": ["quiero"]},
            {"q": "pedir → ella", "a": ["pide"]},
            {"q": "poder → nosotros", "a": ["podemos"]},
            {"q": "almorzar → yo", "a": ["almuerzo"]},
            {"q": "volver → ustedes", "a": ["vuelven"]},
            {"q": "preferir → tú", "a": ["prefieres"]},
            {"q": "servir → el mesero", "a": ["sirve"]},
            {"q": "costar → it (\"¿Cuánto ___?\")", "a": ["cuesta"]},
            {"q": "probar → yo", "a": ["pruebo"]},
            {"q": "Translate: The check, please.", "a": ["la cuenta, por favor", "la cuenta por favor"]},
        ],
        "quiz": [
            {"q": "Which form does NOT change its stem?", "o": ["nosotros", "yo", "ellos"], "a": 0, "x": "nosotros sits outside the boot."},
            {"q": "\"¿Qué pides?\" means…", "o": ["What are you ordering?", "What are you asking?", "What do you want to say?"], "a": 0, "x": "pedir = to order / ask for."},
            {"q": "\"I order the soup\"", "o": ["Pido la sopa", "Pregunto la sopa"], "a": 0, "x": "pedir = request something."},
            {"q": "\"¿Puedo probar?\" means…", "o": ["Can I try some?", "Can I prove it?", "Can I pay?"], "a": 0, "x": "probar o→ue = to taste/try."},
            {"q": "almorzar → yo", "o": ["almuerzo", "almorzo", "almuerza"], "a": 0, "x": "o→ue."},
            {"q": "\"Repite\" at dinner means…", "o": ["He has seconds", "He repeats the order", "He returns"], "a": 0, "x": "repetir = repeat — also going back for more food."},
            {"q": "\"Marco vuelve a las diez\" means…", "o": ["Marco comes back at ten", "Marco leaves at ten", "Marco turns around at ten"], "a": 0, "x": "volver o→ue = to return."},
            {"q": "Which verb changes u → ue?", "o": ["jugar", "usar", "buscar"], "a": 0, "x": "jugar is the only one."},
        ],
        "practice": "Write a restaurant scene with your friends or family in 8 sentences: who orders what (*pide*), who wants to try everything (*quiere probar*), who can't pay (*no puede*), who has seconds (*repite*).",
    },
    {
        "id": "gustar", "phase": 1, "title": "Gustar — Who Likes What (and Whom)",
        "goal": "Talk about food you like and people you like (or don't) with gustar, encantar and caer bien/mal.",
        "lesson": """
## Why "me gusta" is backwards
*Me gusta el café* literally means **"Coffee is pleasing to me."** The thing you like is the subject — so the verb matches **the thing**, not you.

- *Me gust**a** el mole.* — one thing → gusta
- *Me gust**an** los tamales.* — plural things → gustan
- *Me gust**a** cocinar.* — activities (infinitives) → always gusta

## Who is pleased
| | |
|---|---|
| me gusta — I like | nos gusta — we like |
| te gusta — you like | les gusta — they / you all like |
| le gusta — he / she / you (usted) like(s) | |

**Clarify or emphasize with "a":** *A Lucía le gusta el picante. A Marco no. A mí me encanta.*

## Same pattern
- **encantar** — to love (things): *Me encantan las enchiladas.*
- **molestar** — to bother: *A doña Rosa le molesta el ruido.*
- **importar** — to matter: *No me importa.* (I don't care)
- **faltar** — to be missing: *A la sopa le falta sal.*
- **doler (o→ue)** — to hurt: *Me duele el estómago.* (too many tacos)

## The gossip's secret weapon: caer bien / caer mal
For **people**, Spanish speakers usually say *caer bien* (to come across well) instead of *gustar*:
- *Javi me cae bien.* — I like Javi.
- *A doña Rosa no le cae bien Javi.* — Doña Rosa doesn't like Javi.
- *Me caen mal los vecinos del 2C.* — I don't like the neighbors in 2C.

> *Me gusta Javi* sounds romantic — it means you're attracted to him! Use *me cae bien* for "I like him (as a person)."

> Never say ~~Yo gusto la pizza~~ — that means "I am pleasing (to) the pizza."
""",
        "chisme": [("A doña Rosa no le cae bien Javi.", "Doña Rosa doesn't like Javi."),
                   ("¿Te cae bien el novio de Lucía?", "Do you like Lucía's boyfriend?"),
                   ("A Lucía le gusta Javi… ¡Ay, no!", "Lucía has a crush on Javi… Oh no!"),
                   ("Al tío Beto le encantan los tamales.", "Tío Beto loves tamales."),
                   ("No me importa… bueno, un poquito.", "I don't care… well, a little.")],
        "worksheet": [
            {"q": "Translate: I like coffee", "a": ["me gusta el café"]},
            {"q": "Translate: I like tamales", "a": ["me gustan los tamales"]},
            {"q": "Translate: She likes to cook", "a": ["le gusta cocinar", "a ella le gusta cocinar"]},
            {"q": "Translate: We love enchiladas (encantar)", "a": ["nos encantan las enchiladas"]},
            {"q": "Translate: My stomach hurts", "a": ["me duele el estómago"]},
            {"q": "Translate: I like Javi (as a person)", "a": ["javi me cae bien", "me cae bien javi"]},
            {"q": "Translate: They don't like him (as a person)", "a": ["no les cae bien", "les cae mal"]},
            {"q": "Translate: The soup needs salt (faltar)", "a": ["a la sopa le falta sal", "le falta sal a la sopa", "le falta sal"]},
            {"q": "A Marco le ___ los tacos. (gustar)", "a": ["gustan"]},
            {"q": "Translate: I don't care", "a": ["no me importa"]},
        ],
        "quiz": [
            {"q": "Why \"gustan\" in \"Me gustan los tamales\"?", "o": ["Because los tamales (plural) is the subject", "Because I like more than one", "It's a typo"], "a": 0,
             "x": "The thing liked is the grammatical subject, and it's plural."},
            {"q": "\"Me gusta Javi\" suggests…", "o": ["You're attracted to Javi", "You think Javi is a nice guy", "Javi likes you"], "a": 0,
             "x": "For people, gustar sounds romantic. Use caer bien for \"I like him as a person.\""},
            {"q": "\"Javi me cae mal\" means…", "o": ["I don't like Javi", "Javi falls on me", "Javi doesn't like me"], "a": 0, "x": "caer mal = to come across badly."},
            {"q": "Which is WRONG?", "o": ["Yo gusto la pizza", "Me gusta la pizza", "A mí me gusta la pizza"], "a": 0, "x": "Yo gusto means \"I am pleasing.\""},
            {"q": "In \"A Lucía le gusta\", what does \"a Lucía\" do?", "o": ["Clarifies who \"le\" is", "Replaces \"le\"", "Makes it past tense"], "a": 0,
             "x": "le could be anyone — a Lucía makes it clear. You still need le."},
            {"q": "\"Les gusta\" can mean…", "o": ["They like or you all like", "Only they like", "He likes"], "a": 0, "x": "les covers ellos, ellas and ustedes."},
            {"q": "\"I like to cook and eat\"", "o": ["Me gusta cocinar y comer", "Me gustan cocinar y comer"], "a": 0, "x": "Infinitives always take singular gusta."},
            {"q": "\"A la sopa le falta sal\" means…", "o": ["The soup needs salt", "The soup has too much salt", "The salt is missing the soup"], "a": 0, "x": "faltar = to be lacking/missing."},
        ],
        "practice": "Write your food opinions: 4 things you like (*me gusta/gustan*), 2 you love (*me encanta*), 1 dish that's missing something (*le falta…*). Then gossip: 3 people who *te caen bien*, 1 who *te cae mal*, and what your best friend likes (*A [name] le gusta…*).",
    },
    {
        "id": "progressive", "phase": 1, "title": "Right Now — Estar + -ando",
        "goal": "Say what's happening at this very moment: estar + -ando / -iendo.",
        "lesson": """
## Happening right now
**estar** (conjugated) + the **-ando / -iendo** form:

| | |
|---|---|
| hablar → habl**ando** | *Estoy hablando.* — I'm talking. |
| comer → com**iendo** | *Estás comiendo.* — You're eating. |
| salir → sal**iendo** | *Está saliendo.* — She's going out. |

| estar | + gerund |
|---|---|
| estoy | cocinando |
| estás | comiendo |
| está | hablando |
| estamos | esperando |
| están | escribiendo |

## Irregular -ing forms
- Vowel + -iendo becomes **-yendo**: *leer → leyendo, traer → trayendo, oír → oyendo, ir → yendo*
- -ir stem-changers change in the gerund too: *pedir → pidiendo, servir → sirviendo, decir → diciendo, dormir → durmiendo, venir → viniendo*

## When to use it
Spanish uses the progressive only for **right now, in progress**:
- *¿Qué estás haciendo? — Estoy cenando.* — What are you doing? — I'm having dinner.
- *Javi está hablando con Lucía.* — Javi is talking to Lucía (at this moment).

But NOT for plans — English "I'm going out tonight" is *Salgo esta noche* (or *Voy a salir*), never ~~Estoy saliendo esta noche~~.

> Exception that gossips love: *Están saliendo* also means "They're dating."

## Phrases
- *¿Qué está pasando?* — What's going on?
- *¿Me estás escuchando?* — Are you listening to me?
- *Estoy esperando.* — I'm waiting.
""",
        "chisme": [("¿Qué está haciendo Javi? — Está hablando con Lucía… otra vez.", "What's Javi doing? — He's talking with Lucía… again."),
                   ("Doña Rosa está mirando por la ventana.", "Doña Rosa is looking out the window."),
                   ("El tío Beto está comiendo. ¡Qué sorpresa!", "Tío Beto is eating. What a surprise!"),
                   ("¿Están saliendo? — ¡No sé!", "Are they dating? — I don't know!"),
                   ("¿Qué está pasando aquí?", "What's going on here?")],
        "worksheet": [
            {"q": "hablar → -ando form", "a": ["hablando"]},
            {"q": "comer → -iendo form", "a": ["comiendo"]},
            {"q": "leer → -ing form", "a": ["leyendo"]},
            {"q": "pedir → -ing form", "a": ["pidiendo"]},
            {"q": "dormir → -ing form", "a": ["durmiendo"]},
            {"q": "decir → -ing form", "a": ["diciendo"]},
            {"q": "Translate: I'm cooking.", "a": ["estoy cocinando", "yo estoy cocinando"]},
            {"q": "Translate: They're eating.", "a": ["están comiendo", "ellos están comiendo", "ellas están comiendo"]},
            {"q": "Translate: What's going on?", "a": ["qué está pasando", "qué pasa"]},
            {"q": "Translate: What are you doing? (tú)", "a": ["qué estás haciendo", "qué haces"]},
        ],
        "quiz": [
            {"q": "\"Está durmiendo\" means…", "o": ["He's sleeping", "He's going to sleep", "He slept"], "a": 0, "x": "dormir → durmiendo (o→u in the gerund)."},
            {"q": "Gerund of \"leer\"", "o": ["leyendo", "leiendo", "leendo"], "a": 0, "x": "Vowel + iendo → yendo."},
            {"q": "\"I'm going out tonight\" (a plan)", "o": ["Salgo esta noche", "Estoy saliendo esta noche"], "a": 0,
             "x": "The progressive is only for what's happening right now, not plans."},
            {"q": "\"Están saliendo\" can mean…", "o": ["They're dating", "They're arriving", "They're tired"], "a": 0, "x": "salir (con) = to go out with / date."},
            {"q": "Which verb do you conjugate?", "o": ["estar", "ser", "the main verb"], "a": 0, "x": "estar + gerund. The gerund never changes."},
            {"q": "\"¿Me estás escuchando?\" means…", "o": ["Are you listening to me?", "Do you hear me?", "Will you listen?"], "a": 0, "x": "In progress right now."},
            {"q": "Gerund of \"servir\"", "o": ["sirviendo", "serviendo", "sirvando"], "a": 0, "x": "e→i stem-changers: sirviendo, pidiendo, diciendo."},
            {"q": "nosotros + esperar, right now", "o": ["Estamos esperando", "Somos esperando", "Estamos esperamos"], "a": 0, "x": "estar (estamos) + gerund."},
        ],
        "practice": "Look out your window (or around your house) for 5 minutes and narrate like doña Rosa: 8 sentences about what people are doing **right now** (*El vecino está lavando el carro. Mi hermana está durmiendo…*).",
    },
    {
        "id": "coming-going", "phase": 1, "title": "Coming, Going & Staying — Me voy",
        "goal": "Say who's arriving, leaving and staying, and use reflexive verbs for your routine.",
        "lesson": """
## Reflexive verbs — actions you do to yourself
The pronoun matches the subject and goes **before** the verb:

| levantarse (to get up) | |
|---|---|
| me levanto | nos levantamos |
| te levantas | se levantan |
| se levanta | |

Routine: *despertarse (e→ie), levantarse, ducharse, vestirse (e→i), arreglarse (to get ready), acostarse (o→ue)*.
Body parts use **el/la**, not *mi*: *Me lavo **las** manos.*

## ir vs irse — going vs leaving
- **ir** = to go somewhere: *Voy al mercado.*
- **irse** = to leave, to take off: *Me voy.* — I'm leaving. *¿Ya te vas?* — You're leaving already?
- *Se va de la ciudad.* — She's leaving town.

## The arrivals and departures board
| | |
|---|---|
| llegar — to arrive | *Javi llega a las ocho.* |
| salir — to go out / leave (a place) | *Salgo de casa a las siete.* (yo: **salgo**) |
| irse — to leave / take off | *Nos vamos.* |
| quedarse — to stay | *Me quedo un rato más.* — I'll stay a bit longer. |
| volver / regresar — to come back | *Vuelve el lunes.* |
| venir — to come | *¿Vienes?* |

## Classic goodbye lines
- *Bueno, me voy.* — Well, I'm off.
- *¿Por qué no te quedas?* — Why don't you stay?
- *Nos vemos.* — See you.
- *Ya me tengo que ir.* — I have to go now.
""",
        "chisme": [("¿Ya te vas? ¡Pero la fiesta está empezando!", "You're leaving already? But the party is starting!"),
                   ("Marco siempre se va temprano. ¿Adónde va?", "Marco always leaves early. Where's he going?"),
                   ("Javi se queda en casa de Lucía.", "Javi is staying at Lucía's place."),
                   ("Valeria se va de la ciudad.", "Valeria is leaving town."),
                   ("Doña Rosa nunca sale, pero sabe todo.", "Doña Rosa never goes out, but she knows everything.")],
        "worksheet": [
            {"q": "levantarse → yo", "a": ["me levanto"]},
            {"q": "irse → yo", "a": ["me voy"]},
            {"q": "irse → tú", "a": ["te vas"]},
            {"q": "quedarse → nosotros", "a": ["nos quedamos"]},
            {"q": "salir → yo", "a": ["salgo"]},
            {"q": "Translate: You're leaving already? (tú)", "a": ["ya te vas", "te vas ya"]},
            {"q": "Translate: I'm staying.", "a": ["me quedo", "yo me quedo"]},
            {"q": "Translate: She's leaving town.", "a": ["se va de la ciudad", "ella se va de la ciudad"]},
            {"q": "acostarse → ellos", "a": ["se acuestan"]},
            {"q": "Translate: I wash my hands.", "a": ["me lavo las manos"]},
        ],
        "quiz": [
            {"q": "\"Me voy\" means…", "o": ["I'm leaving", "I'm going to", "I see myself"], "a": 0, "x": "irse = to leave."},
            {"q": "\"Voy al mercado\" vs \"Me voy\"", "o": ["going somewhere vs leaving", "same meaning", "past vs present"], "a": 0, "x": "ir = go to a place; irse = take off."},
            {"q": "\"Me quedo\" means…", "o": ["I'm staying", "I'm quiet", "I complain"], "a": 0, "x": "quedarse = to stay."},
            {"q": "salir → yo", "o": ["salgo", "salo", "sallo"], "a": 0, "x": "Irregular yo like tengo, vengo, hago."},
            {"q": "\"I wash my hands\"", "o": ["Me lavo las manos", "Lavo mis manos", "Me lavo mis manos"], "a": 0, "x": "Reflexive + definite article for body parts."},
            {"q": "Where does the reflexive pronoun go?", "o": ["Before the conjugated verb", "After the verb", "At the end"], "a": 0, "x": "Me levanto, not Levanto me."},
            {"q": "\"Nos vemos\" means…", "o": ["See you", "We see us", "We saw"], "a": 0, "x": "We'll see each other."},
            {"q": "\"Vuelve el lunes\" means…", "o": ["She's coming back on Monday", "She leaves on Monday", "She turns on Monday"], "a": 0, "x": "volver = to come back."},
        ],
        "practice": "Write your daily routine in 8 sentences with reflexive verbs (*Me despierto, me levanto…*). Then write a party scene: who arrives (*llega*), who leaves early (*se va*), who stays until the end (*se queda*).",
    },
    {
        "id": "ir-a", "phase": 2, "title": "Going To — Va a pasar algo",
        "goal": "Talk about plans and predictions with ir a + infinitive.",
        "lesson": """
## The everyday future: ir + a + infinitive
| ir | + a + infinitive |
|---|---|
| voy | a comer |
| vas | a cocinar |
| va | a llegar |
| vamos | a salir |
| van | a ver |

*Voy a cocinar.* — I'm going to cook. *Van a llegar tarde.* — They're going to arrive late.

This is how most people talk about the future in everyday Latin American Spanish.

## Don't drop the "a"
*Voy **a** comer*, never ~~Voy comer~~. And the second verb stays in the infinitive: never ~~Voy a como~~.

## Future time words
| | |
|---|---|
| *hoy* | today |
| *esta noche* | tonight |
| *mañana* | tomorrow |
| *pasado mañana* | the day after tomorrow |
| *este fin de semana* | this weekend |
| *la próxima semana* / *la semana que viene* | next week |
| *el próximo año* | next year |
| *pronto* | soon |
| *más tarde* | later |

## Predictions
- *Va a llover.* — It's going to rain.
- *Va a haber una fiesta.* — There's going to be a party. (*hay* → *va a haber*)
- *¡Se va a enojar!* — She's going to get angry! (pronoun before *va*, or attached: *Va a enojarse.*)

## Other ways to talk about plans
- *pensar* + infinitive — to plan to: *Pienso cocinar mole.*
- *tener que* + infinitive — to have to: *Tengo que comprar tortillas.*
- *querer* + infinitive — to want to: *Quiero saber todo.*
""",
        "chisme": [("No vas a creer lo que dicen.", "You're not going to believe what they're saying."),
                   ("Van a romper. ¡Estoy seguro!", "They're going to break up. I'm sure!"),
                   ("Marco va a cocinar para Lucía esta noche.", "Marco is going to cook for Lucía tonight."),
                   ("Va a haber una fiesta en el 4A.", "There's going to be a party in 4A."),
                   ("Doña Rosa se va a enterar de todo.", "Doña Rosa is going to find out about everything.")],
        "worksheet": [
            {"q": "Translate: I'm going to eat.", "a": ["voy a comer", "yo voy a comer"]},
            {"q": "Translate: We're going to cook.", "a": ["vamos a cocinar", "nosotros vamos a cocinar"]},
            {"q": "Translate: They're going to arrive late.", "a": ["van a llegar tarde", "ellos van a llegar tarde"]},
            {"q": "Translate: It's going to rain.", "a": ["va a llover"]},
            {"q": "Translate: There's going to be a party.", "a": ["va a haber una fiesta"]},
            {"q": "Translate: tomorrow", "a": ["mañana"]},
            {"q": "Translate: next week", "a": ["la próxima semana", "la semana que viene"]},
            {"q": "Translate: Are you going to come? (tú)", "a": ["vas a venir"]},
            {"q": "Translate: I have to buy tortillas.", "a": ["tengo que comprar tortillas"]},
            {"q": "Javi ___ a salir con Lucía. (ir)", "a": ["va"]},
        ],
        "quiz": [
            {"q": "\"I'm going to eat\"", "o": ["Voy a comer", "Voy comer", "Voy a como"], "a": 0, "x": "ir + a + infinitive."},
            {"q": "\"Va a haber\" means…", "o": ["There's going to be", "He's going to have", "There was"], "a": 0, "x": "hay → va a haber."},
            {"q": "\"pasado mañana\" is…", "o": ["the day after tomorrow", "yesterday", "tomorrow morning"], "a": 0, "x": "pasado = past, mañana = tomorrow → after tomorrow."},
            {"q": "Which verb changes for the person?", "o": ["ir", "the infinitive", "both"], "a": 0, "x": "Only ir is conjugated: voy, vas, va…"},
            {"q": "\"Pienso cocinar\" means…", "o": ["I plan to cook", "I think I cook", "I thought about cooking"], "a": 0, "x": "pensar + infinitive = to plan to."},
            {"q": "\"Se va a enojar\" means…", "o": ["She's going to get angry", "She's leaving angry", "She got angry"], "a": 0, "x": "The pronoun can go before va."},
            {"q": "\"Van a romper\" (gossip) means…", "o": ["They're going to break up", "They're going to break it", "They broke up"], "a": 0, "x": "romper (con) = to break up."},
            {"q": "\"la semana que viene\" means…", "o": ["next week", "last week", "this week"], "a": 0, "x": "Literally \"the week that's coming.\""},
        ],
        "practice": "Make 8 predictions about the people around you for this weekend with *va a / van a* (*Mi hermano va a dormir todo el día. Mis vecinos van a hacer una fiesta…*). Then write 3 of your own plans with *voy a* and *tengo que*.",
    },
    {
        "id": "future", "phase": 2, "title": "The Future — ¿Qué pasará?",
        "goal": "Use the simple future (comeré, vendrá) and the \"I wonder…\" future of probability.",
        "lesson": """
## Simple future: add endings to the WHOLE infinitive
One set of endings for all three families:

| | comer |
|---|---|
| yo | comer**é** |
| tú | comer**ás** |
| él/ella/usted | comer**á** |
| nosotros | comer**emos** |
| ellos/ustedes | comer**án** |

*Mañana cocinaré.* — Tomorrow I'll cook. *Llegarán el lunes.* — They'll arrive on Monday.

## Irregular stems (same endings)
| infinitive | stem | example |
|---|---|---|
| tener | **tendr-** | *tendré* |
| venir | **vendr-** | *vendrá* |
| salir | **saldr-** | *saldremos* |
| poner | **pondr-** | *pondrás* |
| poder | **podr-** | *podrán* |
| saber | **sabr-** | *sabré* |
| haber | **habr-** | *habrá* — there will be |
| hacer | **har-** | *haré* |
| decir | **dir-** | *dirá* |
| querer | **querr-** | *querrá* |

## Simple future vs ir a
- **ir a** — everyday plans, what's about to happen: *Voy a comer.*
- **simple future** — promises, predictions, a bit more formal or distant: *Te llamaré. Algún día lo sabremos.*

## The gossip's favorite: the "I wonder…" future
The future also expresses a **guess about right now**:
- *¿Dónde estará Valeria?* — I wonder where Valeria is. / Where could she be?
- *Estará en casa.* — She's probably at home.
- *¿Quién será?* — Who could that be? (doorbell rings)
- *¿Estarán saliendo?* — Could they be dating?
- *Tendrá unos treinta años.* — He must be about thirty.
""",
        "chisme": [("¿Dónde estará Valeria?", "I wonder where Valeria is."),
                   ("¿Quién será el chico nuevo?", "Who could the new guy be?"),
                   ("¿Estarán saliendo Javi y Lucía?", "Could Javi and Lucía be dating?"),
                   ("Tendrá unos treinta años.", "He must be about thirty."),
                   ("Algún día lo sabremos todo.", "Someday we'll know everything.")],
        "worksheet": [
            {"q": "comer → yo (future)", "a": ["comeré"]},
            {"q": "llegar → ellos (future)", "a": ["llegarán"]},
            {"q": "vivir → nosotros (future)", "a": ["viviremos"]},
            {"q": "tener → yo (future)", "a": ["tendré"]},
            {"q": "venir → ella (future)", "a": ["vendrá"]},
            {"q": "hacer → tú (future)", "a": ["harás"]},
            {"q": "decir → él (future)", "a": ["dirá"]},
            {"q": "haber → \"there will be\"", "a": ["habrá"]},
            {"q": "Translate: I wonder where she is.", "a": ["dónde estará"]},
            {"q": "Translate: Who could it be?", "a": ["quién será"]},
        ],
        "quiz": [
            {"q": "The future endings attach to…", "o": ["the whole infinitive", "the yo stem", "the preterite"], "a": 0, "x": "comer + é = comeré."},
            {"q": "venir → yo (future)", "o": ["vendré", "veniré", "vengré"], "a": 0, "x": "Irregular stem vendr-."},
            {"q": "\"¿Dónde estará Valeria?\" means…", "o": ["I wonder where Valeria is", "Where will Valeria be?", "Both — context decides"], "a": 2,
             "x": "The future can be a real future or a guess about now. In gossip, it's usually the guess."},
            {"q": "\"Habrá una fiesta\" means…", "o": ["There will be a party", "There was a party", "She'll have a party"], "a": 0, "x": "haber → habrá."},
            {"q": "hacer → nosotros (future)", "o": ["haremos", "haceremos", "hacemos"], "a": 0, "x": "Irregular stem har-."},
            {"q": "\"Tendrá treinta años\" means…", "o": ["He's probably thirty", "He was thirty", "He has thirty years left"], "a": 0, "x": "Future of probability."},
            {"q": "Which ending has NO accent?", "o": ["-emos", "-é", "-án"], "a": 0, "x": "comeré, comerás, comerá, comeremos, comerán."},
            {"q": "decir → ellos (future)", "o": ["dirán", "decirán", "dicerán"], "a": 0, "x": "Irregular stem dir-."},
        ],
        "practice": "Write 5 promises for next year with the simple future (*Cocinaré más. Llamaré a mi abuela…*). Then gossip: 5 \"I wonder…\" sentences about people you know (*¿Dónde estará…? ¿Tendrá novia? Estará cansado…*).",
    },
    {
        "id": "preterite", "phase": 3, "title": "Preterite — ¿Qué pasó?",
        "goal": "Tell what happened: regular preterite verbs for meals, arrivals and departures.",
        "lesson": """
## Regular preterite endings
| | cocinar | comer | salir |
|---|---|---|---|
| yo | cocin**é** | com**í** | sal**í** |
| tú | cocin**aste** | com**iste** | sal**iste** |
| él/ella/usted | cocin**ó** | com**ió** | sal**ió** |
| nosotros | cocin**amos** | com**imos** | sal**imos** |
| ellos/ustedes | cocin**aron** | com**ieron** | sal**ieron** |

> Accents matter: *cocino* = I cook, *cocinó* = he cooked. *llego* = I arrive, *llegó* = she arrived.
> -ar and -ir nosotros forms look like the present (*cocinamos, salimos*) — context tells you.

## Spelling changes in the yo form
- -car → **-qué**: buscar → busqué, sacar → saqué
- -gar → **-gué**: llegar → llegué, pagar → pagué
- -zar → **-cé**: almorzar → almorcé, empezar → empecé

## Leer, creer, oír: i → y
*leyó, leyeron* · *creyó* · *oyó* — *¿Oíste? Doña Rosa oyó todo.*

## Signal words
*ayer* (yesterday) · *anoche* (last night) · *anteayer* (the day before yesterday) · *la semana pasada* · *el año pasado* · *hace dos días* (two days ago) · *una vez* (once) · *de repente* (suddenly)

## The gossip's opener
- *¿Qué pasó?* — What happened?
- *¿Viste…?* — Did you see…?
- *¿Oíste…?* — Did you hear…?

> In Latin America the preterite is used for recent things too: *¿Ya comiste?* (Did you eat yet?)
""",
        "chisme": [("¿Viste? Javi llegó a las tres de la mañana.", "Did you see? Javi got home at three in the morning."),
                   ("El tío Beto comió todos los tamales.", "Tío Beto ate all the tamales."),
                   ("Anoche Marco y Lucía salieron juntos.", "Last night Marco and Lucía went out together."),
                   ("¿Qué pasó? — Lucía no contestó.", "What happened? — Lucía didn't answer."),
                   ("Doña Rosa oyó todo.", "Doña Rosa heard everything.")],
        "worksheet": [
            {"q": "cocinar → yo (preterite)", "a": ["cociné"]},
            {"q": "comer → ella (preterite)", "a": ["comió"]},
            {"q": "salir → ellos (preterite)", "a": ["salieron"]},
            {"q": "llegar → yo (preterite)", "a": ["llegué"]},
            {"q": "pagar → yo (preterite)", "a": ["pagué"]},
            {"q": "almorzar → yo (preterite)", "a": ["almorcé"]},
            {"q": "oír → él (preterite)", "a": ["oyó"]},
            {"q": "Translate: What happened?", "a": ["qué pasó"]},
            {"q": "Translate: Last night I ate tacos.", "a": ["anoche comí tacos", "comí tacos anoche"]},
            {"q": "Translate: Did you see? (tú)", "a": ["viste"]},
        ],
        "quiz": [
            {"q": "\"llegó\" vs \"llego\"", "o": ["she arrived vs I arrive", "same word", "I arrived vs she arrives"], "a": 0, "x": "The accent moves the stress and changes the meaning."},
            {"q": "Which word signals the preterite?", "o": ["anoche", "siempre", "normalmente"], "a": 0, "x": "anoche marks a specific finished time."},
            {"q": "\"¿Ya comiste?\" means…", "o": ["Did you eat already?", "Are you eating?", "Will you eat?"], "a": 0, "x": "Latin America uses the preterite for recent events."},
            {"q": "\"Cocinamos\" can be…", "o": ["Present or preterite", "Only present", "Only preterite"], "a": 0, "x": "-ar/-ir nosotros forms are the same in both."},
            {"q": "buscar → yo (preterite)", "o": ["busqué", "buscé", "busqé"], "a": 0, "x": "c → qu to keep the hard k sound."},
            {"q": "\"Salieron juntos\" means…", "o": ["They went out together", "They are going out together", "They will go out together"], "a": 0, "x": "salir → salieron (ellos, preterite)."},
            {"q": "leer → ella (preterite)", "o": ["leyó", "leió", "lió"], "a": 0, "x": "i between vowels becomes y."},
            {"q": "\"hace dos días\" means…", "o": ["two days ago", "in two days", "for two days"], "a": 0, "x": "hace + time = ago."},
        ],
        "practice": "Write the story of yesterday in 8–10 sentences: what you ate for each meal, when you left home, when you got back, and one thing someone else did (*Mi hermano llegó tarde…*). Use *primero, luego, después, al final*.",
    },
    {
        "id": "preterite-irregular", "phase": 3, "title": "Irregular Preterite — Vino, Vio, Se Fue",
        "goal": "Use the irregular preterites that tell who came, who said what, and who left.",
        "lesson": """
## The big irregulars (no accents!)
| | ser / ir | estar | tener | hacer | venir |
|---|---|---|---|---|---|
| yo | fui | estuve | tuve | hice | vine |
| tú | fuiste | estuviste | tuviste | hiciste | viniste |
| él/ella | fue | estuvo | tuvo | hizo | vino |
| nosotros | fuimos | estuvimos | tuvimos | hicimos | vinimos |
| ellos | fueron | estuvieron | tuvieron | hicieron | vinieron |

**ser** and **ir** share the same preterite: *fui* = I went or I was.

## More you'll hear in every story
| | | |
|---|---|---|
| decir → **dije, dijo, dijeron** | poner → **puse, puso** | poder → **pude, pudo** |
| traer → **traje, trajo, trajeron** | querer → **quise, quiso** | saber → **supe, supo** |
| dar → **di, dio** | ver → **vi, vio** | |

- *saber* in the preterite = **found out**: *¿Supiste lo de Marco?* — Did you hear (find out) about Marco?
- *no quiso* = refused: *No quiso venir.*

## -ir stem-changers: only él/ella and ellos change
*pedir → pidió, pidieron* · *servir → sirvió* · *preferir → prefirió* · *dormir → durmió, durmieron*

## Who's gone: irse in the preterite
| | |
|---|---|
| me fui | nos fuimos |
| te fuiste | se fueron |
| se fue | |

- *Valeria se fue.* — Valeria left.
- *Se fue sin decir nada.* — She left without saying anything.
- *Vino, comió y se fue.* — He came, ate, and left.
""",
        "chisme": [("¿Supiste lo de Valeria? Se fue sin decir nada.", "Did you hear about Valeria? She left without saying anything."),
                   ("Javi vino a la fiesta, pero se fue temprano.", "Javi came to the party, but he left early."),
                   ("El tío Beto vino, comió y se fue.", "Tío Beto came, ate, and left."),
                   ("Lucía no quiso hablar con Marco.", "Lucía refused to talk to Marco."),
                   ("¿Qué te dijo? ¡Dime todo!", "What did she tell you? Tell me everything!")],
        "worksheet": [
            {"q": "venir → él (preterite)", "a": ["vino"]},
            {"q": "decir → ella (preterite)", "a": ["dijo"]},
            {"q": "irse → ella (preterite)", "a": ["se fue"]},
            {"q": "estar → yo (preterite)", "a": ["estuve"]},
            {"q": "hacer → él (preterite)", "a": ["hizo"]},
            {"q": "traer → ellos (preterite)", "a": ["trajeron"]},
            {"q": "pedir → ella (preterite)", "a": ["pidió"]},
            {"q": "Translate: Did you hear about Marco? (saber, tú)", "a": ["supiste lo de marco"]},
            {"q": "Translate: He came, ate and left.", "a": ["vino, comió y se fue", "vino comió y se fue"]},
            {"q": "Translate: She refused to come.", "a": ["no quiso venir", "ella no quiso venir"]},
        ],
        "quiz": [
            {"q": "\"Fue\" can mean…", "o": ["he went or he was", "only he went", "he goes"], "a": 0, "x": "ser and ir share preterite forms."},
            {"q": "\"Se fue\" means…", "o": ["She left", "She was", "She goes"], "a": 0, "x": "irse in the preterite."},
            {"q": "\"¿Supiste?\" means…", "o": ["Did you find out / hear?", "Did you know how?", "Do you know?"], "a": 0, "x": "saber in the preterite = found out."},
            {"q": "\"No quiso venir\" means…", "o": ["She refused to come", "She didn't want to come (maybe she did anyway)", "She won't come"], "a": 0, "x": "querer in the preterite, negative = refused."},
            {"q": "decir → ellos (preterite)", "o": ["dijeron", "dijieron", "decieron"], "a": 0, "x": "After j, the ending is -eron."},
            {"q": "dormir → él (preterite)", "o": ["durmió", "dormió", "duermió"], "a": 0, "x": "-ir stem-changers: o → u in él/ellos."},
            {"q": "Do the big irregulars take accents (vino, hizo, dijo)?", "o": ["No", "Yes"], "a": 0, "x": "Irregular preterites have no written accent."},
            {"q": "\"Estuvo aquí\" means…", "o": ["She was here (and left)", "She is here", "She will be here"], "a": 0, "x": "estar → estuvo."},
        ],
        "practice": "Tell the story of the last party or family dinner you went to, in 8–10 sentences: who came (*vino*), who brought what (*trajo*), who said what (*dijo*), and who left first (*se fue*).",
    },
    {
        "id": "imperfect", "phase": 3, "title": "Imperfect — How Things Were",
        "goal": "Describe how things used to be and set the scene, and choose between preterite and imperfect.",
        "lesson": """
## Imperfect endings — very regular
| | cocinar | comer / vivir |
|---|---|---|
| yo | cocin**aba** | com**ía** / viv**ía** |
| tú | cocin**abas** | com**ías** |
| él/ella/usted | cocin**aba** | com**ía** |
| nosotros | cocin**ábamos** | com**íamos** |
| ellos/ustedes | cocin**aban** | com**ían** |

## Only three irregulars
| | ser | ir | ver |
|---|---|---|---|
| yo | era | iba | veía |
| tú | eras | ibas | veías |
| él/ella | era | iba | veía |
| nosotros | éramos | íbamos | veíamos |
| ellos | eran | iban | veían |

And *hay* → **había** (there was / there were).

## When to use it
- **Habits / "used to":** *Antes, Valeria cenaba con nosotros todos los domingos.*
- **Background & description:** *Era tarde. Hacía frío.*
- **Time and age in the past:** *Eran las diez. Tenía veinte años.*
- **Feelings and states:** *Lucía estaba triste.*
- **In progress:** *Estaban comiendo cuando…* (estaba + -ando)

## Preterite vs imperfect: the movie analogy
The **imperfect** is the scenery — what was going on. The **preterite** is what happened.
*Estábamos cenando* (background) *cuando **llegó** Javi* (event).
*Cuando llegué, Lucía ya no estaba.* — When I arrived, Lucía wasn't there anymore.

| Preterite | Imperfect |
|---|---|
| Comí tacos ayer. (once) | Comía tacos cada viernes. (habit) |
| Conocí a Javi. (I met) | Conocía a Javi. (I knew) |
| Estuvo aquí una hora. (and left) | Estaba aquí cuando… (was here at the time) |
""",
        "chisme": [("Antes, Marco y Lucía eran inseparables.", "Marco and Lucía used to be inseparable."),
                   ("Estábamos cenando cuando llegó Javi.", "We were having dinner when Javi showed up."),
                   ("Cuando llegué, Valeria ya no estaba.", "When I got there, Valeria wasn't there anymore."),
                   ("Doña Rosa siempre sabía todo.", "Doña Rosa always knew everything."),
                   ("El tío Beto comía tamales todos los días.", "Tío Beto used to eat tamales every day.")],
        "worksheet": [
            {"q": "cocinar → yo (imperfect)", "a": ["cocinaba"]},
            {"q": "comer → nosotros (imperfect)", "a": ["comíamos"]},
            {"q": "vivir → ellos (imperfect)", "a": ["vivían"]},
            {"q": "ser → yo (imperfect)", "a": ["era"]},
            {"q": "ir → nosotros (imperfect)", "a": ["íbamos"]},
            {"q": "ver → ella (imperfect)", "a": ["veía"]},
            {"q": "hay → \"there was\"", "a": ["había"]},
            {"q": "Estábamos cenando cuando Javi ___ . (llegar)", "a": ["llegó"]},
            {"q": "Cuando llegué, Valeria ya no ___ . (estar)", "a": ["estaba"]},
            {"q": "Translate: They used to be inseparable.", "a": ["eran inseparables", "ellos eran inseparables"]},
        ],
        "quiz": [
            {"q": "\"I used to eat\"", "o": ["comía", "comí", "como"], "a": 0, "x": "Habitual past → imperfect."},
            {"q": "\"It was ten o'clock\"", "o": ["Eran las diez", "Fueron las diez", "Son las diez"], "a": 0, "x": "Time in the past → imperfect."},
            {"q": "\"Cuando llegué, ya no estaba\" means…", "o": ["When I arrived, she wasn't there anymore", "When I arrived, she left", "When I arrive, she won't be there"], "a": 0,
             "x": "llegué = the event; estaba = the state at that moment."},
            {"q": "\"We were eating when he arrived\"", "o": ["Estábamos comiendo cuando llegó", "Estuvimos comiendo cuando llegaba", "Comimos cuando llegaba"], "a": 0,
             "x": "Background action (imperfect) interrupted by an event (preterite)."},
            {"q": "\"I was twenty years old\"", "o": ["Tenía veinte años", "Tuve veinte años", "Era veinte años"], "a": 0, "x": "Age in the past → tener, imperfect."},
            {"q": "How many verbs are irregular in the imperfect?", "o": ["3", "5", "Lots"], "a": 0, "x": "Just ser, ir, ver."},
            {"q": "Which describes a habit?", "o": ["Comía tacos cada viernes", "Comí tacos ayer"], "a": 0, "x": "cada viernes = every Friday → imperfect."},
            {"q": "\"Conocí a Javi\" means…", "o": ["I met Javi", "I knew Javi", "I know Javi"], "a": 0, "x": "conocer in the preterite = met."},
        ],
        "practice": "Write about how your neighborhood or family used to be (imperfect, 6 sentences: who lived where, what you used to eat on Sundays) — then one surprising thing that happened one day (preterite, 3 sentences).",
    },
    {
        "id": "perfect", "phase": 3, "title": "Present Perfect — Ya, Todavía & Acabar de",
        "goal": "Say what has (or hasn't) happened yet, and what just happened.",
        "lesson": """
## haber + past participle
| haber | + participle |
|---|---|
| he | comido |
| has | llegado |
| ha | salido |
| hemos | visto |
| han | dicho |

Participles: **-ar → -ado** (*llegado, cocinado*), **-er/-ir → -ido** (*comido, salido*).

## Irregular participles
*hacer → **hecho*** · *decir → **dicho*** · *ver → **visto*** · *poner → **puesto*** · *volver → **vuelto*** · *escribir → **escrito*** · *abrir → **abierto*** · *romper → **roto*** · *morir → **muerto***

## When Latin Americans use it
Most of Latin America prefers the preterite for finished actions (*¿Ya comiste?*), so the present perfect is mostly for:
- **ever / never:** *¿Has probado el mole?* — Have you ever tried mole? *Nunca he visto algo así.*
- **still not / so far:** *Todavía no ha llegado.* — He still hasn't arrived.
- **up to now:** *Esta semana he comido tacos cuatro veces.*

## ya / todavía / todavía no
| | |
|---|---|
| *ya* | already |
| *todavía* / *aún* | still |
| *todavía no* | not yet |
| *ya no* | not anymore |

*¿Ya llegó Javi? — Todavía no.* · *Todavía está aquí.* · *Ya no vive aquí.*

## Just happened: acabar de + infinitive
- *Acabo de comer.* — I just ate.
- *Acaba de irse.* — She just left.
- *Acaban de llegar.* — They just arrived.
""",
        "chisme": [("¿Has visto a Javi? Todavía no ha llegado.", "Have you seen Javi? He still hasn't arrived."),
                   ("Lucía acaba de irse. ¡Y lloró!", "Lucía just left. And she cried!"),
                   ("¿Quién se ha comido todo el pastel?", "Who has eaten the whole cake?"),
                   ("Nunca he visto algo así.", "I've never seen anything like it."),
                   ("Valeria ya no vive aquí.", "Valeria doesn't live here anymore.")],
        "worksheet": [
            {"q": "comer → yo (present perfect)", "a": ["he comido"]},
            {"q": "llegar → él (present perfect)", "a": ["ha llegado"]},
            {"q": "ver → tú (present perfect)", "a": ["has visto"]},
            {"q": "hacer → nosotros (present perfect)", "a": ["hemos hecho"]},
            {"q": "decir → ellos (present perfect)", "a": ["han dicho"]},
            {"q": "Translate: He still hasn't arrived.", "a": ["todavía no ha llegado", "aún no ha llegado"]},
            {"q": "Translate: I just ate. (acabar de)", "a": ["acabo de comer"]},
            {"q": "Translate: She just left. (acabar de)", "a": ["acaba de irse", "se acaba de ir"]},
            {"q": "Translate: Have you ever tried mole? (tú)", "a": ["has probado el mole", "alguna vez has probado el mole"]},
            {"q": "Translate: not yet", "a": ["todavía no", "aún no"]},
        ],
        "quiz": [
            {"q": "Participle of \"volver\"", "o": ["vuelto", "volvido", "vuelvido"], "a": 0, "x": "One of the irregular participles."},
            {"q": "\"Acabo de comer\" means…", "o": ["I just ate", "I finished eating long ago", "I'm going to eat"], "a": 0, "x": "acabar de + infinitive = just did."},
            {"q": "\"Todavía no ha llegado\" means…", "o": ["He still hasn't arrived", "He already arrived", "He's not arriving anymore"], "a": 0, "x": "todavía no = not yet."},
            {"q": "In Latin America, \"Did you eat already?\" is most often…", "o": ["¿Ya comiste?", "¿Ya has comido?"], "a": 0, "x": "Both are correct; the preterite is more common in Latin America."},
            {"q": "Which part changes for the person?", "o": ["haber (he, has, ha…)", "the participle", "both"], "a": 0, "x": "The participle never changes here: he comido, han comido."},
            {"q": "\"ya no\" means…", "o": ["not anymore", "not yet", "already"], "a": 0, "x": "Ya no vive aquí = she doesn't live here anymore."},
            {"q": "Participle of \"decir\"", "o": ["dicho", "decido", "dichado"], "a": 0, "x": "Irregular: dicho."},
            {"q": "\"Nunca he visto algo así\" means…", "o": ["I've never seen anything like it", "I never saw him like that", "I'll never see that"], "a": 0, "x": "ever/never → present perfect."},
        ],
        "practice": "Write 4 things you've **never** done (*Nunca he probado…*), 4 things that **just** happened (*Mi hermano acaba de…*), and a gossip update about who **still hasn't** done something (*Todavía no ha pagado…*).",
    },
    {
        "id": "timeline", "phase": 3, "title": "Ayer, Hoy, Mañana — Tense Review",
        "goal": "Move one story through past, present and future without mixing up the tenses.",
        "lesson": """
## One verb, every time
| | comer | estar | ir | irse |
|---|---|---|---|---|
| right now | está comiendo | está | va | se va |
| present | come | está | va | se va |
| going to | va a comer | va a estar | va a ir | se va a ir |
| future / guess | comerá | estará | irá | se irá |
| just did | acaba de comer | — | acaba de ir | acaba de irse |
| has (ever) | ha comido | ha estado | ha ido | se ha ido |
| did (once) | comió | estuvo | fue | se fue |
| used to / was | comía | estaba | iba | se iba |

## Signal words tell you the tense
| Past | Present | Future |
|---|---|---|
| *ayer, anoche, el sábado pasado, hace un mes* → preterite | *hoy, ahora, siempre, todos los días* → present | *mañana, esta noche, la próxima semana* → ir a / future |
| *antes, de niño, siempre, cada verano* → imperfect | *ahora mismo, en este momento* → estar + -ando | |
| *ya, todavía no, nunca, alguna vez* → present perfect | | |

## Read the full story — one week in the barrio
*Antes, Valeria vivía arriba y cenaba con nosotros todos los domingos.*
*El mes pasado, se fue sin decir nada.*
*Ayer doña Rosa me dijo que Valeria estaba en Monterrey.*
*Hoy hay una fiesta en el 4A. Ahora mismo, el tío Beto está comiendo y Javi está hablando con Lucía.*
*¿Marco? Todavía no ha llegado.*
*Mañana todos van a hablar de esta fiesta.*
*¿Y Valeria? ¿Volverá algún día? ¿Dónde estará?*

## Common mistakes to watch for
- ❌ ~~Ayer voy al mercado~~ → ✅ *Ayer fui al mercado* — *ayer* needs the past.
- ❌ ~~Mañana fui~~ → ✅ *Mañana voy a ir* / *Mañana iré* — *mañana* needs the future.
- ❌ ~~Cuando era niño, comí tacos cada día~~ → ✅ *Cuando era niño, comía tacos cada día* — "used to / every day" is the imperfect.
- ❌ ~~Voy comer~~ → ✅ *Voy a comer* — *ir* always takes *a* before the verb.
- ❌ ~~Estoy saliendo mañana~~ → ✅ *Salgo mañana* / *Voy a salir mañana* — Spanish doesn't use -ando/-iendo for plans.
- ❌ ~~Me gusta los tacos~~ → ✅ *Me gustan los tacos* — *gustar* agrees with the thing you like.
- ❌ ~~Estoy de México~~ → ✅ *Soy de México* — where you're from uses *ser*, not *estar*.

## Checkpoint
1. Worksheet, quiz and grammar check below mix every tense.
2. Write the story of your week in all three timelines (practice tab).
3. Record yourself telling it for 2 minutes with no notes. Listen back.
""",
        "chisme": [("Antes Valeria vivía arriba. El mes pasado se fue. ¿Volverá?", "Valeria used to live upstairs. Last month she left. Will she come back?"),
                   ("Ayer Javi comió con Lucía, hoy está cenando con ella y mañana van a desayunar juntos.", "Yesterday Javi had lunch with Lucía, today he's having dinner with her, and tomorrow they're having breakfast together."),
                   ("¿Marco? Todavía no ha llegado.", "Marco? He still hasn't arrived."),
                   ("Mañana todos van a hablar de esto.", "Tomorrow everyone's going to talk about this."),
                   ("¿Sabes qué? Ya lo sabía.", "You know what? I already knew it.")],
        "worksheet": [
            {"q": "Ayer yo ___ al mercado. (ir)", "a": ["fui"]},
            {"q": "Mañana nosotros ___ a cocinar. (ir)", "a": ["vamos"]},
            {"q": "Ahora mismo el tío Beto está ___ . (comer)", "a": ["comiendo"]},
            {"q": "Antes Valeria ___ arriba. (vivir)", "a": ["vivía"]},
            {"q": "El mes pasado Valeria se ___ . (ir)", "a": ["fue"]},
            {"q": "Marco todavía no ha ___ . (llegar)", "a": ["llegado"]},
            {"q": "¿Dónde ___ Valeria? (estar — I wonder…)", "a": ["estará"]},
            {"q": "Estábamos cenando cuando ___ Javi. (llegar)", "a": ["llegó"]},
            {"q": "Translate: She just left.", "a": ["acaba de irse", "se acaba de ir"]},
            {"q": "Translate: There's going to be a party tomorrow.", "a": ["mañana va a haber una fiesta", "va a haber una fiesta mañana", "mañana habrá una fiesta", "habrá una fiesta mañana"]},
        ],
        "quiz": [
            {"q": "\"Ayer\" + comer (yo)", "o": ["comí", "como", "comeré"], "a": 0, "x": "ayer → preterite."},
            {"q": "\"Cada domingo\" + cenar (nosotros), in the past", "o": ["cenábamos", "cenamos", "cenaremos"], "a": 0, "x": "A past habit → imperfect."},
            {"q": "\"Ahora mismo\" + hablar (ella)", "o": ["está hablando", "habló", "hablaba"], "a": 0, "x": "Right now → estar + -ando."},
            {"q": "\"Mañana\" + venir (él)", "o": ["va a venir", "vino", "venía"], "a": 0, "x": "Future → ir a + infinitive (or vendrá)."},
            {"q": "\"Todavía no\" + llegar (él)", "o": ["ha llegado", "llegaba", "llegará"], "a": 0, "x": "todavía no → present perfect: Todavía no ha llegado."},
            {"q": "\"She left\"", "o": ["Se fue", "Se va", "Se iba a ir"], "a": 0, "x": "irse → se fue."},
            {"q": "\"¿Dónde estará?\" is about…", "o": ["Now (a guess) or the future", "The past", "A habit"], "a": 0, "x": "The future of probability."},
            {"q": "\"When I was a kid\"", "o": ["Cuando era niño", "Cuando fui niño", "Cuando estaba niño"], "a": 0, "x": "Background/state in the past → imperfect of ser."},
        ],
        "practice": "**Checkpoint writing:** the story of your week in three parts. *La semana pasada…* (preterite, with one imperfect background sentence) · *Hoy / ahora…* (present and estar + -ando) · *La próxima semana…* (ir a and one simple future). Then record yourself telling it for 2 minutes without notes.",
    },
    {
        "id": "cyber-devices", "phase": 4, "title": "Cyber Spanish: Computers & Networks",
        "goal": "Name the hardware and the network, describe its state, and read addresses and acronyms out loud.",
        "lesson": """
## Now put it all to work
You can already talk about the past, present and future. This last phase reuses all of it for teaching high-school cybersecurity. The new words are on the **🛡️ Cyber** tab; this page shows which grammar each one needs.

## Tech nouns have gender — learn them with the article
*la computadora, el servidor, la red, el enrutador, el cortafuegos, la contraseña, el usuario, el puerto, el archivo*
- -dad/-ción words are feminine: *la seguridad, la conexión*
- *el cortafuegos* is the same in the plural: *los cortafuegos*
- Plural of *la red* → *las redes*

## Ser vs estar for devices
- **estar** for a state that can change: *El servidor está caído. La computadora está apagada. La red está conectada.*
- **ser** for what it is and what it's like: *Un cortafuegos es una barrera entre dos redes. La contraseña es débil.*
- Careful: *La red es segura* (the network is secure) vs *¿Estás seguro?* (are you sure?).

## Saying it out loud in class
- Acronyms are spelled with **Spanish letter names**: *IP → i pe*, *USB → u ese be*, *DNS → de ene ese*
- Symbols have names: *@ arroba, . punto, _ guion bajo, / barra*
- *Mi correo es ana punto ruiz arroba colegio punto edu.*
- *La dirección IP es diez punto cero punto cero punto uno.*

Use the **🔤 Speller** in Week 0 to practice spelling any address or username.
""",
        "worksheet": [
            {"q": "___ red (the)", "a": ["la"]},
            {"q": "___ servidor (the)", "a": ["el"]},
            {"q": "Make plural: la red", "a": ["las redes"]},
            {"q": "Make plural: el cortafuegos", "a": ["los cortafuegos"]},
            {"q": "El servidor ___ caído.", "a": ["está"]},
            {"q": "La contraseña ___ débil.", "a": ["es"]},
            {"q": "La computadora ___ apagada.", "a": ["está"]},
            {"q": "Un cortafuegos ___ una barrera.", "a": ["es"]},
            {"q": "Say \"@\" in Spanish", "a": ["arroba"]},
            {"q": "Spell \"USB\" with Spanish letter names", "a": ["u ese be"]},
        ],
        "quiz": [
            {"q": "\"The server is down\"", "o": ["El servidor está caído", "El servidor es caído"], "a": 0, "x": "A state that can change → estar."},
            {"q": "\"La red es segura\" means…", "o": ["The network is secure", "The network is sure"], "a": 0, "x": "ser seguro = safe/secure; estar seguro = to be sure."},
            {"q": "Plural of \"el cortafuegos\"", "o": ["los cortafuegos", "los cortafuegoses", "las cortafuegos"], "a": 0, "x": "Words ending in -s with unstressed last syllable don't change."},
            {"q": "\"punto\" is…", "o": [". (dot)", "@", "/"], "a": 0, "x": "arroba = @, barra = /."},
            {"q": "How do you say \"IP\"?", "o": ["i pe", "ai pi", "ipe"], "a": 0, "x": "Spanish letter names: i, pe."},
            {"q": "\"la computadora\" is…", "o": ["feminine", "masculine"], "a": 0, "x": "Ends in -a → feminine. (el computador in Colombia/Chile.)"},
            {"q": "\"The computer is off\"", "o": ["La computadora está apagada", "La computadora es apagada", "El computadora está apagado"], "a": 0, "x": "estar for state; apagada agrees with computadora."},
            {"q": "\"guion bajo\" is…", "o": ["_", "-", "/"], "a": 0, "x": "guion = -, guion bajo = _."},
        ],
        "practice": "Walk around your classroom or home and label 10 devices with article + noun (*la impresora, el enrutador…*). Then describe the state of 5 of them with estar (*está encendida, está desconectado…*) and spell your school email out loud.",
    },
    {
        "id": "cyber-actions", "phase": 4, "title": "Cyber Spanish: Security Actions & Accounts",
        "goal": "Describe what defenders, attackers and users do, in the present and in plans.",
        "lesson": """
## Most security verbs are regular -ar verbs
*bloquear, filtrar, escanear, conectar, instalar, descargar, actualizar, cifrar, monitorear, respaldar, borrar*
- *El cortafuegos bloquea el tráfico.* — present, él form
- *Ciframos los datos.* — present, nosotros

## Stem-changers you'll need
*pedir (e→i): El sistema pide una contraseña.* · *cerrar (e→ie): Cierro el puerto.* · *probar (o→ue): Pruebo la red.* · *encontrar (o→ue): Encuentro una vulnerabilidad.*

## Gustar-pattern verbs for tech support
- *No me funciona la conexión.* — My connection isn't working.
- *Al servidor le falta un parche.* — The server is missing a patch.
- *Me preocupa la privacidad.* — Privacy worries me.

## Reflexives and pronouns for accounts
*conectarse, registrarse, protegerse* · *iniciar sesión / cerrar sesión* (log in / out)
- *Me conecto a la red del colegio.* · *Te envío el enlace.* · *¿El archivo adjunto? No lo abro.*

## Plans with ir a
- *Vamos a configurar el enrutador.* · *Van a actualizar el software esta noche.*
""",
        "worksheet": [
            {"q": "bloquear → el cortafuegos (present)", "a": ["bloquea"]},
            {"q": "cifrar → nosotros (present)", "a": ["ciframos"]},
            {"q": "pedir → el sistema (present)", "a": ["pide"]},
            {"q": "cerrar → yo (present)", "a": ["cierro"]},
            {"q": "Translate: My connection isn't working.", "a": ["no me funciona la conexión", "la conexión no me funciona"]},
            {"q": "Translate: I log in.", "a": ["inicio sesión", "yo inicio sesión"]},
            {"q": "Translate: I connect to the network.", "a": ["me conecto a la red"]},
            {"q": "Translate: We're going to configure the router.", "a": ["vamos a configurar el enrutador", "vamos a configurar el router"]},
            {"q": "The attachment? I don't open it. → \"No ___ abro.\"", "a": ["lo"]},
            {"q": "encontrar → yo (present)", "a": ["encuentro"]},
        ],
        "quiz": [
            {"q": "\"El sistema pide una contraseña\" means…", "o": ["The system asks for a password", "The system loses a password", "The system asked for a password"], "a": 0, "x": "pedir e→i: pide."},
            {"q": "\"iniciar sesión\" means…", "o": ["to log in", "to log out", "to sign up"], "a": 0, "x": "cerrar sesión = to log out; registrarse = to sign up."},
            {"q": "\"No me funciona\" works like…", "o": ["gustar", "ser", "a reflexive verb"], "a": 0, "x": "The thing that isn't working is the subject."},
            {"q": "\"I close the port\"", "o": ["Cierro el puerto", "Cerro el puerto", "Ciero el puerto"], "a": 0, "x": "cerrar e→ie. (cerro = hill!)"},
            {"q": "\"respaldar\" means…", "o": ["to back up", "to reply", "to restart"], "a": 0, "x": "also: hacer una copia de seguridad."},
            {"q": "\"Te envío el enlace\" means…", "o": ["I'll send you the link", "You send me the link", "I sent the link"], "a": 0, "x": "te = (to) you, before the verb."},
            {"q": "\"Al servidor le falta un parche\"", "o": ["The server is missing a patch", "The server has extra patches", "The patch fails the server"], "a": 0, "x": "faltar works like gustar."},
            {"q": "\"descargar\" is…", "o": ["to download", "to upload", "to discharge a battery only"], "a": 0, "x": "subir / cargar = to upload."},
        ],
        "practice": "Write the steps of a lab you could run with students in 8 sentences, in the present (*Primero, cada estudiante inicia sesión…*), then 3 sentences about next week's plan with *vamos a*.",
    },
    {
        "id": "cyber-incidents", "phase": 4, "title": "Cyber Spanish: Principles & Incident Reports",
        "goal": "Explain core security principles and tell what happened in an incident, using every tense.",
        "lesson": """
## Principles: present tense, ser and definitions
*La confidencialidad significa que solo las personas autorizadas pueden ver los datos.*
*La defensa en profundidad usa varias capas de protección.*

## An incident report is gossip with logs
Everything you practiced with doña Rosa works here.
- **Preterite** for the events: *Alguien hizo clic en el enlace. El servidor se cayó a las tres. Detectamos un ataque.*
- **Imperfect** for the scene: *El sistema no tenía cortafuegos. Mientras el usuario navegaba, el malware se instaló.*
- **Present perfect** for status: *Todavía no hemos encontrado la causa. Ya hemos cambiado las contraseñas.*
- **Future** for next steps: *Vamos a revisar los registros. Instalaremos el parche mañana.*

## Report template
1. *¿Qué pasó?* — preterite
2. *¿Cómo estaba el sistema?* — imperfect
3. *¿Qué hemos hecho?* — present perfect
4. *¿Qué vamos a hacer?* — ir a / future
""",
        "worksheet": [
            {"q": "Translate: confidentiality", "a": ["la confidencialidad", "confidencialidad"]},
            {"q": "Translate: availability", "a": ["la disponibilidad", "disponibilidad"]},
            {"q": "hacer → alguien (preterite): Alguien ___ clic.", "a": ["hizo"]},
            {"q": "caerse → el servidor (preterite)", "a": ["se cayó"]},
            {"q": "tener → el sistema (imperfect): no ___ cortafuegos", "a": ["tenía"]},
            {"q": "navegar → el usuario (imperfect)", "a": ["navegaba"]},
            {"q": "Translate: We have already changed the passwords.", "a": ["ya hemos cambiado las contraseñas", "hemos cambiado las contraseñas"]},
            {"q": "Translate: We're going to check the logs. (revisar)", "a": ["vamos a revisar los registros", "vamos a revisar los logs"]},
            {"q": "instalar → nosotros (simple future)", "a": ["instalaremos"]},
            {"q": "Translate: What happened?", "a": ["qué pasó"]},
        ],
        "quiz": [
            {"q": "The events of an incident go in…", "o": ["the preterite", "the imperfect", "the future"], "a": 0, "x": "What happened → preterite."},
            {"q": "\"El sistema no tenía cortafuegos\" describes…", "o": ["the background situation", "a single event", "a plan"], "a": 0, "x": "Imperfect = the scene."},
            {"q": "\"Todavía no hemos encontrado la causa\" means…", "o": ["We still haven't found the cause", "We found the cause", "We won't find the cause"], "a": 0, "x": "todavía no + present perfect."},
            {"q": "\"La disponibilidad\" means…", "o": ["availability", "disposal", "display"], "a": 0, "x": "The A in the CIA triad."},
            {"q": "\"El servidor se cayó\" means…", "o": ["The server went down", "The server fell asleep", "The server is down"], "a": 0, "x": "caerse = to go down/crash."},
            {"q": "\"Mientras el usuario navegaba, el malware se instaló\"", "o": ["While the user was browsing, the malware installed itself", "The user browsed and installed malware", "The user will browse"], "a": 0, "x": "imperfect background + preterite event."},
            {"q": "\"Instalaremos el parche\" is…", "o": ["simple future", "preterite", "present"], "a": 0, "x": "instalar + emos."},
            {"q": "\"la defensa en profundidad\" means…", "o": ["defense in depth", "deep defense team", "profound defense"], "a": 0, "x": "Several layers of protection."},
        ],
        "practice": "Write a 4-part incident report (use the template) about a made-up phishing attack at your school: what happened, how the system was, what you've done, and what you're going to do.",
    },
    {
        "id": "teach-commands", "phase": 4, "title": "Teaching: Commands & Por vs Para",
        "goal": "Give instructions and choose between por and para.",
        "lesson": """
## Affirmative tú commands
Use the **él/ella present** form: *hablar → **habla**, comer → **come**, escribir → **escribe***.

Irregular ones (mnemonic: *Vin Diesel Has Ten Weapons Sir Ponce*): **ven** (venir), **di** (decir), **haz** (hacer), **ten** (tener), **ve** (ir), **sé** (ser), **pon** (poner), **sal** (salir).

## Negative tú commands
Use the subjunctive (you'll see it properly next week): **no hables, no comas, no vengas, no digas**.

## Usted / ustedes commands (polite, and the only plural)
Take the yo form, drop -o, switch the vowel (-ar → -e, -er/-ir → -a):
- hablar → **hable / hablen**
- comer → **coma / coman**
- venir (vengo) → **venga / vengan**

## Pronouns and commands
- **Attach** to affirmative: *¡Dime! ¡Ponlo aquí! ¡Dímelo!*
- **Before** negative: *¡No me digas! ¡No lo pongas ahí!*

## Por vs para
| POR — the path, the cause, the exchange | PARA — the goal, the destination, the deadline |
|---|---|
| through / along: *Caminamos por el parque.* | destination: *Voy para México.* |
| because of: *Gracias por todo.* | purpose: *Estudio para ser doctor.* |
| exchange: *Pagué 20 dólares por la camisa.* | recipient: *Es para ti.* |
| duration: *por dos horas* | deadline: *para el lunes* |
| parts of the day: *por la mañana* | opinion: *Para mí, es fácil.* |
| by means of: *por teléfono* | |
""",
        "worksheet": [
            {"q": "hablar → tú command", "a": ["habla"]},
            {"q": "venir → tú command", "a": ["ven"]},
            {"q": "decir + me → tú command (\"tell me\")", "a": ["dime"]},
            {"q": "hacer → tú command", "a": ["haz"]},
            {"q": "hablar → usted command", "a": ["hable"]},
            {"q": "venir → ustedes command", "a": ["vengan"]},
            {"q": "Gracias ___ todo.", "a": ["por"]},
            {"q": "Este regalo es ___ ti.", "a": ["para"]},
            {"q": "Estudio ___ ser doctor.", "a": ["para"]},
            {"q": "Caminamos ___ el parque.", "a": ["por"]},
        ],
        "quiz": [
            {"q": "Negative tú command of hablar", "o": ["no hables", "no habla", "no hablas"], "a": 0, "x": "Negative commands use the subjunctive."},
            {"q": "\"Ponlo aquí\" means…", "o": ["Put it here", "He put it here", "Don't put it here"], "a": 0, "x": "pon (poner) + lo attached."},
            {"q": "\"in the morning\"", "o": ["por la mañana", "para la mañana"], "a": 0, "x": "Parts of the day → por."},
            {"q": "\"I need it by Monday\"", "o": ["Lo necesito para el lunes", "Lo necesito por el lunes"], "a": 0, "x": "Deadline → para."},
            {"q": "\"I paid $20 for the shirt\"", "o": ["Pagué 20 dólares por la camisa", "Pagué 20 dólares para la camisa"], "a": 0, "x": "Exchange → por."},
            {"q": "tener → tú command", "o": ["ten", "tiene", "tenga"], "a": 0, "x": "One of the eight irregulars."},
            {"q": "salir → tú command", "o": ["sal", "sale", "salga"], "a": 0, "x": "One of the eight irregulars."},
            {"q": "\"Voy para México\" expresses…", "o": ["Destination", "Exchange", "Cause"], "a": 0, "x": "para points toward a goal/destination."},
        ],
        "practice": "Write instructions for a recipe or for getting from your home to a store (8+ commands, tú form). Then write 6 sentences: 3 with **por** and 3 with **para**, each a different use.",
    },
    {
        "id": "teach-advice", "phase": 4, "title": "Teaching: Advice & the Subjunctive",
        "goal": "Recognize the subjunctive and use it after wishes, hopes and \"cuando\" + future.",
        "lesson": """
## What it is
The subjunctive is a **mood**, not a tense. It's for things that are wished, hoped, doubted, felt or not yet real.

## How to form it (present subjunctive)
Take the **yo** present, drop **-o**, add the "opposite" endings:
| | hablar (hablo) | comer (como) | tener (tengo) |
|---|---|---|---|
| yo | hable | coma | tenga |
| tú | hables | comas | tengas |
| él/ella/usted | hable | coma | tenga |
| nosotros | hablemos | comamos | tengamos |
| ellos/ustedes | hablen | coman | tengan |

Irregular (**DISHES**): **d**ar → dé · **i**r → vaya · **s**er → sea · **h**aber → haya · **e**star → esté · **s**aber → sepa

## When to use it: WEIRDO
**W**ishes · **E**motions · **I**mpersonal expressions · **R**ecommendations · **D**oubt/denial · **O**jalá

The pattern is usually: *[trigger] + **que** + [different subject] + subjunctive*
- *Quiero que **vengas**.* — I want you to come.
- *Espero que **estés** bien.* — I hope you're well.
- *Es importante que **estudies**.* — It's important that you study.
- *No creo que **sea** verdad.* — I don't think it's true. (but *Creo que **es** verdad* — no doubt → indicative)
- *Ojalá (que) no **llueva**.* — Hopefully it doesn't rain.

**Same subject? Use the infinitive:** *Quiero **ir**.* (not ~~quiero que yo vaya~~)

## Cuando + future = subjunctive
*Llámame cuando **llegues**.* — Call me when you arrive (hasn't happened yet).
*Cuando **tenga** tiempo, te escribo.*

> Don't aim to master this now. Learn these phrases as chunks; the rest comes with exposure.
""",
        "worksheet": [
            {"q": "hablar → yo (subjunctive)", "a": ["hable"]},
            {"q": "comer → tú (subjunctive)", "a": ["comas"]},
            {"q": "venir → tú (subjunctive)", "a": ["vengas"]},
            {"q": "tener → él (subjunctive)", "a": ["tenga"]},
            {"q": "estar → tú (subjunctive)", "a": ["estés"]},
            {"q": "ser → nosotros (subjunctive)", "a": ["seamos"]},
            {"q": "ir → ustedes (subjunctive)", "a": ["vayan"]},
            {"q": "Translate: I hope you're well (tú)", "a": ["espero que estés bien"]},
            {"q": "Translate: Hopefully it doesn't rain", "a": ["ojalá que no llueva", "ojalá no llueva"]},
            {"q": "Translate: Call me when you arrive (tú)", "a": ["llámame cuando llegues"]},
        ],
        "quiz": [
            {"q": "The W in WEIRDO stands for…", "o": ["Wishes", "Weather", "When"], "a": 0, "x": "Wishes, Emotions, Impersonal, Recommendations, Doubt, Ojalá."},
            {"q": "Why subjunctive in \"Quiero que tú vengas\"?", "o": ["A wish about a different person", "Because of tú", "Because it's future"], "a": 0, "x": "Wish + que + different subject."},
            {"q": "Which needs the subjunctive?", "o": ["No creo que ___ verdad", "Creo que ___ verdad"], "a": 0, "x": "Doubt/denial triggers it; belief doesn't."},
            {"q": "\"I want to go\"", "o": ["Quiero ir", "Quiero que vaya", "Quiero que yo vaya"], "a": 0, "x": "Same subject → infinitive."},
            {"q": "How do you form most present subjunctives?", "o": ["yo form, drop -o, opposite vowel", "Infinitive + -e", "Preterite + -a"], "a": 0, "x": "tengo → teng- → tenga."},
            {"q": "Why \"cuando llegues\" and not \"cuando llegas\" in \"Call me when you arrive\"?", "o": ["It hasn't happened yet", "Because it's a command", "Because of llamar"], "a": 0, "x": "cuando + future/unrealized event → subjunctive."},
            {"q": "\"It's important that you study\"", "o": ["Es importante que estudies", "Es importante que estudias", "Es importante estudias"], "a": 0, "x": "Impersonal expression → subjunctive."},
            {"q": "\"Ojalá\" is followed by…", "o": ["The subjunctive", "The preterite", "The infinitive"], "a": 0, "x": "Ojalá (from Arabic, \"God willing\") always takes the subjunctive."},
        ],
        "practice": "Write a short message to a friend with 6 wishes/hopes for them using *espero que, quiero que, ojalá* and *cuando + subjunctive* (e.g. *Espero que tengas un buen viaje. Llámame cuando llegues.*).",
    },
]

# Cybersecurity / networking vocabulary sets, saved for the last phase once every tense is known.
# Each set uses one grammar point; the cyber weeks below combine several sets.
CYBER_SETS = {
    1: {
        "focus": "Tech nouns have gender too. Learn every term with its article.",
        "terms": [("la computadora", "computer (also el computador in Colombia/Chile)"), ("el servidor", "server"),
                  ("la red", "network"), ("el enrutador / el router", "router"), ("el cortafuegos / el firewall", "firewall (cortafuegos is the same in singular and plural)"),
                  ("la contraseña", "password"), ("el usuario", "user"), ("la dirección IP", "IP address"),
                  ("el puerto", "port"), ("el paquete", "packet"), ("el dispositivo", "device"),
                  ("el archivo", "file"), ("la base de datos", "database"), ("la pantalla", "screen"), ("el teclado", "keyboard")],
        "examples": [("los servidores nuevos", "the new servers"), ("una red segura", "a secure network"),
                     ("las contraseñas largas", "the long passwords"), ("los cortafuegos", "the firewalls — no change in the plural")],
        "drill": [
            {"q": "the server", "a": ["el servidor"]},
            {"q": "the networks", "a": ["las redes"]},
            {"q": "the strong passwords", "a": ["las contraseñas seguras", "las contraseñas fuertes"]},
            {"q": "a secure network", "a": ["una red segura"]},
            {"q": "the firewalls", "a": ["los cortafuegos", "los firewalls"]},
            {"q": "the device", "a": ["el dispositivo"]},
        ],
    },
    2: {
        "focus": "Device states use **estar** (está caído, está apagado). Definitions and traits use **ser**. Careful: *ser seguro* = to be secure/safe, *estar seguro* = to be sure.",
        "terms": [("estar conectado / desconectado", "to be connected / disconnected"), ("estar caído", "to be down (server, network)"),
                  ("estar encendido / apagado", "to be on / off"), ("estar actualizado", "to be up to date"),
                  ("estar infectado", "to be infected"), ("ser seguro", "to be secure"), ("ser vulnerable", "to be vulnerable"),
                  ("ser débil / fuerte", "to be weak / strong"), ("la amenaza", "threat"), ("el riesgo", "risk")],
        "examples": [("El servidor está caído.", "The server is down."), ("La contraseña es débil.", "The password is weak."),
                     ("Un cortafuegos es una barrera entre dos redes.", "A firewall is a barrier between two networks."),
                     ("¿Estás seguro? — Sí, la red es segura.", "Are you sure? — Yes, the network is secure.")],
        "drill": [
            {"q": "The server is down.", "a": ["el servidor está caído"]},
            {"q": "The password is weak.", "a": ["la contraseña es débil"]},
            {"q": "The network is secure.", "a": ["la red es segura"]},
            {"q": "The computer is infected.", "a": ["la computadora está infectada", "el computador está infectado"]},
            {"q": "The router is off.", "a": ["el enrutador está apagado", "el router está apagado"]},
            {"q": "A firewall is a barrier.", "a": ["un cortafuegos es una barrera", "un firewall es una barrera"]},
        ],
    },
    3: {
        "focus": "Most security action verbs are regular -ar verbs. You can use them right away.",
        "terms": [("bloquear", "to block"), ("filtrar", "to filter"), ("escanear", "to scan"), ("conectar", "to connect"),
                  ("instalar", "to install"), ("descargar", "to download"), ("actualizar", "to update"),
                  ("cifrar / descifrar", "to encrypt / decrypt"), ("enviar / recibir", "to send / receive"),
                  ("monitorear", "to monitor"), ("respaldar", "to back up"), ("borrar / eliminar", "to delete"),
                  ("el tráfico", "traffic"), ("los datos", "data")],
        "examples": [("El cortafuegos bloquea el tráfico.", "The firewall blocks traffic."), ("Ciframos los datos.", "We encrypt the data."),
                     ("Los atacantes envían correos falsos.", "Attackers send fake emails."), ("No descargo archivos desconocidos.", "I don't download unknown files.")],
        "drill": [
            {"q": "The firewall blocks the traffic.", "a": ["el cortafuegos bloquea el tráfico", "el firewall bloquea el tráfico"]},
            {"q": "We encrypt the data.", "a": ["ciframos los datos", "nosotros ciframos los datos"]},
            {"q": "I download the file.", "a": ["descargo el archivo", "yo descargo el archivo"]},
            {"q": "They monitor the network.", "a": ["monitorean la red", "ellos monitorean la red"]},
            {"q": "I don't install unknown programs.", "a": ["no instalo programas desconocidos", "yo no instalo programas desconocidos"]},
            {"q": "The server receives packets.", "a": ["el servidor recibe paquetes"]},
        ],
    },
    4: {
        "focus": "Questions you'll ask a class, plus *tener que* (have to), *hacer clic* (to click) and *ir a* for lab plans.",
        "terms": [("¿Qué es…?", "What is…?"), ("¿Cómo funciona…?", "How does… work?"), ("¿Cuál es la diferencia entre…?", "What's the difference between…?"),
                  ("hacer clic", "to click"), ("hacer una copia de seguridad", "to make a backup"), ("configurar", "to configure"),
                  ("la nube", "the cloud"), ("el navegador", "browser"), ("el protocolo", "protocol"),
                  ("el ancho de banda", "bandwidth"), ("la VPN (red privada virtual)", "VPN"), ("la subred", "subnet")],
        "examples": [("¿Qué es un cortafuegos?", "What is a firewall?"), ("¿Cómo funciona una VPN?", "How does a VPN work?"),
                     ("Tienes que cambiar tu contraseña.", "You have to change your password."), ("Vamos a configurar el enrutador.", "We're going to configure the router.")],
        "drill": [
            {"q": "What is a firewall?", "a": ["qué es un cortafuegos", "qué es un firewall"]},
            {"q": "How does a VPN work?", "a": ["cómo funciona una vpn"]},
            {"q": "You (tú) have to change your password.", "a": ["tienes que cambiar tu contraseña"]},
            {"q": "We're going to configure the router.", "a": ["vamos a configurar el enrutador", "vamos a configurar el router"]},
            {"q": "I make a backup.", "a": ["hago una copia de seguridad", "yo hago una copia de seguridad"]},
            {"q": "Click here (\"Haz ___ aquí\")", "a": ["clic"]},
        ],
    },
    5: {
        "focus": "Many security verbs change their stem: *pedir* (the system asks for), *cerrar* (to close a port), *defender*, *probar* (to test), *perder* (to lose data).",
        "terms": [("pedir (e→i)", "to ask for / request"), ("cerrar (e→ie)", "to close"), ("defender (e→ie)", "to defend"),
                  ("perder (e→ie)", "to lose"), ("probar (o→ue)", "to test / try"), ("mostrar (o→ue)", "to show"),
                  ("encontrar (o→ue)", "to find"), ("reiniciar", "to restart (regular)"), ("la vulnerabilidad", "vulnerability"),
                  ("el atacante", "attacker"), ("la autenticación", "authentication"), ("la prueba de penetración", "penetration test")],
        "examples": [("El sistema pide una contraseña.", "The system asks for a password."), ("Cierro los puertos abiertos.", "I close the open ports."),
                     ("Los atacantes pueden robar datos.", "Attackers can steal data."), ("Pruebo la red cada semana.", "I test the network every week.")],
        "drill": [
            {"q": "The system asks for a password.", "a": ["el sistema pide una contraseña"]},
            {"q": "I close the port.", "a": ["cierro el puerto", "yo cierro el puerto"]},
            {"q": "We defend the network.", "a": ["defendemos la red", "nosotros defendemos la red"]},
            {"q": "Attackers can steal data.", "a": ["los atacantes pueden robar datos", "los atacantes pueden robar los datos"]},
            {"q": "I find a vulnerability.", "a": ["encuentro una vulnerabilidad", "yo encuentro una vulnerabilidad"]},
            {"q": "The screen shows an error.", "a": ["la pantalla muestra un error"]},
        ],
    },
    6: {
        "focus": "*faltar* (to be missing), *funcionar* in *no me funciona* (it's not working for me), *preocupar* (to worry) and *interesar* all follow the gustar pattern.",
        "terms": [("faltar", "to be missing / lacking"), ("funcionar", "to work / function"), ("preocupar", "to worry"),
                  ("interesar", "to interest"), ("el parche", "patch"), ("la ciberseguridad", "cybersecurity"),
                  ("la privacidad", "privacy"), ("los datos personales", "personal data"), ("la conexión", "connection"),
                  ("el antivirus", "antivirus"), ("el malware / el software malicioso", "malware"), ("el virus", "virus")],
        "examples": [("Al servidor le falta un parche.", "The server is missing a patch."), ("No me funciona la conexión.", "My connection isn't working."),
                     ("Nos interesa la ciberseguridad.", "We're interested in cybersecurity."), ("Me preocupa la privacidad.", "Privacy worries me.")],
        "drill": [
            {"q": "The server is missing a patch. (\"Al servidor…\")", "a": ["al servidor le falta un parche", "le falta un parche"]},
            {"q": "My connection isn't working.", "a": ["no me funciona la conexión"]},
            {"q": "We're interested in cybersecurity.", "a": ["nos interesa la ciberseguridad"]},
            {"q": "Privacy worries me.", "a": ["me preocupa la privacidad"]},
            {"q": "The students like the labs. (\"A los estudiantes…\")", "a": ["a los estudiantes les gustan los laboratorios", "les gustan los laboratorios"]},
            {"q": "Do you (tú) have the antivirus working? → \"¿Te ___ el antivirus?\"", "a": ["funciona"]},
        ],
    },
    7: {
        "focus": "Log in/out, connect and sign up are reflexive or pronoun-heavy. *Te envío el enlace*, *me conecto a la red*.",
        "terms": [("conectarse / desconectarse", "to connect / disconnect (yourself)"), ("iniciar sesión", "to log in"),
                  ("cerrar sesión", "to log out"), ("registrarse", "to sign up"), ("protegerse", "to protect yourself"),
                  ("el enlace", "link"), ("el correo electrónico", "email"), ("el archivo adjunto", "attachment"),
                  ("el phishing / la suplantación de identidad", "phishing"), ("el remitente", "sender"), ("la cuenta", "account")],
        "examples": [("Me conecto a la red del colegio.", "I connect to the school network."), ("Te envío el enlace.", "I'll send you the link."),
                     ("¿El archivo adjunto? No lo abro.", "The attachment? I don't open it."), ("Los estudiantes inician sesión.", "The students log in.")],
        "drill": [
            {"q": "I connect to the network.", "a": ["me conecto a la red", "yo me conecto a la red"]},
            {"q": "I send you (tú) the link.", "a": ["te envío el enlace", "te mando el enlace"]},
            {"q": "I'm going to delete it (el archivo).", "a": ["voy a borrarlo", "lo voy a borrar", "voy a eliminarlo", "lo voy a eliminar"]},
            {"q": "The students log in.", "a": ["los estudiantes inician sesión"]},
            {"q": "The attachment? I don't open it. → \"No ___ abro.\"", "a": ["lo"]},
            {"q": "We protect ourselves.", "a": ["nos protegemos", "nosotros nos protegemos"]},
        ],
    },
    8: {
        "focus": "Core security principles: how to name them and explain them simply in Spanish.",
        "terms": [("la tríada CIA (confidencialidad, integridad, disponibilidad)", "CIA triad: confidentiality, integrity, availability"),
                  ("la defensa en profundidad", "defense in depth"), ("el principio de mínimo privilegio", "principle of least privilege"),
                  ("la autenticación / la autorización", "authentication / authorization"), ("el control de acceso", "access control"),
                  ("la política de seguridad", "security policy"), ("la capa", "layer")],
        "examples": [("La confidencialidad significa que solo las personas autorizadas pueden ver los datos.", "Confidentiality means only authorized people can see the data."),
                     ("La integridad significa que nadie cambia los datos sin permiso.", "Integrity means nobody changes the data without permission."),
                     ("La disponibilidad significa que el sistema está disponible cuando lo necesitamos.", "Availability means the system is available when we need it."),
                     ("La defensa en profundidad usa varias capas de protección.", "Defense in depth uses several layers of protection.")],
        "drill": [
            {"q": "confidentiality", "a": ["la confidencialidad", "confidencialidad"]},
            {"q": "integrity", "a": ["la integridad", "integridad"]},
            {"q": "availability", "a": ["la disponibilidad", "disponibilidad"]},
            {"q": "defense in depth", "a": ["la defensa en profundidad", "defensa en profundidad"]},
            {"q": "principle of least privilege", "a": ["el principio de mínimo privilegio", "principio de mínimo privilegio", "el principio de menor privilegio", "principio de menor privilegio"]},
            {"q": "The system is available. (ser or estar?)", "a": ["el sistema está disponible"]},
        ],
    },
    9: {
        "focus": "Incident reports are told in the preterite: what happened, who clicked, when the server went down.",
        "terms": [("el incidente", "incident"), ("la brecha de seguridad", "security breach"), ("la filtración de datos", "data leak"),
                  ("detectar", "to detect"), ("robar", "to steal"), ("el ataque", "attack"), ("el ransomware", "ransomware"),
                  ("el registro / el log", "log"), ("caerse", "to go down (se cayó = it went down)"), ("hackear", "to hack")],
        "examples": [("Alguien hizo clic en el enlace.", "Someone clicked the link."), ("Detectamos un ataque anoche.", "We detected an attack last night."),
                     ("El servidor se cayó a las tres.", "The server went down at three."), ("El atacante robó las contraseñas.", "The attacker stole the passwords.")],
        "drill": [
            {"q": "Someone clicked the link.", "a": ["alguien hizo clic en el enlace"]},
            {"q": "We detected an attack.", "a": ["detectamos un ataque", "nosotros detectamos un ataque"]},
            {"q": "The server went down last night.", "a": ["el servidor se cayó anoche", "anoche el servidor se cayó", "anoche se cayó el servidor"]},
            {"q": "The attacker stole the passwords.", "a": ["el atacante robó las contraseñas"]},
            {"q": "I checked the logs. (revisar)", "a": ["revisé los registros", "revisé los logs", "yo revisé los registros"]},
            {"q": "They installed the patch.", "a": ["instalaron el parche", "ellos instalaron el parche"]},
        ],
    },
    10: {
        "focus": "Set the scene of an incident or explain how things used to be: the background is in the imperfect.",
        "terms": [("navegar", "to browse"), ("el sitio web / la página web", "website / web page"), ("la red inalámbrica / el wifi", "wireless network / wifi"),
                  ("el cifrado", "encryption"), ("antes", "before / in the past"), ("mientras", "while"),
                  ("la configuración", "settings / configuration"), ("el software", "software")],
        "examples": [("Antes, las contraseñas eran muy cortas.", "Passwords used to be very short."), ("El sistema no tenía cortafuegos.", "The system didn't have a firewall."),
                     ("Mientras el usuario navegaba, el malware se instaló.", "While the user was browsing, the malware installed itself."),
                     ("El wifi no usaba cifrado.", "The wifi wasn't using encryption.")],
        "drill": [
            {"q": "The system didn't have a firewall.", "a": ["el sistema no tenía cortafuegos", "el sistema no tenía firewall", "el sistema no tenía un cortafuegos", "el sistema no tenía un firewall"]},
            {"q": "Passwords used to be short.", "a": ["las contraseñas eran cortas", "antes las contraseñas eran cortas"]},
            {"q": "The user was browsing. (imperfect)", "a": ["el usuario navegaba"]},
            {"q": "The wifi didn't use encryption.", "a": ["el wifi no usaba cifrado"]},
            {"q": "While I was working, the server went down. → \"Mientras yo ___, el servidor se cayó.\"", "a": ["trabajaba"]},
            {"q": "There were many vulnerabilities. (haber → había)", "a": ["había muchas vulnerabilidades"]},
        ],
    },
    11: {
        "focus": "Classroom and lab instructions. Use **ustedes** commands for a whole class, **tú** for one student. *por* and *para* explain how something works and what it's for.",
        "terms": [("la terminal", "terminal"), ("el comando", "command"), ("ejecutar", "to run / execute"), ("escribir", "to type / write"),
                  ("compartir", "to share"), ("abrir / cerrar", "to open / close"), ("por correo / por seguridad", "by email / for security reasons"),
                  ("servir para", "to be used for"), ("para proteger", "in order to protect")],
        "examples": [("No compartas tu contraseña.", "Don't share your password. (tú)"), ("Abran la terminal y escriban el comando.", "Open the terminal and type the command. (ustedes)"),
                     ("Por seguridad, cierren sesión.", "For security, log out."), ("Un cortafuegos sirve para filtrar el tráfico.", "A firewall is used to filter traffic.")],
        "drill": [
            {"q": "Don't share your password. (tú)", "a": ["no compartas tu contraseña"]},
            {"q": "Open the terminal. (tú)", "a": ["abre la terminal"]},
            {"q": "Log in. (ustedes)", "a": ["inicien sesión"]},
            {"q": "Type the command. (ustedes)", "a": ["escriban el comando"]},
            {"q": "___ seguridad, cierren sesión. (For security)", "a": ["por"]},
            {"q": "A firewall is used to filter traffic.", "a": ["un cortafuegos sirve para filtrar el tráfico", "un firewall sirve para filtrar el tráfico"]},
        ],
    },
    12: {
        "focus": "Teacher recommendations and security advice: *Es importante que…, Recomiendo que…, Quiero que…*",
        "terms": [("la autenticación de dos factores", "two-factor authentication"), ("el gestor de contraseñas", "password manager"),
                  ("la ingeniería social", "social engineering"), ("recomendar (e→ie)", "to recommend"),
                  ("es importante que", "it's important that"), ("es necesario que", "it's necessary that"), ("crear", "to create (subj. cree)")],
        "examples": [("Es importante que usen la autenticación de dos factores.", "It's important that you all use two-factor authentication."),
                     ("Les recomiendo que actualicen el software.", "I recommend you all update the software."),
                     ("Quiero que cada estudiante cree una contraseña segura.", "I want each student to create a secure password."),
                     ("Cuando reciban un correo raro, no hagan clic.", "When you get a strange email, don't click.")],
        "drill": [
            {"q": "It's important that you all update the software.", "a": ["es importante que actualicen el software"]},
            {"q": "I recommend that you (tú) use a password manager.", "a": ["te recomiendo que uses un gestor de contraseñas", "recomiendo que uses un gestor de contraseñas"]},
            {"q": "I hope the network is secure.", "a": ["espero que la red sea segura"]},
            {"q": "I want you all to log in.", "a": ["quiero que inicien sesión", "quiero que ustedes inicien sesión"]},
            {"q": "It's necessary that you (tú) create a strong password. → \"Es necesario que ___ una contraseña fuerte.\"", "a": ["crees"]},
            {"q": "When you all get a strange email, don't click. → \"Cuando ___ un correo raro, no hagan clic.\"", "a": ["reciban"]},
        ],
    },
}
CYBER_SETS[0] = {  # saying symbols and acronyms out loud
    "focus": "In class you'll spell usernames, read acronyms and dictate addresses out loud. Acronyms are spelled with **Spanish letter names**, and symbols have their own names.",
    "terms": [("arroba", "@"), ("punto", ". (dot)"), ("guion", "- (hyphen)"), ("guion bajo", "_ (underscore)"),
              ("barra", "/ (slash)"), ("barra invertida", "\\ (backslash)"), ("dos puntos", ": (colon)"),
              ("mayúscula / minúscula", "uppercase / lowercase"), ("i pe", "IP"), ("ve pe ene", "VPN (Spain says uve pe ene)"),
              ("u ese be", "USB"), ("de ene ese", "DNS"), ("hache te te pe ese", "HTTPS"), ("el wifi", "Wi-Fi (said \"wee-fee\" or \"wai-fai\")")],
    "examples": [("Mi correo es ana punto ruiz arroba colegio punto edu.", "My email is ana.ruiz@colegio.edu"),
                 ("La dirección IP es diez punto cero punto cero punto uno.", "The IP address is 10.0.0.1"),
                 ("La contraseña tiene una mayúscula y un número.", "The password has an uppercase letter and a number."),
                 ("Escriban: ese, ese, hache.", "Type: s, s, h. (the ssh command)")],
    "drill": [
        {"q": "Name this symbol: @", "a": ["arroba"]},
        {"q": "Name this symbol: .", "a": ["punto"]},
        {"q": "Name this symbol: _", "a": ["guion bajo"]},
        {"q": "Name this symbol: /", "a": ["barra"]},
        {"q": "Spell \"VPN\" with Spanish letter names", "a": ["ve pe ene", "ve corta pe ene", "uve pe ene"]},
        {"q": "Spell \"IP\" with Spanish letter names", "a": ["i pe"]},
    ],
}


def merge_cyber(focus, *parts):
    """One cyber week built from several vocabulary sets (drill: the first 4 of each)."""
    return {"focus": focus, "terms": [t for p in parts for t in CYBER_SETS[p]["terms"]],
            "examples": [e for p in parts for e in CYBER_SETS[p]["examples"]],
            "drill": [d for p in parts for d in CYBER_SETS[p]["drill"][:4]]}


CYBER = {
    "cyber-devices": merge_cyber("Hardware and network nouns (learn each with its article), device states with **estar**, and how to say symbols and acronyms out loud.", 0, 1, 2, 4),
    "cyber-actions": merge_cyber("Security action verbs (mostly regular -ar), the stem-changers you'll need, gustar-pattern tech-support phrases, and logging in and out.", 3, 5, 6, 7),
    "cyber-incidents": merge_cyber("Core security principles, and incident reports told in the preterite (events), imperfect (the scene) and future (next steps).", 8, 9, 10),
    "teach-commands": CYBER_SETS[11],
    "teach-advice": CYBER_SETS[12],
}

# Key words for each week's 🔤 Say it first list (lesson italics and cyber terms are added after these).
WORDS = {
    "nouns": ["el vecino", "la vecina", "el chisme", "chismoso", "la tortilla", "el pollo", "el queso", "la sopa", "la fruta",
              "el pan", "el agua", "caliente", "picante", "el novio", "la novia", "el hermano", "la tía", "ustedes", "nosotros"],
    "ser-estar": ["soy", "eres", "es", "somos", "son", "estoy", "estás", "está", "estamos", "están", "aquí", "acá", "ahí",
                  "allí", "allá", "ya no", "hay", "enojada", "lleno", "rico"],
    "present-regular": ["cocinar", "comer", "compartir", "desayunar", "cenar", "el desayuno", "el almuerzo", "la cena",
                        "beber", "tomar", "pagar", "comprar", "vivir", "nunca", "la carne"],
    "irregulars": ["tengo", "tienes", "voy", "vamos", "vengo", "viene", "hago", "digo", "dicen", "¿Quién?", "¿Dónde?",
                   "¿Cuándo?", "¿Por qué?", "porque", "¿Cuántos?", "hambre", "sed", "razón", "contar"],
    "stem-changers": ["quiero", "prefiero", "puedo", "almuerzo", "pruebo", "cuesta", "vuelvo", "pido", "sirve", "repite",
                      "juego", "el mesero", "la cuenta", "el menú", "la propina"],
    "gustar": ["me gusta", "me gustan", "le gusta", "les gusta", "me encanta", "me molesta", "me importa", "me falta",
               "me duele", "me cae bien", "me cae mal", "el picante", "los tamales", "la sal", "el estómago"],
    "progressive": ["hablando", "comiendo", "saliendo", "leyendo", "trayendo", "oyendo", "yendo", "pidiendo", "sirviendo",
                    "diciendo", "durmiendo", "viniendo", "esperando", "pasando", "ahora mismo"],
    "coming-going": ["me levanto", "me despierto", "me ducho", "me acuesto", "me voy", "te vas", "se va", "nos vamos",
                     "me quedo", "llegar", "salgo", "volver", "regresar", "temprano", "tarde"],
    "ir-a": ["voy a", "vas a", "va a", "vamos a", "van a", "mañana", "pasado mañana", "esta noche", "el fin de semana",
             "la próxima semana", "pronto", "más tarde", "llover", "va a haber", "pienso"],
    "future": ["comeré", "comerás", "comerá", "comeremos", "comerán", "tendré", "vendrá", "saldremos", "podrán", "sabré",
               "habrá", "haré", "dirá", "querrá", "¿Dónde estará?", "¿Quién será?"],
    "preterite": ["cociné", "cocinó", "comí", "comió", "salí", "salieron", "busqué", "llegué", "pagué", "almorcé",
                  "leyó", "oyó", "ayer", "anoche", "anteayer", "de repente", "¿Qué pasó?"],
    "preterite-irregular": ["fui", "fue", "fueron", "estuve", "estuvo", "tuve", "hice", "hizo", "vine", "vino", "dije",
                            "dijo", "dijeron", "trajo", "supe", "quiso", "pidió", "durmió", "se fue"],
    "imperfect": ["cocinaba", "comía", "vivía", "cenábamos", "era", "éramos", "iba", "íbamos", "veía", "había",
                  "estaba", "tenía", "antes", "siempre", "cada domingo"],
    "perfect": ["he comido", "has llegado", "ha salido", "hemos visto", "han dicho", "hecho", "puesto", "vuelto",
                "escrito", "abierto", "roto", "muerto", "ya", "todavía", "todavía no", "acabo de", "nunca"],
    "timeline": ["ayer", "hoy", "mañana", "ahora mismo", "antes", "todavía no", "la semana pasada", "la próxima semana",
                 "el mes pasado", "algún día"],
}

# Picture vocabulary: real photos from Wikimedia Commons (free licenses, fine for a classroom).
# q = Commons search; photo_pins.json holds the exact Commons file chosen after reviewing results.
PHOTOS = {
    "nouns": [{"q": "fruit stand market Mexico", "es": "las frutas", "en": "the fruit"},
              {"q": "pan dulce conchas", "es": "el pan dulce", "en": "the sweet bread"},
              {"q": "grandmother cooking kitchen", "es": "la abuela", "en": "the grandmother"},
              {"q": "group of friends laughing", "es": "los amigos", "en": "the friends"}],
    "ser-estar": [{"q": "yawning woman", "es": "Estoy cansada.", "en": "I'm tired. (estar — condition)"},
                  {"q": "woman doctor stethoscope", "es": "Ella es doctora.", "en": "She's a doctor. (ser — occupation)"},
                  {"q": "empty apartment room", "es": "Valeria ya no está.", "en": "Valeria isn't here anymore. (estar)"},
                  {"q": "old woman looking out window", "es": "Doña Rosa es muy chismosa.", "en": "Doña Rosa is a big gossip. (ser — trait)"},
                  {"q": "restroom sign", "es": "¿Dónde está el baño?", "en": "Where's the bathroom? (estar — location)"}],
    "present-regular": [{"q": "tacos al pastor", "es": "Comemos tacos.", "en": "We eat tacos."},
                        {"q": "huevos rancheros breakfast", "es": "Desayuno huevos.", "en": "I have eggs for breakfast."},
                        {"q": "man cooking in kitchen", "es": "Marco cocina.", "en": "Marco cooks."},
                        {"q": "family dinner table eating", "es": "Cenamos juntos.", "en": "We have dinner together."}],
    "irregulars": [{"q": "two women whispering", "es": "Dicen que…", "en": "Word is… / They say that…"},
                   {"q": "birthday cake candles", "es": "¿Cuántos años tienes?", "en": "How old are you?"},
                   {"q": "woman scarf cold winter snow", "es": "Tengo frío.", "en": "I'm cold."},
                   {"q": "woman drinking glass of water", "es": "Tengo sed.", "en": "I'm thirsty."}],
    "stem-changers": [{"q": "waiter serving restaurant", "es": "El mesero sirve la comida.", "en": "The waiter serves the food."},
                      {"q": "restaurant menu", "es": "¿Qué pides?", "en": "What are you ordering?"},
                      {"q": "paying restaurant bill", "es": "La cuenta, por favor.", "en": "The check, please."},
                      {"q": "man sleeping in bed", "es": "Duermo ocho horas.", "en": "I sleep eight hours."}],
    "gustar": [{"q": "cup of coffee", "es": "Me gusta el café.", "en": "I like coffee."},
               {"q": "tamales", "es": "Me encantan los tamales.", "en": "I love tamales."},
               {"q": "chili peppers", "es": "No me gusta el picante.", "en": "I don't like spicy food."},
               {"q": "headache", "es": "Me duele la cabeza.", "en": "My head hurts."},
               {"q": "mariachi", "es": "Nos encanta la música.", "en": "We love music."}],
    "progressive": [{"q": "woman talking on mobile phone", "es": "Está hablando por teléfono.", "en": "She's talking on the phone."},
                    {"q": "man reading newspaper", "es": "Está leyendo el periódico.", "en": "He's reading the newspaper."},
                    {"q": "sleeping cat", "es": "El gato está durmiendo.", "en": "The cat is sleeping."},
                    {"q": "chapulines tacos", "es": "El tío Beto está comiendo.", "en": "Tío Beto is eating."}],
    "coming-going": [{"q": "alarm clock", "es": "Me despierto temprano.", "en": "I wake up early."},
                     {"q": "suitcase airport", "es": "Valeria se va de la ciudad.", "en": "Valeria is leaving town."},
                     {"q": "taxi Mexico City", "es": "Me voy en taxi.", "en": "I'm leaving by taxi."},
                     {"q": "washing hands soap", "es": "Me lavo las manos.", "en": "I wash my hands."}],
    "ir-a": [{"q": "beach Mexico Caribbean", "es": "Vamos a ir a la playa.", "en": "We're going to go to the beach."},
             {"q": "dark rain clouds sky", "es": "Va a llover.", "en": "It's going to rain."},
             {"q": "party balloons decorations", "es": "Va a haber una fiesta.", "en": "There's going to be a party."},
             {"q": "grocery shopping cart supermarket", "es": "Voy a comprar comida.", "en": "I'm going to buy food."}],
    "future": [{"q": "fortune teller crystal ball", "es": "¿Qué pasará?", "en": "What will happen?"},
               {"q": "wedding couple", "es": "¿Se casarán?", "en": "Will they get married?"},
               {"q": "doorbell", "es": "¿Quién será?", "en": "Who could that be?"},
               {"q": "Airbus A320 takeoff", "es": "Llegará mañana.", "en": "She'll arrive tomorrow."}],
    "preterite": [{"q": "mercado Mexico market stalls", "es": "Ayer compré fruta en el mercado.", "en": "Yesterday I bought fruit at the market."},
                  {"q": "empty plate", "es": "El tío Beto comió todo.", "en": "Tío Beto ate everything."},
                  {"q": "salsa dancing couple", "es": "Bailaron toda la noche.", "en": "They danced all night."}],
    "preterite-irregular": [{"q": "house party friends", "es": "Javi vino a la fiesta.", "en": "Javi came to the party."},
                            {"q": "person walking away street", "es": "Se fue sin decir nada.", "en": "She left without saying anything."},
                            {"q": "wrapped present gift", "es": "Me trajo un regalo.", "en": "He brought me a present."}],
    "imperfect": [{"q": "rain street umbrella", "es": "Llovía cuando llegué.", "en": "It was raining when I arrived."},
                  {"q": "children playing marbles", "es": "Cuando era niño, jugaba con mis amigos.", "en": "When I was a kid, I used to play with my friends."},
                  {"q": "vintage family photograph", "es": "Antes éramos muy unidos.", "en": "We used to be very close."}],
    "perfect": [{"q": "open refrigerator", "es": "¿Quién se ha comido todo?", "en": "Who has eaten everything?"},
                {"q": "people waiting bus stop", "es": "Todavía no ha llegado.", "en": "It still hasn't arrived."},
                {"q": "broken glass floor", "es": "¿Quién ha roto el vaso?", "en": "Who has broken the glass?"}],
    "timeline": [{"q": "wall calendar", "es": "ayer, hoy y mañana", "en": "yesterday, today and tomorrow"},
                 {"q": "family photo smiling outdoors", "es": "mi familia", "en": "my family"}],
    "cyber-devices": [{"q": "laptop computer", "es": "la computadora", "en": "the computer"},
                      {"q": "server rack data center", "es": "los servidores", "en": "the servers"},
                      {"q": "wifi router home", "es": "el enrutador", "en": "the router"},
                      {"q": "computer keyboard", "es": "el teclado", "en": "the keyboard"},
                      {"q": "network switch ethernet cables", "es": "la red", "en": "the network"},
                      {"q": "blue screen of death", "es": "El sistema está caído.", "en": "The system is down. (estar)"},
                      {"q": "padlock", "es": "La red es segura.", "en": "The network is secure. (ser)"}],
    "cyber-actions": [{"q": "hands typing on laptop keyboard", "es": "Escribo en la computadora.", "en": "I write on the computer."},
                      {"q": "firewall appliance", "es": "El cortafuegos bloquea el tráfico.", "en": "The firewall blocks traffic."},
                      {"q": "external hard drive", "es": "Hago una copia de seguridad.", "en": "I make a backup."},
                      {"q": "login screen username password", "es": "El sistema pide una contraseña.", "en": "The system asks for a password."},
                      {"q": "phishing email example", "es": "un correo de phishing", "en": "a phishing email"}],
    "cyber-incidents": [{"q": "Beaumaris Castle aerial", "es": "la defensa en profundidad", "en": "defense in depth — many layers, like a castle"},
                        {"q": "fingerprint scanner", "es": "la autenticación", "en": "authentication — proving who you are"},
                        {"q": "WannaCry ransomware screenshot", "es": "El ransomware WannaCry infectó computadoras en 150 países.", "en": "WannaCry ransomware infected computers in 150 countries (2017). Red = infected."},
                        {"q": "security operations center", "es": "Detectamos un ataque.", "en": "We detected an attack."},
                        {"q": "vintage personal computer 1980s", "es": "Antes, las computadoras eran grandes.", "en": "Computers used to be big."}],
    "teach-commands": [{"q": "terminal command line bash screenshot", "es": "Abran la terminal.", "en": "Open the terminal. (ustedes)"},
                       {"q": "students computer lab classroom", "es": "Trabajen en parejas.", "en": "Work in pairs. (ustedes)"},
                       {"q": "walking path park trees people", "es": "Caminamos por el parque.", "en": "We walk through the park. (por)"},
                       {"q": "wrapped present gift", "es": "Es para ti.", "en": "It's for you. (para)"}],
    "teach-advice": [{"q": "security token two-factor authentication", "es": "la autenticación de dos factores", "en": "two-factor authentication"},
                     {"q": "Airbus A320 takeoff", "es": "Espero que tengas un buen viaje.", "en": "I hope you have a good trip."},
                     {"q": "teacher teaching students classroom", "es": "Es importante que estudien.", "en": "It's important that you all study."},
                     {"q": "dark rain clouds sky", "es": "Ojalá que no llueva.", "en": "Hopefully it doesn't rain."}],
}

# Week 0 comes before the grammar: how to SAY what you read, instead of reading it like English.
# Worksheet items with "listen" are dictation: the learner hears the clip and types what they heard.
COURSE.insert(0, {
    "id": "alphabet", "phase": 0, "title": "Alphabet & Pronunciation",
    "goal": "Pronounce any Spanish word you read: vowels, the alphabet, the letters that trick English speakers, and where the stress goes.",
    "lesson": """
## Say it before you learn it
Don't memorize a word until you can **say** it. Spanish makes this possible: every letter almost always makes the **same sound**, so once you know the rules you can read any word aloud — even one you've never seen. The trap is reading with English sounds.

**For every new word, do this:**
1. **Split** it into syllables: man·te·qui·lla
2. **Find the stress** with the 3 rules below: man·te·QUI·lla
3. **Say it slowly**, one syllable at a time, with pure vowels
4. **Say it at normal speed**
5. **Check** with 🔊 and repeat until you match

From now on, every lesson starts with a **🔤 Say it first** list that does steps 1–2 for you. Always try saying the word **before** pressing 🔊.

## Step 1: The five vowels — the most important thing
Spanish vowels are **short, crisp and never change**. English slides vowels ("no" becomes "noh-oo", "day" becomes "deh-ee"). Spanish never does.

| Letter | Sounds like | Say these |
|---|---|---|
| a | "ah" in f**a**ther | *casa*, *mapa*, *agua*, *hablar*, *nada*, *mañana* |
| e | "eh" in b**e**t | *mesa*, *té*, *leche*, *verde*, *tres*, *clase* |
| i | "ee" in s**ee** | *sí*, *libro*, *mi*, *vivir*, *chica*, *fin* |
| o | "oh" in **o**r — short, no "oo" at the end | *no*, *todo*, *foto*, *como*, *ocho*, *poco* |
| u | "oo" in f**oo**d | *uno*, *uva*, *luna*, *mucho*, *azul*, *música* |

**Vowel ladders** — read each line out loud, then check:
- *a, e, i, o, u*
- *ma, me, mi, mo, mu*
- *pa, pe, pi, po, pu*
- *ta, te, ti, to, tu*
- *la, le, li, lo, lu*

**Stop the English glide:**
| Word | Reading it like English | Spanish |
|---|---|---|
| *no* | "noh-oo" | short "no" — cut it off |
| *de* | "day" | "deh" |
| *me* | "mee" | "meh" |
| *se* | "say" | "seh" |
| *te* | "tee" | "teh" |
| *lo* | "loh-oo" | short "lo" |

> **Final e is never silent:** *grande* (GRAHN-deh), *clase* (KLAH-seh), *nube* (NOO-beh), *leche* (LEH-cheh), *noche* (NOH-cheh), *siete* (SYEH-teh), *nombre* (NOHM-breh)

## Step 2: The alphabet — el abecedario
You'll need these to spell names, usernames and acronyms out loud.

| Letter | Name | | Letter | Name |
|---|---|---|---|---|
| A | *a* | | N | *ene* |
| B | *be* | | Ñ | *eñe* |
| C | *ce* | | O | *o* |
| D | *de* | | P | *pe* |
| E | *e* | | Q | *cu* |
| F | *efe* | | R | *erre* |
| G | *ge* | | S | *ese* |
| H | *hache* | | T | *te* |
| I | *i* | | U | *u* |
| J | *jota* | | V | *ve* (Latin America often says *ve corta* or *ve chica*) |
| K | *ka* | | W | *doble u* (or *doble ve*) |
| L | *ele* | | X | *equis* |
| M | *eme* | | Y | *ye* (older name: *i griega*) |
| | | | Z | *zeta* |

## Step 3: The letters that trick English speakers
Read every example out loud **before** pressing 🔊.

### H is always silent
*hola* (OH-lah), *hora* (OH-rah), *hacer* (ah-SEHR), *hoy* (oy), *hermano* (ehr-MAH-noh), *ahora* (ah-OH-rah)

### J — and G before E or I — is a throaty "h"
Like the "h" in "hot," but scratchier.
- Ladder: *ja, je, ji, jo, ju* · *ge, gi*
- *jota*, *jugar*, *trabajo*, *ojo*, *joven*, *gente*, *página*, *general*

### G before A, O, U is a hard "g" — GUE / GUI too (the u is silent)
- Ladder: *ga, gue, gui, go, gu*
- *gato*, *gusto*, *amigo*, *guitarra*, *seguir*, *guerra*
- With **ü** the u is said like "w": *pingüino* (peen-GWEE-noh), *bilingüe* (bee-LEEN-gweh)

### C is "k" before A, O, U — and "s" before E, I. QU is always "k"
- Ladder: *ca, que, qui, co, cu* · *ce, ci*
- "k": *casa*, *computadora*, *cuenta*, *que*, *quiero*, *equipo*
- "s": *cero*, *ciudad*, *cifrar*, *gracias*, *hacer*, *cinco*

### Z is "s" in Latin America
*zapato*, *diez*, *azul*, *lápiz*, *cabeza*, *empezar*

### LL and Y sound like the "y" in "yes"
- Ladder: *lla, lle, lli, llo, llu*
- *llamar*, *calle*, *llave*, *pollo*, *yo*, *ayer*, *playa*, *mayo*
- On its own, *y* (and) sounds like "ee."

### Ñ is "ny," as in "canyon"
- Ladder: *ña, ñe, ñi, ño, ñu*
- *año*, *niño*, *mañana*, *español*, *piña*, *señor*

### R (one tap) vs RR (rolled)
- **One r between vowels** is a single quick tap, like the "tt" in American "butter": *pero*, *para*, *hora*, *caro*, *cara*, *naranja*
- **rr**, or **r at the start of a word or after n, l, s**, is rolled: *perro*, *carro*, *rojo*, *arroz*, *rápido*, *Enrique*
- Tip: say "butter, butter, butter" fast and feel the tap. To roll, relax your tongue on that same spot and let air flutter it: rrr.
- **Can't roll yet?** That's normal. Open the **🌀 R Trill Lab** (home page) — 7 different techniques, a practice ladder, slow audio and a daily routine.

**Hear the difference — it changes the meaning:**
| Tap | Rolled |
|---|---|
| *pero* — but | *perro* — dog |
| *caro* — expensive | *carro* — car |
| *cero* — zero | *cerro* — hill |
| *coro* — choir | *corro* — I run |

### B and V are the same sound
A soft "b," lips barely touching: *bueno*, *vamos*, *vino*, *bien*, *vivir*, *beber*

### D between vowels is soft, like "th" in "this"
*nada*, *todo*, *cada*, *lado*, *helado* — and a final d is barely said: *ciudad*, *usted*, *verdad*

### X is usually "ks" — except México
*examen*, *taxi*, *éxito* — but *México* and *Oaxaca* use the throaty j sound.

## Step 4: Vowel pairs blend into one syllable
When **i** or **u** sits next to another vowel, they glide together into one beat:

| Pair | Say these |
|---|---|
| ie | *bien*, *tiene*, *siete* |
| ue | *bueno*, *puerto*, *nueve* |
| ia / io | *gracias*, *familia*, *servicio*, *radio* |
| ua | *agua*, *cuando*, *cuatro* |
| ai / ei / oi | *aire*, *seis*, *hoy* |
| au | *auto*, *aula* |
| iu / ui | *ciudad*, *muy*, *cuidado* |

An accent on the i or u **breaks** the pair into two beats: *día* (DEE-ah), *tío* (TEE-oh), *país* (pah-EES), *frío* (FREE-oh)

## Step 5: Where does the stress go? Three rules
**Rule 1** — word ends in a **vowel, n or s** → stress the **second-to-last** syllable:
*casa* (CA·sa), *hablan* (HA·blan), *tacos* (TA·cos), *hamburguesa* (ham·bur·GUE·sa), *enchilada* (en·chi·LA·da), *vecino* (ve·CI·no)

**Rule 2** — word ends in **any other consonant** → stress the **last** syllable:
*hablar* (ha·BLAR), *ciudad* (ciu·DAD), *cenar* (ce·NAR), *mujer* (mu·JER), *usted* (us·TED), *papel* (pa·PEL)

**Rule 3** — a written **accent mark** overrides both rules:
*teléfono* (te·LÉ·fo·no), *café* (ca·FÉ), *plátano* (PLÁ·ta·no), *información* (in·for·ma·CIÓN), *número* (NÚ·me·ro), *está* (es·TÁ)

> The accent mark doesn't change the vowel's sound — it only marks stress. It also separates look-alike words: *si* (if) vs *sí* (yes), *el* (the) vs *él* (he), *tu* (your) vs *tú* (you).

## Step 6: Words you already know — said the Spanish way
These look like English, which is exactly why they trip you up.

| Word | Spanish stress | Watch out for |
|---|---|---|
| *hotel* | o·TEL | silent h |
| *hospital* | os·pi·TAL | silent h, stress at the end |
| *chocolate* | cho·co·LA·te | final e = "eh" |
| *tomate* | to·MA·te | final e = "eh" |
| *animal* | a·ni·MAL | stress at the end |
| *doctor* | doc·TOR | stress at the end |
| *familia* | fa·MI·lia | ia blends into one beat |
| *restaurante* | res·tau·RAN·te | au blends, final e = "eh" |
| *error* | e·RROR | rolled rr |
| *idea* | i·DE·a | three syllables |
| *banana* | ba·NA·na | every a is "ah" |
| *general* | ge·ne·RAL | g before e = j sound |

## Step 7: Build up long words
Say each line out loud, adding one piece at a time:
- *ham* → *hambur* → *hamburguesa*
- *re* → *refri* → *refrigera* → *refrigerador*
- *chis* → *chismo* → *chismosa*
- *in* → *insepa* → *inseparable*

## Step 8: Read these sentences — then check with 🔊
- *Hola, ¿cómo estás?*
- *Buenos días. Mucho gusto.*
- *¿Dónde está el baño?*
- *Quiero aprender español.*
- *La sopa está caliente.*
- *¿Dónde está Valeria?*
- *El perro come, pero no corre.*
- *Mi vecina es muy chismosa.*
""",
    "worksheet": [
        {"q": "Listen and type what you hear", "listen": "hola", "a": ["hola"]},
        {"q": "Listen and type what you hear", "listen": "jugar", "a": ["jugar"]},
        {"q": "Listen and type what you hear", "listen": "gente", "a": ["gente"]},
        {"q": "Listen and type what you hear", "listen": "queso", "a": ["queso"]},
        {"q": "Listen and type what you hear", "listen": "llamar", "a": ["llamar"]},
        {"q": "Listen and type what you hear", "listen": "perro", "a": ["perro"]},
        {"q": "Listen and type what you hear", "listen": "pero", "a": ["pero"]},
        {"q": "Listen and type what you hear", "listen": "ciudad", "a": ["ciudad"]},
        {"q": "Listen and type what you hear", "listen": "guitarra", "a": ["guitarra"]},
        {"q": "Listen and type what you hear", "listen": "chisme", "a": ["chisme"]},
        {"q": "Listen and type what you hear", "listen": "mañana", "a": ["mañana"]},
        {"q": "Listen and type what you hear", "listen": "cuidado", "a": ["cuidado"]},
        {"q": "Type the **stressed** syllable: *casa*", "a": ["ca"]},
        {"q": "Type the **stressed** syllable: *comer*", "a": ["mer"]},
        {"q": "Type the **stressed** syllable: *enchilada*", "a": ["la"]},
        {"q": "Type the **stressed** syllable: *ciudad*", "a": ["dad"]},
        {"q": "Type the **stressed** syllable: *teléfono*", "a": ["lé", "le"]},
        {"q": "Type the **stressed** syllable: *mantequilla*", "a": ["qui"]},
    ],
    "quiz": [
        {"q": "The h in \"hola\" is…", "o": ["silent", "like English h", "like Spanish j"], "a": 0, "x": "h is always silent: OH-lah."},
        {"q": "The j in \"jugar\" sounds like…", "o": ["English h (strong)", "English j", "English y"], "a": 0, "x": "jota is a throaty h: hoo-GAR."},
        {"q": "In \"queso\", the u is…", "o": ["silent", "said \"oo\"", "said \"w\""], "a": 0, "x": "qu = k. KEH-soh."},
        {"q": "In Latin America, \"ll\" (llamar) usually sounds like…", "o": ["y in \"yes\"", "l in \"lamp\"", "j in \"jam\""], "a": 0, "x": "yah-MAR. (In Argentina it's closer to \"sh.\")"},
        {"q": "The c in \"ciudad\" sounds like…", "o": ["s", "k", "ch"], "a": 0, "x": "c before e or i = s in Latin America."},
        {"q": "\"pero\" and \"perro\" mean…", "o": ["but / dog", "dog / but", "the same thing"], "a": 0, "x": "One tap r = pero (but). Rolled rr = perro (dog)."},
        {"q": "Where is the stress in \"hablar\"?", "o": ["ha-BLAR", "HA-blar"], "a": 0, "x": "Ends in a consonant other than n or s → last syllable."},
        {"q": "The final e in \"grande\" is…", "o": ["said \"eh\"", "silent"], "a": 0, "x": "Every vowel is pronounced: GRAHN-deh."},
        {"q": "Which word has a rolled r?", "o": ["Enrique", "pero", "hora"], "a": 0, "x": "r after n is rolled: en-RRI-que. pero and hora have one tap."},
        {"q": "\"hotel\" in Spanish is said…", "o": ["o·TEL", "HO·tel", "ho·TEL"], "a": 0, "x": "Silent h, and it ends in l so the stress is on the last syllable."},
        {"q": "The v in \"vino\" sounds like…", "o": ["a soft b", "English v"], "a": 0, "x": "b and v are the same sound in Spanish: BEE-noh."},
        {"q": "Where is the stress in \"información\"?", "o": ["in·for·ma·CIÓN", "in·FOR·ma·cion", "IN·for·ma·cion"], "a": 0, "x": "The accent mark wins."},
    ],
    "practice": "Use **Say it out loud** below. Read each line yourself FIRST, then play the 🔊 model, record yourself with 🎙, play yours back and compare. Repeat until they match. Then spell your full name and your email address out loud with Spanish letter names (*a, be, ce…*) and *arroba* / *punto*.",
    "speak": ["a, e, i, o, u", "ma, me, mi, mo, mu", "ja, je, ji, jo, ju", "ca, que, qui, co, cu", "ga, gue, gui, go, gu",
              "lla, lle, lli, llo, llu", "ña, ñe, ñi, ño, ñu", "pero, perro", "caro, carro", "cero, cerro",
              "hotel, hospital, chocolate, error, idea", "Hola, ¿cómo estás?", "Buenos días. Mucho gusto.",
              "Quiero aprender español.", "La sopa está caliente.", "El perro come, pero no corre.",
              "Tres tristes tigres tragaban trigo en un trigal.", "Erre con erre, cigarro; erre con erre, barril."],
})

for _i, _w in enumerate(COURSE):
    _w["week"] = _i
    _w["cyber"] = CYBER.get(_w["id"])
    _w["photos"] = PHOTOS.get(_w["id"], [])
    if _w.get("chisme"):
        _w["lesson"] += ("\n## 🗣️ El chisme\nSay each line out loud before pressing 🔊.\n"
                         + "\n".join(f"- *{es}* — {en}" for es, en in _w["chisme"]) + "\n")
        _w.setdefault("speak", [es for es, _ in _w["chisme"]])

# ---------- pronunciation helpers ----------
# Spanish spelling is regular enough to split syllables and find the stress by rule.
VOWELS = set("aeiouáéíóúü")
STRONG = set("aeoáéíóú")          # accented i/u act strong, which breaks a vowel pair
ACCENTED = set("áéíóú")
INSEPARABLE = {"bl", "br", "cl", "cr", "dr", "fl", "fr", "gl", "gr", "kl", "kr", "pl", "pr", "tr", "tl"}
UNSTRESSED = {"el", "la", "los", "las", "un", "de", "del", "al", "a", "en", "y", "o", "con", "por", "que", "se", "me", "te", "lo", "le", "les", "nos", "mi", "tu", "su", "mis", "tus", "sus"}
LOANWORDS = {"web", "firewall", "router", "wifi", "malware", "phishing", "hacker", "software", "ransomware", "log", "edu", "ssh"}


def _units(word):
    w, out, i = word.lower(), [], 0
    while i < len(w):
        two = w[i:i + 2]
        if two in ("ch", "ll", "rr") or (two in ("qu", "gu") and i + 2 < len(w) and w[i + 2] in "eéií"):
            out.append(two)
            i += 2
        else:
            out.append(w[i])
            i += 1
    return out


def _split_cluster(c):
    if len(c) <= 1:
        return [], c
    if "".join(c[-2:]) in INSEPARABLE:
        return c[:-2], c[-2:]
    return c[:-1], c[-1:]


def syllabify(word):
    units = _units(word)
    # final y after a vowel is a vowel glide (hoy, muy); otherwise y is a consonant
    kinds = ["V" if u in VOWELS or (u == "y" and i == len(units) - 1 and i and units[i - 1] in VOWELS) else "C"
             for i, u in enumerate(units)]
    segs = []
    for u, k in zip(units, kinds):
        if segs and segs[-1][0] == k:
            segs[-1][1].append(u)
        else:
            segs.append([k, [u]])
    parts = []  # alternating C / V, with vowel runs split where two strong vowels meet
    for k, us in segs:
        if k == "C":
            parts.append(["C", us])
            continue
        groups = [[us[0]]]
        for v in us[1:]:
            (groups.append([v]) if groups[-1][-1] in STRONG and v in STRONG else groups[-1].append(v))
        for g in groups:
            if parts and parts[-1][0] == "V":
                parts.append(["C", []])
            parts.append(["V", g])
    onset = []
    if parts and parts[0][0] == "C":
        onset = parts.pop(0)[1]
    sylls = []
    for i in range(0, len(parts), 2):
        cur = onset + parts[i][1]
        onset = []
        if i + 1 < len(parts):
            coda, onset = _split_cluster(parts[i + 1][1]) if i + 2 < len(parts) else (parts[i + 1][1], [])
            cur += coda
        sylls.append("".join(cur))
    return sylls or [word]


def stressed(sylls, word):
    for i, syl in enumerate(sylls):
        if any(ch in ACCENTED for ch in syl):
            return i
    if len(sylls) == 1:
        return 0
    return len(sylls) - 2 if word.lower()[-1] in "aeiouns" else len(sylls) - 1


def say_it(phrase):
    """'La contraseña es segura.' -> 'la con·tra·SE·ña es se·GU·ra'"""
    words = re.findall(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+", phrase)
    out = []
    for w in words:
        if w.lower() in LOANWORDS or (len(w) > 1 and w.isupper()):
            out.append(w)
            continue
        sylls = syllabify(w)
        if w.lower() in UNSTRESSED and len(words) > 1:
            out.append(w.lower())  # articles, prepositions and object pronouns aren't stressed
            continue
        k = stressed(sylls, w)
        out.append("·".join(s.upper() if i == k else s for i, s in enumerate(sylls)))
    return " ".join(out)


def say_first(w, limit=30):
    """Key words for a week, to practice saying before learning them."""
    items = list(WORDS.get(w["id"], []))
    for es, _ in (w["cyber"] or {}).get("terms", []):
        items += [t.strip() for t in re.sub(r"\([^)]*\)", "", es).split(" / ")]
    italic = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")
    for t in italic.findall(w["lesson"].replace("**", "")):
        if len(t.split()) <= 3 and not re.search(r"[=…\d→]", t) and t.count(",") == 0:
            items.append(t.strip().rstrip(".").strip())
    seen, out = set(), []
    for t in items:
        if t and t.lower() not in seen and t.lower() not in UNSTRESSED and re.search(r"[a-záéíóúñ]", t, re.I):
            seen.add(t.lower())
            out.append({"es": t, "say": say_it(t)})
    return out[:limit]


# ---------- Week 0 drills: alphabet explorer, speller and quick-fire listening drills ----------
ALPHABET = [
    ("A", "a", "\"ah\" as in father", ["casa", "agua", "mañana"], ""),
    ("B", "be", "soft b — exactly the same as v", ["bueno", "beber", "bien"], "When spelling, say *be larga* (or *be grande*) so nobody confuses it with v."),
    ("C", "ce", "\"k\" before a, o, u · \"s\" before e, i", ["casa", "cero", "ciudad"], ""),
    ("CH", "che", "\"ch\" as in church", ["chico", "noche", "mucho"], "Used to be its own letter; you'll still hear *che*."),
    ("D", "de", "d — soft like \"th\" in this between vowels", ["dos", "nada", "todo"], ""),
    ("E", "e", "\"eh\" as in bet — never silent", ["mesa", "leche", "verde"], ""),
    ("F", "efe", "f, like English", ["foto", "fácil", "fin"], ""),
    ("G", "ge", "hard g before a, o, u · throaty h before e, i", ["gato", "gente", "guitarra"], "gue / gui: the u is silent."),
    ("H", "hache", "silent — always", ["hola", "hora", "ahora"], ""),
    ("I", "i", "\"ee\" as in see", ["sí", "libro", "vivir"], ""),
    ("J", "jota", "throaty h, like a scratchy \"h\" in hot", ["jugar", "ojo", "trabajo"], ""),
    ("K", "ka", "k — mostly in borrowed words", ["kilo", "karate", "kiosco"], ""),
    ("L", "ele", "a light, clean l", ["luna", "libro", "papel"], ""),
    ("LL", "doble ele", "\"y\" as in yes (Argentina: \"sh\")", ["llamar", "calle", "llave"], ""),
    ("M", "eme", "m, like English", ["mesa", "mamá", "mucho"], ""),
    ("N", "ene", "n, like English", ["no", "nada", "nueve"], ""),
    ("Ñ", "eñe", "\"ny\" as in canyon", ["año", "niño", "piña"], ""),
    ("O", "o", "\"oh\" — short, no \"oo\" glide", ["no", "todo", "ocho"], ""),
    ("P", "pe", "p without the puff of air", ["papá", "puerto", "pero"], ""),
    ("Q", "cu", "always written qu, sounds like k", ["que", "queso", "quiero"], "The u after q is silent."),
    ("R", "erre", "one tap in the middle of a word · rolled at the start or after n, l, s", ["pero", "rojo", "Enrique"], "Can't roll yet? Try the R Trill Lab."),
    ("RR", "doble erre", "always rolled", ["perro", "carro", "tierra"], ""),
    ("S", "ese", "s, like English", ["sí", "casa", "seis"], ""),
    ("T", "te", "t with the tongue on the back of the teeth, no puff", ["tres", "todo", "tú"], ""),
    ("U", "u", "\"oo\" as in food · silent in que, qui, gue, gui", ["uno", "uva", "luna"], ""),
    ("V", "ve", "soft b — exactly the same as b", ["vamos", "vino", "vivir"], "When spelling, say *ve corta* (or *ve chica*) to tell it apart from b."),
    ("W", "doble u", "w — borrowed words", ["wifi", "web", "sándwich"], "Also called *doble ve*."),
    ("X", "equis", "\"ks\" · throaty h in México and some names", ["examen", "taxi", "México"], ""),
    ("Y", "ye", "\"y\" as in yes · \"ee\" when it's alone (y = and)", ["yo", "ayer", "y"], ""),
    ("Z", "zeta", "\"s\" in Latin America", ["zapato", "diez", "azul"], ""),
]

# What to SAY for each character when spelling something out loud.
SPELL = {**{L.lower(): name for L, name, *_ in ALPHABET if len(L) == 1},
         "b": "be larga", "v": "ve corta",
         **dict(zip("0123456789", ["cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve"])),
         "@": "arroba", ".": "punto", "-": "guion", "_": "guion bajo", "/": "barra", "\\": "barra invertida",
         ":": "dos puntos", "#": "numeral", "*": "asterisco", "!": "signo de exclamación", "?": "signo de interrogación",
         "+": "más", "=": "igual", " ": "espacio"}
SPELL_EXTRA = ["mayúscula", "con tilde", "con diéresis"]

STRESS_POOL = ["casa", "hablar", "ciudad", "teléfono", "café", "número", "información", "papel", "mañana", "español",
               "examen", "hotel", "hospital", "animal", "chocolate", "idea", "música", "lápiz", "fácil", "joven", "gracias",
               "familia", "usted", "pregunta", "estudiante", "profesor", "clase", "escuela", "enchilada", "hamburguesa",
               "mantequilla", "vecino", "tortilla", "tomate", "plátano", "limón", "chisme", "chismoso", "abuela", "hermano",
               "desayuno", "almuerzo", "refrigerador", "restaurante", "cocina", "mesero", "novio", "sándwich", "azúcar",
               "árbol", "comer", "mujer", "verdad", "fiesta", "Enrique"]

RULES = [  # [x] marks the letter(s) in question
    ("[g]ente", ["throaty h", "hard g as in go"]), ("[g]ato", ["hard g as in go", "throaty h"]),
    ("[c]iudad", ["s", "k"]), ("[c]asa", ["k", "s"]), ("q[u]eso", ["silent", "oo"]), ("[u]no", ["oo", "silent"]),
    ("[h]ola", ["silent", "h as in hat"]), ("a[h]ora", ["silent", "h as in hat"]), ("[ll]ave", ["y as in yes", "l as in lamp"]),
    ("e[x]amen", ["ks", "throaty h"]), ("Mé[x]ico", ["throaty h", "ks"]), ("g[u]itarra", ["silent", "w"]),
    ("ping[ü]ino", ["w", "silent"]), ("[j]ugar", ["throaty h", "j as in jam"]), ("[z]apato", ["s", "z as in zoo"]),
    ("[r]ojo", ["rolled", "one tap"]), ("pe[r]o", ["one tap", "rolled"]), ("En[r]ique", ["rolled", "one tap"]),
    ("na[d]a", ["soft, like th in this", "hard d"]), ("[v]amos", ["soft b", "English v"]), ("grand[e]", ["eh", "silent"]),
    ("a[ñ]o", ["ny as in canyon", "n"]), ("[c]ena", ["s", "k"]), ("[g]uerra", ["hard g as in go", "throaty h"]),
    ("pá[g]ina", ["throaty h", "hard g as in go"]), ("[y]o", ["y as in yes", "ee"]), ("[q]uiero", ["k", "kw"]),
]

DRILLS = {
    "alphabet": [{"letter": L, "name": n, "sound": snd, "examples": ex, "say": [say_it(e) for e in ex], "tip": tip} for L, n, snd, ex, tip in ALPHABET],
    "spell": SPELL,
    "vowels": [c + v for c in "mptlsn" for v in "aeiou"],
    "pairs": [["pero", "perro"], ["caro", "carro"], ["cero", "cerro"], ["coro", "corro"], ["para", "parra"]],
    "stress": [{"w": w, "syl": syllabify(w), "k": stressed(syllabify(w), w)} for w in STRESS_POOL],
    "rules": [{"w": w, "o": o} for w, o in RULES],
    "dictation": ["hola", "casa", "perro", "gato", "pan", "queso", "sopa", "leche", "chisme", "vecino", "arroz", "carne", "jugo", "llave", "jefe"],
}
COURSE[0]["drills"] = DRILLS


def drill_texts():
    texts = [d["name"] for d in DRILLS["alphabet"]] + [e for d in DRILLS["alphabet"] for e in d["examples"]]
    texts += list(SPELL.values()) + SPELL_EXTRA + DRILLS["vowels"] + [w for p in DRILLS["pairs"] for w in p]
    texts += STRESS_POOL + [r["w"].replace("[", "").replace("]", "") for r in DRILLS["rules"]]
    return list(dict.fromkeys(texts))


def spell_texts():
    """Short clips that get chained together when spelling; their silence is trimmed."""
    return list(dict.fromkeys(list(SPELL.values()) + SPELL_EXTRA + [d["name"] for d in DRILLS["alphabet"]]))


# Grammar check: (meaning, correct sentence, [incorrect versions], why, [other accepted corrections]).
# The site turns each into multiple choice, "type the fix" (from the first incorrect version) or "listen & choose".
GRAMMAR = {
    "nouns": [("The soup is hot.", "La sopa está caliente.", ["El sopa está caliente.", "La sopa está calientes."], "sopa is feminine and singular: la sopa, caliente.", []),
              ("It's a problem.", "Es un problema.", ["Es una problema."], "problema ends in -a but is masculine (Greek -ma words).", []),
              ("the spicy tacos", "los tacos picantes", ["los tacos picante", "las tacos picantes"], "Article and adjective both match: masculine plural.", []),
              ("the nosy neighbors (women)", "las vecinas chismosas", ["las vecinas chismosos", "los vecinas chismosas"], "Everything agrees with vecinas: feminine plural.", []),
              ("the cold water", "el agua fría", ["la agua fría", "el agua frío"], "agua takes el (stressed a-) but stays feminine: fría.", []),
              ("the breads", "los panes", ["los pans", "las panes"], "Consonant ending → add -es.", []),
              ("a white tortilla", "una tortilla blanca", ["un tortilla blanca", "una tortilla blanco"], "Everything agrees with tortilla: feminine singular.", []),
              ("the day", "el día", ["la día"], "día is masculine even though it ends in -a.", []),
              ("the new boyfriend", "el novio nuevo", ["la novio nuevo", "el novio nueva"], "novio is masculine: el … nuevo.", []),
              ("the big cities", "las ciudades grandes", ["las ciudads grandes", "los ciudades grandes"], "Consonant ending → add -es; -dad words are feminine.", [])],
    "ser-estar": [("I'm from Mexico.", "Soy de México.", ["Estoy de México."], "Origin uses ser.", []),
                  ("Where is Marco?", "¿Dónde está Marco?", ["¿Dónde es Marco?"], "Location of a person uses estar.", []),
                  ("Doña Rosa is a big gossip.", "Doña Rosa es muy chismosa.", ["Doña Rosa está muy chismosa."], "A personality trait uses ser.", []),
                  ("Lucía is angry today.", "Lucía está enojada hoy.", ["Lucía es enojada hoy."], "An emotion right now uses estar.", ["Hoy Lucía está enojada."]),
                  ("Valeria isn't here anymore.", "Valeria ya no está.", ["Valeria ya no es.", "Valeria ya no hay."], "Presence/location uses estar; ya no = not anymore.", ["Valeria ya no está aquí."]),
                  ("There's a new guy in the building.", "Hay un chico nuevo en el edificio.", ["Está un chico nuevo en el edificio."], "Something that exists, not yet known → hay.", []),
                  ("The party is at my house.", "La fiesta es en mi casa.", ["La fiesta está en mi casa."], "Where an EVENT happens uses ser.", []),
                  ("These tacos are tasty! (eating them now)", "¡Los tacos están ricos!", ["¡Los tacos están rico!", "¡Los tacos es ricos!"], "Tasting it now → estar, and rico agrees with tacos: ricos. (Son ricos also works for food in general; about a person, ser rico = rich.)", ["Los tacos están ricos.", "¡Los tacos son ricos!", "Los tacos son ricos."]),
                  ("It's three o'clock.", "Son las tres.", ["Es las tres.", "Están las tres."], "Time uses ser, plural for hours above one.", []),
                  ("We are at home.", "Estamos en casa.", ["Somos en casa."], "Location of people uses estar.", ["Nosotros estamos en casa."])],
    "present-regular": [("I cook on Sundays.", "Cocino los domingos.", ["Cocina los domingos.", "Cocinar los domingos."], "yo → -o. Don't leave the verb in the infinitive.", ["Yo cocino los domingos."]),
                        ("We share the food.", "Compartimos la comida.", ["Compartemos la comida."], "-ir verbs: nosotros → -imos.", ["Nosotros compartimos la comida."]),
                        ("They eat tacos.", "Ellos comen tacos.", ["Ellos comemos tacos.", "Ellos come tacos."], "ellos → -en.", ["Comen tacos."]),
                        ("Lucía doesn't eat meat.", "Lucía no come carne.", ["Lucía come no carne."], "no goes right before the verb.", []),
                        ("You live alone.", "Tú vives solo.", ["Tú vive solo."], "tú → -es for -ir verbs.", ["Vives solo.", "Tú vives sola.", "Vives sola."]),
                        ("Javi never cooks.", "Javi no cocina nunca.", ["Javi no cocinas nunca."], "él → -a (no -s; -s is tú).", ["Javi nunca cocina."]),
                        ("You all drink a lot of coffee.", "Ustedes beben mucho café.", ["Ustedes bebes mucho café."], "ustedes → -en.", ["Ustedes toman mucho café."]),
                        ("We have dinner late.", "Cenamos tarde.", ["Cenemos tarde."], "-ar nosotros → -amos.", ["Nosotros cenamos tarde."]),
                        ("Doña Rosa watches everything.", "Doña Rosa mira todo.", ["Doña Rosa miran todo."], "One person → él/ella form.", []),
                        ("I have breakfast at seven.", "Desayuno a las siete.", ["Desayuna a las siete."], "yo → -o.", ["Yo desayuno a las siete."])],
    "irregulars": [("I'm twenty years old.", "Tengo veinte años.", ["Soy veinte años."], "Age uses tener.", []),
                   ("Word is Javi has a girlfriend.", "Dicen que Javi tiene novia.", ["Dicen que Javi tene novia.", "Dicen que Javi tiene una novio."], "tener: e → ie (tiene); novia is feminine.", []),
                   ("Is Valeria coming?", "¿Viene Valeria?", ["¿Va Valeria?", "¿Vene Valeria?"], "Coming toward here → venir: viene.", ["¿Valeria viene?"]),
                   ("I'm hungry.", "Tengo hambre.", ["Estoy hambre.", "Soy hambre."], "Hunger uses tener.", []),
                   ("I'm not saying anything.", "No digo nada.", ["No dico nada.", "No dice nada."], "decir is irregular in yo: digo.", []),
                   ("She's right.", "Tiene razón.", ["Es razón.", "Está razón."], "tener razón = to be right.", ["Ella tiene razón."]),
                   ("Why is she angry? — Because Marco doesn't cook.", "¿Por qué está enojada? — Porque Marco no cocina.", ["¿Porque está enojada? — Por qué Marco no cocina."], "por qué (two words, accent) = why; porque = because.", []),
                   ("I have to tell you something.", "Tengo que contarte algo.", ["Tengo contarte algo.", "Tengo que cuentas algo."], "tener que + infinitive.", ["Te tengo que contar algo."]),
                   ("Marco goes to the market.", "Marco va al mercado.", ["Marco va a el mercado.", "Marco viene al mercado."], "a + el = al; going away from here → ir.", []),
                   ("How many cousins do you have?", "¿Cuántas primas tienes?", ["¿Cuántos primas tienes?"], "cuánto agrees with the noun: primas → cuántas.", [])],
    "stem-changers": [("I want the tacos.", "Quiero los tacos.", ["Quero los tacos."], "querer: e → ie.", ["Yo quiero los tacos."]),
                      ("We can pay.", "Podemos pagar.", ["Puedemos pagar."], "No stem change in nosotros.", ["Nosotros podemos pagar."]),
                      ("I have lunch at two.", "Almuerzo a las dos.", ["Almorzo a las dos."], "almorzar: o → ue.", ["Yo almuerzo a las dos."]),
                      ("She orders the soup.", "Ella pide la sopa.", ["Ella pede la sopa.", "Ella pregunta la sopa."], "pedir (e → i) = to order / ask FOR.", ["Pide la sopa."]),
                      ("How much does it cost?", "¿Cuánto cuesta?", ["¿Cuánto costa?"], "costar: o → ue.", []),
                      ("Can I try some?", "¿Puedo probar?", ["¿Podo probar?"], "poder: o → ue.", []),
                      ("Tío Beto has seconds.", "El tío Beto repite.", ["El tío Beto repete."], "repetir: e → i.", []),
                      ("The waiter serves the food.", "El mesero sirve la comida.", ["El mesero serve la comida."], "servir: e → i.", []),
                      ("They come back late.", "Vuelven tarde.", ["Volven tarde."], "volver: o → ue.", ["Ellos vuelven tarde."]),
                      ("Javi prefers to eat alone.", "Javi prefiere comer solo.", ["Javi prefere comer solo."], "preferir: e → ie.", [])],
    "gustar": [("I like tamales.", "Me gustan los tamales.", ["Me gusta los tamales.", "Yo gusto los tamales."], "The thing liked is the subject: plural → gustan.", []),
               ("I like to cook.", "Me gusta cocinar.", ["Yo gusta cocinar.", "Me gusto cocinar."], "me + gusta + infinitive.", []),
               ("Lucía likes spicy food.", "A Lucía le gusta el picante.", ["A Lucía gusta el picante.", "Lucía le gusta el picante."], "You need le, and the person takes a: a Lucía.", []),
               ("We love enchiladas.", "Nos encantan las enchiladas.", ["Nos encanta las enchiladas.", "Nosotros encantamos las enchiladas."], "encantar works like gustar; plural → encantan.", ["A nosotros nos encantan las enchiladas."]),
               ("I like Javi (as a person).", "Javi me cae bien.", ["Yo caigo bien Javi.", "Javi me caigo bien."], "caer bien: the person is the subject → cae.", ["Me cae bien Javi."]),
               ("Doña Rosa doesn't like Javi.", "A doña Rosa no le cae bien Javi.", ["Doña Rosa no cae bien Javi."], "a + person + le + cae bien.", ["A doña Rosa le cae mal Javi."]),
               ("My stomach hurts.", "Me duele el estómago.", ["Me duelen el estómago.", "Yo duelo el estómago."], "One stomach → duele.", []),
               ("My feet hurt.", "Me duelen los pies.", ["Me duele los pies."], "Plural feet → duelen.", []),
               ("The soup needs salt.", "A la sopa le falta sal.", ["La sopa falta sal."], "faltar works like gustar.", ["Le falta sal a la sopa."]),
               ("Do you like movies?", "¿Te gustan las películas?", ["¿Tú gustas las películas?"], "te + gustan (películas is plural).", ["¿A ti te gustan las películas?"])],
    "progressive": [("I'm cooking.", "Estoy cocinando.", ["Soy cocinando.", "Estoy cocino."], "estar + -ando.", ["Yo estoy cocinando."]),
                    ("Tío Beto is eating.", "El tío Beto está comiendo.", ["El tío Beto está comando.", "El tío Beto es comiendo."], "-er verbs → -iendo, with estar.", []),
                    ("She's reading.", "Está leyendo.", ["Está leiendo."], "Vowel + iendo → yendo.", ["Ella está leyendo."]),
                    ("He's sleeping.", "Está durmiendo.", ["Está dormiendo."], "dormir → durmiendo (o → u).", ["Él está durmiendo."]),
                    ("What are you doing?", "¿Qué estás haciendo?", ["¿Qué estás haces?"], "The gerund never changes: haciendo.", ["¿Qué haces?"]),
                    ("Javi is talking to Lucía.", "Javi está hablando con Lucía.", ["Javi está hablar con Lucía."], "estar + gerund, not the infinitive.", []),
                    ("I'm going out tonight.", "Salgo esta noche.", ["Estoy saliendo esta noche."], "Plans don't use the progressive in Spanish.", ["Voy a salir esta noche."]),
                    ("We're waiting.", "Estamos esperando.", ["Estamos esperamos."], "Only estar is conjugated.", []),
                    ("They're ordering.", "Están pidiendo.", ["Están pediendo."], "pedir → pidiendo (e → i).", ["Ellos están pidiendo."]),
                    ("What's going on?", "¿Qué está pasando?", ["¿Qué es pasando?"], "estar, not ser.", ["¿Qué pasa?"])],
    "coming-going": [("I'm leaving.", "Me voy.", ["Voy.", "Me vas."], "Leaving = irse: me voy.", ["Ya me voy."]),
                     ("You're leaving already?", "¿Ya te vas?", ["¿Ya vas?", "¿Ya se vas?"], "irse with tú → te vas.", []),
                     ("I'm staying.", "Me quedo.", ["Quedo.", "Me quedas."], "quedarse is reflexive: me quedo.", ["Yo me quedo."]),
                     ("I leave home at seven.", "Salgo de casa a las siete.", ["Salo de casa a las siete."], "salir: yo → salgo.", []),
                     ("I get up at seven.", "Me levanto a las siete.", ["Yo levanto me a las siete."], "The pronoun goes before the conjugated verb.", ["Yo me levanto a las siete."]),
                     ("I wash my hands.", "Me lavo las manos.", ["Lavo mis manos me.", "Me lavo mis manos."], "Reflexive + the article for body parts.", []),
                     ("Valeria is leaving town.", "Valeria se va de la ciudad.", ["Valeria va de la ciudad.", "Valeria se va a la ciudad."], "irse de = to leave (a place).", []),
                     ("We're staying a little longer.", "Nos quedamos un rato más.", ["Se quedamos un rato más."], "nosotros → nos.", []),
                     ("They go to bed late.", "Se acuestan tarde.", ["Se acostan tarde."], "acostarse: o → ue.", ["Ellos se acuestan tarde."]),
                     ("Javi arrives at eight.", "Javi llega a las ocho.", ["Javi se llega a las ocho."], "llegar is not reflexive.", [])],
    "ir-a": [("I'm going to eat.", "Voy a comer.", ["Voy comer.", "Voy a como."], "ir + a + infinitive.", ["Yo voy a comer."]),
             ("We're going to cook.", "Vamos a cocinar.", ["Vamos a cocinamos.", "Vamos cocinar."], "Only ir changes; the second verb stays in the infinitive.", []),
             ("They're going to arrive late.", "Van a llegar tarde.", ["Van llegar tarde.", "Va a llegar tarde."], "ellos → van.", ["Ellos van a llegar tarde."]),
             ("It's going to rain.", "Va a llover.", ["Va llover.", "Va a llueve."], "ir a + infinitive.", []),
             ("There's going to be a party.", "Va a haber una fiesta.", ["Va a hay una fiesta.", "Van a haber una fiesta."], "hay → va a haber (always singular).", []),
             ("Are you going to come?", "¿Vas a venir?", ["¿Vas venir?", "¿Va a vienes?"], "tú → vas a + infinitive.", []),
             ("She's going to get angry.", "Se va a enojar.", ["Va a se enojar."], "Pronoun before va, or attached: va a enojarse.", ["Va a enojarse."]),
             ("I plan to cook mole.", "Pienso cocinar mole.", ["Pienso a cocinar mole.", "Penso cocinar mole."], "pensar + infinitive (no a), e → ie.", []),
             ("I have to buy tortillas.", "Tengo que comprar tortillas.", ["Tengo comprar tortillas."], "tener que + infinitive.", []),
             ("They're going to break up.", "Van a romper.", ["Van romper.", "Van a rompen."], "ir a + infinitive.", [])],
    "future": [("I'll cook tomorrow.", "Mañana cocinaré.", ["Mañana cocinré.", "Mañana cociné."], "Future: whole infinitive + é.", ["Cocinaré mañana."]),
               ("They'll arrive on Monday.", "Llegarán el lunes.", ["Llegaron el lunes.", "Llegarían el lunes."], "ellos → -án. (llegaron is the past!)", []),
               ("She'll come.", "Vendrá.", ["Venirá.", "Vendré."], "venir → vendr- + á.", ["Ella vendrá."]),
               ("I'll have time.", "Tendré tiempo.", ["Teneré tiempo."], "tener → tendr-.", []),
               ("We'll do it.", "Lo haremos.", ["Lo haceremos."], "hacer → har-.", []),
               ("There will be a party.", "Habrá una fiesta.", ["Haberá una fiesta.", "Habrán una fiesta."], "haber → habr-, always singular.", []),
               ("I wonder where Valeria is.", "¿Dónde estará Valeria?", ["¿Dónde estara Valeria?", "¿Dónde estuvo Valeria?"], "Future of probability; the ending has an accent.", []),
               ("Who could it be?", "¿Quién será?", ["¿Quién sera?", "¿Quién fue?"], "Future of probability: será.", []),
               ("He must be about thirty.", "Tendrá unos treinta años.", ["Será unos treinta años."], "Age uses tener, even when guessing.", []),
               ("What will they say?", "¿Qué dirán?", ["¿Qué decirán?"], "decir → dir-.", [])],
    "preterite": [("Yesterday I cooked.", "Ayer cociné.", ["Ayer cocino.", "Ayer cocinó."], "Preterite yo → -é. (cocinó = he cooked)", []),
                  ("Tío Beto ate all the tamales.", "El tío Beto comió todos los tamales.", ["El tío Beto comí todos los tamales."], "él → -ió.", []),
                  ("Javi arrived at three.", "Javi llegó a las tres.", ["Javi llego a las tres."], "Without the accent, llego = I arrive.", []),
                  ("I arrived late.", "Llegué tarde.", ["Llegé tarde."], "-gar verbs: yo → -gué.", []),
                  ("I paid the check.", "Pagué la cuenta.", ["Pagé la cuenta."], "-gar verbs: yo → -gué.", []),
                  ("I had lunch at two.", "Almorcé a las dos.", ["Almorzé a las dos."], "-zar verbs: yo → -cé.", []),
                  ("They went out together.", "Salieron juntos.", ["Salaron juntos.", "Salen juntos."], "-ir ellos → -ieron.", ["Ellos salieron juntos."]),
                  ("Doña Rosa heard everything.", "Doña Rosa oyó todo.", ["Doña Rosa oió todo."], "oír: i → y.", []),
                  ("Did you see?", "¿Viste?", ["¿Vistes?"], "tú preterite never ends in -s: viste.", []),
                  ("Last night we had dinner at home.", "Anoche cenamos en casa.", ["Anoche cenemos en casa."], "-ar nosotros preterite → -amos.", ["Cenamos en casa anoche."])],
    "preterite-irregular": [("Javi came to the party.", "Javi vino a la fiesta.", ["Javi venió a la fiesta.", "Javi vinó a la fiesta."], "venir → vino (no accent).", []),
                            ("She left without saying anything.", "Se fue sin decir nada.", ["Se fui sin decir nada.", "Fue sin decir nada."], "irse → se fue.", ["Ella se fue sin decir nada."]),
                            ("What did she tell you?", "¿Qué te dijo?", ["¿Qué te decí?", "¿Qué te dijó?"], "decir → dijo (no accent).", []),
                            ("They told me everything.", "Me dijeron todo.", ["Me dijieron todo."], "After j: -eron, not -ieron.", []),
                            ("He came, ate and left.", "Vino, comió y se fue.", ["Venió, comió y se fue."], "venir → vino.", []),
                            ("Did you hear about Marco?", "¿Supiste lo de Marco?", ["¿Sabiste lo de Marco?"], "saber → supe/supiste = found out.", []),
                            ("I was here for an hour.", "Estuve aquí una hora.", ["Estaba aquí una hora.", "Esté aquí una hora."], "A bounded time (una hora) → preterite estuve.", []),
                            ("She ordered the soup.", "Pidió la sopa.", ["Pedió la sopa."], "-ir stem-changers: e → i in él/ellos.", ["Ella pidió la sopa."]),
                            ("He brought tamales.", "Trajo tamales.", ["Traió tamales.", "Trajó tamales."], "traer → trajo.", ["Él trajo tamales."]),
                            ("Lucía refused to talk.", "Lucía no quiso hablar.", ["Lucía no querió hablar."], "querer → quiso.", [])],
    "imperfect": [("We used to have dinner together every Sunday.", "Cenábamos juntos todos los domingos.", ["Cenaron juntos todos los domingos.", "Cenimos juntos todos los domingos."], "A past habit → imperfect.", []),
                  ("It was ten o'clock.", "Eran las diez.", ["Fueron las diez."], "Time in the past → imperfect.", []),
                  ("I was twenty years old.", "Tenía veinte años.", ["Tuve veinte años."], "Age in the past → imperfect.", []),
                  ("We were eating when Javi arrived.", "Estábamos comiendo cuando llegó Javi.", ["Estuvimos comiendo cuando llegaba Javi."], "Background → imperfect; the interruption → preterite.", []),
                  ("When I arrived, she wasn't there anymore.", "Cuando llegué, ya no estaba.", ["Cuando llegaba, ya no estuvo."], "The arrival is the event; her absence is the scene.", []),
                  ("They used to be inseparable.", "Eran inseparables.", ["Estaban inseparables.", "Fueron inseparables siempre."], "A general characteristic → ser, imperfect.", ["Ellos eran inseparables."]),
                  ("Doña Rosa always knew everything.", "Doña Rosa siempre sabía todo.", ["Doña Rosa siempre supo todo."], "siempre + ongoing state → imperfect.", []),
                  ("There were a lot of people.", "Había mucha gente.", ["Habían mucha gente.", "Hubo mucha gente."], "Description → había (always singular).", []),
                  ("I used to see her every day.", "La veía todos los días.", ["La vía todos los días."], "ver is irregular: veía.", []),
                  ("When I was a kid, I used to eat tamales.", "Cuando era niño, comía tamales.", ["Cuando estaba niño, comí tamales."], "Childhood (ser) and habits → imperfect.", ["Cuando era niña, comía tamales."])],
    "perfect": [("I've eaten.", "He comido.", ["Ha comido.", "He comer."], "yo → he + participle.", ["Yo he comido."]),
                ("He still hasn't arrived.", "Todavía no ha llegado.", ["Todavía no he llegado.", "Todavía no ha llegó."], "él → ha; participle -ado.", ["Aún no ha llegado."]),
                ("Have you seen Javi?", "¿Has visto a Javi?", ["¿Has veído a Javi?", "¿Ha visto a Javi?"], "ver → visto (irregular); tú → has.", []),
                ("What have you done?", "¿Qué has hecho?", ["¿Qué has hacido?"], "hacer → hecho.", []),
                ("They've said a lot.", "Han dicho mucho.", ["Han decido mucho."], "decir → dicho.", []),
                ("I just ate.", "Acabo de comer.", ["Acabo comer.", "Acabo de comí."], "acabar de + infinitive.", []),
                ("She just left.", "Acaba de irse.", ["Acaba irse.", "Acaba de se fue."], "acabar de + infinitive (+ pronoun).", ["Se acaba de ir."]),
                ("I've never seen anything like it.", "Nunca he visto algo así.", ["Nunca he vido algo así."], "ver → visto.", []),
                ("Who broke the glass?", "¿Quién ha roto el vaso?", ["¿Quién ha rompido el vaso?"], "romper → roto.", ["¿Quién rompió el vaso?"]),
                ("She doesn't live here anymore.", "Ya no vive aquí.", ["Todavía no vive aquí."], "ya no = not anymore; todavía no = not yet.", ["Ella ya no vive aquí."])],
    "timeline": [("Yesterday I went to the market.", "Ayer fui al mercado.", ["Ayer voy al mercado.", "Ayer iba al mercado."], "One finished trip yesterday → preterite.", ["Fui al mercado ayer."]),
                 ("Tomorrow I'm going to go.", "Mañana voy a ir.", ["Mañana fui.", "Mañana voy ir."], "Future → ir a + infinitive.", ["Mañana iré."]),
                 ("When I was a kid, I ate tacos every day.", "Cuando era niño, comía tacos todos los días.", ["Cuando era niño, comí tacos todos los días."], "A habit → imperfect.", ["Cuando era niña, comía tacos todos los días."]),
                 ("Right now he's eating.", "Ahora mismo está comiendo.", ["Ahora mismo comió.", "Ahora mismo es comiendo."], "In progress now → estar + -ando.", []),
                 ("She left last month.", "Se fue el mes pasado.", ["Se va el mes pasado.", "Se iba el mes pasado."], "A single finished event → preterite.", ["El mes pasado se fue."]),
                 ("Marco still hasn't arrived.", "Marco todavía no ha llegado.", ["Marco todavía no llegará."], "todavía no → present perfect.", ["Marco aún no ha llegado."]),
                 ("I'm going out tomorrow.", "Mañana salgo.", ["Mañana estoy saliendo."], "Plans → present or ir a, never the progressive.", ["Mañana voy a salir.", "Salgo mañana."]),
                 ("I like the tacos.", "Me gustan los tacos.", ["Me gusta los tacos."], "Plural thing liked → gustan.", []),
                 ("I wonder where she is.", "¿Dónde estará?", ["¿Dónde estuvo?"], "A guess about now → future of probability.", []),
                 ("We were having dinner when they called.", "Estábamos cenando cuando llamaron.", ["Estuvimos cenando cuando llamaban."], "Scene (imperfect) + event (preterite).", [])],
    "cyber-devices": [("the new server", "el servidor nuevo", ["la servidor nuevo", "el servidor nueva"], "servidor is masculine: el … nuevo.", []),
                      ("the secure passwords", "las contraseñas seguras", ["las contraseñas seguros", "los contraseñas seguras"], "contraseña is feminine: las … seguras.", []),
                      ("the networks", "las redes", ["las reds", "los redes"], "Consonant ending → -es; red is feminine.", []),
                      ("The server is down.", "El servidor está caído.", ["El servidor es caído."], "A device's state uses estar.", []),
                      ("The computer is infected.", "La computadora está infectada.", ["La computadora es infectada.", "La computadora está infectado."], "A state → estar, and it agrees: infectada.", []),
                      ("A firewall is a barrier.", "Un cortafuegos es una barrera.", ["Un cortafuegos está una barrera."], "Definitions use ser.", ["Un firewall es una barrera."]),
                      ("The password is weak.", "La contraseña es débil.", ["La contraseña está débil."], "A characteristic → ser.", []),
                      ("What's your email?", "¿Cuál es tu correo?", ["¿Qué es tu correo?"], "Specific info → cuál.", []),
                      ("What is a firewall?", "¿Qué es un cortafuegos?", ["¿Cuál es un cortafuegos?"], "Asking for a definition → qué.", ["¿Qué es un firewall?"]),
                      ("The router is off.", "El enrutador está apagado.", ["El enrutador es apagado."], "On/off is a state → estar.", ["El router está apagado."])],
    "cyber-actions": [("The firewall blocks the traffic.", "El cortafuegos bloquea el tráfico.", ["El cortafuegos bloquean el tráfico."], "One firewall → él form, -a.", ["El firewall bloquea el tráfico."]),
                      ("We encrypt the data.", "Nosotros ciframos los datos.", ["Nosotros cifran los datos."], "nosotros → -amos.", ["Ciframos los datos."]),
                      ("The system asks for a password.", "El sistema pide una contraseña.", ["El sistema pede una contraseña."], "pedir: e → i.", []),
                      ("I close the port.", "Cierro el puerto.", ["Cerro el puerto."], "cerrar: e → ie. (cerro = hill!)", ["Yo cierro el puerto."]),
                      ("You have to change your password.", "Tienes que cambiar tu contraseña.", ["Tienes cambiar tu contraseña.", "Tienes que cambias tu contraseña."], "tener que + infinitive.", []),
                      ("My connection isn't working.", "No me funciona la conexión.", ["No funciono la conexión."], "No me funciona = it isn't working for me.", ["La conexión no me funciona."]),
                      ("The server is missing a patch.", "Al servidor le falta un parche.", ["El servidor falta un parche."], "faltar works like gustar.", ["Le falta un parche al servidor."]),
                      ("We connect to the network.", "Nos conectamos a la red.", ["Conectamos nos a la red.", "Me conectamos a la red."], "nosotros → nos, before the verb.", []),
                      ("The file? I don't open it.", "¿El archivo? No lo abro.", ["¿El archivo? No la abro.", "¿El archivo? No abro lo."], "archivo is masculine → lo, before the verb.", []),
                      ("I'll send you the link.", "Te envío el enlace.", ["Envío te el enlace."], "Object pronoun before the verb.", ["Te mando el enlace."])],
    "cyber-incidents": [("We detected an attack last night.", "Detectamos un ataque anoche.", ["Detectemos un ataque anoche."], "-ar nosotros preterite → -amos.", ["Anoche detectamos un ataque."]),
                        ("Someone clicked the link.", "Alguien hizo clic en el enlace.", ["Alguien hició clic en el enlace."], "hacer → hizo.", []),
                        ("The server went down at three.", "El servidor se cayó a las tres.", ["El servidor se caía a las tres.", "El servidor se cayó a la tres."], "A single event → preterite; plural hour → las tres.", []),
                        ("The system didn't have a firewall.", "El sistema no tenía cortafuegos.", ["El sistema no tení cortafuegos."], "tener imperfect → tenía.", ["El sistema no tenía firewall."]),
                        ("Passwords used to be short.", "Antes, las contraseñas eran cortas.", ["Antes, las contraseñas estaban cortas."], "A general characteristic → ser.", ["Las contraseñas eran cortas."]),
                        ("While the user was browsing, the malware installed itself.", "Mientras el usuario navegaba, el malware se instaló.", ["Mientras el usuario navegó, el malware se instalaba."], "Background → imperfect; event → preterite.", []),
                        ("We have already changed the passwords.", "Ya hemos cambiado las contraseñas.", ["Ya hemos cambiamos las contraseñas."], "haber + participle -ado.", []),
                        ("We're going to check the logs.", "Vamos a revisar los registros.", ["Vamos revisar los registros."], "ir a + infinitive.", ["Vamos a revisar los logs."]),
                        ("We'll install the patch tomorrow.", "Instalaremos el parche mañana.", ["Instalé el parche mañana.", "Instalaramos el parche mañana."], "Simple future: instalar + emos.", ["Mañana instalaremos el parche."]),
                        ("The system is available.", "El sistema está disponible.", ["El sistema es disponible."], "Availability right now is a state → estar.", [])],
    "teach-commands": [("Speak more slowly! (tú)", "¡Habla más despacio!", ["¡Hablas más despacio!"], "tú command = él form: habla.", []),
         ("Don't speak. (tú)", "No hables.", ["No habla."], "Negative tú commands use the subjunctive.", []),
         ("Come here. (tú)", "Ven aquí.", ["Viene aquí.", "Venga aquí."], "Irregular tú command: ven. (venga is usted.)", ["Ven acá."]),
         ("Open the terminal. (ustedes)", "Abran la terminal.", ["Abren la terminal."], "ustedes command: -ir → -an.", []),
         ("Tell it to me. (tú)", "Dímelo.", ["Dime lo."], "Pronouns attach to affirmative commands, written as one word.", []),
         ("Don't tell it to me. (tú)", "No me lo digas.", ["No dímelo."], "Negative command: pronouns go before.", []),
         ("Thanks for everything.", "Gracias por todo.", ["Gracias para todo."], "Gratitude/exchange → por.", []),
         ("This gift is for you.", "Este regalo es para ti.", ["Este regalo es por ti."], "Recipient → para.", []),
         ("I study to become a doctor.", "Estudio para ser doctor.", ["Estudio por ser doctor."], "Purpose → para.", ["Estudio para ser doctora."]),
         ("A firewall is used to filter traffic.", "Un cortafuegos sirve para filtrar el tráfico.", ["Un cortafuegos sirve por filtrar el tráfico."], "servir para = to be used for.", ["Un firewall sirve para filtrar el tráfico."])],
    "teach-advice": [("I want you to come.", "Quiero que vengas.", ["Quiero que vienes.", "Quiero tú venir."], "Wish about someone else → que + subjunctive.", []),
         ("I hope you're well.", "Espero que estés bien.", ["Espero que estás bien."], "Hope → subjunctive.", []),
         ("I want to go.", "Quiero ir.", ["Quiero que yo vaya."], "Same subject → infinitive.", []),
         ("I don't think it's true.", "No creo que sea verdad.", ["No creo que es verdad."], "Doubt → subjunctive.", []),
         ("I think it's true.", "Creo que es verdad.", ["Creo que sea verdad."], "Belief (no doubt) → indicative.", []),
         ("Call me when you arrive.", "Llámame cuando llegues.", ["Llámame cuando llegas.", "Llámame cuando llegarás."], "cuando + future event → subjunctive.", []),
         ("It's important that you all study.", "Es importante que estudien.", ["Es importante que estudian."], "Impersonal expression → subjunctive.", []),
         ("Hopefully it doesn't rain.", "Ojalá que no llueva.", ["Ojalá que no llueve."], "ojalá → subjunctive.", ["Ojalá no llueva."]),
         ("I recommend you all update the software.", "Recomiendo que actualicen el software.", ["Recomiendo que actualizan el software."], "Recommendation → subjunctive.", ["Les recomiendo que actualicen el software."]),
         ("You need to create a strong password.", "Es necesario que crees una contraseña fuerte.", ["Es necesario que creas una contraseña fuerte."], "crear → crees. (creas = you believe!)", [])],
}
for _w in COURSE:
    _w["grammar"] = [{"en": en, "ok": ok, "bad": bad, "x": x, "alt": alt} for en, ok, bad, x, alt in GRAMMAR.get(_w["id"], [])]


def grammar_texts():
    return [t for items in GRAMMAR.values() for _, ok, bad, *_ in items for t in [ok, *bad]]


for _w in COURSE:
    _w["say_first"] = say_first(_w)
    if _w["cyber"]:
        _w["cyber"]["say"] = [say_it(es) for es, _ in _w["cyber"]["terms"]]

PHASES = {0: "Start Here", 1: "The Present — Right Now", 2: "The Future — What's Coming", 3: "The Past — What Happened", 4: "Cybersecurity Spanish"}


def note_name(w):
    title = re.sub(r'[\\/*"<>|?¿]', "", w["title"].replace(": ", " — "))  # characters Obsidian can't use in file names
    return f"Week {w['week']:02d} - {title}"


def write_note(path, text, force):
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")
    return True


def load_media():
    path = HERE / "media.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"images": {}, "audio": {}}


MEDIA = load_media()
ITALIC = re.compile(r"(?<!\*)\*(?!\*)([^*\n]+?)\*(?!\*)")


def play(text):
    """Obsidian audio embed for a Spanish phrase, or '' if no clip exists."""
    f = MEDIA["audio"].get(text.strip())
    return f"![[{Path(f).name}]]" if f else ""


def photo_section(w):
    # Obsidian won't show an audio player inside a table cell, so each photo is its own block with the clip on its own line.
    blocks = []
    for i, ph in enumerate(w["photos"]):
        img = MEDIA["images"].get(f"{w['id']}-{i + 1}")
        if img:
            blocks.append(f"> [!example] {ph['es']}\n> ![[{Path(img['file']).name}|260]]\n> {ph['en']}\n> {play(ph['es'])}")
    if not blocks:
        return ""
    return "## 📷 Picture vocabulary\n" + "\n\n".join(blocks) + "\n\nPhotos: Wikimedia Commons — see [[Image Credits]]."


def listen_section(w):
    phrases = [t.strip() for t in dict.fromkeys(ITALIC.findall(w["lesson"].replace("**", ""))) if play(t)]
    if not phrases:
        return ""
    return "> [!example]- 🔊 Listen: lesson phrases\n" + "\n".join(f"> - *{t}* {play(t)}" for t in phrases)


def listen_box(title, texts):
    """Collapsed callout of audio players. Obsidian can't play audio inside a table cell, so tables point here."""
    lines = [f"> - **{t}** {play(t)}" for t in dict.fromkeys(texts) if play(t)]
    return f"> [!example]- {title}\n" + "\n".join(lines) if lines else ""


def say_first_section(w):
    rows = [f"| **{x['es']}** | {x['say']} |" for x in w["say_first"]]
    if not rows:
        return ""
    return ("## 🔤 Say it first\nSay each word out loud **before** listening. Syllables are split with · and the stressed one is in CAPITALS.\n\n"
            "| Word | Say it |\n|---|---|\n" + "\n".join(rows) + "\n\n" + listen_box("🔊 Now check yourself", [x["es"] for x in w["say_first"]]))


def grammar_section(w):
    if not w["grammar"]:
        return ""
    lines = [f"> - ✅ *{g['ok']}* {play(g['ok'])} — ❌ ~~{g['bad'][0]}~~ — {g['x']}" for g in w["grammar"]]
    return "> [!question]- ✅ Grammar check: correct vs incorrect (quiz yourself on the site first)\n" + "\n".join(lines)


def cyber_section(w):
    c = w["cyber"]
    if not c:
        return ""
    terms = "\n".join(f"| {es} | {say} | {en} |" for (es, en), say in zip(c["terms"], c["say"]))
    examples = "\n".join(f"- *{es}* — {en} {play(es)}" for es, en in c["examples"])
    return f"""## 🛡️ Cybersecurity vocabulary
{c['focus']}

| Español | Say it | English |
|---|---|---|
{terms}

{listen_box("🔊 Listen: vocabulary", [es for es, _ in c["terms"]])}

**Using this week's grammar:**
{examples}

Full list: [[Cybersecurity Glossary]] · Teaching: [[Classroom Phrases]]"""


def glossary_note():
    out = ["# Cybersecurity Glossary", "Every cybersecurity/networking term from the course, grouped by week.", ""]
    for w in (w for w in COURSE if w["cyber"]):
        out += [f"## Week {w['week']}: {w['title']}", "| Español | English |", "|---|---|"]
        out += [f"| {es} | {en} |" for es, en in w["cyber"]["terms"]]
        out.append("")
    return "\n".join(out)


# R Trill Lab: several independent ways into the rolled r, a graded word ladder and a daily routine.
RR_LAB = {
    "intro": "The rolled **rr** isn't strength — it's a **relaxed tongue tip flapping in a stream of air**, like a flag in the wind. Most adults can't do it at first; many take 1–3 months of a few minutes a day. Spanish-speaking kids are often 5 or 6 before they get it. Try every technique below — different ones click for different people — and practice **5 minutes a day** rather than 30 minutes once a week.",
    "routine": [
        "1 min — **Find the spot**: tongue taps on the ridge behind your top teeth (*de, de, de*)",
        "1 min — **Taps**: butter, pot of tea, then *pero, para, cara*",
        "1 min — **Launch** off tr / dr: *tres, otro, padre*",
        "1 min — **Air + relax**: long breath out, loose tongue, let it flutter",
        "1 min — **Your current ladder stage** + one tongue twister, recorded with 🎙",
    ],
    "techniques": [
        {"name": "1. Find the spot", "why": "The trill happens in one place: the bumpy ridge just behind your top front teeth (where you say t and d). If your tongue is anywhere else, nothing will vibrate.",
         "steps": ["Say \"t\" and \"d\" a few times and notice where the tip of your tongue touches — that's the spot.",
                   "Let the sides of your tongue rest against your upper side teeth; only the tip should be free.",
                   "Keep your jaw slightly open and the tip of your tongue loose, not pressed.",
                   "Tap the spot lightly and quickly: \"d-d-d-d,\" like a tiny drum roll."],
         "say": ["de, de, de, de", "te, de, te, de"]},
        {"name": "2. The butter tap — you already know the single r", "why": "The American \"tt\" in butter and \"dd\" in ladder is exactly the Spanish single r. Get the tap first — the trill is just several taps in a row.",
         "steps": ["Say \"butter, butter, butter\" fast, the American way (\"budder\"). Feel the one quick flick.",
                   "Say \"ladder\" and \"water\" the same way.",
                   "Now say *pero* using that flick: pe-(flick)-o. That's correct Spanish!",
                   "Do it with *para*, *cara*, *hora*."],
         "say": ["pero", "para", "cara", "hora", "toro"]},
        {"name": "3. \"Pot of tea\" faster and faster", "why": "Repeating a phrase with flaps gets your tongue flicking in a rhythm, and speed turns the separate flicks into a trill.",
         "steps": ["Say \"pot of tea\" slowly, then faster: \"pod-a-tea, pod-a-tea.\"",
                   "Keep speeding up until it becomes \"p-d-d-tea.\"",
                   "Do the same with \"gotta go, gotta go\" and \"edda, edda, edda.\"",
                   "When the middle part blurs into a buzz — you just trilled. Stretch that buzz out."],
         "say": ["era, era, era", "arriba"]},
        {"name": "4. Launch off T and D", "why": "t and d put your tongue in the exact spot and release a burst of air — a running start into the trill.",
         "steps": ["Say \"tree\" but hold and exaggerate the middle: \"t-rrrr-ee.\"",
                   "Say \"dream\" the same way: \"d-rrrr-eam.\"",
                   "Now Spanish words: *tres* (t-rrr-es), *otro*, *padre*.",
                   "Once the buzz shows up after t or d, try to keep it going for a second.",
                   "In real speech *tres* and *otro* use a quick single tap — the long buzz is only a practice trick."],
         "say": ["tres", "tren", "otro", "cuatro", "padre", "dragón"]},
        {"name": "5. Brrr, it's cold!", "why": "b, g and p before r build air pressure behind the tongue, which helps start the vibration.",
         "steps": ["Shiver and say \"brrr\" — but make the buzz with your tongue tip, not your lips.",
                   "Do \"grrr\" like an angry dog (tongue tip, not throat).",
                   "Spanish: *brazo*, *grande*, *primo*, *gracias*, *frío*."],
         "say": ["brazo", "grande", "primo", "gracias", "frío"]},
        {"name": "6. Air power + relax", "why": "The trill is driven by air, not muscle. If your tongue is tense it can't flap. Strong steady air + a loose tongue = vibration.",
         "steps": ["Put your tongue on the spot, barely touching.",
                   "Take a deep breath and blow out steadily, like blowing out birthday candles.",
                   "Let the air push the tongue tip so it flutters — don't try to move it yourself.",
                   "Try starting with a breathy \"h\": \"h-rrrr,\" or with a vowel: \"ah-rrrr.\"",
                   "If nothing happens, relax more and blow harder. It often comes as 2–3 flaps at first — that counts!"],
         "say": ["arriba", "error", "carro"]},
        {"name": "7. Vowel running start", "why": "A vowel before the rr gives your tongue momentum and plenty of air.",
         "steps": ["Stretch the word: \"a-rrrr-iba,\" \"e-rrrr-or,\" \"pe-rrrr-o.\"",
                   "Exaggerate the rr far longer than real speech, then shorten it to normal.",
                   "Compare the tap and the trill: *pero / perro*."],
         "say": ["arriba", "error", "perro", "carro", "tierra", "guerra"]},
    ],
    "ladder": [
        {"stage": "Stage 1 — Single tap (you can already do this)", "words": ["pero", "para", "cara", "hora", "toro", "mira"]},
        {"stage": "Stage 2 — After t / d (stretch it to practice; normally a tap)", "words": ["tres", "otro", "cuatro", "padre", "dragón", "tren"]},
        {"stage": "Stage 3 — After b, g, p, f, c (stretch it to practice; normally a tap)", "words": ["brazo", "grande", "primo", "gracias", "frío", "crear"]},
        {"stage": "Stage 4 — rr between vowels", "words": ["perro", "carro", "tierra", "arriba", "error", "guerra"]},
        {"stage": "Stage 5 — r at the start of a word (always rolled)", "words": ["rojo", "red", "rápido", "rosa", "ratón", "Roberto"]},
        {"stage": "Stage 6 — r after n, l, s (always rolled)", "words": ["enrutador", "honra", "alrededor", "Israel", "Enrique", "sonreír"]},
        {"stage": "Stage 7 — Tap vs trill pairs", "words": ["pero, perro", "caro, carro", "cero, cerro", "coro, corro", "para, parra"]},
        {"stage": "Stage 8 — Cybersecurity words", "words": ["la red", "el error", "el registro", "respaldar", "el correo", "rastrear", "robar"]},
    ],
    "twisters": [
        "Erre con erre, cigarro; erre con erre, barril.",
        "Rápido ruedan los carros cargados de azúcar del ferrocarril.",
        "El perro de San Roque no tiene rabo, porque Ramón Ramírez se lo ha robado.",
        "Tres tristes tigres tragaban trigo en un trigal.",
    ],
    "troubleshooting": [
        ("My tongue only taps once.", "You're close! Use more air and less tension. A trill is just 2–5 taps — keep blowing after the first one."),
        ("It sounds like a gargle or a French r.", "That's the back of your throat. Move it to the tongue tip: start from t or d (technique 4)."),
        ("I get \"brrr\" with my lips.", "That's a lip trill. Keep your lips relaxed and slightly open, and raise your tongue tip to the spot."),
        ("My tongue gets tired or tense.", "Stop for today. 5 minutes daily beats long sessions. Tension is the #1 thing that blocks the trill."),
        ("Nothing works sitting at a desk…", "Try lying on your back — gravity relaxes the tongue and some people get their first trill this way."),
        ("It's been weeks and I still can't.", "Normal for adults. Keep going daily. Meanwhile a strong single tap is understood — context tells pero from perro — and some native speakers don't trill the textbook way either."),
    ],
}


def alphabet_note():
    out = ["# Alphabet & Letter Sounds", "Every letter: its Spanish name, how it sounds, and examples (stressed syllable in CAPS).",
           "Interactive version with quick-fire drills and a username speller: site → Week 0 → 🎯 Drills.", "",
           "| Letter | Name | Sounds like | Examples |", "|---|---|---|---|"]
    for d in DRILLS["alphabet"]:
        ex = "<br>".join(f"{e} ({say})" for e, say in zip(d["examples"], d["say"]))
        tip = f"<br>💡 {d['tip']}" if d["tip"] else ""
        out.append(f"| **{d['letter']}** | {d['name']} | {d['sound']}{tip} | {ex} |")
    out += ["", listen_box("🔊 Listen: letter names", [d["name"] for d in DRILLS["alphabet"]]),
            "", listen_box("🔊 Listen: example words", [e for d in DRILLS["alphabet"] for e in d["examples"]])]
    symbols = [(k if k != " " else "space", v) for k, v in SPELL.items() if not k.isalnum()]
    out += ["", "## Spelling things out loud", "| Symbol | Say |", "|---|---|", *[f"| `{k}` | {v} |" for k, v in symbols],
            "", listen_box("🔊 Listen: symbol names", [v for _, v in symbols])]
    out += ["", "Capital letters: add *mayúscula* after the letter (P → *pe mayúscula*). Accented letters: *a con tilde*.",
            "Say **be larga** for B and **ve corta** for V when spelling, so they can't be confused.", "", "Back to [[Week 00 - Alphabet & Pronunciation]]"]
    return "\n".join(out)


def rr_texts():
    texts = [t for tech in RR_LAB["techniques"] for t in tech["say"]]
    texts += [w for stage in RR_LAB["ladder"] for w in stage["words"]] + RR_LAB["twisters"]
    return list(dict.fromkeys(texts))


def rr_note():
    def slow(t):
        f = MEDIA["audio"].get("slow:" + t)
        return f"![[{Path(f).name}]]" if f else ""

    out = ["# Rolling Your R — R Trill Lab", RR_LAB["intro"], "",
           "Practice on the site: home page → **🌀 R Trill Lab** (has 🐢 slow audio and 🎙 record-yourself).", "",
           "## Daily 5-minute routine", *[f"{i + 1}. {r}" for i, r in enumerate(RR_LAB["routine"])], ""]
    out.append("## Techniques — try them all")
    for tech in RR_LAB["techniques"]:
        out += [f"### {tech['name']}", f"*Why it works:* {tech['why']}", "", *[f"{i + 1}. {s}" for i, s in enumerate(tech["steps"])], ""]
        out += [f"- **{t}** {play(t)} 🐢 {slow(t)}" for t in tech["say"]] + [""]
    out.append("## Practice ladder — move up when the current stage feels easy")
    for stage in RR_LAB["ladder"]:
        out += [f"### {stage['stage']}", *[f"- **{t}** — {say_it(t)} {play(t)} 🐢 {slow(t)}" for t in stage["words"]], ""]
    out += ["## Tongue twisters", *[f"- *{t}* {play(t)} 🐢 {slow(t)}" for t in RR_LAB["twisters"]], ""]
    out += ["## Troubleshooting", *[f"- **{q}** {a}" for q, a in RR_LAB["troubleshooting"]], "",
            "Log each practice on the site (R Trill Lab → *Log today's practice*) so it shows in [[Study Log]].", "Back to [[Week 00 - Alphabet & Pronunciation]]"]
    return "\n".join(out)



def lesson_note(w):
    i = COURSE.index(w)
    prev_link = f"[[{note_name(COURSE[i - 1])}|← Week {w['week'] - 1}]]" if i > 0 else ""
    next_link = f"[[{note_name(COURSE[i + 1])}|Week {w['week'] + 1} →]]" if i + 1 < len(COURSE) else ""
    nav = " · ".join(x for x in [prev_link, "[[Dashboard]]", next_link] if x)
    return f"""---
week: {w['week']}
phase: {json.dumps(f"{w['phase']} - {PHASES[w['phase']]}", ensure_ascii=False)}
topic: {json.dumps(w['title'], ensure_ascii=False)}
tags: [spanish, lesson, phase{w['phase']}]
---
# Week {w['week']}: {w['title']}
{nav}

**Goal:** {w['goal']}

{say_first_section(w)}

{photo_section(w)}

{w['lesson'].strip()}

{listen_section(w)}

{cyber_section(w)}

{grammar_section(w)}

## Practice task
{w['practice']}

Your saved practice writing: [[Practice/{note_name(w)} - Practice]]

## My notes
-
"""


REFERENCE = {
    "Verb Endings Cheat Sheet": """
# Verb Endings Cheat Sheet
Endings for regular verbs. Order: yo / tú / él·ella·usted / nosotros / ellos·ustedes.

| Tense | -ar | -er | -ir |
|---|---|---|---|
| Present | o, as, a, amos, an | o, es, e, emos, en | o, es, e, imos, en |
| Preterite | é, aste, ó, amos, aron | í, iste, ió, imos, ieron | í, iste, ió, imos, ieron |
| Imperfect | aba, abas, aba, ábamos, aban | ía, ías, ía, íamos, ían | ía, ías, ía, íamos, ían |
| Future (on the whole infinitive) | é, ás, á, emos, án | é, ás, á, emos, án | é, ás, á, emos, án |
| Present subjunctive | e, es, e, emos, en | a, as, a, amos, an | a, as, a, amos, an |

| Compound forms | Pattern | Example |
|---|---|---|
| Right now | estar + -ando / -iendo | está comiendo |
| Going to | ir + a + infinitive | va a comer |
| Has done | haber (he, has, ha, hemos, han) + -ado / -ido | ha comido |
| Just did | acabar de + infinitive | acaba de comer |

See also: [[@present-regular]], [[@progressive]], [[@ir-a]], [[@future]], [[@preterite]], [[@imperfect]], [[@perfect]], [[@timeline]], [[@teach-advice]]
""",
    "Sentence Structure by Tense": """
# Sentence Structure by Tense
**The big idea:** the sentence order stays the same in every tense. Only the **end of the verb** changes,
and that ending tells you two things: **who** did it and **when**.

## 1. The sentence skeleton (same for present, past and future)
| (Who) | (no) | (him/it…) | **VERB** | (the rest) | (when) |
|---|---|---|---|---|---|
| Tío Beto | | | **come** | tacos | hoy. |
| Doña Rosa | no | lo | **vio** | | ayer. |
| Valeria | | | **va a volver** | a la ciudad | mañana. |

- **Who** is optional — the ending already says it: *Comió tacos* = he/she ate tacos.
- **no** always goes right before the verb (or before *lo / la / le / se* if there is one).
- **Questions** use the same order, just with ¿…? and a rising voice: *¿Javi llegó ayer?* You can also flip it: *¿Llegó Javi?*
- Describing words come **after** the noun: *un vecino nuevo*, *la comida rica*.

## 2. The rule for the end of the verb
1. Take the infinitive: habl**ar**, com**er**, viv**ir**.
2. Chop off **-ar / -er / -ir** → the stem: *habl-, com-, viv-*. (Future is the exception — keep the whole word.)
3. Add the ending for **when** + **who**.

### The "who" clues that never change
These hold in present, past and future, so learn them once:
| Who | Clue | Examples |
|---|---|---|
| tú (you) | ends in **-s** | hablas, hablabas, hablarás (*only exception: past* habla**ste**) |
| nosotros (we) | ends in **-mos** | hablamos, hablábamos, hablaremos |
| ellos / ustedes (they / you all) | ends in **-n** | hablan, hablaron, hablarán |

So only **yo** and **él / ella / usted** really change from tense to tense.

### The "when" clues
| When | Clue to spot | doña Rosa *habla* (talks) | tío Beto *come* (eats) |
|---|---|---|---|
| **Now / usually** (present) | plain vowel: **-a** for -ar, **-e** for -er/-ir; yo = **-o** | habla · yo hablo | come · yo como |
| **Right now** | estar + **-ando / -iendo** | está hablando | está comiendo |
| **Did, once, done** (preterite) | **accent on the last letter**: yo **-é / -í**, él **-ó / -ió** | habló · yo hablé | comió · yo comí |
| **Used to / was …ing** (imperfect) | **-aba-** (for -ar) or **-ía-** (for -er/-ir) in the middle; yo = él | hablaba | comía |
| **Has done** | ha + **-ado / -ido** | ha hablado | ha comido |
| **Going to** | va a + **whole infinitive** | va a hablar | va a comer |
| **Will** (future) | **whole infinitive + accented ending**: é, ás, á, emos, án | hablará · yo hablaré | comerá · yo comeré |

## 3. Memory tricks
- **"-s you, -mos us, -n them."** Say it until it sticks; it works in nearly every tense.
- **Accent at the end = it's finished.** *pasó, comió, llegó, se fue* — the voice lands hard on the end like a door slamming.
- **-aba / -ía = a long, blurry memory.** The imperfect sets the scene ("Valeria **vivía** aquí…"), the preterite is the event ("…y un día **se fue**").
- **Future = the whole verb + haber's endings.** *he, has, ha, hemos, han* minus the h → *é, ás, á, emos, án*: comer**é**, comer**ás**, comer**á**.
- **Stuck on the future? Use *va a*.** *Va a comer* is always correct and needs no new endings — conjugate *ir* and keep the infinitive.
- **Same base, different tense with ha / está / va a:** only the helper changes for who; the main verb keeps one fixed shape (*comido / comiendo / comer*).

## 4. Watch out
- **-ar and -ir:** *hablamos / vivimos* means both "we talk" and "we talked". The time word (*hoy* vs *ayer*) tells you which.
- **Accents matter:** *hablo* (I talk) vs *habló* (he talked). Stress the end for the past.
- **Irregular verbs** change the stem but mostly keep the who-clues: *tuvo, vino, dijeron, fueron*. Irregular preterites drop the accent: *tuve, vino*.

## 5. Time words that point to the tense
| Word | Tense to use |
|---|---|
| hoy, ahora, siempre, todos los días | present (or *está + -ando* for right now) |
| ayer, anoche, la semana pasada, de repente | preterite — *¿Qué pasó?* |
| antes, de niño, siempre (in the past), mientras | imperfect — *¿Cómo era?* |
| ya, todavía no, hoy (already happened) | has done — *ha + -ado* |
| mañana, la próxima semana, pronto | *va a* + infinitive, or the future |

## 6. Upgrade your verbs: base verb → action verb
Base verbs (*decir, ver, ir, comer…*) are always correct, but they're flat. Swap in a more specific action verb
to sound like a real chismoso. **Good news:** most upgrades are regular **-ar** verbs, so the endings above work unchanged.
⚠️ = stem change or irregular — check the lesson before using it in the past.

| Base verb | Upgrade to… | Example |
|---|---|---|
| **decir** (say) | **contar** ⚠️ (tell a story, o→ue), **susurrar** (whisper), **gritar** (shout), **comentar** (mention), **confesar** ⚠️ (confess, e→ie), **chismear** (gossip) | Doña Rosa **susurró**: "Valeria se fue." |
| **hablar** (talk) | **platicar** (chat — very Mexican), **charlar** (chat), **discutir** (argue), **chismear** (gossip) | Marco y Lucía **discutieron** anoche. |
| **ver** (see) | **mirar** (look at), **observar** (watch closely), **notar** (notice), **espiar** (spy on), **fijarse en** (notice) | Doña Rosa **espía** por la ventana. |
| **saber** (know) | **enterarse de** (find out, hear about), **descubrir** (discover), **averiguar** (figure out) | ¿Te **enteraste** de lo de Javi? |
| **ir** (go) | **salir** ⚠️ (go out, yo salgo), **correr** (run), **irse** ⚠️ (leave), **mudarse** (move house), **escaparse** (sneak off) | Valeria **se mudó** sin decir nada. |
| **venir / llegar** (come / arrive) | **aparecer** ⚠️ (show up, yo aparezco), **volver / regresar** (come back), **asomarse** (peek out) | Javi **apareció** a medianoche. |
| **comer** (eat) | **devorar** (devour), **probar** ⚠️ (taste/try, o→ue), **picar** (snack), **tragar** (wolf down), **almorzar / cenar** (have lunch / dinner) | Tío Beto **devoró** tres tamales. |
| **hacer** (do / make) | **cocinar** (cook), **preparar** (prepare), **arreglar** (fix, tidy), **organizar** (organize) | Lucía **preparó** pozole para todos. |
| **tener** (have) | **guardar** (keep), **esconder** (hide), **conseguir** ⚠️ (get, e→i) | Marco **esconde** algo. |
| **poner** (put) | **dejar** (leave something), **meter** (put inside), **colocar** (place) | **Dejó** una carta en la puerta. |
| **gustar** (like) | **encantar** (love), **fascinar** (fascinate), **molestar** (bother) — same pattern as gustar | A doña Rosa le **encanta** el chisme. |

### How to practice the upgrade
1. Write a flat sentence: *Doña Rosa dijo que Javi llegó tarde.*
2. Upgrade each base verb: *Doña Rosa **susurró** que Javi **apareció** a las tres.*
3. Say it in three tenses (section 2): *susurra · susurró · va a susurrar*.

Add the new verbs to [[Vocab]] as you start using them.

## 7. El gerundio — the -ing form (*-ando / -iendo*)
The gerundio is the Spanish **-ing**: *comiendo* = eating, *espiando* = spying. It never changes for who —
only the helper verb does: *estoy / estás / está / estamos / están* **comiendo**. Full lesson: [[@progressive]]

### How to make it
| Verb type | Rule | Examples |
|---|---|---|
| **-ar** | drop -ar, add **-ando** | susurrar → **susurrando**, cocinar → **cocinando** |
| **-er / -ir** | drop the ending, add **-iendo** | comer → **comiendo**, descubrir → **descubriendo** |
| stem ends in a vowel | the **i** turns into **y**: **-yendo** | leer → **leyendo**, oír → **oyendo**, ir → **yendo** |
| **-ir** stem-changers | e → i, o → u | decir → **diciendo**, conseguir → **consiguiendo**, dormir → **durmiendo**, venir → **viniendo** |

**Shortcut:** -ar and -er stem-changers do **not** change here: contar → **contando**, probar → **probando**, volver → **volviendo**. Only **-ir** verbs change.

### Your upgrade verbs as gerundios
| Base verb | Upgrades in the gerundio |
|---|---|
| decir → **diciendo** | contando, susurrando, gritando, comentando, confesando, chismeando |
| hablar → **hablando** | platicando, charlando, discutiendo |
| ver → **viendo** | mirando, observando, notando, espiando, fijándose en |
| saber → **sabiendo** | enterándose de, descubriendo, averiguando |
| ir → **yendo** | saliendo, corriendo, yéndose, mudándose, escapándose |
| venir / llegar → **viniendo / llegando** | apareciendo, volviendo, regresando, asomándose |
| comer → **comiendo** | devorando, probando, picando, tragando, almorzando, cenando |
| hacer → **haciendo** | cocinando, preparando, arreglando, organizando |
| tener → **teniendo** | guardando, escondiendo, consiguiendo |
| poner → **poniendo** | dejando, metiendo, colocando |

### Where *se / lo / la* go
Two options, same meaning — before *estar*, or glued to the end of the gerundio (add an accent to keep the stress):
- *Valeria **se** está mudando.* = *Valeria está mudándo**se**.* — Valeria is moving out.
- *Doña Rosa **lo** está espiando.* = *Doña Rosa está espiándo**lo**.* — Doña Rosa is spying on him.

### More than *estar*
| Pattern | Meaning | Example |
|---|---|---|
| estaba + gerundio | was …ing (sets the scene) | *Estaba cenando cuando Javi apareció.* |
| seguir + gerundio | still …ing, keeps on | *Tío Beto sigue comiendo.* |
| llevar + time + gerundio | has been …ing for | *Doña Rosa lleva dos horas chismeando.* |
| andar + gerundio | goes around …ing (very Latin American) | *Javi anda diciendo cosas raras.* |
| pasar + time + gerundio | spends (time) …ing | *Pasa el día espiando a los vecinos.* |

### Traps — where English *-ing* is NOT the gerundio
- **-ing as a noun → use the base verb.** "Gossiping is fun" → *Chismear es divertido* (not ~~chismeando~~). "I like eating" → *Me gusta comer*.
- **-ing for plans → use the present or *va a*.** "I'm leaving tomorrow" → *Me voy mañana* (not ~~me estoy yendo mañana~~).
- **After *antes de / después de / sin* → base verb.** "before eating" → *antes de comer*; "without saying anything" → *sin decir nada*.

## 🗣️ El chisme in every tense
- Doña Rosa **habla** de todos. (present)
- Ayer doña Rosa **habló** con Javi. (preterite)
- Antes doña Rosa **hablaba** con Valeria todos los días. (imperfect)
- Doña Rosa **ha hablado** con medio barrio. (has done)
- Mañana doña Rosa **va a hablar** con Marco y Lucía. (going to)
- Doña Rosa **hablará** con todos. ¡Siempre! (future)

Endings table: [[Verb Endings Cheat Sheet]] · Lessons: [[@present-regular]], [[@progressive]], [[@ir-a]], [[@future]], [[@preterite]], [[@imperfect]], [[@perfect]], [[@timeline]]
""",
    "Describing & Comparing": """
# Describing & Comparing
Articles, *my / your*, *this / that*, comparing people (*más chismoso que…*) and *-mente* adverbs.

## 1. Articles: "the" and "a"
| | masculine | feminine |
|---|---|---|
| the (one) | **el** vecino | **la** vecina |
| the (many) | **los** vecinos | **las** vecinas |
| a / an | **un** taco | **una** torta |
| some | **unos** tacos | **unas** tortas |

- **a + el = al**, **de + el = del**: *Voy **al** mercado.* *Es la casa **del** tío Beto.* (Not with *él* "him": *de él*.)
- Feminine words that start with a stressed *a-* take *el* in the singular: *el agua fría*, *el hambre*.
- Spanish says "the" for things in general: *Me gustan **los** tacos.* (I like tacos.) And for days: *el lunes* = on Monday.
- Spanish drops "a" for jobs after *ser*: *Lucía es doctora.* (Lucía is a doctor.)

## 2. Possessives: my, your, his, our
| owner | before the noun | after the noun / alone |
|---|---|---|
| yo | **mi**, mis | mío, mía, míos, mías |
| tú | **tu**, tus | tuyo, tuya… |
| él / ella / usted / ellos / ustedes | **su**, sus | suyo, suya… |
| nosotros | **nuestro**, nuestra, nuestros, nuestras | nuestro… |

- They match the **thing owned**, not the owner: *nuestras tías*, *sus tamales*.
- *su* can mean his / her / your / their. To be clear, say *la casa **de ella***.
- Long forms: *¿Es **tuyo** este taco?* — *Sí, es **mío**.* · *un amigo **mío*** (a friend of mine).

## 3. This, that, that over there
| | near me (aquí) | near you (ahí) | over there (allá) |
|---|---|---|---|
| masc. | **este**, estos | **ese**, esos | **aquel**, aquellos |
| fem. | **esta**, estas | **esa**, esas | **aquella**, aquellas |
| an idea | **esto** | **eso** | **aquello** |

- *¿Quién es **ese** chico?* — *Es Javi.* · ***Aquella** casa era de Valeria.*
- For ideas and things you can't name: *¿Qué es **eso**?* · *¡**Eso** es mentira!*

## 4. Comparing
- **más / menos … que**: *Tío Beto come **más que** Javi.* · *Javi es **más** alto **que** Marco.*
- **tan + describing word + como** (as … as): *Javi es **tan** chismoso **como** doña Rosa.*
- **tanto / tanta / tantos / tantas + noun + como** (as much / many … as): *Nadie come **tantos** tamales **como** Beto.*
- Irregular: **mejor** (better), **peor** (worse), **mayor** (older), **menor** (younger): *El pozole de Lucía es **mejor que** el de Marco.*
- With a number use **más de**: *Comió **más de** diez tacos.*

## 5. The most: superlatives and -ísimo
- **el / la / los / las + más + describing word + de**: *Doña Rosa es **la más chismosa del** barrio.* (Spanish uses *de*, not "in".)
- **-ísimo** = extremely: *rico → riquísimo*, *bueno → buenísimo*, *fácil → facilísimo*, *largo → larguísimo*. *¡Este mole está **buenísimo**!*

## 6. Adverbs: -mente = -ly
Feminine form + **-mente**: *rápido → rápidamente*, *tranquilo → tranquilamente*, *fácil → fácilmente* (keeps its accent).
- Two in a row: only the last one gets it: *lenta y cuidadosamente*.
- Everyday ones without -mente: *bien, mal, muy, mucho, poco, despacio*. In speech *rápido* works too: *Habla rápido.*

## ✍️ Try it
1. Doña Rosa es ___ chismosa ___ barrio. (the most … in the)
2. ¿Es ___ (your) taco? — Sí, es ___ (mine).
3. Marco es ___ alto ___ Javi. (as … as)
4. ¡Estos tacos están ___! (extremely good)
> Answers: 1. la más … del · 2. tu … mío · 3. tan … como · 4. buenísimos

Lessons: [[@nouns]], [[@ser-estar]], [[@present-regular]]
""",
    "Numbers, Time & Dates": """
# Numbers, Time & Dates
Numbers, telling time, days and dates, and *hace* for "ago".

## 1. Numbers 0–29
| 0–9 | 10–15 | 16–19 | 20–29 |
|---|---|---|---|
| cero, uno, dos, tres, cuatro | diez, once, doce | dieciséis, diecisiete | veinte, veintiuno |
| cinco, seis, siete, ocho, nueve | trece, catorce, quince | dieciocho, diecinueve | veintidós, veintitrés… veintinueve |

16–29 are written as **one word**.

## 2. 30 and up
- Tens + **y** + ones: *treinta y uno*, *cuarenta y dos*, *cincuenta*, *sesenta*, *setenta*, *ochenta*, *noventa*.
- **cien** = exactly 100; **ciento** after that: *ciento uno*, *ciento cincuenta*.
- Hundreds: *doscientos, trescientos, cuatrocientos,* **quinientos**, *seiscientos,* **setecientos**, *ochocientos,* **novecientos** — they agree: *doscientas personas*.
- *mil* (1,000), *dos mil*, *un millón de pesos*.
- *uno* becomes **un / una** before a noun: *veintiún años*, *veintiuna personas*.
- Mexico writes numbers like the US (1,500.50); much of South America swaps them (1.500,50).

## 3. First, second, third
*primero (**primer** before a masc. noun), segundo, tercero (**tercer**), cuarto, quinto, sexto, séptimo, octavo, noveno, décimo.*
- *Marco y Lucía viven en el **tercer** piso.* After ten, people just use the number: *el piso doce*.
- Dates use plain numbers except the 1st: *el **primero** de mayo*, *el dos de mayo*.

## 4. Telling time
- *¿Qué hora es?* — *Es **la** una.* (only for 1) · *Son **las** dos.* · *Son las tres **y cuarto**.* · *Son las cuatro **y media**.*
- Before the hour (Latin America): *Son **cuarto para** las cinco.* / *Faltan quince **para** las cinco.*
- *de la mañana / de la tarde / de la noche*, *mediodía*, *medianoche*.
- At what time: *¿**A qué hora** llegó Javi?* — ***A las** tres de la mañana.*
- In the past use the imperfect: ***Eran** las tres cuando Javi llegó.*

## 5. Days, months and dates
- Days (lowercase): *lunes, martes, miércoles, jueves, viernes, sábado, domingo*. ***el** lunes* = on Monday, ***los** lunes* = on Mondays.
- Months (lowercase): *enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre*.
- *¿Qué fecha es hoy?* — *Hoy es el doce de noviembre.*
- Years are full numbers: 2026 = *dos mil veintiséis*.

## 6. Ago and "for": hace
- **Ago** = *hace* + time + preterite: *Valeria se fue **hace** dos meses.* = ***Hace** dos meses **que** se fue.*
- **For (and still going)** = *hace* + time + *que* + present: ***Hace** un año **que** vivo aquí.* = *Vivo aquí **desde hace** un año.* = ***Llevo** un año aquí.*
- *¿**Cuánto tiempo hace que** conoces a Javi?*

## 7. Age and money
- *Tengo treinta años.* (Age uses *tener*.) · *¿Cuántos años tiene doña Rosa?*
- *¿**Cuánto cuesta**?* — *Cuesta cincuenta pesos.* · *¿Cuánto es?*

## ✍️ Try it
1. 47 → ___
2. It's 2:30. → ___
3. Valeria left three weeks ago. → Valeria se fue ___
4. I've lived here for two years. → ___ dos años ___ vivo aquí.
> Answers: 1. cuarenta y siete · 2. Son las dos y media. · 3. hace tres semanas · 4. Hace … que

Lessons: [[@ser-estar]], [[@irregulars]], [[@preterite]]
""",
    "Little Words — Negatives, Connectors & Prepositions": """
# Little Words — Negatives, Connectors & Prepositions
The short words that hold sentences together: *nadie, pero, sino, debajo de, que, lo que*.

## 1. Negatives — the double negative is correct
| positive | negative |
|---|---|
| algo (something) | **nada** (nothing) |
| alguien (someone) | **nadie** (no one) |
| siempre (always) | **nunca** / jamás (never) |
| también (also) | **tampoco** (neither) |
| algún, alguna (some) | **ningún, ninguna** (none, not any) |
| o … o (either … or) | **ni … ni** (neither … nor) |

- Negative word **after** the verb → you need *no* in front: ***No** vi a **nadie**.* · ***No** dijo **nada**.*
- Negative word **before** the verb → no *no*: ***Nunca** sale.* = ***No** sale **nunca**.*
- *A mí **tampoco**.* (Me neither.) · ***Ni** Marco **ni** Lucía saben.* · *No hay **ningún** problema.*

## 2. Connectors
- **y** (and) → **e** before an "ee" sound: *padres **e** hijos*, *Valeria **e** Isabel*.
- **o** (or) → **u** before an "o" sound: *siete **u** ocho*.
- **pero** (but) vs **sino** (but rather, after a *no*): *Es raro, **pero** simpático.* · *No es tímido, **sino** misterioso.*
- **porque** (because) — **por qué** (why).
- **como** (since, at the start): ***Como** no llamó, me preocupé.*
- **aunque** (although), **así que** (so), **entonces** (so, then), **mientras** (while), **cuando** (when), **si** (if).
- Filler words you'll hear: *bueno* (well, ok), *pues* (well), *o sea* (I mean), *este…* (umm, Mexico).

## 3. Where things are
| | |
|---|---|
| **en** — in / on / at | **al lado de** — next to |
| **encima de** / **sobre** — on top of | **entre** — between |
| **debajo de** — under | **cerca de** / **lejos de** — near / far from |
| **delante de** — in front of | **dentro de** / **fuera de** — inside / outside |
| **enfrente de** — across from | **detrás de** — behind |

- *Doña Rosa vive **enfrente de** Marco y Lucía.* · *El gato está **debajo de** la mesa.* · *Javi vive **al lado del** mercado.*
- Other key ones: *a* (to), *de* (of, from), *con* (with), *sin* (without), *desde* (since, from), *hasta* (until), *sobre* (about): *Hablan **sobre** Valeria.* For *por / para* see Week 19.

## 4. The personal "a"
When the object is a **person**, put **a** in front: *Vi **a** Javi.* · *Conozco **a** doña Rosa.*
Not for things: *Vi el carro.* And not after *tener*: *Tengo dos hermanos.*

## 5. Joining ideas: que, quien, lo que, donde
- **que** = that / who / which (the most common): *El chico **que** vive en el 4A es Javi.* — Spanish **never** drops it: "the guy I saw" = *el chico **que** vi*.
- **quien / quienes** for people after *con, a, de*: *la vecina **con quien** hablé*.
- **lo que** = what, the thing that: *No sé **lo que** pasó.* · ***Lo que** dijo es mentira.*
- **donde** = where: *el mercado **donde** trabaja Beto*.

## ✍️ Try it
1. No vi a ___ en la fiesta. (anyone)
2. No es pobre, ___ tacaño. (but rather)
3. Padres ___ hijos. (and)
4. No sé ___ pasó con Valeria. (what)
> Answers: 1. nadie · 2. sino · 3. e · 4. lo que

Lessons: [[@present-regular]], [[@irregulars]], [[@stem-changers]]
""",
    "Tricky Verb Pairs & False Friends": """
# Tricky Verb Pairs & False Friends
Verbs that share one English translation, and Spanish words that look English but aren't.

## 1. Saber vs conocer — both "to know"
| **saber** — facts, info, how to | **conocer** — people, places, being familiar |
|---|---|
| *Sé dónde vive.* | *Conozco a Javi.* |
| *¿Sabes cocinar?* (know how to) | *¿Conoces Oaxaca?* |
| *Doña Rosa lo sabe todo.* | *No conozco ese restaurante.* |

- Irregular *yo*: **sé**, **conozco**.
- In the preterite they shift: **supe** = I found out, **conocí** = I met. *Ayer **supe** que Valeria se fue.* · ***Conocí** a Javi en la fiesta.*

## 2. More pairs
| pair | difference | example |
|---|---|---|
| **pedir / preguntar** | ask *for* something / ask a question | *Pidió más tamales.* · *Me preguntó por Valeria.* (asked about) |
| **llevar / traer** | take (there) / bring (here) | *Lleva el pastel a la fiesta.* · *Trae las tortillas.* |
| **tocar / jugar** | play an instrument, touch / play a game or sport | *Toca la guitarra.* · *Juega fútbol.* |
| **salir / irse / dejar** | go out of / leave, go away / leave something behind, let | *Salió de la casa.* · *Se fue.* · *Dejó a Marco.* · *Déjame ver.* |
| **volver / devolver** | come back / give back | *Volvió tarde.* · *Me devolvió el dinero.* |
| **quedar / quedarse** | be located, arrange to meet / stay | *¿Dónde queda el mercado?* · *Me quedo en casa.* |
| **darse cuenta / realizar** | realize / carry out | *Me di cuenta de que mentía.* |
| **gastar / pasar** | spend money / spend time | *Gastó todo.* · *Pasamos el día juntos.* |
| **oír / escuchar** | hear / listen to | *¿Oíste eso?* · *Escucha bien.* |
| **mirar / ver** | look at / see, watch | *Mira esto.* · *Vemos la tele.* |
| **esperar** | wait, hope **and** expect | *Espero que venga.* |

⚠️ In Mexico and Argentina avoid **coger** (it's vulgar there). Use **tomar** or **agarrar**: *Toma el autobús.*

## 3. False friends
| looks like… | actually means | the word you want |
|---|---|---|
| embarazada | pregnant | avergonzada (embarrassed) |
| actual / actualmente | current / currently | en realidad (actually) |
| éxito | success | salida (exit) |
| librería | bookstore | biblioteca (library) |
| asistir | attend | ayudar (assist) |
| molestar | bother, annoy | acosar (molest) |
| carpeta | folder | alfombra (carpet) |
| recordar | remember | grabar (record) |
| sensible | sensitive | sensato (sensible) |
| lectura | reading | clase / conferencia (lecture) |
| ropa | clothes | cuerda (rope) |
| introducir | insert | presentar (introduce someone) |
| pariente | relative | padre / madre (parent) |

## 4. "To be" in English, other verbs in Spanish
- **tener** for how you feel: *tengo hambre / sed / frío / calor / sueño / miedo / prisa / razón*, *tengo ganas de…* (feel like). See Week 4.
- **hacer** for weather: *Hace calor / frío / sol / viento / buen tiempo.* · *¿Qué tiempo hace?*
- Other weather: *Llueve.* / *Está lloviendo.* · *Está nublado.* · *Hay neblina.*
- Hot three ways: *Tengo calor* (I'm hot) · *Hace calor* (the weather) · *La sopa está caliente* (a thing).

## 5. "To become" — five ways, no single verb
| verb | use it for | example |
|---|---|---|
| **ponerse** + describing word | a quick change of mood or look | *Marco **se puso** rojo.* · *Lucía **se puso** furiosa.* |
| **volverse** + describing word | a big change in who someone is | *Desde que se mudó, Valeria **se volvió** muy creída.* |
| **hacerse** + job / describing word | a change you work for | *Javi **se hizo** famoso en el barrio.* · *Se hizo doctora.* |
| **convertirse en** + noun | turning into something else | *La tienda **se convirtió en** restaurante.* |
| **quedarse** + describing word | how someone ends up after something happens | *Doña Rosa **se quedó** sin palabras.* · *Beto **se quedó** dormido.* |

## ✍️ Try it
1. ¿___ a la novia de Javi? (Do you know — a person)
2. Doña Rosa me ___ por Valeria. (asked about)
3. ___ el pastel a la fiesta, por favor. (Take)
4. Hoy ___ mucho calor. (weather)
> Answers: 1. Conoces · 2. preguntó · 3. Lleva · 4. hace

Lessons: [[@irregulars]], [[@stem-changers]], [[@coming-going]]
""",
    "Pronouns — Lo, Le, Se Lo": """
# Pronouns — Lo, Le, Se Lo
Gossip is all about **who told what to whom**. These short words stand in for people and things so you don't repeat names.

## 1. The two sets
| | direct — *what? whom?* | indirect — *to / for whom?* |
|---|---|---|
| me | **me** | **me** |
| you (tú) | **te** | **te** |
| him / it / you (usted) | **lo** | **le** |
| her / it / you (usted) | **la** | **le** |
| us | **nos** | **nos** |
| them / you all | **los / las** | **les** |

## 2. Direct — the person or thing
- *¿Viste a Javi?* — *Sí, **lo** vi ayer.* (I saw him)
- *¿Probaste el mole?* — *Sí, **lo** probé.* (I tasted it)
- *¿Conoces a Valeria?* — *Sí, **la** conozco.*

## 3. Indirect — to / for whom
- *Doña Rosa **le** contó todo.* (told him / her everything)
- *Javi **me** trajo tamales.* (brought me)
- *¿**Les** dijiste la verdad?* (Did you tell them?)
- Spanish often names the person too — that's normal: ***Le** dije **a Marco** que no.*

## 4. Both together: me lo, te lo, se lo
Order: **indirect before direct**, both before the verb. *Me **lo** dijo.* (He told it to me.)
**le / les + lo / la → se lo / se la.** Never "le lo".
- *¿Le contaste el chisme a Lucía?* — *Sí, **se lo** conté.*
- ***Te lo** juro.* (I swear it to you.) · *¡No **me lo** digas!*

## 5. Where they go
- Before a conjugated verb: ***Lo** vi.* · *No **se lo** dije.*
- Or glued to an infinitive or gerundio (same meaning, add an accent to keep the stress): ***Se lo** voy a decir* = *Voy a decír**selo**.* · ***Se lo** está contando* = *Está contándo**selo**.*
- Glued to yes-commands: *¡Dí**melo**!* (Week 19)

## 6. After prepositions: mí, ti, conmigo
- *para **mí**, para **ti**, para él / ella / usted, para nosotros, para ellos*.
- *con + mí = **conmigo***, *con + ti = **contigo***: *¿Vienes **conmigo**?*
- *entre* uses *tú / yo*: *Esto queda **entre tú y yo**.*
- Extra stress with gustar verbs: ***A mí** me encanta.* (Week 6)

## 7. Each other: se, nos
Plural *se / nos* can mean "each other":
- *Marco y Lucía **se** besaron.* (kissed each other) · *Ya no **se** hablan.* (They don't talk to each other anymore.)
- ***Nos** conocimos en la fiesta.* (We met at the party.)

## ✍️ Try it
1. ¿Viste a Lucía? — Sí, ___ vi.
2. ¿Le dijiste el secreto a Javi? — No, no ___ ___ dije.
3. Javi y Valeria ya no ___ hablan.
4. ¿Vas a la fiesta ___? (with me)
> Answers: 1. la · 2. se lo · 3. se · 4. conmigo

Lessons: [[@gustar]], [[@progressive]], [[@coming-going]], [[@teach-commands]]
""",
    "Would, Had & Must Have — More Tenses": """
# Would, Had & Must Have — More Tenses
*Diría* (would say), *había ido* (had gone), *habrá ido* (must have gone), and the -ing form in other tenses.

## 1. The conditional — "would"
Whole infinitive + **-ía, -ías, -ía, -íamos, -ían**. Irregular stems are the same as the future: *tendr-, saldr-, vendr-, pondr-, podr-, sabr-, querr-, habr-, dir-, har-*.
- **would**: *Yo no le **diría** nada.*
- **polite**: *¿**Podría** pasarme la sal?* · *Me **gustaría** un café.*
- **"would" in reported speech**: *Javi dice que **vendrá*** → *Javi dijo que **vendría**.* (said he would come)
- **guessing about the past**: *¿Dónde **estaría** Valeria anoche?* (I wonder where she was) · ***Serían** las tres.* (It must have been about three.)

## 2. Past perfect — "had done"
**había, habías, había, habíamos, habían** + *-ado / -ido*:
- *Cuando llegué, Valeria ya **se había ido**.*
- *Nunca **había visto** algo así.*

## 3. Past participles as describing words
With *estar*, the *-ado / -ido* form describes a state, and it agrees: *La puerta está **cerrada**.* · *Marco está muy **preocupado**.* · *Los tamales ya están **hechos**.*
Irregulars from Week 14: *abierto, roto, muerto, escrito, visto, puesto, dicho, hecho, vuelto*.

## 4. The -ing form in other tenses
| form | meaning | example |
|---|---|---|
| **estaba** + -ando | was …ing (scene) | *Estaba cenando cuando sonó el teléfono.* |
| **estuvo** + -ando | was …ing (for a set time, over) | *Estuvo hablando dos horas.* |
| **estará** + -ando | will be / must be …ing | *A esta hora estará durmiendo.* |
| **estaría** + -ando | would be …ing / I wonder | *¿Qué estaría haciendo?* |

## 5. Future perfect and conditional perfect
- **habré, habrás, habrá, habremos, habrán** + participle = will have / **must have**: *¿**Habrá llegado** Javi?* (I wonder if he's arrived) · *Ya **se habrá ido**.* (He must have left already.)
- **habría, habrías, habría…** + participle = would have: *Yo no **habría dicho** nada.*

## 6. The whole family
| | simple | with haber |
|---|---|---|
| present | come | ha comido (has eaten) |
| past | comió / comía | había comido (had eaten) |
| future | comerá | habrá comido (will have / must have eaten) |
| conditional | comería | habría comido (would have eaten) |

## ✍️ Try it
1. Yo no le ___ (decir) nada. (would)
2. Cuando llegamos, la fiesta ya ___ ___ (terminar). (had)
3. Javi dijo que ___ (venir). (would)
4. No contesta. ___ ___ (salir). (must have)
> Answers: 1. diría · 2. había terminado · 3. vendría · 4. Habrá salido

Lessons: [[@future]], [[@imperfect]], [[@perfect]], [[@timeline]]
""",
    "Se Dice Que — Impersonal & Passive": """
# Se Dice Que — Impersonal & Passive
The best gossip has no source: *se dice que…*, *dicen que…*. Plus *se venden tamales* and the "it wasn't my fault" *se*.

## 1. Impersonal se — "people / you / they"
**se** + the *él* form, no named subject:
- ***Se dice** que Valeria se casó.* (People say / it's said)
- *Aquí **se come** muy bien.* (You eat well here.)
- *¿Cómo **se dice** "gossip" en español?* · *No **se puede** entrar.*
- Same idea without se: ***Dicen** que Javi es espía.* · ***Uno** nunca sabe.*

## 2. Passive se — things being done
**se** + verb that agrees with the thing:
- ***Se vende** pan.* · ***Se venden** tamales.* (Tamales for sale.)
- ***Se rentan** departamentos.* · ***Se buscan** meseros.*

## 3. Accidental se — "it just happened to me"
**se + me / te / le / nos / les + verb**. The verb agrees with the thing, and the person is just the unlucky one:
- ***Se me cayó** el plato.* (I dropped the plate — oops.)
- ***Se le olvidó** la cita.* (He forgot the date.)
- ***Se nos acabó** el café.* (We ran out of coffee.)
- ***Se me olvidaron** las llaves.* (plural thing → plural verb)

## 4. True passive: ser + participle
*El restaurante **fue cerrado** por la policía.* The participle agrees: *Las tiendas **fueron cerradas**.*
It sounds formal, like the news. In conversation Latin Americans say ***Cerraron** el restaurante.* or *La policía **cerró** el restaurante.*

## ✍️ Try it
1. ___ ___ que Marco y Lucía se van a casar. (It's said)
2. Aquí ___ ___ tortillas. (are sold)
3. A Beto ___ ___ ___ los tamales. (dropped — by accident)
4. ¿Cómo ___ ___ "neighbor"? (do you say)
> Answers: 1. Se dice · 2. se venden · 3. se le cayeron · 4. se dice

Lessons: [[@perfect]], [[@timeline]]
""",
    "Subjunctive Plus — Si Fuera…": """
# Subjunctive Plus — Si Fuera…
Read this after Week 20. It covers *haya*, *fuera / tuviera*, *hubiera* and "if" sentences.

## 1. Fact or not? Indicative vs subjunctive
| indicative — fact, certain | subjunctive — doubt, wish, not real (yet) |
|---|---|
| *Creo que **viene**.* | *No creo que **venga**.* |
| *Sé que **está** aquí.* | *Dudo que **esté** aquí.* |
| *Busco al chico que **vive** aquí.* (he exists) | *Busco a alguien que **sepa** la verdad.* (if anyone does) |
| *Cuando **llega**, saluda.* (habit) | *Cuando **llegue**, avísame.* (future) |
| *Aunque **llueve**…* (it is raining) | *Aunque **llueva**…* (even if it rains) |

## 2. Present perfect subjunctive — haya + participle
*haya, hayas, haya, hayamos, hayan* + *-ado / -ido*:
- *Espero que **hayan llegado** bien.* · *No creo que Javi lo **haya dicho**.* · *Ojalá no **se haya enterado**.*

## 3. Imperfect subjunctive — fuera, tuviera, dijera
Take the *ellos* preterite, drop **-ron**, add **-ra, -ras, -ra, -ramos, -ran**:
*hablaron → hablara* · *tuvieron → tuviera* · *fueron → fuera* · *dijeron → dijera* (nosotros gets an accent: *habláramos*).
- After a past "trigger": *Doña Rosa quería que le **contara** todo.* · *Me pidió que no **dijera** nada.*
- Wishes: *Ojalá Valeria **volviera**.* (I wish she'd come back.)
- *como si* (as if): *Habla como si lo **supiera** todo.*
- Polite: ***Quisiera** un café.*

## 4. Past perfect subjunctive — hubiera + participle
Regrets and "if only": *Ojalá no lo **hubiera dicho**.* · *Si **hubiera sabido**, no habría venido.*
In everyday speech you'll also hear *Si hubiera sabido, no **hubiera** venido.*

## 5. "If" sentences
| if … | then … | meaning |
|---|---|---|
| si + **present** | present / future / command | real: *Si viene, le pregunto.* |
| si + **imperfect subj.** | **conditional** | unlikely now: *Si viniera, le preguntaría.* |
| si + **hubiera** + participle | **habría** + participle | too late: *Si hubiera venido, le habría preguntado.* |

Never put the present subjunctive after *si*.

## ✍️ Try it
1. Si yo ___ (ser) tú, no le diría nada.
2. No creo que Javi lo ___ ___ (hacer). (has done)
3. Ojalá ___ (tener) más tiempo.
4. Si ___ ___ (saber), te lo habría dicho.
> Answers: 1. fuera · 2. haya hecho · 3. tuviera · 4. hubiera sabido

Lessons: [[@teach-advice]]
""",
    "Latin American Word Choices": """
# Latin American Word Choices
Latin America isn't one accent. This course uses **Mexican Spanish** — the 🔊 voice is from Mexico, and it's the Spanish your students are most likely to hear in the US.
**Rule:** learn the 🇲🇽 word first. The other column is what you'll hear from students with family in other countries — recognize it, no need to use it.

## 1. Getting around
| English | 🇲🇽 use this | also heard in Latin America |
|---|---|---|
| car | **el carro** | el auto (Arg, Chile) |
| bus | **el camión** | el bus, el colectivo (Arg), la guagua (Caribbean) |
| cell phone | **el celular** | el celular |
| computer | **la computadora** | el computador (Chile, Col) |
| apartment | **el departamento** | el apartamento (Col, Ven) |
| sidewalk | **la banqueta** | la vereda (Arg), la acera |
| car trunk | **la cajuela** | el baúl (Col, Arg), la maleta (Chile) |
| license plate | **la placa** | la patente (Arg, Chile) |
| to park | **estacionarse** | parquear (Col, Caribbean) |
| parking lot | **el estacionamiento** | el parqueadero (Col) |
| to drive | **manejar** | manejar |
| ticket | **el boleto** | el pasaje (for a trip) |
| ticket office | **la taquilla** | la boletería |

## 2. Home and clothes
| English | 🇲🇽 use this | also heard in Latin America |
|---|---|---|
| glasses | **los lentes** | los anteojos (Arg) |
| jacket | **la chamarra** | la campera (Arg), la chaqueta |
| sweater | **el suéter** | el buzo, el pulóver (Arg) |
| T-shirt | **la playera** | la remera (Arg), la camiseta |
| zipper | **el cierre**, el zíper | el cierre |
| pajamas | **la piyama** | el piyama |
| blanket | **la cobija** | la frazada (Arg), la manta |
| light bulb | **el foco** | la ampolleta (Chile), el bombillo (Col, Ven) |
| light switch | **el apagador** | el interruptor, el suiche (Ven) |
| bucket | **la cubeta** | el balde |
| trash can | **el bote de basura** | el tacho (Arg), la caneca (Col) |
| fridge | **el refrigerador**, el refri | la heladera (Arg), la nevera (Col, Ven) |
| lawn, grass | **el pasto** | la grama (Ven) |

## 3. Food
| English | 🇲🇽 use this | also heard in Latin America |
|---|---|---|
| peas | **los chícharos** | las arvejas |
| banana | **el plátano** | la banana (Arg), el banano (Col), el guineo (Caribbean) |
| strawberry | **la fresa** | la frutilla (Arg, Chile) |
| apricot | **el chabacano** | el damasco (Arg, Chile) |
| peach | **el durazno** | el durazno |
| beans | **los frijoles** | los porotos (Arg, Chile), las caraotas (Ven) |
| potato | **la papa** | la papa |
| butter | **la mantequilla** | la manteca (Arg) |
| corn on the cob | **el elote** | el choclo (Arg, Chile, Peru), la mazorca (Col) |
| avocado | **el aguacate** | la palta (Arg, Chile, Peru) |
| juice | **el jugo** | el jugo |
| straw | **el popote** | el pitillo (Col, Ven), el sorbete (Arg) |
| cake | **el pastel** | la torta (Arg, Ven), el ponqué (Col) |

## 4. Everyday talk
| English | 🇲🇽 use this | also heard in Latin America |
|---|---|---|
| right now / in a sec | **ahorita** | ya, ahora |
| cool! | **¡qué padre!**, **¡qué chido!** | ¡chévere! (Col, Ven), ¡bacán! (Chile, Peru), ¡copado! (Arg) |
| money (slang) | **la lana** | la plata |
| to fail a class | **reprobar** | perder (Col), jalar (Peru), aplazar (Arg) |
| high school | **la prepa** (preparatoria) | el colegio, el liceo (Chile, Ven) |
| ID card | **la credencial**, la INE | la cédula (Col, Ven), el DNI (Arg) |
| to break down (a machine) | **descomponerse** | dañarse (Col), malograrse (Peru) |
| to pull | **jalar** | halar (Caribbean) |
| to throw away | **tirar** | botar (Col, Caribbean, Chile) |
| to grab | **agarrar** | agarrar |
| to turn on | **prender** | prender |
| to stand up | **pararse** | pararse |
| to hurry | **apurarse** | apurarse |
| to get angry | **enojarse** | enojarse |
| in the morning | **en la mañana** | a la mañana (Arg) |
| Pardon? / Yes? | **¿Mande?** | ¿Cómo?, ¿Qué? |

## 5. Same word, different meaning
| word | 🇲🇽 in Mexico | elsewhere in Latin America |
|---|---|---|
| **manteca** | lard | butter (Arg) — in Mexico ask for *mantequilla* |
| **taco** | the food 🌮 | shoe heel (Arg, Chile); traffic jam (Chile) |
| **torta** | sandwich on a roll | cake (Arg, Ven) |
| **camión** | bus (and truck) | truck only |
| **coger** | ⚠️ vulgar — use *agarrar / tomar* | to take, grab (Col, Caribbean) |
| **pena** | embarrassment: *Me da pena.* | sorrow, pity |
| **guagua** | — | bus (Cuba, Puerto Rico); baby (Chile, Andes) |
| **bicho** | bug, critter | ⚠️ vulgar in Puerto Rico |

## 6. You: tú, usted, ustedes — and vos
- Mexico: **tú** (friends, kids, students), **usted** (respect, strangers, parents of students), **ustedes** (any group).
- **vos** — Argentina, Uruguay, Paraguay, much of Central America and parts of Colombia: *vos sos, vos tenés, ¿vos querés?* Recognize it when students use it; you don't need to.
- Flashcards with vosotros, vuestro or os aren't Latin American — skip them.

## 7. Fixes for the Quizlet class "Mastering Spanish Vocabulary"
Its *Americanisms* set mixes countries under one "L.A." label (lots of Argentina and Chile) and has some errors:
- *la vajilla* means dishes — suitcase is **la maleta**.
- *en concreto* means "specifically" — "in cash" is **en efectivo**.
- *el palo* is a stick — tree is **el árbol** everywhere.
- *voltear* means to turn around / turn over — "to return" is **volver** or **regresar**.
- *por lo visto* means "apparently", not "obviously".
- *el cabro, el liceo, la heladera, el corpiño, el pulóver, la frutilla* are regional (Chile / Argentina), not general Latin American.
- Typos: **apenas** (not aspenas), **dieciséis** (not deiciseis), **el parqueadero** (not parkadero).

Lessons: [[@nouns]], [[@timeline]]
""",
    "Ser vs Estar": """
# Ser vs Estar
- **SER = DOCTOR:** Description, Occupation, Characteristics, Time, Origin, Relationship (+ where events happen)
- **ESTAR = PLACE:** Position, Location, Action (-ando/-iendo), Condition, Emotion

| | ser | estar |
|---|---|---|
| aburrido | boring | bored |
| listo | clever | ready |
| rico | rich | tasty |
| malo | bad | sick / spoiled |

Full lesson: [[@ser-estar]]
""",
    "Latin American Spanish Notes": """
# Latin American Spanish Notes
- **ustedes** for every "you all" — no *vosotros*.
- **Seseo:** z and soft c (ce/ci) sound like s. *cinco* = "SEEN-ko".
- **Preterite over present perfect:** *¿Ya comiste?* rather than *¿Ya has comido?*
- **Voseo** (Argentina, Uruguay, much of Central America): *vos* instead of *tú* — *vos tenés, vos sos, vení*. Learn tú first.
- **Direct objects:** *lo/la* for people and things (*Lo vi* = I saw him), not *le*.
- **Vocabulary varies:** car = *carro* (Mex, Col, Ven) / *auto* (Arg, Chi) · bus = *camión* (Mex) / *colectivo* (Arg) / *bus* · cool = *chido* (Mex), *chévere* (Col, Ven), *bacán* (Chi, Peru), *copado* (Arg)
""",
    "Classroom Phrases": """
# Classroom Phrases
For teaching a high-school cybersecurity class in Spanish. Use **ustedes** commands with the whole class and **tú** with one student.

## Starting and running class
| Español | English |
|---|---|
| Buenos días, clase. | Good morning, class. |
| Abran sus computadoras. | Open your computers. |
| Inicien sesión con su usuario. | Log in with your username. |
| Hoy vamos a aprender sobre… | Today we're going to learn about… |
| Trabajen en parejas / en grupos. | Work in pairs / in groups. |
| Lean las instrucciones. | Read the instructions. |
| Levanten la mano si tienen una pregunta. | Raise your hand if you have a question. |
| ¿Tienen preguntas? / ¿Alguna pregunta? | Do you have questions? / Any questions? |
| ¿Entienden? / ¿Está claro? | Do you understand? / Is it clear? |
| Repitan, por favor. | Repeat, please. |
| ¿Puedes explicarlo con tus palabras? | Can you explain it in your own words? |
| Muy bien. / ¡Excelente trabajo! | Very good. / Excellent work! |
| Casi. Inténtalo otra vez. | Almost. Try again. |
| Cierren sesión antes de salir. | Log out before leaving. |
| La tarea para mañana es… | Homework for tomorrow is… |

## Lab and safety
| Español | English |
|---|---|
| Abran la terminal. | Open the terminal. |
| Escriban este comando. | Type this command. |
| Presionen Enter. | Press Enter. |
| ¿Qué ven en la pantalla? | What do you see on the screen? |
| No hagan clic en enlaces desconocidos. | Don't click unknown links. |
| Nunca compartan su contraseña. | Never share your password. |
| Esto es solo para el laboratorio — nunca en una red real sin permiso. | This is only for the lab — never on a real network without permission. |

## Explaining concepts
- *Un cortafuegos es como un guardia en la puerta: decide qué tráfico entra y qué tráfico sale.* — A firewall is like a guard at the door: it decides what traffic gets in and out.
- *Una contraseña segura es larga, única y difícil de adivinar.* — A secure password is long, unique and hard to guess.
- *El phishing es cuando alguien finge ser una persona o empresa de confianza para robar tu información.* — Phishing is when someone pretends to be a trusted person or company to steal your information.

See also: [[Cybersecurity Glossary]]
""",
    "Question Words": """
# Question Words
| | |
|---|---|
| ¿Qué? — what | ¿Quién(es)? — who |
| ¿Dónde? — where | ¿Adónde? — to where |
| ¿Cuándo? — when | ¿Por qué? — why (porque = because) |
| ¿Cómo? — how | ¿Cuál(es)? — which / what (from options, with ser) |
| ¿Cuánto/a? — how much | ¿Cuántos/as? — how many |

Full lesson: [[@irregulars]]
""",
}


# Palabra del día — everyday topics (from SpanishDict's intro lessons) + gossip words.
# One word per line: español | English | example | example in English
DAILY_WORDS = {
    "🌦️ El clima": """
el clima | the weather | ¿Cómo está el clima hoy? | How's the weather today?
Hace calor | It's hot | Hace calor y tío Beto pide una paleta. | It's hot and Uncle Beto orders a popsicle.
Hace frío | It's cold | Hace frío, pero doña Rosa sigue en la ventana. | It's cold, but doña Rosa is still at the window.
Está lloviendo | It's raining | Está lloviendo y Javi no trae paraguas. | It's raining and Javi doesn't have an umbrella.
el paraguas | umbrella | Javi le pidió un paraguas a Lucía. | Javi asked Lucía for an umbrella.
Está nublado | It's cloudy | Está nublado; va a llover. | It's cloudy; it's going to rain.
la tormenta | storm | Con la tormenta se fue la luz. | The power went out with the storm.
el viento | wind | Hace mucho viento hoy. | It's very windy today.
húmedo | humid | El día está muy húmedo. | The day is very humid.
""",
    "👨‍👩‍👧 La familia": """
los parientes | relatives | Todos los parientes de Lucía vinieron a la fiesta. | All of Lucía's relatives came to the party.
la suegra | mother-in-law | La suegra de Marco llega el viernes. | Marco's mother-in-law arrives on Friday.
el cuñado | brother-in-law | El cuñado de Beto le debe dinero. | Beto's brother-in-law owes him money.
el sobrino | nephew | ¿Javi es sobrino de doña Rosa? | Is Javi doña Rosa's nephew?
la prima | cousin (female) | Valeria se fue a vivir con su prima. | Valeria went to live with her cousin.
los nietos | grandchildren | Doña Rosa les enseña fotos de sus nietos a todos. | Doña Rosa shows everyone photos of her grandkids.
la novia | girlfriend | ¿Javi tiene novia? | Does Javi have a girlfriend?
el ex | the ex | El ex de Valeria apareció en el barrio. | Valeria's ex showed up in the neighborhood.
hijo único | only child | Javi es hijo único. | Javi is an only child.
""",
    "👕 La ropa": """
la playera | T-shirt (Mexico) | Beto tiene salsa en la playera. | Beto has salsa on his T-shirt.
el vestido | dress | Lucía se compró un vestido rojo. | Lucía bought herself a red dress.
los tenis | sneakers | Javi siempre lleva tenis blancos. | Javi always wears white sneakers.
la chamarra | jacket (Mexico) | Ponte la chamarra, hace frío. | Put on your jacket, it's cold.
la gorra | cap | Javi nunca se quita la gorra. | Javi never takes off his cap.
los lentes | glasses | Doña Rosa se pone los lentes para espiar mejor. | Doña Rosa puts on her glasses to spy better.
la talla | size | ¿Qué talla usas? | What size do you wear?
probarse | to try on | Lucía se probó cinco vestidos. | Lucía tried on five dresses.
me queda grande | it's too big on me | Esta chamarra me queda grande. | This jacket is too big on me.
""",
    "🏨 El hotel": """
la reservación | reservation | Hay una reservación a nombre de Valeria. | There's a reservation under Valeria's name.
la habitación | room | La habitación tiene vista al mar. | The room has an ocean view.
la llave | key | Perdí la llave del cuarto. | I lost the room key.
la recepción | front desk | Pregunta en la recepción. | Ask at the front desk.
el elevador | elevator | El elevador no funciona. | The elevator doesn't work.
la toalla | towel | ¿Me trae más toallas, por favor? | Could you bring me more towels, please?
el aire acondicionado | air conditioning | El aire acondicionado hace mucho ruido. | The AC is very noisy.
registrarse | to check in | Valeria se registró con otro nombre. | Valeria checked in under another name.
el huésped | guest (hotel) | El huésped del 204 nunca sale. | The guest in 204 never comes out.
""",
    "🩺 El doctor": """
Me duele la cabeza | My head hurts | Me duele la cabeza de tanto chisme. | My head hurts from so much gossip.
el estómago | stomach | A Beto le duele el estómago. ¡Comió quince tacos! | Beto's stomach hurts. He ate fifteen tacos!
la fiebre | fever | Javi tiene fiebre y no salió. | Javi has a fever and didn't go out.
la gripa | the flu (Mexico) | Beto tiene gripa, pero sigue comiendo. | Beto has the flu, but he keeps eating.
la garganta | throat | Me duele la garganta. | My throat hurts.
la receta | prescription (also recipe) | El doctor me dio una receta. | The doctor gave me a prescription.
la pastilla | pill | Tómese una pastilla cada ocho horas. | Take one pill every eight hours.
la cita | appointment (also a date) | Tengo cita con el doctor a las diez. | I have a doctor's appointment at ten.
mareado | dizzy | Doña Rosa está mareada. | Doña Rosa is dizzy.
¿Qué le pasa? | What's wrong? (formal) | ¿Qué le pasa, doña Rosa? Está muy pálida. | What's wrong, doña Rosa? You look very pale.
""",
    "🧹 Los quehaceres": """
los quehaceres | chores | Marco odia los quehaceres. | Marco hates chores.
barrer | to sweep | Doña Rosa barre la banqueta para ver quién pasa. | Doña Rosa sweeps the sidewalk to see who goes by.
trapear | to mop | Lucía trapea la cocina. | Lucía mops the kitchen.
lavar los trastes | to do the dishes | Marco nunca lava los trastes. | Marco never does the dishes.
tender la cama | to make the bed | Javi no tiende la cama. | Javi doesn't make his bed.
sacar la basura | to take out the trash | ¿Quién saca la basura hoy? | Who's taking out the trash today?
lavar la ropa | to do laundry | Lavo la ropa los domingos. | I do laundry on Sundays.
planchar | to iron | Lucía plancha la camisa de Marco. | Lucía irons Marco's shirt.
el desorden | mess | ¡Qué desorden hay en el 3B! | What a mess there is in 3B!
""",
    "🎸 Los pasatiempos": """
el pasatiempo | hobby | Su pasatiempo favorito es el chisme. | Her favorite hobby is gossip.
en mi tiempo libre | in my free time | En mi tiempo libre veo series. | In my free time I watch shows.
tocar la guitarra | to play guitar | Javi toca la guitarra a medianoche. | Javi plays guitar at midnight.
jugar fútbol | to play soccer | Marco juega fútbol los sábados. | Marco plays soccer on Saturdays.
salir a correr | to go for a run | Lucía sale a correr temprano. | Lucía goes running early.
tejer | to knit | Doña Rosa teje y escucha todo. | Doña Rosa knits and listens to everything.
pintar | to paint | Valeria pintaba en su balcón. | Valeria used to paint on her balcony.
bailar | to dance | Beto baila cumbia en todas las fiestas. | Beto dances cumbia at every party.
ir al gimnasio | to go to the gym | Javi va al gimnasio todos los días. | Javi goes to the gym every day.
""",
    "🎉 La fiesta": """
el cumpleaños | birthday | El cumpleaños de doña Rosa es el sábado. | Doña Rosa's birthday is on Saturday.
el pastel | cake | Beto se comió medio pastel. | Beto ate half the cake.
las velas | candles | ¡Sopla las velas! | Blow out the candles!
los invitados | guests | Llegaron cincuenta invitados. | Fifty guests arrived.
el regalo | gift | ¿Quién trajo este regalo? | Who brought this gift?
los quince años | 15th birthday party (the girl is la quinceañera) | Los quince años de la sobrina de Rosa fueron enormes. | Rosa's niece's quinceañera was huge.
brindar | to toast | ¡Vamos a brindar por los novios! | Let's toast the couple!
¡Salud! | Cheers! | ¡Salud por Marco y Lucía! | Cheers to Marco and Lucía!
colarse | to crash (a party) | Javi se coló en la fiesta. | Javi crashed the party.
la piñata | piñata | Los niños rompieron la piñata. | The kids broke the piñata.
""",
    "✈️ De viaje": """
el vuelo | flight | El vuelo de Valeria salió a las seis. | Valeria's flight left at six.
la maleta | suitcase | Valeria hizo la maleta en diez minutos. | Valeria packed her suitcase in ten minutes.
el boleto | ticket | Compró un boleto de ida. | She bought a one-way ticket.
el pasaporte | passport | ¿Dónde está mi pasaporte? | Where's my passport?
la aduana | customs | Tardamos una hora en la aduana. | We spent an hour at customs.
el equipaje | luggage | Perdieron el equipaje de Beto. | They lost Beto's luggage.
el retraso | delay | El vuelo tiene retraso. | The flight is delayed.
perder el vuelo | to miss the flight | Javi perdió el vuelo. | Javi missed his flight.
de vacaciones | on vacation | ¿Valeria está de vacaciones o se fue para siempre? | Is Valeria on vacation or did she leave for good?
""",
    "🛒 En el mercado": """
el puesto | (market) stall | Beto conoce todos los puestos del mercado. | Beto knows every stall in the market.
¿Cuánto cuesta? | How much is it? | ¿Cuánto cuesta el kilo de aguacate? | How much is a kilo of avocados?
barato | cheap | Aquí todo es barato. | Everything is cheap here.
caro | expensive | ¡Qué caro está el limón! | Limes are so expensive!
medio kilo | half a kilo | Medio kilo de tortillas, por favor. | Half a kilo of tortillas, please.
regatear | to haggle | Doña Rosa regatea en cada puesto. | Doña Rosa haggles at every stall.
el cambio | change (money) | ¿Tiene cambio de quinientos? | Do you have change for 500?
la bolsa | bag | ¿Le doy una bolsa? | Shall I give you a bag?
¿Algo más? | Anything else? | ¿Algo más, señora? | Anything else, ma'am?
en oferta | on sale | Los mangos están en oferta. | Mangoes are on sale.
""",
    "☕ El cafecito": """
un cafecito | a little coffee (and a chat) | ¿Un cafecito? Te tengo un chisme. | Coffee? I've got some gossip for you.
el café de olla | Mexican spiced coffee | Doña Rosa hace el mejor café de olla. | Doña Rosa makes the best café de olla.
el pan dulce | sweet bread | Beto compra pan dulce todas las mañanas. | Beto buys sweet bread every morning.
la concha | concha (sweet bun) | ¿Me pasas una concha? | Can you pass me a concha?
la taza | cup | Se me rompió la taza. | My cup broke.
sin azúcar | without sugar | Un café sin azúcar, por favor. | A coffee without sugar, please.
para llevar | to go | Dos cafés para llevar. | Two coffees to go.
""",
    "😏 Personalidades": """
chismoso | gossipy | Doña Rosa es la más chismosa del barrio. | Doña Rosa is the biggest gossip in the neighborhood.
metiche | nosy (Mexico) | ¡No seas metiche! | Don't be nosy!
presumido | show-off | Javi es un poco presumido. | Javi is a bit of a show-off.
tacaño | stingy | Beto es tacaño, nunca invita. | Beto is stingy, he never treats.
celoso | jealous | Marco es muy celoso. | Marco is very jealous.
mentiroso | liar, lying | ¡Eres un mentiroso! | You're a liar!
creído | conceited | Desde que se mudó, Valeria está muy creída. | Since she moved, Valeria is very stuck-up.
buena onda | cool, nice (Mexico) | Javi es muy buena onda. | Javi is really cool.
flojo | lazy | Marco es flojo para los quehaceres. | Marco is lazy about chores.
terco | stubborn | Lucía es terca como una mula. | Lucía is as stubborn as a mule.
""",
    "🇲🇽 Así se dice en México": """
ahorita | right now, in a sec | Ahorita vengo, voy por tortillas. | I'll be right back, I'm going for tortillas.
¡Qué padre! | How cool! | ¡Qué padre está tu playera! | Your T-shirt is so cool!
chido | cool | Javi tiene un carro muy chido. | Javi has a really cool car.
la lana | money (slang) | Beto nunca trae lana. | Beto never has money on him.
¿Mande? | Pardon? / Yes? | —¡Javi! —¿Mande? | "Javi!" "Yes?"
¡Aguas! | Watch out! | ¡Aguas, ahí viene doña Rosa! | Watch out, here comes doña Rosa!
¡No manches! | No way! | ¿Valeria se casó? ¡No manches! | Valeria got married? No way!
me da pena | I'm embarrassed | Me da pena preguntarle. | I'm too embarrassed to ask him.
el camión | the bus | Valeria se fue en el camión de las seis. | Valeria left on the six o'clock bus.
la cajuela | car trunk | ¿Qué esconde Marco en la cajuela? | What is Marco hiding in the trunk?
estacionarse | to park | Javi se estacionó enfrente de la casa de Rosa. | Javi parked in front of Rosa's house.
la cubeta | bucket | Doña Rosa lava la banqueta con una cubeta. | Doña Rosa washes the sidewalk with a bucket.
el foco | light bulb | Se fundió el foco del pasillo. | The hallway light bulb burned out.
el apagador | light switch | ¿Dónde está el apagador? | Where's the light switch?
la cobija | blanket | Hace frío; pásame una cobija. | It's cold; pass me a blanket.
el refri | fridge | Beto abre el refri cada diez minutos. | Beto opens the fridge every ten minutes.
el bote de basura | trash can | Tiraron la carta al bote de basura. | They threw the letter in the trash can.
los chícharos | peas | Lucía le pone chícharos al arroz. | Lucía puts peas in the rice.
el elote | corn on the cob | Beto se comió tres elotes con chile. | Beto ate three ears of corn with chili.
el popote | straw | Un agua de horchata con popote, por favor. | A horchata with a straw, please.
reprobar | to fail (a class) | Javi reprobó matemáticas. | Javi failed math.
la prepa | high school | Marco y Lucía se conocieron en la prepa. | Marco and Lucía met in high school.
""",
    "🔗 Conectores": """
sin embargo | however | Beto está a dieta; sin embargo, pidió tacos. | Beto is on a diet; however, he ordered tacos.
a pesar de | despite | A pesar de la lluvia, doña Rosa salió a espiar. | Despite the rain, doña Rosa went out to spy.
en vez de | instead of | En vez de estudiar, Javi chismea. | Instead of studying, Javi gossips.
según | according to | Según doña Rosa, Valeria se casó. | According to doña Rosa, Valeria got married.
por eso | that's why | Marco llegó tarde; por eso Lucía está enojada. | Marco came home late; that's why Lucía is angry.
ya que | since | Ya que estás aquí, ¿me ayudas? | Since you're here, will you help me?
además de | besides | Además de chismosa, es metiche. | Besides being a gossip, she's nosy.
apenas | barely | Javi apenas habla con nadie. | Javi barely talks to anyone.
casi | almost | Casi me caigo de la risa. | I almost fell over laughing.
incluso | even | Todos lo saben, incluso el perro. | Everyone knows, even the dog.
por lo visto | apparently | Por lo visto, Marco y Lucía ya se reconciliaron. | Apparently, Marco and Lucía already made up.
o sea | I mean, so | O sea, ¿se fue o no se fue? | I mean, did she leave or not?
¡Qué casualidad! | What a coincidence! | ¡Qué casualidad! Valeria y Javi en el mismo café. | What a coincidence! Valeria and Javi at the same café.
el lío | mess, trouble | Javi se metió en un lío. | Javi got himself into trouble.
lo demás | the rest | Lo demás te lo cuento mañana. | I'll tell you the rest tomorrow.
cada | each, every | Cada día hay un chisme nuevo. | Every day there's new gossip.
""",
    "🗣️ Verbos chismosos": """
susurrar | to whisper | Doña Rosa susurró: "Valeria se fue." | Doña Rosa whispered, "Valeria left."
enterarse de | to find out about | ¿Te enteraste de lo de Javi? | Did you hear about Javi?
espiar | to spy on | Doña Rosa espía por la ventana. | Doña Rosa spies through the window.
platicar | to chat (Mexico) | Platicamos toda la tarde. | We chatted all afternoon.
discutir | to argue | Marco y Lucía discutieron anoche. | Marco and Lucía argued last night.
devorar | to devour | Tío Beto devoró tres tamales. | Uncle Beto devoured three tamales.
aparecer | to show up | Javi apareció a medianoche. | Javi showed up at midnight.
mudarse | to move (house) | Valeria se mudó sin decir nada. | Valeria moved without saying anything.
esconder | to hide | Marco esconde algo. | Marco is hiding something.
confesar | to confess | Al final, Javi confesó todo. | In the end, Javi confessed everything.
averiguar | to figure out | Voy a averiguar qué pasó. | I'm going to figure out what happened.
""",
}


def daily_words():
    out = [{"topic": topic, "es": es, "en": en, "ex": ex, "ex_en": ex_en, "say": say_it(es)}
           for topic, block in DAILY_WORDS.items()
           for es, en, ex, ex_en in (map(str.strip, line.split("|")) for line in block.strip().splitlines())]
    random.Random(2026).shuffle(out)  # fixed order, so every device shows the same word on the same day
    return out


def word_bank_note():
    lines = ["# Word Bank — Palabra del día", "Every word the site can pick as *Palabra del día*. Tap ➕ on the site to copy one into [[Vocab]].", ""]
    for topic, block in DAILY_WORDS.items():
        lines += [f"## {topic}", "| Español | English | Example |", "|---|---|---|"]
        lines += [f"| **{es}** | {en} | *{ex}* — {ex_en} |" for es, en, ex, ex_en in (map(str.strip, l.split("|")) for l in block.strip().splitlines())]
        lines.append("")
    return "\n".join(lines)


QUIZLET = VAULT / "Quizlet"
QZ_ROW = re.compile(r"^\| (.*?) \| (.*?) \|$")
QZ_AMERICANISM = re.compile(r"^(.*\((?:L\.A\.|Mex|Ven|Col)\))[.,]?\s*(.*?)\s*\(Sp\)$")  # "X (L.A.), Y (Sp)"

# Words on the index's skip list that are in fact also normal in Latin America (English, Spanish as Quizlet has them)
ALSO_LATAM = {
    ("bill, banknote; ticket", "el billete"), ("to drive", "conducir"), ("car; automobile", "el coche"),
    ("salesperson; clerk (Spain)", "el dependiente, la dependienta"), ("olive (Spain)", "la oliva"), ("refrigerator", "la nevera"),
    ("artificial lake, storage lake; reservoir (Spain); swamp (America)", "el pantano"), ("mountain pass (Spain)", "el puerto"),
}
# The Americanisms folder labels every second word "(Sp)", but most are used all over Latin America too (la fresa, el árbol,
# el examen…). These are the ones that really are Spain-only.
SPAIN_ONLY_SP = {
    "coger", "darse prisa", "la peluqueria de caballeros", "tirar", "la peluqueria de señoras", "la cerilla", "las gafas", "el empaste",
    "enfadado, enfadada", "enfadarse", "el guisante", "el estanco", "el sujetador", "la nata", "el albaricoque", "el melocotón",
    "la judia", "la patata", "el bocadillo", "la cremallera", "la bombilla", "el cubo", "el cubo de basura", "la manta", "el piso",
    "suspender", "el instituto", "quedar suspendido/suspendida", "el fontanero, la fontanera", "la tienda de campaña", "el visado",
    "el, la contable", "el altavoz", "la lista de correos", "el móvil", "el sello", "el maletero", "el billete", "la matricula",
    "el coche-cama", "estropeado, estropeada", "aparcar", "el coche-restaurante", "la mofeta",
}


def quizlet_data():
    """The saved Quizlet folders for the Vocabulary page (#/vocab). Each word is [English, Spanish], or, when Quizlet's
    Spanish is (or includes) a Spain word, [English, Spanish, Latin American word to say instead, "spain" | "also"]:
    "spain" = Spain-only, "also" = used in Latin America too. Skip-list rows come from Quizlet Index.md; Americanisms
    rows ("X (L.A.), Y (Sp)") have no instead word, since X already is the Latin American one."""
    if not QUIZLET.is_dir():
        return []
    skip, stem = {}, None  # (folder stem, English, Spanish) -> what to say instead
    index = QUIZLET / "Quizlet Index.md"
    for line in (index.read_text(encoding="utf-8").split("## Not Latin American", 1)[-1].splitlines() if index.exists() else []):
        if line.startswith("### [["):
            stem = line[6:-2]
        elif (m := QZ_ROW.match(line)) and "~~" in line:
            en, es, hint = (c.strip() for c in line.strip("| ").split(" | "))
            skip[(stem, en, es.strip("~"))] = hint
    out = []
    for f in sorted(QUIZLET.glob("[0-9][0-9] - *.md")):
        sets = []
        for line in f.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                sets.append({"title": re.sub(r"^\d+\.\d+ ", "", line[3:]), "words": []})
            elif sets and (m := QZ_ROW.match(line)) and line != "| English | Español |" and m[1].strip():  # skip headers and blank cards
                en, es = (c.replace("\\|", "|") for c in m.groups())
                row = [en, es]
                if (f.stem, m[1], m[2]) in skip:
                    row += [skip[(f.stem, m[1], m[2])], "also" if (m[1], m[2]) in ALSO_LATAM else "spain"]
                elif am := QZ_AMERICANISM.match(es):
                    row += ["", "spain" if am[2] in SPAIN_ONLY_SP else "also"]
                sets[-1]["words"].append(row)
        out.append({"id": f.stem[:2], "title": f.stem[5:], "sets": sets})
    return out


# Reference notes that also get a page on the site (#/guide/<id>)
GUIDES = [  # (id, note name, icon, blurb, week ids it goes with) — in course order
    ("describing", "Describing & Comparing", "📏", "Articles, my/your, this/that, más … que, -ísimo and -mente.", ["nouns", "ser-estar", "present-regular"]),
    ("numbers", "Numbers, Time & Dates", "🔢", "Numbers, telling time, days and dates, and hace for “ago”.", ["ser-estar", "irregulars"]),
    ("little", "Little Words — Negatives, Connectors & Prepositions", "🔗", "nadie/nunca, pero vs sino, debajo de, the personal a, que/lo que.", ["present-regular", "irregulars", "stem-changers"]),
    ("tricky", "Tricky Verb Pairs & False Friends", "🪤", "saber vs conocer, pedir vs preguntar, llevar vs traer, false friends, weather, and five ways to say “become”.", ["irregulars", "stem-changers", "coming-going"]),
    ("pronouns", "Pronouns — Lo, Le, Se Lo", "🎯", "Who told what to whom: lo/la, le/les, se lo, conmigo, each other.", ["gustar", "progressive", "coming-going"]),
    ("sentences", "Sentence Structure by Tense", "🧩", "Word order in every tense, what goes on the end of verbs, upgrading base verbs to action verbs, and el gerundio (-ando / -iendo).", ["present-regular", "progressive", "timeline"]),
    ("endings", "Verb Endings Cheat Sheet", "📋", "Every regular ending on one page: present, past, imperfect, future.", ["present-regular", "preterite", "imperfect", "future"]),
    ("more-tenses", "Would, Had & Must Have — More Tenses", "⏳", "Conditional, past perfect, future perfect and the -ing form in other tenses.", ["imperfect", "perfect", "timeline"]),
    ("se", "Se Dice Que — Impersonal & Passive", "📣", "se dice que, se venden tamales, se me cayó, and the passive voice.", ["perfect", "timeline"]),
    ("latam", "Latin American Word Choices", "🌎", "Which word to use (Mexico) and what you'll hear elsewhere in Latin America — plus words that change meaning by country.", ["nouns", "timeline"]),
    ("subjunctive-plus", "Subjunctive Plus — Si Fuera…", "🔮", "haya, fuera/tuviera, hubiera and “if” sentences — after Week 20.", ["teach-advice"]),
]


def guides_data():
    by_id = {w["id"]: w for w in COURSE}
    pages = {name: gid for gid, name, *_ in GUIDES}

    def link(m):
        if m[1].startswith("@"):
            w = by_id[m[1][1:]]
            return f"[Week {w['week']}](#/week/{w['week']}/lesson)"
        return f"[{m[1]}](#/guide/{pages[m[1]]})" if m[1] in pages else m[1]
    out = []
    for gid, name, icon, blurb, weeks in GUIDES:
        body = REFERENCE[name].strip().split("\n", 1)[1]  # drop the "# Title" line; the page shows its own heading
        out.append({"id": gid, "title": name, "icon": icon, "blurb": blurb, "weeks": sorted(by_id[i]["week"] for i in weeks), "md": re.sub(r"\[\[([^\]]+)\]\]", link, body)})
    return out


CLAUDE_MD = """
# Spanish Learning Vault — read me first (for Claude sessions)

This vault tracks a learner studying **Latin American Spanish** through a {n}-week course (Week 0 to Week {last}).
They found themselves reading Spanish with English sounds — keep pronunciation in mind (point them to 🔊 audio, give respellings like OH-lah).
Their starting point was basic phrases (me gusta, ¿dónde está?, eres/estás).

**Goal:** be able to teach high-school cybersecurity (networking, firewalls, security principles) in Spanish
to students who need it, within a few months.

## How the course is built
- **Week 0** — alphabet & pronunciation ("say it before you learn it").
- **Phase 1–3 — tenses with everyday topics**: the present (incl. estar + -ando, coming/going/staying), the future
  (ir a, simple future, "¿dónde estará?"), and the past (preterite, irregular preterite, imperfect, present perfect, a tense review).
  Topics are **food** and **people being here, there or gone**.
- **Theme: gossip.** The learner wants to become *el más chismoso del barrio*. Every lesson uses the same cast:
  doña Rosa (nosy neighbor), Marco y Lucía (the couple in 3B), el tío Beto (always eating), Valeria (moved away — why?),
  Javi (the new guy). Each lesson ends with "🗣️ El chisme" lines. Use this cast and gossip framing in examples and role-play.
- **Phase 4 — Cybersecurity Spanish (last)**: computers & networks, security actions & accounts, principles & incident
  reports, then teaching with commands/por-para and advice with the subjunctive. Cyber vocabulary lives ONLY here —
  don't weave cyber terms into the earlier tense weeks. See `Reference/Cybersecurity Glossary.md` and `Reference/Classroom Phrases.md`.
- **Grammar guides** — `GUIDES` in build.py: reference notes that are also site pages (`#/guide/<id>`), linked from the lessons
  they go with. They fill gaps the weeks don't teach (object pronouns, numbers & time, comparisons, saber/conocer, conditional, se…).
  Point the learner to the matching guide when one of these comes up.
- **Palabra del día** — `DAILY_WORDS` in build.py: everyday-topic vocab (weather, clothes, doctor, travel…) shown one a day on the
  site home page; ➕ copies a word into `My Notes/Vocab.md`. Full list in `Reference/Word Bank.md`. Re-run `fetch_media.py audio` after adding words.
- **Vocabulary Bank** — `#/vocab` on the site: the 24 Quizlet folders saved in `Quizlet/` (5,800+ words), searchable. `build.py` reads them
  plus the "Not Latin American — skip" list in `Quizlet/Quizlet Index.md`, so Spain-only words show the Latin American word instead.
  Its 🔊 uses a Latin American browser voice when the device has one; otherwise `server.py` `/api/say` makes an es-MX clip
  (same Dalia voice as the course audio) the first time a word is played and caches it in `Media/audio/say/`.
- **Public copy** — `python3 publish.py` builds a read-only copy (no saving, no Vocabulary Bank: that's Quizlet's content)
  into `Site/public/` and pushes it to the repo's `gh-pages` branch for GitHub Pages. The tailnet site stays the main one.

## Where to look
1. **`Progress/Dashboard.md`** — current week, scores, weak spots, recent activity. Start here.
2. `Progress/Quiz Log.md` — every worksheet/quiz/grammar-check attempt with the exact items missed.
3. `Progress/Study Log.md` — study sessions (date, minutes, notes).
4. `Practice/` — the learner's own writing for each week's practice task. Review these for errors when asked.
5. `Lessons/` — lesson notes for every week (the learner may add notes under "My notes").
6. `My Notes/` — the learner's free-form notes, vocab, and questions.
7. `My Notes/Tutor Notes.md` — notes left by previous Claude sessions. Read it; append a short dated entry at the end of a tutoring session.

## How progress is recorded
- The course website lives at `~/Documents/Spanish/Site` (`python3 ~/Documents/Spanish/Site/server.py`, then http://127.0.0.1:8765).
- The site writes progress to `Progress/progress.json` and regenerates `Dashboard.md`. **Don't hand-edit Dashboard.md** — it gets overwritten.
- If the learner asks you to mark something done, edit `Progress/progress.json` and run `python3 ~/Documents/Spanish/Site/server.py --regen`.
- A week counts as complete when: lesson read, worksheet attempted, quiz ≥ 80%, practice saved.
- Course content is defined in `~/Documents/Spanish/Site/build.py`. Weeks are numbered by their order in `COURSE`; each has a stable
  `id` that keys `WORDS`, `PHOTOS`, `GRAMMAR` and `CYBER`. Run `python3 build.py` after editing it.
- Photos (Wikimedia Commons, credits in `Media/Image Credits.md`) and audio clips (es-MX neural TTS) live in `Media/`.
  To add a photo or new phrases: edit `build.py`, then `cd ~/Documents/Spanish/Site && .venv/bin/python fetch_media.py images` (or `audio`) and `python3 build.py --force`.
  Photo picks are pinned in `photo_pins.json` (keyed `<week id>-<n>`); `fetch_media.py candidates` makes contact sheets to choose from.

## How to tutor
- Latin American Spanish: use **ustedes**, never vosotros; prefer Latin American vocabulary.
- Pitch explanations at the learner's current week — don't lean on tenses they haven't reached yet.
- Prioritize the weak spots listed on the dashboard.
- Keep it fun: gossip about the barrio cast, food, who came and who left. Save cybersecurity and classroom language for Phase 4.
- When correcting writing, show the corrected sentence and a one-line reason tied to the relevant week.
"""

HOME_MD = """
# Spanish 🇲🇽🇨🇴🇦🇷
Week 0 pronunciation, then present → future → past tense told through neighborhood gossip (become *el más chismoso del barrio*), then a final cybersecurity-teaching phase — goal: teach high-school cybersecurity in Spanish.

- **[[Dashboard]]** — where I'm at
- [[Quiz Log]] · [[Study Log]]
- Course site: run `python3 ~/Documents/Spanish/Site/server.py` → http://127.0.0.1:8765

## Lessons
{lessons}

## Grammar guides (also on the site)
{guides}

## Reference
- [[Cybersecurity Glossary]]
- [[Classroom Phrases]]
- [[Rolling Your R]] — R Trill Lab
- [[Alphabet & Letter Sounds]]
- [[Verb Endings Cheat Sheet]]
- [[Word Bank]] — every Palabra del día word, by topic
- [[Word Lists]] — themed vocabulary for every week (fruit, family, clothes…)
- [[Ser vs Estar]]
- [[Question Words]]
- [[Latin American Spanish Notes]]

## My notes
- [[Vocab]]
- [[Questions for Claude]]
- [[Tutor Notes]]

## Daily routine (30–45 min)
1. 10 min — grammar from this week's lesson
2. 10 min — vocabulary flashcards (Anki or similar)
3. 10 min — listening (Dreaming Spanish, Español con Juan, Latin American shows)
4. 5–10 min — output: 5 sentences or talk to yourself out loud
5. Weekly — one conversation with a Latin American speaker (iTalki / Tandem)
"""

MY_NOTES = {
    "Vocab": "# Vocab\nWords I'm learning. Format: `español — English (week)`\n\n- ",
    "Questions for Claude": "# Questions for Claude\nThings I'm confused about — ask Claude in a session.\n\n- ",
    "Tutor Notes": "# Tutor Notes\nShort dated notes left by Claude sessions: what was covered, what to work on next.\n",
}


from words import WORDS, words_data  # noqa: E402  (📖 Words tab lists)


def word_clip(es):
    """The text the voice reads for a word-list entry: drop (notes) and trailing …"""
    t = re.sub(r"\s*\([^)]*\)", "", es).replace("…", "").replace(" / ", ", ")
    return re.sub(r"\s+", " ", t).strip(" ,")


def words_texts():
    return [r[3] for sections in words_data(word_clip).values() for sec in sections for r in sec["rows"]]


def word_list_note(w, sections):
    out = [f"# Words — {w['title']}", f"Themed word lists for [[{note_name(w)}]]. Mexican Spanish first; 🌎 = other Latin American countries, 🇪🇸 = Spain, 💡 = tip.",
           "On the site: open the week → **📖 Words** (🔊 audio, ➕ add to [[Vocab]], 🙈 hide English, 🎲 quiz).", ""]
    for sec in sections:
        out.append(f"## {sec['title']}")
        group = None
        for es, en, note, _, g in sec["rows"]:
            if g != group:
                out += ([f"### {g}"] if g else []) + ["| Español | English | Note |", "|---|---|---|"]
                group = g
            out.append(f"| **{es}** | {en} | {note} |")
        out.append("")
    out.append("Back to [[Word Lists]]")
    return "\n".join(out)


def build(force=False):
    site = HERE / "site"
    site.mkdir(exist_ok=True)
    wd = words_data(word_clip)
    for w in COURSE:
        w["words"] = wd.get(w["id"], [])
    data = {"phases": PHASES, "weeks": COURSE, "media": MEDIA, "rr_lab": {**RR_LAB, "say": {t: say_it(t) for t in rr_texts()}}, "guides": guides_data(), "daily": daily_words()}
    (site / "content.js").write_text(
        "window.COURSE = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    # Quizlet vocabulary is big, so it gets its own file that the Vocabulary page loads on demand
    (site / "quizlet.js").write_text(
        "window.QUIZLET = " + json.dumps(quizlet_data(), ensure_ascii=False, separators=(",", ":")) + ";\n", encoding="utf-8")

    created = []
    for w in COURSE:
        path = VAULT / "Lessons" / f"{note_name(w)}.md"
        text = lesson_note(w)
        if path.exists() and "## My notes" in path.read_text(encoding="utf-8"):  # keep the learner's own notes on rebuild
            text = text.split("## My notes")[0] + "## My notes" + path.read_text(encoding="utf-8").split("## My notes", 1)[1]
        if write_note(path, text, force):
            created.append(note_name(w))
    by_id = {w["id"]: w for w in COURSE}
    for name, text in {**REFERENCE, "Cybersecurity Glossary": glossary_note(), "Rolling Your R": rr_note(), "Alphabet & Letter Sounds": alphabet_note(), "Word Bank": word_bank_note()}.items():
        text = re.sub(r"\[\[@([\w-]+)\]\]", lambda m: f"[[{note_name(by_id[m[1]])}]]", text)  # [[@id]] links to that week's lesson
        if write_note(VAULT / "Reference" / f"{name}.md", text, force):
            created.append(name)
    folder = VAULT / "Word Lists"
    index = ["# Word Lists", "Themed vocabulary for every week — the **📖 Words** tab on the site. Mexican Spanish first.", ""]
    for w in COURSE:
        if w["words"]:
            name = f"Week {w['week']:02d} Words"
            write_note(folder / f"{name}.md", word_list_note(w, w["words"]), True)  # generated — no learner notes in here
            index.append(f"- [[{name}]] — {w['title']}: " + ", ".join(re.sub(r"^[^\w¿¡-]+", "", sec["title"]) for sec in w["words"]))
    write_note(folder / "Word Lists.md", "\n".join(index), True)
    lessons = "\n".join(f"- [[{note_name(w)}]]" for w in COURSE)
    for path, text in [(VAULT / "CLAUDE.md", CLAUDE_MD.replace("{n}", str(len(COURSE))).replace("{last}", str(COURSE[-1]["week"]))), (VAULT / "Home.md", HOME_MD.replace("{lessons}", lessons).replace("{guides}", "\n".join(f"- [[{name}]] — {blurb}" for _, name, _, blurb, _ in GUIDES)))]:
        if write_note(path, text, force):
            created.append(path.name)
    if MEDIA["images"]:
        credits = ["# Image Credits", "All photos are from Wikimedia Commons under free licenses. Keep this attribution if you reuse them in class materials.", "",
                   "| Image | File | Author | License |", "|---|---|---|---|"]
        credits += [f"| {k} | [{i['title'][5:]}]({i['source']}) | {i['artist'].replace('|', '/')} | {i['license']} |" for k, i in sorted(MEDIA["images"].items())]
        write_note(VAULT / "Media" / "Image Credits.md", "\n".join(credits), True)
    for name, text in MY_NOTES.items():  # never overwritten, even with --force
        if write_note(VAULT / "My Notes" / f"{name}.md", text, False):
            created.append(name)
    print(f"Wrote {site / 'content.js'}; created/updated {len(created)} notes in {VAULT}")


if __name__ == "__main__":
    build(force="--force" in sys.argv)
