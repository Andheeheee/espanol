"""Themed word lists for each week's 📖 Words tab — Mexican Spanish first.

WORDS[week id] = [(section title, Vocabulary Bank folder id or "", block)]
Each block line: Spanish | English | note (optional); a '## Name' line starts a subheading. Notes start with 🌎 (what other Latin American countries say),
🇪🇸 (what Spain says) or 💡 (a tip). Checked against the Quizlet Vocabulary Bank for coverage, but written for Mexico.
"""
WORDS = {}

WORDS["alphabet"] = [
("👋 Greetings", "07", """
hola | hi |
buenos días | good morning |
buenas tardes | good afternoon | 💡 from about noon until dark
buenas noches | good evening / good night |
¿Cómo estás? | How are you? (tú) |
¿Cómo está usted? | How are you? (usted) |
¿Qué tal? | How's it going? |
¿Qué onda? | What's up? | 💡 casual, Mexico
bien, gracias | fine, thanks |
muy bien | very well |
más o menos | so-so |
mal | bad, not well |
¿Y tú? | And you? |
¿Cómo te llamas? | What's your name? |
me llamo… | my name is… |
¿De dónde eres? | Where are you from? |
soy de… | I'm from… |
mucho gusto | nice to meet you |
encantado, encantada | delighted (to meet you) |
igualmente | likewise |
bienvenido, bienvenida | welcome |
adiós | goodbye |
hasta luego | see you later |
hasta mañana | see you tomorrow |
nos vemos | see you |
cuídate | take care |
que te vaya bien | hope it goes well for you | 💡 a very Mexican goodbye
"""),
("🙏 Polite words", "07", """
por favor | please |
gracias | thank you |
muchas gracias | thank you very much |
de nada | you're welcome |
no hay de qué | don't mention it |
con permiso | excuse me (to get past, to leave) |
perdón | sorry, pardon |
disculpe | excuse me (to get attention, usted) |
lo siento | I'm sorry |
¿Mande? | Pardon? / Yes? | 💡 Mexico — how you answer when someone calls you
¡Salud! | Bless you! / Cheers! |
¡Buen provecho! | Enjoy your meal! | 💡 said to people eating, even strangers
sí | yes |
no | no |
claro | of course |
¡Cómo no! | Sure! Of course! |
ándale pues | OK then, go ahead | 💡 Mexico
"""),
("🔢 Numbers", "21", """
cero | 0 |
uno | 1 |
dos | 2 |
tres | 3 |
cuatro | 4 |
cinco | 5 |
seis | 6 |
siete | 7 |
ocho | 8 |
nueve | 9 |
diez | 10 |
once | 11 |
doce | 12 |
trece | 13 |
catorce | 14 |
quince | 15 |
dieciséis | 16 |
diecisiete | 17 |
dieciocho | 18 |
diecinueve | 19 |
veinte | 20 |
veintiuno | 21 |
veintidós | 22 |
treinta | 30 |
treinta y uno | 31 | 💡 from 31 up, numbers are written as three words
cuarenta | 40 |
cincuenta | 50 |
sesenta | 60 |
setenta | 70 |
ochenta | 80 |
noventa | 90 |
cien | 100 |
ciento uno | 101 |
doscientos | 200 |
trescientos | 300 |
quinientos | 500 |
setecientos | 700 |
novecientos | 900 |
mil | 1,000 |
dos mil | 2,000 |
un millón | 1,000,000 |
"""),
("📅 Days & months", "19", """
lunes | Monday | 💡 days and months are lowercase
martes | Tuesday |
miércoles | Wednesday |
jueves | Thursday |
viernes | Friday |
sábado | Saturday |
domingo | Sunday |
enero | January |
febrero | February |
marzo | March |
abril | April |
mayo | May |
junio | June |
julio | July |
agosto | August |
septiembre | September |
octubre | October |
noviembre | November |
diciembre | December |
el día | day |
la semana | week |
el fin de semana | weekend |
el mes | month |
el año | year |
hoy | today |
mañana | tomorrow |
ayer | yesterday |
¿Qué día es hoy? | What day is it today? |
¿Qué fecha es hoy? | What's the date today? |
el primero de enero | January 1st | 💡 only the 1st uses primero; then el dos, el tres…
"""),
]

WORDS["nouns"] = [
("🍓 Fruit", "05", """
## Everyday fruit
la fruta | fruit |
la manzana | apple |
la pera | pear |
la naranja | orange |
la mandarina | tangerine |
la toronja | grapefruit | 🌎 pomelo (Arg, Uru) · 🇪🇸 pomelo
el limón | lime (the small green one) | 💡 in Mexico limón is the green lime everyone squeezes on tacos
el limón amarillo | lemon |
la lima | sweet lime | 💡 a mild, sweet citrus — not the same as limón
el plátano | banana | 🌎 banana (Arg), banano (Col), guineo (Caribbean)
el plátano macho | plantain | 🌎 plátano (Caribbean, Col)
la fresa | strawberry | 🌎 frutilla (Arg, Chile)
la uva | grape |
la sandía | watermelon | 🌎 patilla (Ven, Col)
el melón | cantaloupe, melon |
la piña | pineapple | 🌎 ananá (Arg, Uru)
el mango | mango |
la papaya | papaya | 🌎 lechosa (Ven), fruta bomba (Cuba)
el durazno | peach | 🇪🇸 melocotón
el chabacano | apricot | 🌎 damasco (Arg, Chile) · 🇪🇸 albaricoque
la ciruela | plum |
la cereza | cherry |
la frambuesa | raspberry |
la zarzamora | blackberry | 🌎 mora (Col, Central America)
el arándano | blueberry; cranberry |
el higo | fig |
la granada | pomegranate |
el coco | coconut |
el kiwi | kiwi |
## Tropical & Mexican favorites
la guayaba | guava |
la tuna | prickly pear (cactus fruit) | 🇪🇸 higo chumbo
la pitaya | dragon fruit | 🌎 pitahaya
el mamey | mamey sapote |
el zapote negro | black sapote |
el chicozapote | sapodilla |
la guanábana | soursop |
la chirimoya | cherimoya, custard apple |
el tamarindo | tamarind |
el maracuyá | passion fruit | 🌎 parchita (Ven), fruta de la pasión
el lichi | lychee |
la carambola | starfruit |
el nanche | nance (small yellow fruit) |
el tejocote | Mexican hawthorn | 💡 goes in ponche at Christmas
la jícama | jicama | 💡 eaten raw with lime and chile
## From other countries
el lulo | lulo, naranjilla | 🌎 Colombia, Ecuador — not common in Mexico
la uchuva | goldenberry | 🌎 Colombia — not common in Mexico
el marañón | cashew fruit | 🌎 Central America, Venezuela
el mamoncillo | Spanish lime | 🌎 Caribbean, Colombia — not common in Mexico
## Talking about fruit
maduro, madura | ripe |
verde | unripe; green |
pelar | to peel |
"""),
("🥕 Vegetables", "05", """
la verdura | vegetables | 💡 also las legumbres
el jitomate | tomato (red) | 💡 Mexico; the rest of Latin America and 🇪🇸 Spain say tomate
el tomate verde | tomatillo | 💡 the green one for salsa verde; also just tomate in Mexico
la cebolla | onion |
el ajo | garlic |
el chile | chili pepper | 🌎 ají (South America, Caribbean) · 🇪🇸 guindilla
el chile jalapeño | jalapeño |
el chile serrano | serrano pepper |
el chile poblano | poblano pepper |
el chile chipotle | chipotle (smoked jalapeño) |
el pimiento morrón | bell pepper | 🌎 pimentón (Col, Ven), ají (Arg)
la papa | potato | 🇪🇸 patata
el camote | sweet potato | 🌎 batata (Arg, Caribbean), boniato (Cuba)
la zanahoria | carrot |
la lechuga | lettuce |
la espinaca | spinach |
el pepino | cucumber |
la calabaza | pumpkin, squash |
la calabacita | zucchini | 🌎 zapallito (Arg) · 🇪🇸 calabacín
el chayote | chayote squash |
el elote | corn on the cob | 🌎 choclo (South America), mazorca (Col)
el maíz | corn (the grain) |
el nopal | cactus pad |
el aguacate | avocado | 🌎 palta (Arg, Chile, Peru)
el brócoli | broccoli |
la coliflor | cauliflower |
el repollo | cabbage | 💡 also la col
el betabel | beet | 🌎 remolacha (most of Latin America) · 🇪🇸 remolacha
el rábano | radish |
el apio | celery |
el champiñón | mushroom (button) | 💡 any mushroom: el hongo
los chícharos | peas | 🌎 arvejas · 🇪🇸 guisantes
los ejotes | green beans | 🌎 vainitas (Ven, Peru), habichuelas (Col), chauchas (Arg) · 🇪🇸 judías verdes
los frijoles | beans | 🌎 porotos (Arg, Chile), caraotas (Ven) · 🇪🇸 judías, alubias
las lentejas | lentils |
los garbanzos | chickpeas |
el espárrago | asparagus |
la berenjena | eggplant |
la yuca | cassava | 🌎 mandioca (Arg, Paraguay)
el cilantro | cilantro |
el perejil | parsley |
el epazote | epazote (herb for beans) |
la flor de calabaza | squash blossom |
el huitlacoche | corn smut (a delicacy) |
"""),
("🍗 Meat, fish & eggs", "05", """
la carne | meat |
la carne de res | beef | 🌎 carne de vaca (Arg) · 🇪🇸 ternera
el pollo | chicken |
el cerdo | pork; pig | 💡 also el puerco in Mexico
el jamón | ham |
el tocino | bacon | 🇪🇸 beicon
la salchicha | hot dog sausage |
el chorizo | chorizo |
el bistec | steak | 🌎 bife (Arg)
la carne molida | ground meat | 🌎 carne picada (Arg) · 🇪🇸 carne picada
la pechuga | breast (chicken) |
la pierna | leg; drumstick |
las costillas | ribs |
el pavo | turkey | 💡 also el guajolote in Mexico
el pescado | fish (food) | 💡 a live fish is el pez
el camarón | shrimp | 🇪🇸 gamba
el atún | tuna |
el salmón | salmon |
la tilapia | tilapia |
el huachinango | red snapper |
el pulpo | octopus |
el calamar | squid |
los mariscos | seafood |
el huevo | egg |
la yema | yolk |
la clara | egg white |
crudo, cruda | raw |
"""),
("🧂 Dairy & pantry", "05", """
la leche | milk |
el queso | cheese |
el queso fresco | fresh white cheese |
el queso Oaxaca | stringy Oaxaca cheese |
la crema | Mexican sour cream |
la mantequilla | butter | 💡 manteca in Mexico is lard
el yogur | yogurt |
el pan | bread |
el bolillo | crusty bread roll |
la tortilla de maíz | corn tortilla | 🇪🇸 a tortilla in Spain is a potato omelet
la tortilla de harina | flour tortilla |
la masa | corn dough |
el arroz | rice |
los fideos | thin noodles |
la pasta | pasta |
la harina | flour |
el azúcar | sugar |
el piloncillo | cone of brown sugar |
la sal | salt |
la pimienta | black pepper |
la canela | cinnamon |
el aceite | oil |
el vinagre | vinegar |
la mayonesa | mayonnaise |
la mostaza | mustard |
la cátsup | ketchup | 💡 also el kétchup
la salsa | sauce, salsa |
la miel | honey |
la mermelada | jam |
el cereal | cereal |
la avena | oatmeal |
los cacahuates | peanuts | 🌎 maní (most of South America) · 🇪🇸 cacahuetes
la nuez | walnut; pecan |
la almendra | almond |
"""),
("🌮 Mexican dishes", "", """
## Tacos & meats
el taco | taco |
los tacos al pastor | marinated pork tacos |
las carnitas | slow-cooked pork |
la barbacoa | slow-cooked beef or lamb |
la birria | spiced goat or beef stew |
los tacos de canasta | basket tacos (steamed) |
los tacos de suadero | tacos of thin-cut beef | 💡 Mexico City
los tacos de lengua | beef tongue tacos |
la carne asada | grilled beef |
la arrachera | skirt steak |
la cochinita pibil | achiote slow-roasted pork | 💡 Yucatán
la tinga | shredded chicken in chipotle sauce |
el chicharrón | fried pork rind |
la cecina | thin salted beef |
la machaca | dried shredded beef | 💡 northern Mexico
el alambre | grilled meat with peppers, onion and cheese |
el cabrito | roast kid goat | 💡 Monterrey
la carne en su jugo | beef in its own broth | 💡 Guadalajara
## Tortilla & masa dishes
la quesadilla | quesadilla | 💡 in Mexico City it may come without cheese — ask con queso
la enchilada | enchilada |
los chilaquiles | tortilla chips in salsa (breakfast) |
el tamal | tamale | 💡 plural los tamales
la gordita | thick stuffed corn cake |
el sope | thick tortilla with toppings |
el tlacoyo | oval stuffed masa cake |
la tlayuda | big crispy Oaxacan tortilla |
la tostada | crispy flat tortilla with toppings | 🇪🇸 in Spain tostada means toast
la flauta | rolled fried taco |
el burrito | burrito | 💡 mostly a northern Mexico thing
el huarache | long oval masa base with toppings |
la chalupa | small fried tortilla with salsa | 💡 Puebla
la memela | oval masa cake with beans | 💡 Oaxaca, Puebla
el panucho | bean-stuffed fried tortilla | 💡 Yucatán
el salbute | puffy fried tortilla with toppings | 💡 Yucatán
las enfrijoladas | tortillas in bean sauce |
las entomatadas | tortillas in tomato sauce |
las enmoladas | tortillas in mole |
las enchiladas suizas | enchiladas in creamy green sauce |
la empanada | turnover |
## Tortas & bread
la torta | sandwich on a roll | 🌎 a torta is a cake in Arg and Ven
el pambazo | chile-dipped sandwich with potato and chorizo |
la guajolota | tamale inside a bread roll | 💡 Mexico City
la torta ahogada | "drowned" sandwich in salsa | 💡 Guadalajara
los molletes | open roll with beans and melted cheese |
## Breakfast eggs
los huevos rancheros | fried eggs on tortillas with salsa |
los huevos a la mexicana | scrambled eggs with tomato, onion and chile |
los huevos divorciados | two eggs with red and green salsa |
los huevos motuleños | eggs on tortillas with beans, ham and peas | 💡 Yucatán
## Soups & stews
el pozole | hominy soup |
la sopa de tortilla | tortilla soup |
el menudo | tripe soup | 💡 Mexico City says la pancita
el caldo de pollo | chicken soup |
el caldo de res | beef and vegetable soup |
el caldo tlalpeño | chicken soup with chipotle |
la sopa de lima | lime soup | 💡 Yucatán
la sopa de fideo | noodle soup |
el consomé | broth (served with birria, barbacoa) |
el mole de olla | beef and vegetable stew |
## Seafood
el ceviche | ceviche |
el aguachile | raw shrimp in lime and chile | 💡 Sinaloa
el coctel de camarón | shrimp cocktail |
el pescado a la veracruzana | fish with tomato, olives and capers |
el pescado zarandeado | grilled butterflied fish | 💡 Nayarit, Sinaloa
los camarones a la diabla | shrimp in spicy red sauce |
## Moles, salsas & sides
el mole | mole sauce |
el chile relleno | stuffed poblano pepper |
los frijoles refritos | refried beans |
el guacamole | guacamole |
el pico de gallo | fresh tomato salsa |
el arroz rojo | Mexican red rice | 💡 also arroz a la mexicana
los frijoles charros | cowboy beans with pork |
los frijoles de la olla | whole pot beans |
los chiles en nogada | stuffed chiles in walnut sauce | 💡 Puebla, in September
las rajas con crema | poblano strips in cream |
el pipián | pumpkin-seed sauce |
el adobo | chile marinade |
el queso fundido | melted cheese (often with chorizo) |
la ensalada de nopales | cactus salad |
la salsa verde | green salsa |
la salsa roja | red salsa |
la salsa macha | chile oil salsa |
## Street snacks
el esquite | corn in a cup |
el antojito | street snack |
los chicharrones de harina | wheat crisps with hot sauce |
los tostilocos | loaded tortilla-chip snack |
la fruta con chile | fruit with lime and chile powder |
el chamoy | salty-sweet chile sauce |
la chamoyada | mango slush with chamoy | 💡 also la mangonada
"""),
("🥤 Drinks", "05", """
la bebida | drink |
el agua | water |
el agua natural | still water | 💡 agua mineral in Mexico means sparkling water
el agua mineral | sparkling water |
el agua fresca | fruit water |
el agua de jamaica | hibiscus water |
el agua de horchata | rice-cinnamon drink |
el agua de tamarindo | tamarind water |
el jugo | juice | 🇪🇸 zumo
el licuado | smoothie, milkshake | 🌎 batido
el refresco | soda | 🌎 gaseosa (Col, Arg, Peru)
el café | coffee |
el café de olla | spiced coffee with piloncillo |
el té | tea |
el chocolate caliente | hot chocolate |
el atole | warm corn drink |
el champurrado | chocolate atole |
la cerveza | beer | 💡 la chela (slang, Mexico)
la michelada | beer with lime, salt and salsa |
el vino | wine |
el tequila | tequila |
el mezcal | mezcal |
con hielo | with ice |
sin hielo | without ice |
"""),
("🧑 People", "07", """
la persona | person |
la gente | people | 💡 singular: La gente dice que…
el hombre | man |
la mujer | woman |
el niño, la niña | boy, girl; child |
el bebé | baby |
el chico, la chica | boy, girl; young person |
el muchacho, la muchacha | young man, young woman |
el joven | young person |
el señor | man, sir, Mr. |
la señora | woman, ma'am, Mrs. |
la señorita | young woman, Miss |
el vecino, la vecina | neighbor |
el amigo, la amiga | friend |
el compañero, la compañera | classmate; coworker |
el jefe, la jefa | boss |
el desconocido | stranger |
el chavo, la chava | guy, girl | 💡 casual, Mexico
el cuate | buddy | 💡 Mexico
los chamacos | kids | 💡 Mexico
"""),
("👨‍👩‍👧 Family", "07", """
la familia | family |
los padres | parents | 💡 also los papás in Mexico
el papá | dad |
la mamá | mom |
el hijo, la hija | son, daughter |
los hijos | children (sons and daughters) |
el hermano, la hermana | brother, sister |
el abuelo, la abuela | grandfather, grandmother |
el bisabuelo | great-grandfather |
el nieto, la nieta | grandson, granddaughter |
el tío, la tía | uncle, aunt |
el primo, la prima | cousin |
el sobrino, la sobrina | nephew, niece |
el esposo, la esposa | husband, wife |
el suegro, la suegra | father-in-law, mother-in-law |
el cuñado, la cuñada | brother-in-law, sister-in-law |
el yerno | son-in-law |
la nuera | daughter-in-law |
el padrastro | stepfather |
la madrastra | stepmother |
el medio hermano | half brother |
el padrino, la madrina | godfather, godmother |
el compadre, la comadre | co-godparent; close family friend | 💡 a big deal in Mexico
los parientes | relatives |
"""),
]

WORDS["ser-estar"] = [
("😊 Personality (ser)", "04", """
simpático, simpática | nice, likable |
amable | kind |
chistoso, chistosa | funny | 💡 also gracioso
divertido, divertida | fun |
aburrido, aburrida | boring (with ser) | 💡 estar aburrido = bored
trabajador, trabajadora | hard-working |
flojo, floja | lazy | 🌎 vago (Arg) · 🇪🇸 vago
inteligente | intelligent |
listo, lista | clever (with ser) | 💡 estar listo = ready
tímido, tímida | shy |
serio, seria | serious |
generoso, generosa | generous |
tacaño, tacaña | stingy |
honesto, honesta | honest |
mentiroso, mentirosa | liar, lying |
chismoso, chismosa | gossipy |
metiche | nosy | 💡 Mexico
celoso, celosa | jealous |
creído, creída | stuck-up |
terco, terca | stubborn |
educado, educada | polite | 💡 not "educated"
grosero, grosera | rude |
valiente | brave |
miedoso, miedosa | easily scared |
paciente | patient |
buena onda | cool, nice | 💡 Mexico
mala onda | not nice, uncool | 💡 Mexico
sangrón, sangrona | annoying, unpleasant | 💡 Mexico, casual
fresa | posh, preppy | 💡 Mexico, casual
"""),
("🧍 Looks (ser)", "02", """
alto, alta | tall |
bajo, baja | short | 💡 chaparro is very common in Mexico
delgado, delgada | thin | 💡 also flaco
gordito, gordita | chubby | 💡 gordo can sound rude; gordito is affectionate
fuerte | strong |
guapo, guapa | good-looking |
bonito, bonita | pretty |
feo, fea | ugly |
joven | young |
mayor | older, elderly | 💡 politer than viejo
güero, güera | blond, fair-skinned | 💡 Mexico; 🌎 rubio
moreno, morena | dark-haired, dark-skinned |
pelirrojo, pelirroja | redhead |
el pelo largo | long hair |
el pelo corto | short hair |
el pelo chino | curly hair | 💡 Mexico; 🌎 rizado, crespo (Col), enrulado (Arg)
el pelo lacio | straight hair |
pelón, pelona | bald | 💡 Mexico; 🌎 calvo
los ojos cafés | brown eyes | 🌎 ojos marrones (Arg) · 🇪🇸 marrones
los ojos azules | blue eyes |
los ojos verdes | green eyes |
la barba | beard |
el bigote | mustache |
las pecas | freckles |
el tatuaje | tattoo |
"""),
("😟 Feelings (estar)", "04", """
contento, contenta | happy, pleased |
feliz | happy | 💡 usually with estar for a moment, ser for a happy person
triste | sad |
enojado, enojada | angry | 🇪🇸 enfadado
cansado, cansada | tired |
aburrido, aburrida | bored (with estar) |
nervioso, nerviosa | nervous |
preocupado, preocupada | worried |
emocionado, emocionada | excited |
sorprendido, sorprendida | surprised |
asustado, asustada | scared |
apenado, apenada | embarrassed | 💡 Mexico; 🌎 avergonzado
confundido, confundida | confused |
ocupado, ocupada | busy |
tranquilo, tranquila | calm |
estresado, estresada | stressed |
harto, harta | fed up |
enamorado, enamorada | in love |
de buen humor | in a good mood |
de mal humor | in a bad mood |
enfermo, enferma | sick |
listo, lista | ready (with estar) |
desvelado, desvelada | tired from staying up late | 💡 Mexico
crudo, cruda | hungover | 💡 Mexico; 🌎 enguayabado (Col), con resaca
"""),
("👩‍🏫 Jobs", "09", """
el maestro, la maestra | teacher |
el profesor, la profesora | teacher, professor |
el doctor, la doctora | doctor | 💡 also el médico
el enfermero, la enfermera | nurse |
el dentista, la dentista | dentist |
el abogado, la abogada | lawyer |
el ingeniero, la ingeniera | engineer |
el programador, la programadora | programmer |
el policía, la policía | police officer | 💡 la policía also means the police
el bombero, la bombera | firefighter |
el mesero, la mesera | waiter, waitress | 🌎 mozo (Arg), mesonero (Ven) · 🇪🇸 camarero
el cocinero, la cocinera | cook |
el cajero, la cajera | cashier |
el vendedor, la vendedora | salesperson |
el chofer | driver | 🌎 chófer · 🇪🇸 chófer
el taxista | taxi driver |
el mecánico | mechanic |
el plomero | plumber | 🌎 gasfitero (Chile, Peru) · 🇪🇸 fontanero
el electricista | electrician |
el albañil | bricklayer, builder |
el carpintero | carpenter |
el estilista, la estilista | hairdresser |
el contador, la contadora | accountant | 🇪🇸 contable
el secretario, la secretaria | secretary |
el periodista, la periodista | journalist |
el veterinario, la veterinaria | vet |
el gerente, la gerente | manager |
el dueño, la dueña | owner |
el empleado, la empleada | employee |
el ama de casa | homemaker | 💡 la ama → el ama because of the stressed a
el jubilado, la jubilada | retiree |
el estudiante, la estudiante | student |
"""),
("🌎 Countries & nationalities", "01", """
mexicano, mexicana | Mexican — México |
guatemalteco, guatemalteca | Guatemalan — Guatemala |
salvadoreño, salvadoreña | Salvadoran — El Salvador |
hondureño, hondureña | Honduran — Honduras |
nicaragüense | Nicaraguan — Nicaragua |
costarricense | Costa Rican — Costa Rica | 💡 casual: tico, tica
panameño, panameña | Panamanian — Panamá |
cubano, cubana | Cuban — Cuba |
dominicano, dominicana | Dominican — República Dominicana |
puertorriqueño, puertorriqueña | Puerto Rican — Puerto Rico | 💡 also boricua
colombiano, colombiana | Colombian — Colombia |
venezolano, venezolana | Venezuelan — Venezuela |
ecuatoriano, ecuatoriana | Ecuadorian — Ecuador |
peruano, peruana | Peruvian — Perú |
boliviano, boliviana | Bolivian — Bolivia |
chileno, chilena | Chilean — Chile |
argentino, argentina | Argentine — Argentina |
uruguayo, uruguaya | Uruguayan — Uruguay |
paraguayo, paraguaya | Paraguayan — Paraguay |
estadounidense | American — Estados Unidos | 💡 also americano, gringo (casual)
canadiense | Canadian — Canadá |
brasileño, brasileña | Brazilian — Brasil |
español, española | Spanish — España |
"""),
]

WORDS["present-regular"] = [
("🗣️ -ar verbs", "", """
hablar | to talk, speak |
trabajar | to work |
estudiar | to study |
cocinar | to cook |
comprar | to buy |
preparar | to prepare |
tomar | to take; to drink |
llegar | to arrive |
regresar | to come back |
caminar | to walk |
escuchar | to listen |
mirar | to look at, watch |
buscar | to look for |
llamar | to call |
platicar | to chat | 💡 Mexico; 🌎 conversar, charlar
chismear | to gossip |
ayudar | to help |
limpiar | to clean |
lavar | to wash |
manejar | to drive | 🇪🇸 conducir
necesitar | to need |
esperar | to wait; to hope |
pagar | to pay |
usar | to use |
viajar | to travel |
bailar | to dance |
cantar | to sing |
nadar | to swim |
terminar | to finish |
descansar | to rest |
ganar | to win; to earn |
contestar | to answer |
enseñar | to teach; to show |
desayunar | to have breakfast |
cenar | to have dinner |
"""),
("📖 -er & -ir verbs", "", """
comer | to eat |
beber | to drink | 💡 tomar is more common in Mexico
correr | to run |
leer | to read |
aprender | to learn |
comprender | to understand |
vender | to sell |
deber | to owe; should |
creer | to believe |
responder | to answer |
prometer | to promise |
barrer | to sweep |
romper | to break |
vivir | to live |
escribir | to write |
abrir | to open |
recibir | to receive |
decidir | to decide |
compartir | to share |
subir | to go up; to upload |
discutir | to argue |
asistir | to attend | 💡 not "to assist"
describir | to describe |
permitir | to allow |
sufrir | to suffer |
"""),
("🛁 Daily routine", "02", """
despertarse | to wake up |
levantarse | to get up |
bañarse | to shower, bathe | 💡 Mexico says bañarse for a shower · 🇪🇸 ducharse
lavarse los dientes | to brush your teeth | 💡 also cepillarse
peinarse | to comb your hair |
vestirse | to get dressed |
maquillarse | to put on makeup |
rasurarse | to shave | 🌎 afeitarse
arreglarse | to get ready |
desayunar | to have breakfast |
irse al trabajo | to leave for work |
ir a la escuela | to go to school |
comer | to eat; to have the main meal | 💡 in Mexico la comida is the big meal, around 2–4 pm
tomar una siesta | to take a nap |
cenar | to have dinner |
ver la tele | to watch TV |
acostarse | to go to bed |
dormirse | to fall asleep |
quedarse dormido | to oversleep; to fall asleep |
desvelarse | to stay up late |
"""),
("🍽️ Meals & times of day", "05", """
el desayuno | breakfast |
el almuerzo | late breakfast, brunch | 💡 Mexico; 🌎 lunch in most other countries
la comida | main midday meal; food |
la cena | dinner |
la merienda | afternoon snack |
la botana | snack, appetizer | 💡 Mexico; 🌎 picada (Arg), pasabocas (Col) · 🇪🇸 tapa
el antojo | craving |
la madrugada | early morning (after midnight) |
en la mañana | in the morning | 🇪🇸 por la mañana
al mediodía | at noon |
en la tarde | in the afternoon |
en la noche | at night |
temprano | early |
tarde | late |
"""),
("🔁 How often", "19", """
siempre | always |
casi siempre | almost always |
a veces | sometimes |
de vez en cuando | once in a while |
casi nunca | hardly ever |
nunca | never |
todos los días | every day |
diario | daily | 💡 Mexico: Voy diario.
seguido | often | 💡 Mexico
a menudo | often |
cada semana | every week |
una vez a la semana | once a week |
dos veces al día | twice a day |
los lunes | on Mondays |
los fines de semana | on weekends |
de lunes a viernes | Monday to Friday |
normalmente | usually |
por lo general | generally |
"""),
]

WORDS["irregulars"] = [
("❓ Question words", "23", """
¿Qué? | What? |
¿Quién? | Who? (one) |
¿Quiénes? | Who? (more than one) |
¿Dónde? | Where? |
¿Adónde? | Where to? |
¿De dónde? | Where from? |
¿Cuándo? | When? |
¿Por qué? | Why? | 💡 porque = because
¿Para qué? | What for? |
¿Cómo? | How? |
¿Cuál? | Which? What? (one) |
¿Cuáles? | Which? (more than one) |
¿Cuánto? | How much? |
¿Cuántos? | How many? |
¿A qué hora? | At what time? |
¿Con quién? | With whom? |
¿De quién? | Whose? |
¿Qué pasó? | What happened? |
¿En serio? | Seriously? |
¿Neta? | Really? For real? | 💡 Mexico, casual
¿A poco? | No way, really? | 💡 Mexico
"""),
("⭐ Key irregular verbs", "", """
ser | to be (who, what) | 💡 soy, eres, es, somos, son
estar | to be (where, how) | 💡 estoy, estás, está, estamos, están
ir | to go | 💡 voy, vas, va, vamos, van
tener | to have | 💡 tengo, tienes, tiene
hacer | to do, make | 💡 hago
decir | to say, tell | 💡 digo, dices
poner | to put | 💡 pongo
salir | to go out, leave | 💡 salgo
venir | to come | 💡 vengo, vienes
traer | to bring; to have on you | 💡 traigo
oír | to hear | 💡 oigo, oyes
dar | to give | 💡 doy
saber | to know (facts) | 💡 sé
conocer | to know (people, places) | 💡 conozco
ver | to see | 💡 veo
caer | to fall | 💡 caigo
"""),
("🏘️ Places in town", "18", """
la casa | house, home |
el edificio | building |
el departamento | apartment | 🌎 apartamento (Col, Ven) · 🇪🇸 piso
la colonia | neighborhood | 💡 Mexico; 🌎 el barrio
el barrio | neighborhood |
la calle | street |
la esquina | corner |
la tienda | store |
la tiendita | corner store | 💡 Mexico; also la tienda de abarrotes
el mercado | market |
el tianguis | open-air street market | 💡 Mexico
el supermercado | supermarket | 💡 el súper
la panadería | bakery |
la tortillería | tortilla shop |
la carnicería | butcher shop |
la farmacia | pharmacy |
el banco | bank |
el cajero automático | ATM |
la iglesia | church |
la escuela | school |
el parque | park |
la plaza | square; mall |
el zócalo | main square | 💡 Mexico
el centro | downtown |
el hospital | hospital |
la oficina | office |
el restaurante | restaurant |
la fonda | small family restaurant | 💡 Mexico
la taquería | taco place |
el puesto | street stall |
la gasolinera | gas station |
la papelería | stationery store |
la lavandería | laundromat |
el gimnasio | gym |
el cine | movie theater |
la biblioteca | library |
el correo | post office |
"""),
("🤫 Gossip expressions", "", """
el chisme | gossip |
el rumor | rumor |
¿Ya supiste? | Did you hear? |
dicen que | they say that |
me contaron que | someone told me that |
fíjate que | guess what, get this |
¡No me digas! | You don't say! |
¡Qué escándalo! | What a scandal! |
¡Cuéntamelo todo! | Tell me everything! |
no le digas a nadie | don't tell anyone |
entre nos | between us | 💡 Mexico
se rumora que | rumor has it |
¡Híjole! | Oh man! Yikes! | 💡 Mexico
¡Órale! | Wow! / OK, let's go! | 💡 Mexico
¡Qué oso! | How embarrassing! | 💡 Mexico
¡No manches! | No way! | 💡 Mexico
¡No inventes! | You're kidding! | 💡 Mexico
¡Qué metiche! | So nosy! | 💡 Mexico
"""),
]

WORDS["stem-changers"] = [
("🍽️ At the restaurant", "05", """
la mesa | table |
el menú | menu | 💡 also la carta
el mesero, la mesera | waiter, waitress | 🌎 mozo (Arg) · 🇪🇸 camarero
la cuenta | the check | 💡 La cuenta, por favor.
la propina | tip |
la orden | order; serving | 💡 Mexico: una orden de tacos
para llevar | to go |
para comer aquí | for here |
la reservación | reservation | 🇪🇸 reserva
la entrada | starter |
el plato fuerte | main course |
el postre | dessert |
la comida corrida | set lunch menu | 💡 Mexico; 🇪🇸 menú del día
la especialidad de la casa | house specialty |
¿Qué me recomienda? | What do you recommend? |
¿Me trae…? | Could you bring me…? |
quisiera… | I'd like… |
para mí… | for me… |
sin cebolla | without onion |
bien cocido | well done |
término medio | medium (steak) | 💡 Mexico
la salsa picante | hot sauce |
el baño | restroom |
"""),
("🍴 Table & kitchen", "06", """
el plato | plate |
el tazón | bowl | 💡 also el plato hondo
el vaso | glass |
la taza | cup |
la copa | wine glass |
el tenedor | fork |
el cuchillo | knife |
la cuchara | spoon |
la cucharita | teaspoon |
la servilleta | napkin |
el mantel | tablecloth |
la jarra | pitcher |
el popote | straw | 🌎 pitillo (Col, Ven), sorbete (Arg) · 🇪🇸 pajita
la olla | pot |
el sartén | frying pan | 💡 Mexico says el sartén; 🌎 🇪🇸 la sartén
el comal | flat griddle for tortillas |
el molcajete | stone mortar for salsa |
la tapa | lid |
el cucharón | ladle |
la licuadora | blender | 🇪🇸 batidora
la estufa | stove | 🌎 cocina (Arg, Chile) · 🇪🇸 cocina, fogón
el horno | oven |
el microondas | microwave |
el refrigerador | refrigerator | 💡 el refri · 🌎 heladera (Arg), nevera (Col, Ven) · 🇪🇸 nevera, frigorífico
la tabla para picar | cutting board |
el colador | strainer |
el abrelatas | can opener |
"""),
("👩‍🍳 Cooking verbs", "05", """
cocinar | to cook |
hervir | to boil | 💡 hierve
freír | to fry | 💡 frío, fríe
asar | to grill, roast |
hornear | to bake |
picar | to chop | 💡 also "to sting, be spicy": Esto pica.
cortar | to cut |
pelar | to peel |
mezclar | to mix |
batir | to beat, whisk |
revolver | to stir | 💡 revuelve
calentar | to heat up | 💡 calienta
enfriar | to cool |
agregar | to add | 💡 also echar, añadir
probar | to taste, try | 💡 prueba
sazonar | to season |
licuar | to blend |
rallar | to grate |
derretir | to melt |
tostar | to toast | 💡 tuesta
exprimir | to squeeze |
servir | to serve | 💡 sirve
"""),
("😋 Flavors & textures", "05", """
dulce | sweet |
salado, salada | salty |
picante | spicy | 💡 Mexico also says ¡Pica!
agrio, agria | sour |
amargo, amarga | bitter |
rico, rica | tasty | 💡 with estar for food you're eating
sabroso, sabrosa | tasty |
delicioso, deliciosa | delicious |
desabrido, desabrida | bland | 💡 also sin sabor · 🇪🇸 soso
crujiente | crunchy |
suave | soft |
jugoso, jugosa | juicy |
duro, dura | hard, tough |
cocido, cocida | cooked |
frito, frita | fried |
asado, asada | grilled |
quemado, quemada | burnt |
fresco, fresca | fresh |
echado a perder | spoiled, gone bad | 💡 Mexico
caliente | hot |
tibio, tibia | lukewarm |
frío, fría | cold |
"""),
("🔄 Stem-changing verbs", "", """
pensar (e→ie) | to think |
querer (e→ie) | to want; to love |
preferir (e→ie) | to prefer |
empezar (e→ie) | to begin |
entender (e→ie) | to understand |
cerrar (e→ie) | to close |
perder (e→ie) | to lose |
recomendar (e→ie) | to recommend |
sentir (e→ie) | to feel |
mentir (e→ie) | to lie |
poder (o→ue) | to be able, can |
volver (o→ue) | to return |
costar (o→ue) | to cost |
almorzar (o→ue) | to have lunch |
dormir (o→ue) | to sleep |
encontrar (o→ue) | to find |
contar (o→ue) | to tell; to count |
recordar (o→ue) | to remember |
probar (o→ue) | to taste, try |
devolver (o→ue) | to give back |
pedir (e→i) | to ask for, order |
servir (e→i) | to serve |
repetir (e→i) | to repeat |
seguir (e→i) | to follow, keep going |
conseguir (e→i) | to get |
jugar (u→ue) | to play |
"""),
("🍮 Sweets & pan dulce", "05", """
el pan dulce | sweet bread |
la concha | shell-topped sweet bun |
el cuerno | croissant-style roll |
la oreja | palmier pastry |
la dona | donut |
el churro | churro |
el flan | flan |
el arroz con leche | rice pudding |
la gelatina | gelatin dessert |
el pastel | cake | 🌎 torta (Arg, Ven), ponqué (Col)
el pastel de tres leches | tres leches cake |
el pay | pie | 💡 Mexico
el helado | ice cream |
la nieve | sorbet-style ice cream | 💡 Mexico
la paleta | popsicle; lollipop | 💡 Mexico
los dulces | candy |
la cajeta | goat-milk caramel | 💡 Mexico; 🌎 dulce de leche
la galleta | cookie |
la rosca de reyes | Three Kings bread |
el pan de muerto | Day of the Dead bread |
las alegrías | amaranth candy bars |
"""),
]

WORDS["gustar"] = [
("💖 Verbs like gustar", "04", """
gustar | to like (be pleasing) | 💡 Me gusta el café. Me gustan los tacos.
encantar | to love (things) |
fascinar | to fascinate |
interesar | to interest |
importar | to matter |
molestar | to bother |
caer bien | to like (a person) | 💡 Javi me cae bien.
caer mal | to dislike (a person) |
doler | to hurt | 💡 Me duele la cabeza.
faltar | to be missing, lack |
quedar | to fit; to have left |
parecer | to seem |
aburrir | to bore |
preocupar | to worry |
dar miedo | to scare | 💡 Me dan miedo las arañas.
dar pena | to embarrass | 💡 Mexico
dar asco | to disgust |
dar flojera | to not feel like it | 💡 Mexico: Me da flojera.
antojarse | to crave | 💡 Mexico: Se me antoja un taco.
"""),
("🎨 Hobbies", "10", """
el pasatiempo | hobby |
leer | to read |
ver series | to watch shows |
ir al cine | to go to the movies |
escuchar música | to listen to music |
cantar | to sing |
bailar | to dance |
tocar la guitarra | to play guitar |
tocar el piano | to play piano |
dibujar | to draw |
pintar | to paint |
cocinar | to cook |
tejer | to knit |
coser | to sew |
la jardinería | gardening |
tomar fotos | to take photos |
viajar | to travel |
acampar | to go camping |
pescar | to fish |
ir de compras | to go shopping |
jugar videojuegos | to play video games |
jugar cartas | to play cards |
jugar dominó | to play dominoes |
jugar ajedrez | to play chess |
salir con amigos | to go out with friends |
ir de fiesta | to go partying |
pasear al perro | to walk the dog |
hacer ejercicio | to exercise |
armar rompecabezas | to do jigsaw puzzles |
"""),
("⚽ Sports", "10", """
el deporte | sport |
el fútbol | soccer |
el fútbol americano | American football |
el béisbol | baseball |
el básquetbol | basketball | 🌎 baloncesto · 🇪🇸 baloncesto
el voleibol | volleyball |
el tenis | tennis |
la natación | swimming |
el ciclismo | cycling |
el boxeo | boxing |
la lucha libre | Mexican wrestling |
el atletismo | track and field |
correr | to run |
nadar | to swim |
andar en bicicleta | to ride a bike | 🇪🇸 montar en bici
patinar | to skate |
el equipo | team |
el partido | game, match |
el jugador, la jugadora | player |
el entrenador | coach |
el árbitro | referee |
el aficionado | fan |
la porra | cheering fans; cheer | 💡 Mexico
el gol | goal |
meter un gol | to score a goal |
la cancha | field, court | 🇪🇸 campo, pista
el estadio | stadium |
ganar | to win |
perder | to lose |
empatar | to tie |
"""),
("🎶 Music & dance", "12", """
la música | music |
la canción | song |
la letra | lyrics |
el cantante, la cantante | singer |
el grupo | band | 💡 also la banda
el concierto | concert |
la guitarra | guitar |
la batería | drums |
el violín | violin |
la trompeta | trumpet |
el mariachi | mariachi |
la música ranchera | ranchera |
la cumbia | cumbia |
la salsa | salsa |
el reguetón | reggaeton |
la banda | Mexican brass-band music |
la música norteña | norteño |
el corrido | ballad (story song) |
el bolero | bolero |
la bachata | bachata |
el merengue | merengue |
el son jarocho | son jarocho (Veracruz folk) |
el rock | rock |
"""),
("🎬 Movies & TV", "10", """
la película | movie | 💡 la peli
la serie | TV series |
la telenovela | soap opera |
el capítulo | episode |
la temporada | season |
el actor | actor |
la actriz | actress |
el personaje | character |
el final | ending |
la comedia | comedy |
el drama | drama |
de terror | horror |
de acción | action |
de ciencia ficción | sci-fi |
las caricaturas | cartoons | 💡 Mexico; 🌎 dibujos animados
el documental | documentary |
el noticiero | the news (program) |
la tele | TV |
el control remoto | remote control |
el canal | channel |
las palomitas | popcorn | 🌎 pochoclo (Arg), crispetas (Col), cotufas (Ven)
los subtítulos | subtitles |
doblada | dubbed |
el estreno | premiere |
"""),
]

WORDS["progressive"] = [
("🏠 Rooms of the house", "06", """
la sala | living room |
el comedor | dining room |
la cocina | kitchen |
la recámara | bedroom | 💡 Mexico; 🌎 cuarto, habitación, pieza (Arg) · 🇪🇸 dormitorio
el baño | bathroom |
el pasillo | hallway |
la escalera | stairs |
el patio | patio, yard |
el jardín | garden, yard |
la cochera | garage | 💡 Mexico; 🌎 garaje
la azotea | flat roof | 💡 Mexico: where the laundry and water tank are
el techo | roof; ceiling |
el piso | floor; story | 💡 🇪🇸 piso also means apartment
la pared | wall |
la puerta | door |
la ventana | window |
el balcón | balcony |
el sótano | basement |
el cuarto de lavado | laundry room |
"""),
("🛋️ Furniture & bedding", "06", """
la cama | bed |
el sillón | armchair; sofa |
el sofá | sofa |
la silla | chair |
la mesa | table |
el escritorio | desk |
el clóset | closet | 💡 also el ropero
el buró | nightstand | 💡 Mexico; 🌎 mesita de noche
la cómoda | dresser |
el librero | bookshelf | 💡 Mexico; 🌎 estante, biblioteca
el espejo | mirror |
la lámpara | lamp |
el tapete | rug | 💡 Mexico; 🌎 alfombra
la cortina | curtain |
el cojín | cushion |
el cuadro | picture, painting |
la hamaca | hammock |
la almohada | pillow |
la cobija | blanket | 🌎 frazada (Arg), manta
la sábana | sheet |
el colchón | mattress |
"""),
("🔌 Things around the house", "06", """
la estufa | stove |
la lavadora | washing machine |
la secadora | dryer |
la plancha | iron |
la aspiradora | vacuum cleaner |
la televisión | TV |
el ventilador | fan |
el aire acondicionado | air conditioning |
el foco | light bulb | 🌎 bombillo (Col, Ven), ampolleta (Chile) · 🇪🇸 bombilla
el apagador | light switch | 🌎 interruptor
el contacto | outlet | 💡 Mexico; 🌎 enchufe, tomacorriente
la llave | faucet; key | 🌎 grifo, canilla (Arg)
el fregadero | kitchen sink | 🌎 lavaplatos (Col), pileta (Arg)
el lavabo | bathroom sink | 🌎 lavamanos
el excusado | toilet | 💡 Mexico; also el inodoro, el baño
la regadera | shower | 💡 Mexico; 🌎 ducha
la tina | bathtub | 🌎 bañera
el calentador | water heater | 💡 Mexico; 🌎 boiler
la escoba | broom |
el trapeador | mop | 💡 Mexico; 🌎 trapero (Col), coleto (Ven) · 🇪🇸 fregona
el recogedor | dustpan |
la cubeta | bucket | 🌎 balde
el cloro | bleach | 🇪🇸 lejía
el jabón | soap |
el bote de basura | trash can | 🌎 tacho (Arg), caneca (Col) · 🇪🇸 cubo de basura
"""),
("🧹 Chores", "06", """
barrer | to sweep |
trapear | to mop |
sacudir | to dust |
aspirar | to vacuum |
lavar los trastes | to do the dishes | 💡 Mexico; 🌎 lavar los platos · 🇪🇸 fregar
secar | to dry |
tender la cama | to make the bed |
tender la ropa | to hang up laundry |
doblar la ropa | to fold laundry |
planchar | to iron |
sacar la basura | to take out the trash |
limpiar el baño | to clean the bathroom |
regar las plantas | to water the plants |
cortar el pasto | to mow the lawn | 🌎 cortar la grama (Ven) · 🇪🇸 cortar el césped
poner la mesa | to set the table |
levantar la mesa | to clear the table | 🌎 recoger la mesa · 🇪🇸 quitar la mesa
recoger el cuarto | to tidy the room |
hacer el súper | to do the grocery shopping | 💡 Mexico
darle de comer al gato | to feed the cat |
arreglar | to fix |
"""),
("📱 Phone & texting", "16", """
el celular | cell phone | 🇪🇸 el móvil
el mensaje | message |
mandar un mensaje | to send a message |
mandar un whats | to send a WhatsApp | 💡 Mexico, casual
llamar | to call |
la llamada | call |
marcar | to dial; to call | 💡 ¿Me marcas? = Will you call me?
contestar | to answer |
colgar | to hang up |
¿Bueno? | Hello? (answering the phone) | 💡 Mexico; 🌎 ¿Aló?, ¿Hola? · 🇪🇸 ¿Diga?
la pila | battery | 💡 Mexico; 🌎 batería
cargar el celular | to charge the phone |
el cargador | charger |
la señal | signal |
los datos | mobile data |
la foto | photo |
la selfi | selfie |
el audio | voice message |
las redes sociales | social media |
publicar | to post |
subir una foto | to upload a photo |
compartir | to share |
el grupo | group chat |
dejar en visto | to leave on read |
bloquear | to block |
"""),
]

WORDS["coming-going"] = [
("🚌 Getting around", "17", """
el carro | car | 🌎 auto (Arg, Chile) · 🇪🇸 coche
el camión | bus | 🌎 bus, colectivo (Arg), guagua (Caribbean) · 🇪🇸 autobús
la combi | minibus | 💡 Mexico; also el pesero (Mexico City)
el metro | subway |
el metrobús | rapid-transit bus |
el tren | train |
el avión | plane |
el taxi | taxi |
la bicicleta | bicycle | 💡 la bici
la moto | motorcycle |
a pie | on foot |
la parada | stop (bus) |
la estación | station |
la central de autobuses | bus station | 💡 Mexico; 🌎 terminal de buses
el boleto | ticket | 🌎 pasaje (trip) · 🇪🇸 billete
el chofer | driver |
el pasajero | passenger |
el tráfico | traffic |
la hora pico | rush hour | 🇪🇸 hora punta
subirse a | to get on |
bajarse de | to get off |
tomar el camión | to take the bus | 💡 Mexico uses tomar, not coger
"""),
("🧭 Directions", "19", """
a la derecha | to the right |
a la izquierda | to the left |
derecho | straight ahead | 💡 todo derecho · 🌎 recto
la cuadra | block | 🇪🇸 manzana
la esquina | corner |
el semáforo | traffic light |
la glorieta | roundabout | 💡 Mexico; 🌎 rotonda
dar vuelta | to turn | 💡 Mexico; 🌎 doblar, girar
cruzar la calle | to cross the street |
seguir | to keep going |
cerca de | near |
lejos de | far from |
enfrente de | across from, in front of |
al lado de | next to |
junto a | right next to |
detrás de | behind |
entre | between |
a dos cuadras | two blocks away |
¿Dónde queda…? | Where is…? |
¿Cómo llego a…? | How do I get to…? |
aquí | here |
ahí | there |
allá | over there |
el norte | north |
el sur | south |
el oriente | east | 💡 Mexico street names use oriente / poniente
el poniente | west |
"""),
("🚶 Coming & going verbs", "17", """
ir | to go |
irse | to leave, go away |
venir | to come |
llegar | to arrive |
salir | to go out, leave |
entrar | to go in |
regresar | to come back |
volver | to return |
quedarse | to stay |
subir | to go up |
bajar | to go down |
caminar | to walk |
correr | to run |
cruzar | to cross |
pasar | to pass; to come in |
pasar por | to pick (someone) up | 💡 Paso por ti a las ocho.
dejar | to drop off; to leave |
llevar | to take (somewhere) |
traer | to bring |
acompañar | to go with |
mudarse | to move (house) |
visitar | to visit |
"""),
("🚗 Car & road", "17", """
manejar | to drive | 🇪🇸 conducir
la licencia de manejo | driver's license | 🌎 licencia de conducir, pase (Col) · 🇪🇸 carné de conducir
la gasolina | gas |
la gasolinera | gas station | 🌎 bomba (Col, Ven), estación de servicio
la llanta | tire | 🌎 goma (Arg), caucho (Ven) · 🇪🇸 neumático
la llanta ponchada | flat tire | 💡 Mexico; 🌎 pinchada
la cajuela | trunk | 🌎 baúl (Col, Arg), maleta (Chile) · 🇪🇸 maletero
el cofre | hood | 💡 Mexico; 🌎 capó
el volante | steering wheel |
el freno | brake |
el cinturón de seguridad | seat belt |
la placa | license plate | 🌎 patente (Arg, Chile) · 🇪🇸 matrícula
el tope | speed bump | 💡 Mexico; 🌎 lomo de burro (Arg), policía acostado (Col) · 🇪🇸 badén
la carretera | highway |
la autopista | freeway |
la caseta | toll booth | 💡 Mexico; 🌎 peaje
la multa | fine, ticket |
estacionarse | to park | 🌎 parquear (Col, Caribbean) · 🇪🇸 aparcar
el estacionamiento | parking lot | 🌎 parqueadero (Col) · 🇪🇸 aparcamiento, parking
el embotellamiento | traffic jam | 💡 also el tráfico
chocar | to crash |
la grúa | tow truck |
la banqueta | sidewalk | 🌎 vereda (Arg), acera · 🇪🇸 acera
el peatón | pedestrian |
"""),
]

WORDS["ir-a"] = [
("⏭️ Future time words", "19", """
mañana | tomorrow |
pasado mañana | the day after tomorrow |
esta noche | tonight |
este fin de semana | this weekend |
la próxima semana | next week | 💡 Mexico also says la semana que entra
el próximo mes | next month |
el año que viene | next year |
el lunes que viene | next Monday |
al rato | later | 💡 Mexico
luego | later, then |
más tarde | later |
pronto | soon |
ahorita | in a moment | 💡 Mexico — can mean now, soon or never
en un ratito | in a little while |
dentro de dos días | in two days |
en dos semanas | in two weeks |
a fin de mes | at the end of the month |
algún día | someday |
"""),
("🗓️ Weekend plans", "10", """
hacer planes | to make plans |
ir a la playa | to go to the beach |
ir de compras | to go shopping |
ir al tianguis | to go to the street market | 💡 Mexico
salir a cenar | to go out to dinner |
quedarse en casa | to stay home |
visitar a la familia | to visit family |
descansar | to rest |
dormir hasta tarde | to sleep in |
hacer una carne asada | to have a barbecue | 💡 Mexico; 🌎 asado (Arg)
ir a misa | to go to Mass |
ver el partido | to watch the game |
ir al antro | to go clubbing | 💡 Mexico; 🌎 discoteca, boliche (Arg)
echarse una chela | to grab a beer | 💡 Mexico, casual
quedar de verse | to agree to meet | 💡 Mexico; 🇪🇸 quedar
tener una cita | to have a date; an appointment |
invitar | to invite; to treat |
cancelar | to cancel |
"""),
("🎉 Parties", "10", """
la fiesta | party |
la pachanga | party | 💡 Mexico, casual
el cumpleaños | birthday |
¡Feliz cumpleaños! | Happy birthday! |
Las Mañanitas | the Mexican birthday song |
los invitados | guests |
el anfitrión | host |
el regalo | gift |
el pastel | cake |
las velas | candles |
la piñata | piñata |
los dulces | candy |
la sorpresa | surprise |
la boda | wedding |
los novios | the bride and groom; couple |
los quince años | 15th birthday party | 💡 la quinceañera is the girl
el bautizo | baptism |
el brindis | toast |
¡Salud! | Cheers! |
¡Felicidades! | Congratulations! |
colarse | to crash a party |
la cruda | hangover | 💡 Mexico; 🌎 guayabo (Col), resaca · 🇪🇸 resaca
"""),
("🎆 Holidays & traditions", "13", """
el día festivo | holiday |
el puente | long weekend | 💡 Mexico, Spain
la Navidad | Christmas |
la Nochebuena | Christmas Eve |
las posadas | Christmas processions (Dec 16–24) |
la pastorela | nativity play |
el Año Nuevo | New Year |
el Día de Reyes | Three Kings Day (Jan 6) |
el Día de la Candelaria | Candlemas (Feb 2) — tamales day |
la Semana Santa | Holy Week |
el Día de las Madres | Mother's Day (May 10 in Mexico) |
el Día del Padre | Father's Day |
el Grito | Independence night (Sept 15) |
el Día de la Independencia | Independence Day (Sept 16) |
el Día de Muertos | Day of the Dead (Nov 1–2) |
la ofrenda | Day of the Dead altar | 💡 also el altar
la calavera | skull; funny death poem |
la catrina | elegant skeleton lady |
el cempasúchil | marigold |
el Día de la Virgen de Guadalupe | Our Lady of Guadalupe Day (Dec 12) |
el Carnaval | Carnival |
la feria | fair |
el desfile | parade |
los fuegos artificiales | fireworks | 💡 also los cohetes
"""),
]

WORDS["future"] = [
("⛅ Weather", "18", """
el clima | weather |
el pronóstico | forecast |
hace sol | it's sunny |
hace calor | it's hot |
hace frío | it's cold |
hace fresco | it's cool |
hace viento | it's windy |
está nublado | it's cloudy |
está despejado | it's clear |
llueve | it rains | 💡 está lloviendo = it's raining now
la lluvia | rain |
la llovizna | drizzle |
el aguacero | downpour |
la tormenta | storm |
el relámpago | lightning |
el trueno | thunder |
el granizo | hail |
la nieve | snow |
la neblina | fog |
la humedad | humidity |
el huracán | hurricane |
el temblor | earthquake | 💡 also el sismo; a big one is un terremoto
la temperatura | temperature |
los grados | degrees |
el paraguas | umbrella |
el impermeable | raincoat |
"""),
("🏔️ Seasons & nature", "18", """
la primavera | spring |
el verano | summer |
el otoño | fall |
el invierno | winter |
la temporada de lluvias | rainy season |
la temporada de secas | dry season | 💡 Mexico
el sol | sun |
la luna | moon |
las estrellas | stars |
el cielo | sky |
la nube | cloud |
el mar | sea |
el río | river |
el lago | lake |
la montaña | mountain |
el cerro | hill |
el volcán | volcano |
el bosque | forest |
la selva | jungle, rainforest |
el desierto | desert |
la isla | island |
la cascada | waterfall |
la cueva | cave |
el árbol | tree |
la flor | flower |
la planta | plant |
el pasto | grass | 🌎 grama (Ven) · 🇪🇸 césped, hierba
la tierra | earth, soil |
la piedra | rock, stone |
la arena | sand |
"""),
("🐾 Animals", "18", """
el perro | dog |
el gato | cat |
el pájaro | bird |
el pez | fish (live) | 💡 pescado = fish you eat
la vaca | cow |
el toro | bull |
el caballo | horse |
el burro | donkey |
el puerco | pig | 💡 also el cerdo, el cochino
la gallina | hen |
el gallo | rooster |
el pollito | chick |
el borrego | sheep | 💡 Mexico; 🌎 oveja
el chivo | goat | 💡 also la cabra
el conejo | rabbit |
el ratón | mouse |
la rata | rat |
la ardilla | squirrel |
el chango | monkey | 💡 Mexico; 🌎 mono
el león | lion |
el tigre | tiger |
el jaguar | jaguar |
el oso | bear |
el lobo | wolf |
el coyote | coyote |
la víbora | snake | 💡 also la serpiente
la tortuga | turtle |
la rana | frog |
el cocodrilo | crocodile |
la iguana | iguana |
el águila | eagle |
el perico | parrot | 💡 Mexico; 🌎 loro
el colibrí | hummingbird |
la mariposa | butterfly |
la abeja | bee |
la hormiga | ant |
la mosca | fly |
el mosquito | mosquito | 🌎 zancudo (Col, Ven, Central America)
la cucaracha | cockroach |
la araña | spider |
el alacrán | scorpion | 💡 Mexico; 🌎 escorpión
el delfín | dolphin |
la ballena | whale |
el tiburón | shark |
el ajolote | axolotl |
el tlacuache | opossum | 💡 Mexico; 🌎 zarigüeya, chucha (Col)
el guajolote | turkey | 💡 Mexico
"""),
("🎓 Life events & careers", "09", """
nacer | to be born |
crecer | to grow up |
graduarse | to graduate |
la graduación | graduation |
la carrera | college degree; career |
la universidad | university |
conseguir trabajo | to get a job |
la chamba | job, work | 💡 Mexico, casual
cambiar de trabajo | to change jobs |
el sueldo | salary |
ahorrar | to save (money) |
rentar | to rent | 💡 Mexico; 🌎 alquilar, arrendar
comprar una casa | to buy a house |
mudarse | to move (house) |
enamorarse | to fall in love |
comprometerse | to get engaged |
casarse | to get married |
divorciarse | to get divorced |
tener hijos | to have children |
embarazada | pregnant | 💡 not "embarrassed" — that's apenada
jubilarse | to retire |
envejecer | to grow old |
morir | to die |
la meta | goal |
el sueño | dream |
tener éxito | to be successful | 💡 not "to have an exit"
independizarse | to move out, become independent |
"""),
]

WORDS["preterite"] = [
("⏪ Past time words", "19", """
ayer | yesterday |
antier | the day before yesterday | 💡 Mexico; 🌎 anteayer
anoche | last night |
la semana pasada | last week |
el mes pasado | last month |
el año pasado | last year |
el lunes pasado | last Monday |
hace dos días | two days ago |
hace una semana | a week ago |
hace mucho | a long time ago |
el otro día | the other day |
esta mañana | this morning |
una vez | once |
de repente | suddenly |
primero | first |
luego | then |
después | afterward |
al final | in the end |
entonces | so, then |
ya | already |
todavía no | not yet |
en ese momento | at that moment |
"""),
("🫀 The body", "02", """
el cuerpo | body |
la cabeza | head |
la cara | face |
el pelo | hair |
los ojos | eyes |
las cejas | eyebrows |
las pestañas | eyelashes |
la nariz | nose |
la boca | mouth |
los labios | lips |
los dientes | teeth |
la muela | molar |
la lengua | tongue |
la oreja | ear (outer) |
el oído | ear (inner); hearing |
el cuello | neck |
la garganta | throat |
el hombro | shoulder |
el brazo | arm |
el codo | elbow |
la muñeca | wrist; doll |
la mano | hand | 💡 la mano, even though it ends in -o
el dedo | finger |
la uña | nail |
el pecho | chest |
la espalda | back |
el estómago | stomach |
la panza | belly | 💡 casual, Mexico
la cintura | waist |
la cadera | hip |
la pierna | leg |
la rodilla | knee |
el tobillo | ankle |
el pie | foot |
el dedo del pie | toe |
el corazón | heart |
los pulmones | lungs |
el cerebro | brain |
la piel | skin |
el hueso | bone |
la sangre | blood |
"""),
("🩺 At the doctor", "03", """
el médico | doctor |
el consultorio | doctor's office |
la clínica | clinic |
urgencias | emergency room |
la ambulancia | ambulance |
la cita | appointment |
la receta | prescription |
la pastilla | pill |
el jarabe | syrup |
la inyección | shot, injection |
la vacuna | vaccine |
el termómetro | thermometer |
tener fiebre | to have a fever | 💡 Mexico also says tener temperatura
la gripa | the flu | 💡 Mexico; 🌎 gripe
el resfriado | cold | 💡 also el catarro
la tos | cough |
toser | to cough |
estornudar | to sneeze |
la alergia | allergy |
el dolor | pain |
me duele… | my … hurts |
mareado, mareada | dizzy |
vomitar | to throw up |
la diarrea | diarrhea |
enfermarse | to get sick |
sentirse mal | to feel bad |
el seguro médico | health insurance |
"""),
("🤕 Accidents & mishaps", "03", """
el accidente | accident |
caerse | to fall down |
tropezarse | to trip |
resbalarse | to slip |
golpearse | to hit yourself, bump |
romperse | to break | 💡 Se rompió el brazo.
quebrarse | to break (a bone) | 💡 common in Mexico
torcerse el tobillo | to twist your ankle |
cortarse | to cut yourself |
quemarse | to burn yourself |
la herida | wound |
la cortada | cut | 💡 Mexico; 🌎 cortadura, corte
el moretón | bruise | 🌎 morado (Arg, Col)
el chipote | bump on the head | 💡 Mexico
la curita | band-aid | 🇪🇸 tirita
la venda | bandage |
el yeso | cast |
se me olvidó | I forgot (it slipped my mind) |
se me cayó | I dropped it |
se me rompió | it broke on me |
se me perdió | I lost it |
se me acabó | I ran out of it |
se descompuso | it broke down | 💡 Mexico; 🌎 se dañó (Col), se malogró (Peru)
se fue la luz | the power went out |
sin querer | by accident |
a propósito | on purpose |
¡Qué mala suerte! | What bad luck! |
¿Estás bien? | Are you OK? |
¡Cuidado! | Careful! |
"""),
]

WORDS["preterite-irregular"] = [
("✈️ At the airport", "11", """
el aeropuerto | airport |
el vuelo | flight |
la aerolínea | airline |
el boleto de avión | plane ticket | 🌎 pasaje · 🇪🇸 billete
de ida | one-way |
de ida y vuelta | round-trip | 💡 Mexico also says viaje redondo
el pasaporte | passport |
la visa | visa | 🇪🇸 visado
la maleta | suitcase | 🌎 valija (Arg)
el equipaje | luggage |
el equipaje de mano | carry-on |
documentar | to check (luggage) | 💡 Mexico; 🌎 chequear · 🇪🇸 facturar
el pase de abordar | boarding pass | 💡 Mexico; 🇪🇸 tarjeta de embarque
abordar | to board | 🇪🇸 embarcar
la puerta | gate |
la sala de espera | waiting area |
el asiento | seat |
la ventanilla | window seat |
el pasillo | aisle |
la escala | layover |
el vuelo directo | direct flight |
despegar | to take off |
aterrizar | to land |
el retraso | delay |
cancelado | canceled |
migración | immigration (desk) |
la aduana | customs |
el sobrecargo | flight attendant | 💡 Mexico; 🌎 azafata, aeromozo
la llegada | arrival |
la salida | departure |
"""),
("🏨 At the hotel", "11", """
el hotel | hotel |
el hostal | hostel |
la reservación | reservation | 🇪🇸 reserva
la habitación | room | 💡 also el cuarto
sencilla | single |
doble | double |
la cama matrimonial | double bed |
la recepción | front desk |
el huésped | guest |
registrarse | to check in |
la salida | checkout |
la llave | key |
el elevador | elevator | 🇪🇸 ascensor
el piso | floor |
la alberca | swimming pool | 💡 Mexico; 🌎 piscina, pileta (Arg)
el desayuno incluido | breakfast included |
todo incluido | all-inclusive |
la toalla | towel |
el servicio a cuarto | room service |
la caja fuerte | safe |
la vista al mar | ocean view |
la queja | complaint |
"""),
("🏖️ Beach & outdoors", "18", """
la playa | beach |
la ola | wave |
el bloqueador | sunscreen | 💡 Mexico; 🌎 protector solar · 🇪🇸 crema solar
los lentes de sol | sunglasses | 🇪🇸 gafas de sol
el traje de baño | swimsuit | 🌎 malla (Arg), vestido de baño (Col) · 🇪🇸 bañador
la sombrilla | beach umbrella |
nadar | to swim |
bucear | to scuba dive |
surfear | to surf |
la lancha | small boat |
el barco | ship, boat |
el muelle | dock, pier |
la palmera | palm tree |
asolearse | to sunbathe | 💡 Mexico; 🌎 tomar el sol
quemarse | to get sunburned |
el salvavidas | lifeguard; life jacket |
acampar | to go camping |
la tienda de campaña | tent | 🌎 carpa
la fogata | campfire |
el sendero | trail |
"""),
("💵 Money", "15", """
el dinero | money |
la lana | money (slang) | 💡 Mexico; 🌎 plata
el peso | peso |
el efectivo | cash |
la tarjeta de crédito | credit card |
la tarjeta de débito | debit card |
el cajero automático | ATM |
sacar dinero | to take out money |
el billete | bill (paper money) |
la moneda | coin |
la feria | small change | 💡 Mexico: ¿Traes feria?
el cambio | change |
pagar | to pay |
cobrar | to charge |
la cuenta | bill, check; account |
el ticket | receipt | 💡 Mexico; also el recibo
la factura | invoice (for taxes) |
el precio | price |
el descuento | discount |
gastar | to spend |
ahorrar | to save |
prestar | to lend |
pedir prestado | to borrow |
deber | to owe |
la casa de cambio | currency exchange |
a meses sin intereses | in interest-free monthly payments | 💡 Mexico
¿Aceptan tarjeta? | Do you take cards? |
¿Cuánto es? | How much is it? |
"""),
]

WORDS["imperfect"] = [
("🧸 Childhood", "07", """
la infancia | childhood |
de niño, de niña | as a kid |
cuando era niño | when I was a kid |
el kínder | kindergarten | 💡 Mexico; 🌎 jardín de niños
la primaria | elementary school |
la secundaria | middle school |
el recreo | recess |
el mejor amigo | best friend |
la travesura | prank, mischief |
portarse bien | to behave |
portarse mal | to misbehave |
regañar | to scold | 🌎 retar (Arg)
castigar | to punish, ground |
la mascota | pet |
el columpio | swing |
la resbaladilla | slide | 💡 Mexico; 🌎 tobogán, rodadero (Col)
el sube y baja | seesaw |
llorar | to cry |
la niñera | babysitter |
el cuento | story |
"""),
("📚 School subjects", "08", """
la materia | school subject |
las matemáticas | math | 💡 las mate
la historia | history |
la geografía | geography |
las ciencias | science |
la biología | biology |
la química | chemistry |
la física | physics |
el español | Spanish |
el inglés | English |
la educación física | PE |
el arte | art |
la música | music |
la computación | computer class | 💡 Mexico; 🌎 informática
la literatura | literature |
el civismo | civics |
la tarea | homework |
el examen | test |
la calificación | grade | 💡 Mexico; 🌎 nota
pasar | to pass | 💡 also aprobar
reprobar | to fail | 🌎 perder (Col), jalar (Peru) · 🇪🇸 suspender
"""),
("✏️ School supplies", "08", """
el lápiz | pencil |
la pluma | pen | 💡 Mexico; 🌎 bolígrafo, lapicero (Col, Peru), birome (Arg) · 🇪🇸 boli
la goma | eraser | 🌎 borrador
el sacapuntas | pencil sharpener |
el cuaderno | notebook |
la libreta | notepad, notebook |
el libro | book |
la mochila | backpack |
la regla | ruler |
las tijeras | scissors |
el pegamento | glue | 💡 Mexico also says el resistol
los colores | colored pencils | 💡 Mexico
los crayones | crayons |
el plumón | marker | 💡 Mexico; 🌎 marcador
la hoja | sheet of paper |
la carpeta | folder |
la calculadora | calculator |
el pizarrón | board | 💡 Mexico; 🌎 pizarra, tablero (Col)
el gis | chalk | 💡 Mexico; 🌎 tiza
el borrador | board eraser |
el estuche | pencil case |
la engrapadora | stapler | 🌎 abrochadora (Arg), cosedora (Col) · 🇪🇸 grapadora
el clip | paper clip |
el corrector | white-out |
"""),
("🪁 Toys & games", "10", """
el juguete | toy |
la muñeca | doll |
el carrito | toy car |
la pelota | ball |
el balón | ball (soccer, basketball) |
los patines | skates |
el trompo | spinning top |
el yoyo | yo-yo |
el balero | cup-and-ball toy | 💡 Mexico
las canicas | marbles |
la lotería | Mexican picture bingo |
el papalote | kite | 💡 Mexico; 🌎 cometa, barrilete (Arg), volantín (Chile)
el rompecabezas | jigsaw puzzle |
el peluche | stuffed animal |
el videojuego | video game |
las escondidas | hide-and-seek |
las traes | tag | 💡 Mexico
brincar la cuerda | to jump rope | 🌎 saltar la cuerda
el avión | hopscotch | 💡 Mexico; 🌎 rayuela
la matatena | jacks | 💡 Mexico
"""),
]

WORDS["perfect"] = [
("👕 Clothes", "05", """
la ropa | clothes |
la playera | T-shirt | 🌎 remera (Arg), camiseta · 🇪🇸 camiseta
la camisa | shirt |
la blusa | blouse |
el suéter | sweater | 🌎 buzo, pulóver (Arg) · 🇪🇸 jersey
la sudadera | sweatshirt, hoodie | 🌎 buzo (Arg, Col)
la chamarra | jacket | 🌎 campera (Arg), chaqueta · 🇪🇸 chaqueta, cazadora
el abrigo | coat |
el saco | blazer, suit jacket | 🇪🇸 americana
el traje | suit |
la corbata | tie |
los pantalones | pants |
los jeans | jeans | 💡 also los pantalones de mezclilla · 🇪🇸 vaqueros
los shorts | shorts |
la falda | skirt | 🌎 pollera (Arg)
el vestido | dress |
la pijama | pajamas | 💡 also la piyama
la ropa interior | underwear |
los calzones | underwear (briefs) | 💡 Mexico
el brasier | bra | 💡 Mexico; 🌎 sostén, corpiño (Arg) · 🇪🇸 sujetador
los calcetines | socks | 🌎 medias (Col, Arg)
las medias | tights, pantyhose |
el uniforme | uniform |
el impermeable | raincoat |
"""),
("👟 Shoes & accessories", "05", """
los zapatos | shoes |
los tenis | sneakers | 🌎 zapatillas (Arg, Chile) · 🇪🇸 zapatillas, deportivas
las botas | boots |
las sandalias | sandals |
las chanclas | flip-flops | 🌎 ojotas (Arg), cholas (Ven)
los tacones | high heels |
la gorra | cap |
el sombrero | hat |
la bufanda | scarf |
los guantes | gloves |
el cinturón | belt |
la bolsa | purse, bag | 🌎 cartera (Arg) · 🇪🇸 bolso
la cartera | wallet | 💡 Mexico; 🌎 billetera
los lentes | glasses | 🌎 anteojos (Arg) · 🇪🇸 gafas
el reloj | watch |
los aretes | earrings | 🌎 aros (Arg), zarcillos (Ven) · 🇪🇸 pendientes
el collar | necklace |
la pulsera | bracelet |
el anillo | ring |
el rebozo | shawl |
el sarape | woven blanket-poncho |
el huipil | embroidered tunic |
"""),
("🎨 Colors", "20", """
el color | color |
rojo, roja | red |
azul | blue |
amarillo, amarilla | yellow |
verde | green |
negro, negra | black |
blanco, blanca | white |
gris | gray |
café | brown | 💡 Mexico; 🌎 marrón · 🇪🇸 marrón
morado, morada | purple |
rosa | pink | 🌎 rosado
anaranjado, anaranjada | orange | 💡 also naranja
beige | beige |
dorado, dorada | gold |
plateado, plateada | silver |
azul marino | navy blue |
azul claro | light blue |
verde oscuro | dark green |
color vino | maroon | 💡 also guinda in Mexico
turquesa | turquoise |
celeste | sky blue |
"""),
("🧵 Fit, patterns & materials", "05", """
la talla | size |
chico, mediano, grande | small, medium, large | 🇪🇸 pequeño
el número | shoe size |
el probador | fitting room |
probarse | to try on |
me queda bien | it fits me |
me queda chico | it's too small on me |
me queda grande | it's too big on me |
ajustado, ajustada | tight |
holgado, holgada | loose |
combinar | to match |
de moda | in style |
pasado de moda | out of style |
de manga larga | long-sleeved |
de manga corta | short-sleeved |
sin mangas | sleeveless |
de rayas | striped |
de cuadros | plaid |
de lunares | polka-dot |
liso, lisa | plain |
estampado, estampada | printed, patterned |
de algodón | cotton |
de lana | wool |
de seda | silk |
de piel | leather | 🌎 de cuero
de mezclilla | denim |
de oro | gold |
de plata | silver |
"""),
("🛍️ Stores & shopping", "05", """
la tienda de ropa | clothing store |
la zapatería | shoe store |
la joyería | jewelry store |
la ferretería | hardware store |
la frutería | fruit shop |
la pescadería | fish market |
la tienda de abarrotes | grocery store, corner store | 💡 Mexico
el centro comercial | mall | 💡 Mexico also says la plaza
el súper | supermarket |
la caja | checkout |
el cajero, la cajera | cashier |
el carrito | shopping cart |
la fila | line | 🇪🇸 cola
hacer fila | to wait in line | 🇪🇸 hacer cola
la oferta | sale, special offer |
la rebaja | markdown |
devolver | to return (an item) |
cambiar | to exchange |
la garantía | warranty |
nada más estoy viendo | I'm just looking | 💡 Mexico; 🌎 solo estoy mirando
¿Lo tiene en otro color? | Do you have it in another color? |
¿Me hace un descuento? | Can you give me a discount? |
¿Me lo envuelve? | Can you wrap it for me? |
"""),
]

WORDS["timeline"] = [
("🔗 Connectors", "23", """
y | and |
pero | but |
o | or |
porque | because |
como | since (at the start) | 💡 Como llovía, no salí.
pues | well |
entonces | so, then |
así que | so |
aunque | although |
sin embargo | however |
además | besides, also |
también | also |
tampoco | neither |
por eso | that's why |
mientras | while |
cuando | when |
en cuanto | as soon as |
hasta que | until |
o sea | I mean |
es decir | that is |
por ejemplo | for example |
por cierto | by the way |
de todos modos | anyway |
en fin | anyway, in short |
total | so anyway | 💡 Mexico: Total, que se fue.
"""),
("⏳ Time expressions, all tenses", "19", """
antes | before |
ahora | now |
después | after |
hoy en día | nowadays |
en aquel entonces | back then |
en esa época | at that time |
de niño | as a child |
ya | already |
ya no | no longer |
todavía | still |
todavía no | not yet |
acabar de | to have just | 💡 Acabo de llegar.
hace un año | a year ago | 💡 hace + time = ago
desde | since |
desde hace | for (still going) | 💡 Vivo aquí desde hace dos años.
durante | during, for |
por fin | finally |
a tiempo | on time |
a la vez | at the same time |
cada vez más | more and more |
para entonces | by then |
dentro de | within, in (future) |
algún día | someday |
"""),
("🇲🇽 Mexican slang", "24", """
¡Qué padre! | How cool! |
¡Qué chido! | How cool! |
padrísimo | awesome |
¡Qué onda! | What's up! |
la neta | the truth; honestly |
¿Neta? | For real? |
¡Órale! | Wow! / OK! |
¡Ándale! | Come on! / Exactly! |
¡Híjole! | Oh man! |
¡Aguas! | Watch out! |
¡No manches! | No way! |
¡No inventes! | You're kidding! |
¡Qué oso! | How embarrassing! |
¡Qué flojera! | I can't be bothered! |
¿A poco? | Really? |
sale | OK, deal |
va | OK |
güey | dude | 💡 very casual — friends only, can sound rude
el cuate | buddy |
el compa | pal |
la chamba | job |
la lana | money |
la chela | beer |
el antro | nightclub |
chafa | cheap, low-quality |
fresa | posh, preppy |
apapachar | to cuddle, comfort |
chiquear | to spoil, pamper |
la pachanga | party |
ya ni la friegas | you've really done it now | 💡 informal
"""),
("💔 Relationships & drama", "07", """
salir con | to go out with |
andar con | to be dating | 💡 Mexico
ser novios | to be boyfriend and girlfriend |
coquetear | to flirt |
ligar | to hook up, pick up | 💡 casual
enamorarse | to fall in love |
la cita | date |
el amor | love |
extrañar | to miss (someone) | 🇪🇸 echar de menos
pelearse | to fight |
reconciliarse | to make up |
cortar | to break up | 💡 Mexico: Cortó con su novio.
terminar | to break up, end |
engañar | to cheat on |
los celos | jealousy |
dejar plantado | to stand (someone) up |
comprometerse | to get engaged |
el prometido, la prometida | fiancé, fiancée |
casarse | to get married |
divorciarse | to get divorced |
el ex | ex |
"""),
]

WORDS["cyber-devices"] = [
("💻 Hardware", "16", """
la computadora | computer | 🌎 computador (Col, Chile) · 🇪🇸 ordenador
la laptop | laptop | 💡 also la computadora portátil · 🇪🇸 portátil
la tableta | tablet |
el teclado | keyboard |
el mouse | mouse | 💡 Mexico; 🌎 🇪🇸 ratón
la pantalla | screen |
el monitor | monitor |
las bocinas | speakers | 💡 Mexico; 🌎 parlantes · 🇪🇸 altavoces
los audífonos | headphones | 🌎 auriculares · 🇪🇸 cascos
el micrófono | microphone |
la cámara web | webcam |
la impresora | printer |
el escáner | scanner |
la memoria USB | USB drive | 🌎 pendrive (Arg)
el disco duro | hard drive |
el cable | cable |
el cargador | charger |
el procesador | processor |
la memoria RAM | RAM |
la tarjeta madre | motherboard | 🌎 placa madre · 🇪🇸 placa base
el servidor | server |
el puerto | port |
la batería | battery |
"""),
("🌐 Networks", "16", """
la red | network |
el router | router | 💡 Mexico says router; also el enrutador
el módem | modem |
el switch | network switch | 💡 also el conmutador
el punto de acceso | access point |
el wifi | Wi-Fi |
la conexión | connection |
el cable de red | network cable |
inalámbrico, inalámbrica | wireless |
la dirección IP | IP address |
la dirección MAC | MAC address |
el ancho de banda | bandwidth |
el paquete | packet |
el protocolo | protocol |
el cortafuegos | firewall | 💡 IT people often just say el firewall
la VPN | VPN |
el cliente | client |
la nube | the cloud |
el centro de datos | data center |
la red local | local network |
la velocidad | speed |
la latencia | latency |
el tráfico | traffic |
conectarse | to connect |
desconectarse | to disconnect |
"""),
("🖥️ Software", "16", """
el sistema operativo | operating system |
el programa | program |
la aplicación | app | 💡 la app
el software | software |
el navegador | browser |
el archivo | file |
la carpeta | folder |
el escritorio | desktop |
la ventana | window |
el ícono | icon |
el menú | menu |
la terminal | terminal |
el comando | command |
el código | code |
el usuario | user |
la configuración | settings |
la actualización | update |
actualizar | to update |
instalar | to install |
desinstalar | to uninstall |
descargar | to download | 💡 Mexico also says bajar
reiniciar | to restart |
prender | to turn on | 💡 Mexico; 🌎 encender
apagar | to turn off |
el antivirus | antivirus |
el controlador | driver |
"""),
("🔎 The internet", "16", """
el internet | the internet |
la página web | web page |
el sitio web | website |
el enlace | link | 💡 also el link
el correo electrónico | email | 💡 also el correo, el mail
el buscador | search engine |
buscar | to search |
la cuenta | account |
el perfil | profile |
la publicación | post |
el historial | history |
las cookies | cookies |
la descarga | download |
en línea | online |
fuera de línea | offline |
"""),
]

WORDS["cyber-actions"] = [
("🔑 Accounts & sign-in", "16", """
la cuenta | account |
el nombre de usuario | username |
la contraseña | password |
la contraseña segura | strong password |
el PIN | PIN |
iniciar sesión | to log in |
cerrar sesión | to log out |
registrarse | to sign up |
crear una cuenta | to create an account |
la verificación en dos pasos | two-step verification |
el código de verificación | verification code |
el gestor de contraseñas | password manager |
restablecer la contraseña | to reset the password |
olvidé mi contraseña | I forgot my password |
la cuenta bloqueada | locked account |
la huella digital | fingerprint |
el reconocimiento facial | face recognition |
la llave de seguridad | security key |
los permisos | permissions |
el administrador | administrator |
el acceso | access |
"""),
("🛡️ Security actions", "", """
proteger | to protect |
cifrar | to encrypt | 💡 also encriptar
descifrar | to decrypt |
respaldar | to back up | 💡 hacer un respaldo · 🌎 hacer una copia de seguridad
restaurar | to restore |
actualizar | to update |
aplicar un parche | to patch |
escanear | to scan |
detectar | to detect |
bloquear | to block |
reportar | to report |
verificar | to verify |
autenticar | to authenticate |
autorizar | to authorize |
monitorear | to monitor | 🇪🇸 monitorizar
revisar los registros | to check the logs |
configurar | to configure |
activar | to turn on, enable |
desactivar | to turn off, disable |
aislar | to isolate |
eliminar | to delete, remove |
cambiar la contraseña | to change the password |
rastrear | to track |
filtrar | to filter; to leak |
denegar | to deny |
permitir | to allow |
"""),
("🖱️ Using the computer", "16", """
hacer clic | to click | 💡 also dar clic
dar doble clic | to double-click |
arrastrar | to drag |
seleccionar | to select |
escribir | to type |
presionar | to press | 💡 Presionen Enter.
la tecla | key |
la barra espaciadora | space bar |
copiar | to copy |
pegar | to paste |
guardar | to save |
guardar como | save as |
imprimir | to print |
compartir pantalla | to share the screen |
minimizar | to minimize |
el cursor | cursor |
la flecha | arrow |
la barra de tareas | taskbar |
"""),
("🗂️ Files & data", "16", """
el documento | document |
la hoja de cálculo | spreadsheet |
la base de datos | database |
los datos | data |
la información personal | personal information |
el respaldo | backup | 🌎 copia de seguridad
la versión | version |
el formato | format |
el tamaño | size |
el archivo adjunto | attachment |
comprimir | to compress, zip |
descomprimir | to unzip |
el registro | log |
la ruta | file path |
la extensión | file extension |
confidencial | confidential |
sensible | sensitive |
compartido, compartida | shared |
cifrado, cifrada | encrypted |
"""),
]

WORDS["cyber-incidents"] = [
("🦠 Threats & attacks", "", """
la amenaza | threat |
el ataque | attack |
el atacante | attacker |
el ciberdelincuente | cybercriminal |
el malware | malware |
el virus | virus |
el gusano | worm |
el troyano | Trojan |
el ransomware | ransomware |
el software espía | spyware |
el phishing | phishing |
el correo falso | fake email |
el enlace sospechoso | suspicious link |
la estafa | scam |
el fraude | fraud |
el robo de identidad | identity theft |
la ingeniería social | social engineering |
el ataque de fuerza bruta | brute-force attack |
la denegación de servicio | denial of service |
la vulnerabilidad | vulnerability |
la filtración de datos | data breach |
el acceso no autorizado | unauthorized access |
la puerta trasera | backdoor |
la red de bots | botnet |
"""),
("🏛️ Security principles", "", """
la confidencialidad | confidentiality |
la integridad | integrity |
la disponibilidad | availability |
la autenticación | authentication |
la autorización | authorization |
el privilegio mínimo | least privilege |
la defensa en profundidad | defense in depth |
el riesgo | risk |
el control | control |
la política de seguridad | security policy |
la privacidad | privacy |
la seguridad | security; safety |
la confianza cero | zero trust |
la segmentación | segmentation |
el cumplimiento | compliance |
la ética | ethics |
el permiso | permission |
"""),
("🚨 Incident response", "", """
el incidente | incident |
la alerta | alert |
la detección | detection |
la contención | containment |
la erradicación | eradication |
la recuperación | recovery |
las lecciones aprendidas | lessons learned |
el informe | report | 💡 also el reporte
el equipo de respuesta | response team |
el analista | analyst |
la evidencia | evidence |
la línea de tiempo | timeline |
el impacto | impact |
la causa | cause |
investigar | to investigate |
contener | to contain |
aislar el equipo | to isolate the machine |
restaurar el respaldo | to restore the backup |
notificar | to notify |
documentar | to document |
¿Cuándo empezó? | When did it start? |
¿Quién tuvo acceso? | Who had access? |
"""),
("📝 Describing an incident", "", """
sospechoso, sospechosa | suspicious |
malicioso, maliciosa | malicious |
legítimo, legítima | legitimate |
falso, falsa | fake |
urgente | urgent |
grave | serious |
crítico, crítica | critical |
comprometido, comprometida | compromised |
infectado, infectada | infected |
vulnerable | vulnerable |
protegido, protegida | protected |
desactualizado, desactualizada | out of date |
expuesto, expuesta | exposed |
raro, rara | strange |
lento, lenta | slow |
caído, caída | down (not working) | 💡 El servidor está caído.
sin permiso | without permission |
"""),
]

WORDS["teach-commands"] = [
("🏫 In the classroom", "08", """
el salón de clases | classroom | 💡 Mexico; 🌎 el aula
el pupitre | student desk |
el escritorio | teacher's desk |
el pizarrón | board |
el pizarrón blanco | whiteboard |
el plumón | marker |
el proyector | projector |
la pantalla | screen |
el horario | schedule |
la lista de asistencia | attendance list |
el libro de texto | textbook |
la hoja de trabajo | worksheet |
el laboratorio de cómputo | computer lab | 💡 Mexico; 🌎 sala de informática
el enchufe | outlet |
el reloj | clock |
el cartel | poster |
"""),
("📣 Class commands", "08", """
siéntense | sit down |
levántense | stand up |
abran | open |
cierren | close |
saquen | take out |
guarden | put away |
escuchen | listen |
miren | look |
lean | read |
escriban | write |
repitan | repeat |
contesten | answer |
pregunten | ask |
pongan atención | pay attention |
guarden silencio | be quiet |
levanten la mano | raise your hand |
trabajen en parejas | work in pairs |
formen equipos | make teams |
hagan fila | line up |
entreguen la tarea | turn in the homework |
pasa al frente | come to the front (one student) |
apaguen los celulares | turn off your phones |
esperen | wait |
siéntate | sit down (one student) |
ven | come here (one student) |
"""),
("👥 School people & places", "08", """
el director, la directora | principal |
el subdirector | vice principal |
el alumno, la alumna | student |
el orientador, la orientadora | counselor | 💡 Mexico; 🌎 consejero
el intendente | custodian | 💡 Mexico; 🌎 conserje
la enfermera | nurse |
el bibliotecario | librarian |
los padres de familia | parents |
el grupo | class, homeroom | 💡 Mexico: el grupo 3°B
la dirección | principal's office |
la sala de maestros | teachers' lounge |
la cafetería | cafeteria |
la enfermería | nurse's office |
el patio | schoolyard |
"""),
("📊 Grades & assignments", "08", """
la tarea | homework |
el proyecto | project |
el examen | test |
la prueba | quiz |
la calificación | grade |
el promedio | average |
entregar | to turn in |
la fecha de entrega | due date |
los puntos extra | extra credit |
la boleta | report card | 💡 Mexico; 🌎 libreta de calificaciones
la asistencia | attendance |
la falta | absence |
el retardo | tardy | 💡 Mexico
el semestre | semester |
la rúbrica | rubric |
revisar | to check |
corregir | to correct |
la respuesta correcta | right answer |
la respuesta incorrecta | wrong answer |
sacar un diez | to get a perfect score | 💡 Mexico grades go up to 10
"""),
]

WORDS["teach-advice"] = [
("🌟 Praise & encouragement", "", """
¡Muy bien! | Very good! |
¡Excelente! | Excellent! |
¡Buen trabajo! | Good work! |
¡Bien hecho! | Well done! |
¡Eso es! | That's it! |
¡Así se hace! | That's how it's done! |
¡Casi! | Almost! |
¡Tú puedes! | You can do it! |
¡Sigue así! | Keep it up! |
¡Vas muy bien! | You're doing great! |
¡Qué buena pregunta! | What a good question! |
¡Lo lograste! | You did it! |
¡Échale ganas! | Give it your all! | 💡 Mexico
estoy orgulloso de ti | I'm proud of you |
inténtalo otra vez | try again |
no te preocupes | don't worry |
está bien equivocarse | it's OK to make mistakes |
poco a poco | little by little |
"""),
("💬 Giving advice", "", """
te recomiendo que… | I recommend that you… | 💡 + subjunctive
te sugiero que… | I suggest that you… |
es importante que… | it's important that… |
es mejor que… | it's better that… |
deberías… | you should… |
tienes que… | you have to… |
hay que… | you have to, one must… |
¿Por qué no…? | Why don't you…? |
si yo fuera tú… | if I were you… |
ojalá que… | I hope that… |
espero que… | I hope that… |
asegúrate de… | make sure to… |
no olvides… | don't forget… |
acuérdate de… | remember to… |
ten cuidado con… | be careful with… |
nunca compartas… | never share… |
"""),
("🧑‍🎓 Describing students", "04", """
atento, atenta | attentive |
distraído, distraída | distracted |
participativo, participativa | participates a lot |
callado, callada | quiet |
platicador, platicadora | chatty | 💡 Mexico
respetuoso, respetuosa | respectful |
puntual | punctual |
responsable | responsible |
motivado, motivada | motivated |
frustrado, frustrada | frustrated |
seguro de sí mismo | self-confident |
se porta bien | behaves well |
se porta mal | misbehaves |
copiar | to copy; to cheat |
hacer trampa | to cheat |
echar relajo | to goof around | 💡 Mexico
"""),
("👪 Talking with parents", "07", """
la junta de padres | parent meeting | 💡 Mexico; 🌎 reunión de padres
el comportamiento | behavior |
el progreso | progress |
su hijo va muy bien | your son is doing very well |
necesita mejorar en… | needs to improve in… |
le falta entregar… | still has to turn in… |
le mando un correo | I'll send you an email |
¿Tiene alguna pregunta? | Do you have any questions? |
gracias por venir | thank you for coming |
el apoyo en casa | support at home |
firmar | to sign |
la firma | signature |
el aviso | notice |
el permiso | permission slip |
"""),
]


def words_data(clip):
    """{week id: [{"title", "bank", "rows": [[es, en, note, clip text, group]]}]} for content.js.
    A '## Name' line in a block starts a subheading; the rows after it get that group."""
    out = {}
    for wid, sections in WORDS.items():
        out[wid] = []
        for t, bank, block in sections:
            rows, group = [], ""
            for line in block.strip().splitlines():
                if line.startswith("## "):
                    group = line[3:].strip()
                    continue
                es, en, note = ([x.strip() for x in line.split("|")] + ["", ""])[:3]
                rows.append([es, en, note, clip(es), group])
            out[wid].append({"title": t, "bank": bank, "rows": rows})
    return out
