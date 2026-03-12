#!/usr/bin/env python3
"""
Generate complete Texas Appliances Repair site with ALL 254 counties.
Navigation updated to show Texas service areas.
"""

import os
import re

# Read template
with open('/tmp/lg-appliance-repair-nj/hunterdon-county/clinton-township/freezer-repair/index.html', 'r') as f:
    TEMPLATE = f.read()

# ALL 254 Texas counties with major towns

# Comprehensive list of all legally incorporated Texas cities and towns
TEXAS_COUNTIES = {
    "anderson-county": ['palestine', 'frankston', 'elkhart', 'cayuga', 'montalba', 'neches', 'tennessee-colony'],
    "andrews-county": ['andrews', 'florey', 'mckinney-acres'],
    "angelina-county": ['lufkin', 'hudson', 'diboll', 'huntington', 'zavalla', 'burke', 'redland', 'pollok', 'homer'],
    "aransas-county": ['rockport', 'fulton', 'aransas-pass', 'lamar', 'holiday-beach', 'copano-village', 'estes'],
    "archer-county": ['archer-city', 'holliday', 'lakeside-city', 'megargel', 'scotland', 'windthorst'],
    "armstrong-county": ['claude', 'goodnight', 'wayside', 'washburn'],
    "atascosa-county": ['pleasanton', 'poteet', 'jourdanton', 'lytle', 'charlotte', 'christine', 'leming', 'campbellton', 'mccoy', 'peggy'],
    "austin-county": ['bellville', 'sealy', 'wallis', 'san-felipe', 'brazos-country', 'industry', 'cat-spring', 'new-ulm'],
    "bailey-county": ['muleshoe', 'enochs', 'maple', 'needmore', 'bula', 'progress', 'goodland'],
    "bandera-county": ['bandera', 'lakehills', 'medina', 'pipe-creek', 'tarpley', 'vanderpool', 'mico'],
    "bastrop-county": ['bastrop', 'elgin', 'smithville', 'cedar-creek', 'paige', 'red-rock', 'rosanky', 'mcdade', 'wyldwood', 'camp-swift'],
    "baylor-county": ['seymour', 'bomarton', 'westover', 'red-springs', 'mabelle'],
    "bee-county": ['beeville', 'pettus', 'skidmore', 'tynan', 'normanna', 'tuleta', 'mineral', 'pawnee'],
    "bell-county": ['killeen', 'temple', 'belton', 'harker-heights', 'copperas-cove', 'nolanville', 'salado', "morgan's-point-resort", 'little-river-academy', 'rogers', 'troy', 'holland'],
    "bexar-county": ['san-antonio', 'converse', 'live-oak', 'universal-city', 'schertz', 'selma', 'helotes', 'leon-valley', 'alamo-heights', 'terrell-hills', 'castle-hills', 'balcones-heights', 'shavano-park', 'hollywood-park', 'windcrest', 'kirby', 'china-grove', 'fair-oaks-ranch', 'grey-forest', 'hill-country-village', 'olmos-park', 'sandy-oaks', 'somerset', 'von-ormy', 'st-hedwig', 'elmendorf', 'macdona', 'adkins', 'losoya'],
    "blanco-county": ['johnson-city', 'blanco', 'round-mountain', 'hye', 'sandy'],
    "borden-county": ['gail', 'fluvanna', 'vealmoor', 'mesquite'],
    "bosque-county": ['meridian', 'clifton', 'valley-mills', 'walnut-springs', 'iredell', 'cranfills-gap', 'kopperl', 'morgan', 'laguna-park'],
    "bowie-county": ['texarkana', 'new-boston', 'hooks', 'wake-village', 'nash', 'de-kalb', 'maud', 'redwater', 'leary', 'simms', 'red-lick'],
    "brazoria-county": ['pearland', 'lake-jackson', 'alvin', 'angleton', 'clute', 'freeport', 'brazoria', 'richwood', 'manvel', 'west-columbia', 'sweeny', 'surfside-beach', 'liverpool', 'oyster-creek', 'jones-creek', 'quintana', 'danbury', 'old-ocean', 'damon', 'baileys-prairie', 'bonney', 'brookside-village', 'hillcrest-village', 'iowa-colony'],
    "brazos-county": ['bryan', 'college-station', 'wixon-valley', 'kurten', 'millican', 'wellborn', 'benchley'],
    "brewster-county": ['alpine', 'marathon', 'terlingua', 'study-butte', 'lajitas', 'big-bend'],
    "briscoe-county": ['silverton', 'quitaque', 'south-plains'],
    "brooks-county": ['falfurrias', 'encino', 'rachal'],
    "brown-county": ['brownwood', 'early', 'bangs', 'blanket', 'may', 'zephyr', 'brookesmith'],
    "burleson-county": ['caldwell', 'somerville', 'snook', 'deanville', 'lyons'],
    "burnet-county": ['burnet', 'marble-falls', 'bertram', 'granite-shoals', 'highland-haven', 'cottonwood-shores', 'meadowlakes', 'briggs', 'spicewood'],
    "caldwell-county": ['lockhart', 'luling', 'martindale', 'maxwell', 'dale', 'fentress', 'prairie-lea', 'mcmahan'],
    "calhoun-county": ['port-lavaca', 'seadrift', 'point-comfort', 'port-oconnor', 'long-mott', 'magnolia-beach'],
    "callahan-county": ['baird', 'clyde', 'cross-plains', 'putnam', 'eula', 'oplin'],
    "cameron-county": ['brownsville', 'harlingen', 'san-benito', 'port-isabel', 'la-feria', 'los-fresnos', 'south-padre-island', 'palm-valley', 'primera', 'rancho-viejo', 'laguna-vista', 'rio-hondo', 'santa-rosa', 'bayview', 'combes', 'indian-lake', 'laguna-heights', 'laureles', 'los-indios', 'palm-valley', 'cameron-park', 'bluetown'],
    "camp-county": ['pittsburg', 'rocky-mound', 'leesburg', 'purley'],
    "carson-county": ['panhandle', 'white-deer', 'groom', 'skellytown', 'conway'],
    "cass-county": ['atlanta', 'linden', 'queen-city', 'hughes-springs', 'avinger', 'bloomburg', 'domino', 'douglassville', 'marietta', 'kildare'],
    "castro-county": ['dimmitt', 'hart', 'nazareth', 'summerfield'],
    "chambers-county": ['anahuac', 'mont-belvieu', 'beach-city', 'winnie', 'stowell', 'old-river-winfree', 'cove', 'hankamer', 'oak-island'],
    "cherokee-county": ['jacksonville', 'rusk', 'alto', 'troup', 'wells', 'bullard', 'gallatin', 'cuney', 'reese', 'dialville'],
    "childress-county": ['childress', 'carey', 'tell', 'kirkland', 'loco'],
    "clay-county": ['henrietta', 'petrolia', 'bellevue', 'jolly', 'byers', 'dean', 'bluegrove', 'charlie', 'shannon'],
    "cochran-county": ['morton', 'whiteface', 'bledsoe', 'lehman'],
    "coke-county": ['robert-lee', 'bronte', 'tennyson', 'silver'],
    "coleman-county": ['coleman', 'santa-anna', 'novice', 'valera', 'burkett', 'rockwood', 'talpa', 'gouldbusk'],
    "collin-county": ['plano', 'mckinney', 'frisco', 'allen', 'wylie', 'murphy', 'prosper', 'celina', 'princeton', 'anna', 'farmersville', 'lucas', 'fairview', 'lavon', 'melissa', 'blue-ridge', 'lowry-crossing', 'nevada', 'new-hope', 'parker', 'st-paul', 'weston', 'josephine', 'westminster'],
    "collingsworth-county": ['wellington', 'dodson', 'quail', 'samnorwood'],
    "colorado-county": ['columbus', 'eagle-lake', 'weimar', 'rock-island', 'altair', 'garwood', 'glidden', 'sheridan', 'oakland'],
    "comal-county": ['new-braunfels', 'bulverde', 'garden-ridge', 'canyon-lake', 'spring-branch', 'schertz', 'selma', 'fair-oaks-ranch', 'fischer'],
    "comanche-county": ['comanche', 'de-leon', 'gustine', 'proctor', 'energy', 'sidney', 'downing'],
    "concho-county": ['eden', 'paint-rock', 'eola', 'millersview', 'lowake'],
    "cooke-county": ['gainesville', 'muenster', 'lindsay', 'valley-view', 'callisburg', 'era', 'myra', 'rosston', 'sivells-bend'],
    "coryell-county": ['copperas-cove', 'gatesville', 'evant', 'oglesby', 'south-mountain', 'flat', 'the-grove', 'purmela'],
    "cottle-county": ['paducah', 'cee-vee', 'chalk', 'narcisso'],
    "crane-county": ['crane', 'mccamey'],
    "crockett-county": ['ozona', 'sheffield'],
    "crosby-county": ['crosbyton', 'ralls', 'lorenzo', 'cone', 'robertson'],
    "culberson-county": ['van-horn', 'lobo', 'salt-flat', 'pine-springs'],
    "dallam-county": ['dalhart', 'texline', 'kerrick', 'conlen', 'perico'],
    "dallas-county": ['dallas', 'irving', 'garland', 'grand-prairie', 'mesquite', 'carrollton', 'richardson', 'desoto', 'rowlett', 'duncanville', 'cedar-hill', 'lancaster', 'farmers-branch', 'coppell', 'balch-springs', 'glenn-heights', 'hutchins', 'addison', 'highland-park', 'university-park', 'sachse', 'sunnyvale', 'wilmer', 'cockrell-hill', 'combine', 'seagoville'],
    "dawson-county": ['lamesa', 'welch', 'ackerly', 'los-ybanez', 'klondike'],
    "deaf-smith-county": ['hereford', 'dawn', 'umbarger', 'bootleg'],
    "delta-county": ['cooper', 'pecan-gap', 'klondike', 'ben-franklin'],
    "denton-county": ['denton', 'lewisville', 'flower-mound', 'the-colony', 'little-elm', 'corinth', 'highland-village', 'lake-dallas', 'sanger', 'aubrey', 'pilot-point', 'argyle', 'justin', 'krum', 'trophy-club', 'northlake', 'roanoke', 'bartonville', 'copper-canyon', 'cross-roads', 'double-oak', 'draper', 'hackberry', 'hickory-creek', 'krugerville', 'lincoln-park', 'oak-point', 'ponder', 'providence-village', 'shady-shores'],
    "dewitt-county": ['cuero', 'yoakum', 'nordheim', 'meyersville', 'yorktown', 'hochheim', 'thomaston'],
    "dickens-county": ['spur', 'dickens', 'afton', 'mcadoo', 'glenn'],
    "dimmit-county": ['carrizo-springs', 'asherton', 'big-wells', 'catarina', 'brundage'],
    "donley-county": ['clarendon', 'hedley', 'howardwick', 'lelia-lake', 'jericho'],
    "duval-county": ['san-diego', 'benavides', 'freer', 'concepcion', 'realitos'],
    "eastland-county": ['eastland', 'cisco', 'ranger', 'gorman', 'rising-star', 'carbon', 'desdemona', 'olden'],
    "ector-county": ['odessa', 'west-odessa', 'goldsmith', 'gardendale', 'penwell', 'notrees'],
    "edwards-county": ['rocksprings', 'barksdale', 'leakey'],
    "el-paso-county": ['el-paso', 'socorro', 'horizon-city', 'san-elizario', 'anthony', 'clint', 'fabens', 'tornillo', 'canutillo', 'vinton', 'westway', 'homestead-meadows-south', 'homestead-meadows-north', 'sparks', 'agua-dulce'],
    "ellis-county": ['waxahachie', 'midlothian', 'ennis', 'red-oak', 'ferris', 'palmer', 'italy', 'maypearl', 'milford', 'bardwell', 'avalon', 'garrett', 'alma', 'forreston', 'bristol', 'oak-leaf', 'pecan-hill', 'ovilla'],
    "erath-county": ['stephenville', 'dublin', 'bluff-dale', 'huckabay', 'lingleville', 'morgan-mill', 'thurber'],
    "falls-county": ['marlin', 'rosebud', 'chilton', 'lott', 'reagan', 'golinda', 'perry', 'riesel', 'satin', 'travis'],
    "fannin-county": ['bonham', 'leonard', 'trenton', 'honey-grove', 'dodd-city', 'ector', 'ladonia', 'ravenna', 'savoy', 'bailey', 'telephone', 'windom'],
    "fayette-county": ['la-grange', 'schulenburg', 'flatonia', 'fayetteville', 'carmine', 'ellinger', 'round-top', 'warrenton', 'muldoon', 'plum', 'rutersville'],
    "fisher-county": ['rotan', 'roby', 'hamlin', 'mccaulley', 'sylvester'],
    "floyd-county": ['floydada', 'lockney', 'south-plains', 'dougherty', 'barwise'],
    "foard-county": ['crowell', 'foard-city', 'thalia', 'margaret'],
    "fort-bend-county": ['sugar-land', 'missouri-city', 'rosenberg', 'richmond', 'stafford', 'fulshear', 'meadows-place', 'needville', 'pecan-grove', 'cinco-ranch', 'fresno', 'arcola', 'beasley', 'fairchilds', 'four-corners', 'greatwood', 'kendleton', 'orchard', 'pleak', 'simonton', 'thompsons', 'weston-lakes'],
    "franklin-county": ['mount-vernon', 'winnsboro', 'scroggins', 'hagansport', 'talco'],
    "freestone-county": ['teague', 'fairfield', 'wortham', 'streetman', 'kirvin', 'dew', 'oakwood', 'cotton-gin'],
    "frio-county": ['pearsall', 'dilley', 'bigfoot', 'divot', 'hilltop', 'moore'],
    "gaines-county": ['seminole', 'seagraves', 'loop'],
    "galveston-county": ['galveston', 'texas-city', 'league-city', 'friendswood', 'dickinson', 'la-marque', 'santa-fe', 'kemah', 'hitchcock', 'clear-lake-shores', 'jamaica-beach', 'tiki-island', 'bayou-vista', 'bacliff', 'san-leon', 'alta-loma'],
    "garza-county": ['post', 'justiceburg', 'southland', 'close-city'],
    "gillespie-county": ['fredericksburg', 'harper', 'stonewall', 'luckenbach', 'doss', 'willow-city', 'cain-city'],
    "glasscock-county": ['garden-city', 'st-lawrence'],
    "goliad-county": ['goliad', 'fannin', 'weser', 'berclair'],
    "gonzales-county": ['gonzales', 'nixon', 'waelder', 'smiley', 'harwood', 'leesville', 'belmont', 'cost', 'ottine'],
    "gray-county": ['pampa', 'lefors', 'mclean', 'alanreed', 'laketon'],
    "grayson-county": ['sherman', 'denison', 'van-alstyne', 'howe', 'pottsboro', 'whitesboro', 'whitewright', 'bells', 'gunter', 'tom-bean', 'tioga', 'collinsville', 'dorchester', 'knollwood', 'sadler', 'southmayd'],
    "gregg-county": ['longview', 'kilgore', 'gladewater', 'white-oak', 'clarksville-city', 'easton', 'lakeport', 'liberty-city', 'warren-city'],
    "grimes-county": ['navasota', 'anderson', 'iola', 'bedias', 'todd-mission', 'plantersville', 'shiro'],
    "guadalupe-county": ['seguin', 'schertz', 'cibolo', 'marion', 'santa-clara', 'mcqueeney', 'new-berlin', 'kingsbury', 'zuehl', 'geronimo', 'staples'],
    "hale-county": ['plainview', 'hale-center', 'abernathy', 'petersburg', 'edmonson', 'cotton-center', 'halfway', 'seth-ward'],
    "hall-county": ['memphis', 'estelline', 'turkey', 'lakeview', 'plaska', 'brice'],
    "hamilton-county": ['hamilton', 'hico', 'carlton', 'evant', 'pottsville', 'fairy', 'indian-gap', 'aleman'],
    "hansford-county": ['spearman', 'gruver', 'morse', 'oslo'],
    "hardeman-county": ['quanah', 'chillicothe', 'acme', 'goodlett', 'medicine-mound'],
    "hardin-county": ['silsbee', 'lumberton', 'kountze', 'sour-lake', 'rose-hill-acres', 'village-mills', 'pinewood-estates', 'saratoga'],
    "harris-county": ['houston', 'pasadena', 'baytown', 'pearland', 'sugar-land', 'atascocita', 'channelview', 'mission-bend', 'spring', 'katy', 'la-porte', 'league-city', 'deer-park', 'friendswood', 'galena-park', 'south-houston', 'jacinto-city', 'bellaire', 'west-university-place', 'humble', 'tomball', 'jersey-village', 'seabrook', 'webster', "morgan's-point", 'shoreacres', 'el-lago', 'taylor-lake-village', 'nassau-bay', 'piney-point-village', 'bunker-hill-village', 'hunters-creek-village', 'hedwig-village', 'hilshire-village', 'spring-valley-village', 'memorial-villages', 'southside-place', 'aldine', 'cloverleaf', 'crosby', 'highlands', 'sheldon', 'barrett', 'la-marque'],
    "harrison-county": ['marshall', 'longview', 'hallsville', 'scottsville', 'waskom', 'uncertain', 'nesbitt', 'harleton', 'karnack', 'jonesville', 'elysian-fields'],
    "hartley-county": ['channing', 'hartley', 'romero', 'middlewater'],
    "haskell-county": ['haskell', 'rule', 'rochester', "o'brien", 'weinert', 'sagerton'],
    "hays-county": ['san-marcos', 'kyle', 'buda', 'wimberley', 'dripping-springs', 'mountain-city', 'woodcreek', 'niederwald', 'bear-creek', 'hays', 'uhland', 'manchaca', 'driftwood'],
    "hemphill-county": ['canadian', 'mendota', 'allison', 'glazier'],
    "henderson-county": ['athens', 'gun-barrel-city', 'chandler', 'mabank', 'malakoff', 'brownsboro', 'eustace', 'seven-points', 'tool', 'caney-city', 'moore-station', 'trinidad', 'log-cabin', 'payne-springs', 'star-harbor', 'murchison', 'poynor'],
    "hidalgo-county": ['mcallen', 'edinburg', 'mission', 'pharr', 'san-juan', 'weslaco', 'donna', 'alamo', 'mercedes', 'progreso', 'la-joya', 'hidalgo', 'palmview', 'palmhurst', 'sullivan-city', 'penitas', 'la-villa', 'edcouch', 'elsa', 'granjeno', 'hargill', 'la-blanca', 'lopezville', 'north-alamo', 'olivarez', 'scissors', 'sharyland', 'south-alamo'],
    "hill-county": ['hillsboro', 'whitney', 'itasca', 'blum', 'hubbard', 'bynum', "carl's-corner", 'covington', 'malone', 'mount-calm', 'penelope', 'aquilla', 'abbott', 'mertens'],
    "hockley-county": ['levelland', 'sundown', 'anton', 'opdyke-west', 'pep', 'ropesville', 'smyer', 'whitharral'],
    "hood-county": ['granbury', 'tolar', 'cresson', 'lipan', 'pecan-plantation', 'de-cordova', 'brazos-bend', 'oak-trail-shores'],
    "hopkins-county": ['sulphur-springs', 'como', 'cumby', 'tira', 'brashear', 'dike', 'peerless', 'pickton', 'saltillo', 'birthright', 'miller-grove', 'north-hopkins'],
    "houston-county": ['crockett', 'grapeland', 'lovelady', 'kennard', 'latexo', 'ratcliff', 'weches', 'pennington'],
    "howard-county": ['big-spring', 'coahoma', 'forsan', 'sand-springs', 'vincent', 'vealmoor', 'knott'],
    "hudspeth-county": ['sierra-blanca', 'dell-city', 'fort-hancock', 'salt-flat', 'allamoore'],
    "hunt-county": ['greenville', 'commerce', 'quinlan', 'caddo-mills', 'celeste', 'lone-oak', 'west-tawakoni', 'campbell', 'neylandville', 'merit', 'union-valley', 'hawk-cove', 'floyd'],
    "hutchinson-county": ['borger', 'stinnett', 'fritch', 'sanford', 'plemons'],
    "irion-county": ['mertzon', 'barnhart', 'sherwood', 'arden'],
    "jack-county": ['jacksboro', 'bryson', 'perrin', 'jermyn', 'wizard-wells'],
    "jackson-county": ['edna', 'ganado', 'la-ward', 'lolita', 'francitas', 'vanderbilt'],
    "jasper-county": ['jasper', 'kirbyville', 'buna', 'evadale', 'call', 'browndell', 'magnolia-springs'],
    "jeff-davis-county": ['fort-davis', 'valentine', 'mcdonald', 'mount-locke'],
    "jefferson-county": ['beaumont', 'port-arthur', 'nederland', 'port-neches', 'groves', 'bevil-oaks', 'china', 'nome', 'central-gardens'],
    "jim-hogg-county": ['hebbronville', 'guerra', 'las-lomitas'],
    "jim-wells-county": ['alice', 'premont', 'san-diego', 'orange-grove', 'alfred', 'ben-bolt'],
    "johnson-county": ['burleson', 'cleburne', 'joshua', 'keene', 'alvarado', 'grandview', 'venus', 'godley', 'rio-vista', 'cross-timber', 'briaroaks'],
    "jones-county": ['anson', 'stamford', 'hamlin', 'hawley', 'lueders', 'trent', 'nugent', 'funston'],
    "karnes-county": ['karnes-city', 'kenedy', 'runge', 'falls-city', 'panna-maria', 'coy-city', 'gillett', 'hobson'],
    "kaufman-county": ['terrell', 'forney', 'kaufman', 'heath', 'crandall', 'talty', 'poetry', 'kemp', 'mabank', 'scurry', 'oak-ridge', 'rosser', 'combine', 'post-oak-bend-city', 'grays-prairie', 'oak-grove', 'ables-springs'],
    "kendall-county": ['boerne', 'fair-oaks-ranch', 'comfort', 'bergheim', 'kendalia', 'waring', 'sisterdale'],
    "kenedy-county": ['sarita', 'armstrong', 'norias'],
    "kent-county": ['jayton', 'girard', 'peacock', 'clairemont'],
    "kerr-county": ['kerrville', 'ingram', 'center-point', 'mountain-home', 'hunt', 'camp-verde'],
    "kimble-county": ['junction', 'telegraph', 'london', 'roosevelt', 'segovia'],
    "king-county": ['guthrie', 'dumont'],
    "kinney-county": ['brackettville', 'spofford', 'fort-clark-springs'],
    "kleberg-county": ['kingsville', 'riviera', 'ricardo', 'loyola-beach'],
    "knox-county": ['munday', 'knox-city', 'benjamin', 'goree', 'vera', 'truscott', 'gilliland', 'rhineland'],
    "la-salle-county": ['cotulla', 'encinal', 'fowlerton', 'gardendale'],
    "lamar-county": ['paris', 'blossom', 'deport', 'roxton', 'reno', 'pattonville', 'chicota', 'powderly', 'sun-valley', 'atlas'],
    "lamb-county": ['littlefield', 'olton', 'sudan', 'earth', 'amherst', 'spade', 'springlake', 'fieldton', 'pleasant-valley'],
    "lampasas-county": ['lampasas', 'lometa', 'kempner', 'adamsville', 'nix'],
    "lavaca-county": ['hallettsville', 'yoakum', 'shiner', 'moulton', 'sublime', 'sweet-home', 'moravia', 'vysehrad'],
    "lee-county": ['giddings', 'lexington', 'dime-box', 'lincoln', 'serbin', 'old-dime-box'],
    "leon-county": ['buffalo', 'centerville', 'jewett', 'oakwood', 'marquez', 'normangee', 'flynn', 'hilltop-lakes', 'leona'],
    "liberty-county": ['liberty', 'dayton', 'cleveland', 'ames', 'hardin', 'daisetta', 'devers', 'hull', 'kenefick', 'north-cleveland', 'plum-grove', 'romayor', 'tarkington-prairie'],
    "limestone-county": ['mexia', 'groesbeck', 'kosse', 'coolidge', 'prairie-hill', 'thornton', 'tehuacana', 'lake-limestone'],
    "lipscomb-county": ['booker', 'darrouzett', 'follett', 'higgins', 'lipscomb'],
    "live-oak-county": ['george-west', 'three-rivers', 'whitsett', 'lagarto', 'pernitas-point'],
    "llano-county": ['llano', 'kingsland', 'horseshoe-bay', 'buchanan-dam', 'sunrise-beach-village', 'tow'],
    "loving-county": ['mentone', 'ramsey'],
    "lubbock-county": ['lubbock', 'slaton', 'wolfforth', 'shallowater', 'idalou', 'new-deal', 'ransom-canyon', 'abernathy', 'buffalo-springs'],
    "lynn-county": ['tahoka', "o'donnell", 'wilson', 'new-home', 'draw', 'grassland'],
    "madison-county": ['madisonville', 'midway', 'normangee', 'north-zulch', 'bedias'],
    "marion-county": ['jefferson', 'lone-star', 'uncertain'],
    "martin-county": ['stanton', 'lenorah', 'tarzan', 'ackerly'],
    "mason-county": ['mason', 'art', 'fredonia', 'pontotoc', 'grit', 'streeter'],
    "matagorda-county": ['bay-city', 'palacios', 'matagorda', 'sargent', 'van-vleck', 'wadsworth', 'blessing', 'collegeport', 'markham', 'midfield'],
    "maverick-county": ['eagle-pass', 'quemado', 'el-indio', 'rosita', 'normandy'],
    "mcculloch-county": ['brady', 'rochelle', 'melvin', 'mercury', 'voca', 'doole', 'lohn'],
    "mclennan-county": ['waco', 'hewitt', 'woodway', 'robinson', 'bellmead', 'lacy-lakeview', 'mcgregor', 'west', 'lorena', 'crawford', 'moody', 'mart', 'riesel', 'bruceville-eddy', 'china-spring', 'hallsburg', 'gholson', 'leroy', 'ross', 'axtell', 'beverly-hills'],
    "mcmullen-county": ['tilden', 'calliham'],
    "medina-county": ['hondo', 'castroville', 'devine', 'natalia', 'lacoste', 'rio-medina', 'mico', 'lytle', 'yancey', 'dunlay'],
    "menard-county": ['menard', 'fort-mckavett', 'hext'],
    "midland-county": ['midland', 'greenwood', 'cotton-flat', 'spraberry', 'warfield', 'germania'],
    "milam-county": ['cameron', 'rockdale', 'milano', 'thorndale', 'buckholts', 'davilla', 'ben-arnold', 'gause', 'alcoa'],
    "mills-county": ['goldthwaite', 'mullin', 'star', 'priddy', 'caradan'],
    "mitchell-county": ['colorado-city', 'loraine', 'westbrook', 'cuthbert'],
    "montague-county": ['bowie', 'nocona', 'saint-jo', 'sunset', 'forestburg', 'ringgold', 'stoneburg'],
    "montgomery-county": ['conroe', 'the-woodlands', 'magnolia', 'willis', 'shenandoah', 'oak-ridge-north', 'panorama-village', 'roman-forest', 'cut-and-shoot', 'splendora', 'stagecoach', 'woodbranch', 'patton-village', 'woodloch', 'pinehurst', 'porter-heights', 'tamina'],
    "moore-county": ['dumas', 'sunray', 'cactus', 'masterson'],
    "morris-county": ['daingerfield', 'naples', 'lone-star', 'omaha', 'cason'],
    "motley-county": ['matador', 'roaring-springs', 'northfield', 'flomot'],
    "nacogdoches-county": ['nacogdoches', 'garrison', 'woden', 'appleby', 'cushing', 'chireno', 'martinsville', 'etoile', 'douglass', 'sacul'],
    "navarro-county": ['corsicana', 'kerens', 'blooming-grove', 'frost', 'dawson', 'mildred', 'barry', 'angus', 'emhouse', 'eureka', 'goodlow', 'navarro', 'powell', 'purdon', 'rice', 'richland'],
    "newton-county": ['newton', 'bon-wier', 'deweyville', 'burkeville', 'call', 'wiergate'],
    "nolan-county": ['sweetwater', 'roscoe', 'nolan', 'blackwell', 'maryneal'],
    "nueces-county": ['corpus-christi', 'portland', 'robstown', 'port-aransas', 'bishop', 'agua-dulce', 'driscoll', 'petronila', 'chapman-ranch', 'banquete', 'london'],
    "ochiltree-county": ['perryton', 'farnsworth', 'waka', 'booker'],
    "oldham-county": ['vega', 'adrian', 'wildorado', 'boys-ranch'],
    "orange-county": ['orange', 'bridge-city', 'vidor', 'west-orange', 'pinehurst', 'rose-city', 'little-cypress', 'orangefield', 'mauriceville'],
    "palo-pinto-county": ['mineral-wells', 'palo-pinto', 'gordon', 'graford', 'mingus', 'santo', 'strawn', 'brazos'],
    "panola-county": ['carthage', 'beckville', 'gary', 'long-branch', 'deadwood', 'tatum'],
    "parker-county": ['weatherford', 'willow-park', 'aledo', 'hudson-oaks', 'azle', 'annetta', 'springtown', 'millsap', 'poolville', 'peaster', 'reno', 'sanctuary', 'cool', 'annetta-north', 'annetta-south', 'fort-spunky'],
    "parmer-county": ['friona', 'bovina', 'farwell', 'lazbuddie', 'rhea', 'black'],
    "pecos-county": ['fort-stockton', 'iraan', 'imperial', 'sheffield', 'coyanosa', 'bakersfield'],
    "polk-county": ['livingston', 'onalaska', 'corrigan', 'goodrich', 'seven-oaks', 'ace', 'leggett', 'moscow', 'segno'],
    "potter-county": ['amarillo', 'bishop-hills', 'ady', 'bushland', 'gentry'],
    "presidio-county": ['presidio', 'marfa', 'shafter', 'redford', 'ruidosa'],
    "rains-county": ['emory', 'point', 'east-tawakoni', 'alba'],
    "randall-county": ['amarillo', 'canyon', 'lake-tanglewood', 'palisades', 'umbarger', 'happy'],
    "reagan-county": ['big-lake', 'stiles', 'texon', 'best'],
    "real-county": ['leakey', 'camp-wood', 'rio-frio', 'vance'],
    "red-river-county": ['clarksville', 'bogata', 'annona', 'avery', 'detroit', 'deport', 'bagwell', 'index', 'johntown', 'kanawha', 'manchester'],
    "reeves-county": ['pecos', 'toyah', 'balmorhea', 'lindsey', 'saragosa', 'verhalen'],
    "refugio-county": ['refugio', 'woodsboro', 'austwell', 'bayside', 'tivoli'],
    "roberts-county": ['miami', 'parnell', 'wayside'],
    "robertson-county": ['hearne', 'bremond', 'calvert', 'franklin', 'wheelock', 'mumford', 'new-baden', 'benchley'],
    "rockwall-county": ['rockwall', 'heath', 'fate', 'rowlett', 'mclendon-chisholm', 'mobile-city', 'royse-city'],
    "runnels-county": ['ballinger', 'winters', 'miles', 'rowena', 'norton'],
    "rusk-county": ['henderson', 'kilgore', 'mount-enterprise', 'overton', 'tatum', 'new-london', 'joinerville', 'laneville', 'price', 'turnertown'],
    "sabine-county": ['hemphill', 'pineland', 'milam', 'brookeland', 'fairmount', 'bronson'],
    "san-augustine-county": ['san-augustine', 'broaddus', 'bland-lake'],
    "san-jacinto-county": ['coldspring', 'shepherd', 'oakhurst', 'pointblank', 'evergreen', 'camilla'],
    "san-patricio-county": ['portland', 'sinton', 'ingleside', 'aransas-pass', 'gregory', 'taft', 'odem', 'mathis', 'san-patricio', 'ingleside-on-the-bay', 'edroy', 'lakeside', 'saint-paul'],
    "san-saba-county": ['san-saba', 'richland-springs', 'cherokee', 'bend'],
    "schleicher-county": ['eldorado', 'fort-mckavett'],
    "scurry-county": ['snyder', 'hermleigh', 'ira', 'fluvanna', 'dunn'],
    "shackelford-county": ['albany', 'moran', 'lueders', 'fort-griffin'],
    "shelby-county": ['center', 'tenaha', 'timpson', 'joaquin', 'huxley', 'shelbyville', 'neuville'],
    "sherman-county": ['stratford', 'texhoma', 'sunray', 'spurlock'],
    "smith-county": ['tyler', 'lindale', 'bullard', 'whitehouse', 'winona', 'troup', 'arp', 'noonday', 'new-chapel-hill', 'hideaway', 'flint', 'overton', 'starrville'],
    "somervell-county": ['glen-rose', 'nemo', 'rainbow'],
    "starr-county": ['rio-grande-city', 'roma', 'la-grulla', 'escobares', 'garciasville', 'los-saenz', 'north-escobares', 'la-rosita', 'el-cenizo'],
    "stephens-county": ['breckenridge', 'caddo', 'wayland', 'crystal-falls'],
    "sterling-county": ['sterling-city', 'water-valley'],
    "stonewall-county": ['aspermont', 'old-glory', 'peacock'],
    "sutton-county": ['sonora', 'fort-terrett'],
    "swisher-county": ['tulia', 'kress', 'happy', 'vigo-park'],
    "tarrant-county": ['fort-worth', 'arlington', 'irving', 'grand-prairie', 'grapevine', 'keller', 'euless', 'bedford', 'hurst', 'north-richland-hills', 'southlake', 'colleyville', 'haltom-city', 'mansfield', 'burleson', 'benbrook', 'watauga', 'forest-hill', 'richland-hills', 'saginaw', 'white-settlement', 'lake-worth', 'everman', 'westworth-village', 'crowley', 'kennedale', 'river-oaks', 'azle', 'sansom-park', 'dalworthington-gardens', 'pantego', 'edgecliff-village', 'lakeside', 'westover-hills', 'trophy-club', 'haslet', 'pecan-acres', 'pelican-bay', 'westlake', 'reno', 'newark'],
    "taylor-county": ['abilene', 'merkel', 'tuscola', 'buffalo-gap', 'tye', 'trent', 'lawn', 'ovalo', 'potosi', 'caps'],
    "terrell-county": ['sanderson', 'dryden', 'pumpville'],
    "terry-county": ['brownfield', 'meadow', 'wellman', 'tokio', 'gomez'],
    "throckmorton-county": ['throckmorton', 'woodson', 'elbert', 'miller-creek'],
    "titus-county": ['mount-pleasant', 'winfield', 'talco', 'cookville', 'miller-grove'],
    "tom-green-county": ['san-angelo', 'grape-creek', 'christoval', 'wall', 'carlsbad', 'knickerbocker', 'harriet', 'mertzon'],
    "travis-county": ['austin', 'bee-cave', 'lakeway', 'lago-vista', 'pflugerville', 'manor', 'west-lake-hills', 'rollingwood', 'sunset-valley', 'volente', 'point-venture', 'briarcliff', 'creedmoor', 'jonestown', 'mustang-ridge', 'webberville', 'manchaca', 'del-valle', 'garfield', 'pilot-knob', 'hornsby-bend', 'wells-branch', 'shady-hollow'],
    "trinity-county": ['groveton', 'trinity', 'pennington', 'apple-springs', 'centralia', 'sebastopol'],
    "tyler-county": ['woodville', 'ivanhoe', 'chester', 'colmesneil', 'spurger', 'doucette', 'fred', 'warren'],
    "upshur-county": ['gilmer', 'big-sandy', 'diana', 'gladewater', 'ore-city', 'union-grove', 'east-mountain', 'pritchett'],
    "upton-county": ['mccamey', 'rankin', 'midkiff'],
    "uvalde-county": ['uvalde', 'sabinal', 'knippa', 'concan', 'utopia'],
    "val-verde-county": ['del-rio', 'laughlin-afb', 'comstock', 'langtry', 'loma-alta'],
    "van-zandt-county": ['canton', 'wills-point', 'van', 'grand-saline', 'edgewood', 'fruitvale', 'ben-wheeler', 'edom', 'martins-mill'],
    "victoria-county": ['victoria', 'bloomington', 'inez', 'placedo', 'nursery', 'mcfaddin'],
    "walker-county": ['huntsville', 'riverside', 'new-waverly', 'dodge', 'phelps'],
    "waller-county": ['brookshire', 'hempstead', 'waller', 'katy', 'prairie-view', 'pattison', 'pine-island'],
    "ward-county": ['monahans', 'barstow', 'wickett', 'grandfalls', 'pyote', 'thorntonville'],
    "washington-county": ['brenham', 'burton', 'chappell-hill', 'independence', 'gay-hill', 'william-penn'],
    "webb-county": ['laredo', 'rio-bravo', 'el-cenizo', 'bruni', 'mirando-city', 'oilton'],
    "wharton-county": ['wharton', 'el-campo', 'east-bernard', 'boling', 'louise', 'hungerford', 'glen-flora', 'lane-city', 'danevang'],
    "wheeler-county": ['shamrock', 'wheeler', 'mobeetie', 'allison', 'briscoe', 'kelton', 'lela', 'twitty'],
    "wichita-county": ['wichita-falls', 'burkburnett', 'iowa-park', 'electra', 'pleasant-valley', 'cashion-community'],
    "wilbarger-county": ['vernon', 'harrold', 'lockett', 'oklaunion', 'odell'],
    "willacy-county": ['raymondville', 'lyford', 'port-mansfield', 'lasara', 'sebastian', 'san-perlita'],
    "williamson-county": ['round-rock', 'cedar-park', 'georgetown', 'leander', 'pflugerville', 'taylor', 'hutto', 'liberty-hill', 'jarrell', 'florence', 'bartlett', 'granger', 'thrall', 'weir', 'coupland', 'schwertner', 'walburg'],
    "wilson-county": ['floresville', 'la-vernia', 'stockdale', 'poth', 'pandora', 'saspamco', 'sutherland-springs'],
    "winkler-county": ['kermit', 'wink', 'mentone'],
    "wise-county": ['decatur', 'bridgeport', 'boyd', 'rhome', 'aurora', 'alvord', 'paradise', 'runaway-bay', 'chico', 'new-fairview', 'lake-bridgeport', 'slidell', 'greenwood'],
    "wood-county": ['mineola', 'winnsboro', 'quitman', 'hawkins', 'alba', 'yantis', 'holly-lake-ranch'],
    "yoakum-county": ['denver-city', 'plains'],
    "young-county": ['graham', 'newcastle', 'olney', 'south-bend', 'jean', 'loving'],
    "zapata-county": ['zapata', 'san-ygnacio', 'medina', 'falcon-mesa', 'falcon-heights', 'lopeno'],
    "zavala-county": ['crystal-city', 'la-pryor', 'batesville', 'chula-vista'],
}

APPLIANCES = ["refrigerator-repair", "washer-repair", "dryer-repair", "dishwasher-repair", "oven-repair", "cooktop-repair", "microwave-repair", "freezer-repair", "wine-cooler-repair", "vent-hood-repair"]

def format_name(slug):
    return slug.replace("-", " ").title()

def build_texas_nav():
    """Build Texas service areas navigation HTML."""
    nav_html = ""
    counter = 0
    for county_slug, towns in sorted(TEXAS_COUNTIES.items()):
        county_name = format_name(county_slug)
        nav_html += f'                            <li class="county-item" data-county="county{counter}">{county_name} ▸</li>\n'
        nav_html += f'                            <div class="county-towns" id="county{counter}">\n'
        for town in towns:
            town_name = format_name(town)
            nav_html += f'                                <li><a href="https://www.texasappliancesrepair.com/{county_slug}/{town}/">{town_name}</a></li>\n'
        nav_html += '                            </div>\n'
        counter += 1
    return nav_html

def build_towns_list(county_slug, towns):
    """Build the townsList HTML for footer section."""
    html = ""
    for town in towns:
        town_name = format_name(town)
        html += f'                                <li><a href="https://www.texasappliancesrepair.com/{county_slug}/{town}/"><h3>{town_name}</h3></a></li>\n'
    return html

def generate_page(county_slug, town_slug, appliance_slug, texas_nav, towns_list_html):
    county_name = format_name(county_slug)
    town_name = format_name(town_slug)
    appliance_name = format_name(appliance_slug.replace("-repair", ""))

    html = TEMPLATE

    # Replace the NJ service areas navigation with Texas navigation
    # Find the service-areas-submenu div and replace its contents
    nj_nav_pattern = r'(<div class="service-areas-submenu" id="serviceAreasSubmenu">).*?(</div>\s*</ul>\s*</div>)'
    texas_nav_replacement = r'\1\n' + texas_nav + r'                        \2'
    html = re.sub(nj_nav_pattern, texas_nav_replacement, html, flags=re.DOTALL)

    # Replace the townsList in footer with current county's towns
    towns_list_pattern = r'(<ul id="townsList">).*?(</ul>)'
    towns_list_replacement = r'\1\n' + towns_list_html + r'                            \2'
    html = re.sub(towns_list_pattern, towns_list_replacement, html, flags=re.DOTALL)

    # Replace domain and URLs
    html = html.replace("lgappliancerepairnj.com", "texasappliancesrepair.com")

    # Replace branding
    html = html.replace("LG Appliance Repair New Jersey", "Texas Appliances Repair")
    html = html.replace("LG Appliance Repair", "Texas Appliances Repair")
    html = html.replace("LG appliance repair", "appliance repair")
    html = re.sub(r'LG [Ff]reezer [Rr]epair', f'{appliance_name} Repair', html)
    html = re.sub(r'LG [Ff]reezer', appliance_name.lower(), html)
    html = re.sub(r' LG ', ' ', html)
    html = re.sub(r'>LG ', '>', html)

    # Replace state
    html = html.replace("New Jersey", "Texas")
    html = html.replace(", NJ", ", TX")
    html = re.sub(r'\bNJ\b', 'TX', html)

    # Replace county and town
    html = html.replace("Hunterdon County", county_name)
    html = html.replace("hunterdon-county", county_slug)
    html = html.replace("Clinton Township", town_name)
    html = html.replace("clinton-township", town_slug)

    # Replace appliance
    html = html.replace("freezer-repair", appliance_slug)
    html = re.sub(r'[Ff]reezer [Rr]epair', f'{appliance_name} Repair', html)
    html = re.sub(r'freezer repair', f'{appliance_name.lower()} repair', html)
    html = re.sub(r'\bfreezer\b', appliance_name.lower(), html)
    html = re.sub(r'\bFreezer\b', appliance_name, html)

    # Remove factory/certified/authorized
    html = re.sub(r'[Ff]actory-[Cc]ertified', 'Professional', html)
    html = re.sub(r'[Ff]actory-[Tt]rained', 'Trained', html)
    html = re.sub(r'[Ff]actory [Cc]ertified', 'Professional', html)
    html = re.sub(r'\b[Cc]ertified\b', 'Trained', html)
    html = re.sub(r'\b[Aa]uthorized\b', 'Professional', html)

    # Update canonical - use https www
    html = re.sub(
        r'<link rel="canonical" href="[^"]*">',
        f'<link rel="canonical" href="https://www.texasappliancesrepair.com/{county_slug}/{town_slug}/{appliance_slug}/">',
        html
    )

    # Update og:url
    html = re.sub(
        r'<meta property="og:url" content="[^"]*">',
        f'<meta property="og:url" content="https://www.texasappliancesrepair.com/{county_slug}/{town_slug}/{appliance_slug}/">',
        html
    )

    # Update logo reference
    html = html.replace('/assets/images/lg-logo.png', '/assets/images/logo.png')

    # Make hero image 20% more visible (reduce overlay from 78% to 58%)
    html = html.replace('rgba(0, 0, 0, 0.78)', 'rgba(0, 0, 0, 0.58)')

    return html

def main():
    base_dir = "/tmp/texas-appliances-repair"

    # Build Texas navigation once
    print("Building Texas navigation...")
    texas_nav = build_texas_nav()

    sitemap_urls = ["https://www.texasappliancesrepair.com/"]
    total = 0

    for county_slug, towns in TEXAS_COUNTIES.items():
        county_dir = os.path.join(base_dir, county_slug)
        os.makedirs(county_dir, exist_ok=True)

        # Build towns list HTML for this county's footer
        towns_list_html = build_towns_list(county_slug, towns)

        for town_slug in towns:
            town_dir = os.path.join(county_dir, town_slug)
            os.makedirs(town_dir, exist_ok=True)

            # Town hub page
            sitemap_urls.append(f"https://www.texasappliancesrepair.com/{county_slug}/{town_slug}/")

            for appliance in APPLIANCES:
                appl_dir = os.path.join(town_dir, appliance)
                os.makedirs(appl_dir, exist_ok=True)

                html = generate_page(county_slug, town_slug, appliance, texas_nav, towns_list_html)

                with open(os.path.join(appl_dir, "index.html"), "w") as f:
                    f.write(html)

                sitemap_urls.append(f"https://www.texasappliancesrepair.com/{county_slug}/{town_slug}/{appliance}/")
                total += 1

        print(f"Created {county_slug}: {len(towns)} towns")

    # Generate sitemap with https www
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sitemap_urls:
        sitemap += f'  <url><loc>{url}</loc></url>\n'
    sitemap += '</urlset>'

    with open(os.path.join(base_dir, "sitemap.xml"), "w") as f:
        f.write(sitemap)

    # Update robots.txt with https www
    with open(os.path.join(base_dir, "robots.txt"), "w") as f:
        f.write("User-agent: *\nAllow: /\n\nSitemap: https://www.texasappliancesrepair.com/sitemap.xml\n")

    # Update homepage navigation
    print("Updating homepage navigation...")
    homepage_path = os.path.join(base_dir, "index.html")
    with open(homepage_path, 'r') as f:
        homepage = f.read()

    # Replace header navigation
    nj_nav_pattern = r'(<div class="service-areas-submenu" id="serviceAreasSubmenu">).*?(</div>\s*</ul>\s*</div>)'
    texas_nav_replacement = r'\1\n' + texas_nav + r'                        \2'
    homepage = re.sub(nj_nav_pattern, texas_nav_replacement, homepage, flags=re.DOTALL)

    # Build county list for footer (all counties)
    county_list_html = ""
    for county_slug in sorted(TEXAS_COUNTIES.keys()):
        county_name = format_name(county_slug)
        county_list_html += f'                                <li><a href="https://www.texasappliancesrepair.com/{county_slug}/"><h3>{county_name}</h3></a></li>\n'

    # Replace footer county list
    county_list_pattern = r'(<ul id="townsList">).*?(</ul>)'
    county_list_replacement = r'\1\n' + county_list_html + r'                            \2'
    homepage = re.sub(county_list_pattern, county_list_replacement, homepage, flags=re.DOTALL)

    with open(homepage_path, 'w') as f:
        f.write(homepage)

    print(f"\nTotal: {len(TEXAS_COUNTIES)} counties, {total} service pages")
    print(f"Sitemap: {len(sitemap_urls)} URLs")

if __name__ == "__main__":
    main()
