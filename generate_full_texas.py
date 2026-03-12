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
TEXAS_COUNTIES = {
    "anderson-county": ["palestine", "frankston", "elkhart", "cayuga", "montalba"],
    "andrews-county": ["andrews"],
    "angelina-county": ["lufkin", "hudson", "diboll", "huntington", "zavalla", "burke"],
    "aransas-county": ["rockport", "fulton", "aransas-pass", "lamar", "holiday-beach"],
    "archer-county": ["archer-city", "holliday", "lakeside-city", "megargel", "scotland"],
    "armstrong-county": ["claude"],
    "atascosa-county": ["pleasanton", "poteet", "jourdanton", "lytle", "charlotte"],
    "austin-county": ["bellville", "sealy", "wallis", "san-felipe"],
    "bailey-county": ["muleshoe"],
    "bandera-county": ["bandera", "lakehills", "medina", "pipe-creek"],
    "bastrop-county": ["bastrop", "elgin", "smithville", "cedar-creek", "paige"],
    "baylor-county": ["seymour"],
    "bee-county": ["beeville", "pettus", "skidmore", "tynan"],
    "bell-county": ["killeen", "temple", "belton", "harker-heights", "copperas-cove", "nolanville", "salado"],
    "bexar-county": ["san-antonio", "converse", "live-oak", "universal-city", "schertz", "selma", "helotes", "leon-valley", "alamo-heights", "terrell-hills", "castle-hills", "balcones-heights", "shavano-park", "hollywood-park", "windcrest", "kirby"],
    "blanco-county": ["johnson-city", "blanco", "round-mountain"],
    "borden-county": ["gail"],
    "bosque-county": ["meridian", "clifton", "valley-mills", "walnut-springs"],
    "bowie-county": ["texarkana", "new-boston", "hooks", "wake-village", "nash", "de-kalb"],
    "brazoria-county": ["pearland", "lake-jackson", "alvin", "angleton", "clute", "freeport", "brazoria", "richwood", "manvel", "west-columbia", "sweeny", "surfside-beach"],
    "brazos-county": ["bryan", "college-station", "wixon-valley", "kurten"],
    "brewster-county": ["alpine", "marathon", "terlingua"],
    "briscoe-county": ["silverton", "quitaque"],
    "brooks-county": ["falfurrias", "encino"],
    "brown-county": ["brownwood", "early", "bangs", "blanket"],
    "burleson-county": ["caldwell", "somerville", "snook"],
    "burnet-county": ["burnet", "marble-falls", "bertram", "granite-shoals", "highland-haven"],
    "caldwell-county": ["lockhart", "luling", "martindale", "maxwell", "dale"],
    "calhoun-county": ["port-lavaca", "seadrift", "point-comfort"],
    "callahan-county": ["baird", "clyde", "cross-plains"],
    "cameron-county": ["brownsville", "harlingen", "san-benito", "port-isabel", "la-feria", "los-fresnos", "south-padre-island", "palm-valley", "primera", "rancho-viejo", "laguna-vista", "rio-hondo", "santa-rosa"],
    "camp-county": ["pittsburg"],
    "carson-county": ["panhandle", "white-deer", "groom"],
    "cass-county": ["atlanta", "linden", "queen-city", "hughes-springs"],
    "castro-county": ["dimmitt", "hart", "nazareth"],
    "chambers-county": ["anahuac", "mont-belvieu", "beach-city", "winnie", "stowell"],
    "cherokee-county": ["jacksonville", "rusk", "alto", "troup", "wells"],
    "childress-county": ["childress"],
    "clay-county": ["henrietta", "petrolia", "bellevue"],
    "cochran-county": ["morton", "whiteface"],
    "coke-county": ["robert-lee", "bronte"],
    "coleman-county": ["coleman", "santa-anna"],
    "collin-county": ["plano", "mckinney", "frisco", "allen", "wylie", "murphy", "prosper", "celina", "princeton", "anna", "farmersville", "lucas", "fairview", "lavon", "melissa"],
    "collingsworth-county": ["wellington"],
    "colorado-county": ["columbus", "eagle-lake", "weimar"],
    "comal-county": ["new-braunfels", "bulverde", "garden-ridge", "canyon-lake", "spring-branch"],
    "comanche-county": ["comanche", "de-leon", "gustine"],
    "concho-county": ["eden", "paint-rock"],
    "cooke-county": ["gainesville", "muenster", "lindsay", "valley-view"],
    "coryell-county": ["copperas-cove", "gatesville", "evant"],
    "cottle-county": ["paducah"],
    "crane-county": ["crane"],
    "crockett-county": ["ozona"],
    "crosby-county": ["crosbyton", "ralls", "lorenzo"],
    "culberson-county": ["van-horn"],
    "dallam-county": ["dalhart", "texline"],
    "dallas-county": ["dallas", "irving", "garland", "grand-prairie", "mesquite", "carrollton", "richardson", "desoto", "rowlett", "duncanville", "cedar-hill", "lancaster", "farmers-branch", "coppell", "balch-springs", "glenn-heights", "hutchins", "addison", "highland-park", "university-park"],
    "dawson-county": ["lamesa"],
    "deaf-smith-county": ["hereford"],
    "delta-county": ["cooper"],
    "denton-county": ["denton", "lewisville", "flower-mound", "the-colony", "little-elm", "corinth", "highland-village", "lake-dallas", "sanger", "aubrey", "pilot-point", "argyle", "justin", "krum", "trophy-club", "northlake", "roanoke"],
    "dewitt-county": ["cuero", "yoakum", "nordheim"],
    "dickens-county": ["spur", "dickens"],
    "dimmit-county": ["carrizo-springs", "asherton"],
    "donley-county": ["clarendon", "hedley"],
    "duval-county": ["san-diego", "benavides", "freer"],
    "eastland-county": ["eastland", "cisco", "ranger", "gorman"],
    "ector-county": ["odessa", "west-odessa", "goldsmith", "gardendale"],
    "edwards-county": ["rocksprings"],
    "el-paso-county": ["el-paso", "socorro", "horizon-city", "san-elizario", "anthony", "clint", "fabens", "tornillo", "canutillo"],
    "ellis-county": ["waxahachie", "midlothian", "ennis", "red-oak", "ferris", "palmer", "italy", "maypearl", "milford"],
    "erath-county": ["stephenville", "dublin", "bluff-dale"],
    "falls-county": ["marlin", "rosebud", "chilton"],
    "fannin-county": ["bonham", "leonard", "trenton", "honey-grove"],
    "fayette-county": ["la-grange", "schulenburg", "flatonia", "fayetteville"],
    "fisher-county": ["rotan", "roby"],
    "floyd-county": ["floydada", "lockney"],
    "foard-county": ["crowell"],
    "fort-bend-county": ["sugar-land", "missouri-city", "rosenberg", "richmond", "stafford", "fulshear", "meadows-place", "needville", "pecan-grove", "cinco-ranch", "fresno", "arcola"],
    "franklin-county": ["mount-vernon"],
    "freestone-county": ["teague", "fairfield", "wortham"],
    "frio-county": ["pearsall", "dilley"],
    "gaines-county": ["seminole", "seagraves"],
    "galveston-county": ["galveston", "texas-city", "league-city", "friendswood", "dickinson", "la-marque", "santa-fe", "kemah", "hitchcock", "clear-lake-shores", "jamaica-beach"],
    "garza-county": ["post"],
    "gillespie-county": ["fredericksburg", "harper", "stonewall"],
    "glasscock-county": ["garden-city"],
    "goliad-county": ["goliad"],
    "gonzales-county": ["gonzales", "nixon", "waelder", "smiley"],
    "gray-county": ["pampa", "lefors", "mclean"],
    "grayson-county": ["sherman", "denison", "van-alstyne", "howe", "pottsboro", "whitesboro", "whitewright", "bells", "gunter"],
    "gregg-county": ["longview", "kilgore", "gladewater", "white-oak"],
    "grimes-county": ["navasota", "anderson", "iola"],
    "guadalupe-county": ["seguin", "schertz", "cibolo", "marion", "santa-clara"],
    "hale-county": ["plainview", "hale-center", "abernathy"],
    "hall-county": ["memphis", "estelline", "turkey"],
    "hamilton-county": ["hamilton", "hico"],
    "hansford-county": ["spearman", "gruver"],
    "hardeman-county": ["quanah", "chillicothe"],
    "hardin-county": ["silsbee", "lumberton", "kountze", "sour-lake"],
    "harris-county": ["houston", "pasadena", "baytown", "pearland", "league-city", "missouri-city", "cypress", "katy", "spring", "humble", "atascocita", "bellaire", "deer-park", "la-porte", "seabrook", "south-houston", "jersey-village", "west-university-place", "tomball", "webster", "friendswood"],
    "harrison-county": ["marshall", "waskom", "hallsville"],
    "hartley-county": ["channing", "hartley"],
    "haskell-county": ["haskell", "rochester", "rule"],
    "hays-county": ["san-marcos", "kyle", "buda", "dripping-springs", "wimberley", "mountain-city", "woodcreek"],
    "hemphill-county": ["canadian"],
    "henderson-county": ["athens", "chandler", "gun-barrel-city", "mabank", "malakoff", "brownsboro", "eustace"],
    "hidalgo-county": ["mcallen", "edinburg", "mission", "pharr", "weslaco", "san-juan", "alamo", "donna", "mercedes", "la-joya", "palmview", "hidalgo", "elsa"],
    "hill-county": ["hillsboro", "whitney", "itasca", "hubbard", "blum"],
    "hockley-county": ["levelland", "sundown"],
    "hood-county": ["granbury", "tolar", "lipan", "cresson"],
    "hopkins-county": ["sulphur-springs", "como-pickton", "cumby"],
    "houston-county": ["crockett", "grapeland", "kennard"],
    "howard-county": ["big-spring", "coahoma", "forsan"],
    "hudspeth-county": ["dell-city", "fort-hancock", "sierra-blanca"],
    "hunt-county": ["greenville", "commerce", "quinlan", "caddo-mills", "lone-oak", "celeste", "wolfecity"],
    "hutchinson-county": ["borger", "fritch", "stinnett"],
    "irion-county": ["mertzon"],
    "jack-county": ["jacksboro", "bryson"],
    "jackson-county": ["edna", "ganado", "la-ward"],
    "jasper-county": ["jasper", "kirbyville", "buna"],
    "jeff-davis-county": ["fort-davis", "valentine"],
    "jefferson-county": ["beaumont", "port-arthur", "nederland", "groves", "port-neches"],
    "jim-hogg-county": ["hebbronville"],
    "jim-wells-county": ["alice", "orange-grove", "premont"],
    "johnson-county": ["cleburne", "burleson", "mansfield", "joshua", "alvarado", "keene", "godley", "grandview", "venus"],
    "jones-county": ["anson", "hamlin", "hawley", "stamford"],
    "karnes-county": ["karnes-city", "kenedy", "runge"],
    "kaufman-county": ["kaufman", "terrell", "forney", "crandall", "mabank", "kemp", "heath"],
    "kendall-county": ["boerne", "comfort"],
    "kenedy-county": ["sarita"],
    "kent-county": ["jayton"],
    "kerr-county": ["kerrville", "ingram", "center-point"],
    "kimble-county": ["junction"],
    "king-county": ["guthrie"],
    "kinney-county": ["brackettville"],
    "kleberg-county": ["kingsville", "riviera"],
    "knox-county": ["knox-city", "munday"],
    "lamar-county": ["paris", "blossom", "deport", "roxton"],
    "lamb-county": ["littlefield", "olton", "sudan"],
    "lampasas-county": ["lampasas", "kempner", "lometa"],
    "la-salle-county": ["cotulla", "encinal"],
    "lavaca-county": ["hallettsville", "yoakum", "shiner", "moulton"],
    "lee-county": ["giddings", "lexington"],
    "leon-county": ["centerville", "buffalo", "jewett", "leona"],
    "liberty-county": ["liberty", "cleveland", "dayton", "ames", "daisetta"],
    "limestone-county": ["mexia", "groesbeck", "kosse"],
    "lipscomb-county": ["booker", "darrouzett", "follett", "higgins"],
    "live-oak-county": ["george-west", "three-rivers"],
    "llano-county": ["llano", "kingsland", "horseshoe-bay"],
    "loving-county": ["mentone"],
    "lubbock-county": ["lubbock", "wolfforth", "slaton", "shallowater", "idalou", "abernathy"],
    "lynn-county": ["tahoka", "odonnell"],
    "madison-county": ["madisonville", "midway"],
    "marion-county": ["jefferson"],
    "martin-county": ["stanton"],
    "mason-county": ["mason"],
    "matagorda-county": ["bay-city", "palacios", "sargent", "markham"],
    "maverick-county": ["eagle-pass"],
    "mcculloch-county": ["brady", "melvin"],
    "mclennan-county": ["waco", "hewitt", "woodway", "robinson", "bellmead", "lacy-lakeview", "mcgregor", "lorena", "west", "mart"],
    "mcmullen-county": ["tilden"],
    "medina-county": ["hondo", "castroville", "devine", "natalia", "lacoste", "lytle"],
    "menard-county": ["menard"],
    "midland-county": ["midland", "greenwood"],
    "milam-county": ["cameron", "rockdale", "thorndale"],
    "mills-county": ["goldthwaite", "mullin"],
    "mitchell-county": ["colorado-city", "loraine"],
    "montague-county": ["bowie", "nocona", "saint-jo"],
    "montgomery-county": ["conroe", "the-woodlands", "magnolia", "willis", "shenandoah", "oak-ridge-north", "panorama-village", "cut-and-shoot", "splendora", "montgomery"],
    "moore-county": ["dumas", "sunray", "cactus"],
    "morris-county": ["daingerfield", "naples", "omaha"],
    "motley-county": ["matador", "roaring-springs"],
    "nacogdoches-county": ["nacogdoches", "garrison", "cushing"],
    "navarro-county": ["corsicana", "kerens", "blooming-grove", "rice", "frost"],
    "newton-county": ["newton", "burkeville"],
    "nolan-county": ["sweetwater", "roscoe"],
    "nueces-county": ["corpus-christi", "robstown", "port-aransas", "agua-dulce", "bishop"],
    "ochiltree-county": ["perryton"],
    "oldham-county": ["vega", "adrian"],
    "orange-county": ["orange", "vidor", "bridge-city", "west-orange", "pinehurst"],
    "palo-pinto-county": ["mineral-wells", "graford", "gordon"],
    "panola-county": ["carthage", "beckville", "gary"],
    "parker-county": ["weatherford", "willow-park", "hudson-oaks", "aledo", "azle", "springtown"],
    "parmer-county": ["friona", "bovina", "farwell"],
    "pecos-county": ["fort-stockton", "iraan"],
    "polk-county": ["livingston", "onalaska", "corrigan"],
    "potter-county": ["amarillo"],
    "presidio-county": ["presidio", "marfa"],
    "rains-county": ["emory", "point"],
    "randall-county": ["amarillo", "canyon"],
    "reagan-county": ["big-lake"],
    "real-county": ["leakey", "camp-wood"],
    "red-river-county": ["clarksville", "bogata", "annona"],
    "reeves-county": ["pecos", "balmorhea", "toyah"],
    "refugio-county": ["refugio", "woodsboro"],
    "roberts-county": ["miami"],
    "robertson-county": ["hearne", "franklin", "calvert", "bremond"],
    "rockwall-county": ["rockwall", "heath", "rowlett", "royse-city", "fate"],
    "runnels-county": ["ballinger", "winters"],
    "rusk-county": ["henderson", "kilgore", "tatum", "overton"],
    "sabine-county": ["hemphill", "pineland"],
    "san-augustine-county": ["san-augustine"],
    "san-jacinto-county": ["coldspring", "shepherd"],
    "san-patricio-county": ["portland", "sinton", "aransas-pass", "ingleside", "mathis", "odem", "taft"],
    "san-saba-county": ["san-saba"],
    "schleicher-county": ["eldorado"],
    "scurry-county": ["snyder"],
    "shackelford-county": ["albany", "moran"],
    "shelby-county": ["center", "tenaha", "timpson"],
    "sherman-county": ["stratford"],
    "smith-county": ["tyler", "lindale", "whitehouse", "bullard", "troup", "arp", "hideaway"],
    "somervell-county": ["glen-rose", "rainbow"],
    "starr-county": ["rio-grande-city", "roma", "la-grulla"],
    "stephens-county": ["breckenridge"],
    "sterling-county": ["sterling-city"],
    "stonewall-county": ["aspermont"],
    "sutton-county": ["sonora"],
    "swisher-county": ["tulia", "happy", "kress"],
    "tarrant-county": ["fort-worth", "arlington", "north-richland-hills", "euless", "bedford", "grapevine", "haltom-city", "keller", "southlake", "colleyville", "hurst", "watauga", "saginaw", "benbrook", "crowley", "white-settlement", "forest-hill", "mansfield", "burleson"],
    "taylor-county": ["abilene", "merkel", "tye", "tuscola"],
    "terrell-county": ["sanderson"],
    "terry-county": ["brownfield", "meadow"],
    "throckmorton-county": ["throckmorton"],
    "titus-county": ["mount-pleasant", "talco", "winfield"],
    "tom-green-county": ["san-angelo", "grape-creek", "wall", "christoval"],
    "travis-county": ["austin", "round-rock", "pflugerville", "cedar-park", "bee-cave", "lakeway", "west-lake-hills", "rollingwood", "lago-vista", "manor", "jonestown"],
    "trinity-county": ["groveton", "trinity"],
    "tyler-county": ["woodville", "ivanhoe", "chester"],
    "upshur-county": ["gilmer", "gladewater", "big-sandy", "ore-city"],
    "upton-county": ["rankin", "mccamey"],
    "uvalde-county": ["uvalde", "sabinal", "utopia"],
    "val-verde-county": ["del-rio", "comstock"],
    "van-zandt-county": ["canton", "wills-point", "grand-saline", "van", "edgewood"],
    "victoria-county": ["victoria", "bloomington"],
    "walker-county": ["huntsville", "riverside", "new-waverly"],
    "waller-county": ["waller", "hempstead", "brookshire", "prairie-view"],
    "ward-county": ["monahans", "barstow", "grandfalls"],
    "washington-county": ["brenham", "burton", "chappell-hill"],
    "webb-county": ["laredo", "rio-bravo", "el-cenizo"],
    "wharton-county": ["wharton", "el-campo", "east-bernard", "boling"],
    "wheeler-county": ["shamrock", "wheeler", "mobeetie"],
    "wichita-county": ["wichita-falls", "burkburnett", "iowa-park", "electra"],
    "wilbarger-county": ["vernon"],
    "willacy-county": ["raymondville", "lyford", "port-mansfield"],
    "williamson-county": ["round-rock", "cedar-park", "georgetown", "leander", "taylor", "hutto", "liberty-hill", "jarrell", "florence"],
    "wilson-county": ["floresville", "la-vernia", "stockdale", "poth"],
    "winkler-county": ["kermit", "wink"],
    "wise-county": ["decatur", "bridgeport", "boyd", "rhome", "aurora", "alvord", "chico", "runaway-bay"],
    "wood-county": ["mineola", "quitman", "winnsboro", "hawkins"],
    "yoakum-county": ["denver-city", "plains"],
    "young-county": ["graham", "olney", "newcastle"],
    "zapata-county": ["zapata"],
    "zavala-county": ["crystal-city", "la-pryor"],
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

    print(f"\nTotal: {len(TEXAS_COUNTIES)} counties, {total} service pages")
    print(f"Sitemap: {len(sitemap_urls)} URLs")

if __name__ == "__main__":
    main()
