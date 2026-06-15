from django.core.management.base import BaseCommand
from core.models import Equipment


EQUIPMENT_DATA = [
    {
        "name": "VLCC Crude Oil Tanker Ship",
        "category": "tanker",
        "static_image": "VLCC_Crude_Oil_Tanker_Ship.webp",
        "daily_rate": "85000.00",
        "capacity": "300,000 DWT",
        "location": "Port of Rotterdam, Netherlands",
        "status": "available",
        "featured": True,
        "description": (
            "Our Very Large Crude Carrier (VLCC) is a state-of-the-art ocean-going oil tanker "
            "capable of transporting up to 300,000 tonnes of crude oil across intercontinental "
            "routes. Built to the highest DNV class standards, this vessel features double-hull "
            "construction for maximum environmental protection, advanced navigation systems "
            "including ECDIS and AIS, and full inert gas systems for cargo safety.\n\n"
            "Equipped with 28 cargo tanks and 2 slop tanks, the vessel handles multiple grades "
            "of crude oil simultaneously. Her 21-knot service speed and 30,000nm range make her "
            "ideal for VLCC trades between Middle East Gulf, West Africa, and Asia Pacific "
            "terminals. Comes with a full crew complement of 32 officers and ratings, all "
            "STCW-certified and experienced on VLCC operations. All classification certificates "
            "current. Available for time-charter or voyage-charter arrangements."
        ),
    },
    {
        "name": "Petroleum Tanker Truck — 45,000L",
        "category": "truck",
        "static_image": "Petroleum_Tanker_Truck.jpg",
        "daily_rate": "1800.00",
        "capacity": "45,000 Litres",
        "location": "Oslo, Norway",
        "status": "available",
        "featured": True,
        "description": (
            "Heavy-duty petroleum tanker truck built on a 6x4 prime mover chassis, paired with "
            "a tri-axle aluminum tank trailer with a 45,000-litre capacity. This unit is ADR/DGR "
            "certified for the transport of flammable liquids including diesel, petrol, aviation "
            "fuel, and light crude oil. The elliptical aluminum tank is divided into 5 separate "
            "compartments allowing multi-product loads without cross-contamination.\n\n"
            "Safety features include emergency shut-off valves, overfill protection sensors, "
            "earthing cables, fire extinguishers, and full hazmat placarding. The truck is "
            "equipped with GPS fleet tracking, a digital tachograph, and anti-lock brakes. "
            "Payload capacity of 30 tonnes. Engine overhauled at 200,000 km. Current road "
            "worthiness certificate and carrier permit. Crew training available on request."
        ),
    },
    {
        "name": "Semi-Submersible Offshore Drilling Rig",
        "category": "offshore",
        "static_image": "Semi-Submersible_Offshore_Drilling_Rig.jpg",
        "daily_rate": "420000.00",
        "capacity": "120 POB / 3,000m Water Depth",
        "location": "Gulf of Mexico, USA",
        "status": "available",
        "featured": True,
        "description": (
            "Ultra-deepwater semi-submersible drilling rig rated to 3,000 metres water depth "
            "and 9,000 metres measured depth. This 6th-generation rig is equipped with a top "
            "drive drilling system, 2,000-ton hook load capacity, and a fully automated pipe "
            "handling system capable of running 5,400 metres of riser string. The rig operates "
            "on dynamic positioning (DP3) with triple redundancy for maximum uptime in extreme "
            "weather conditions.\n\n"
            "Living quarters accommodate 120 personnel with full amenities. Onboard facilities "
            "include a 120m² drill floor, mud logging unit, blow-out preventer stack rated to "
            "15,000 PSI, and a certified helideck for S-92/AW139 operations. All equipment "
            "maintained under a Class-approved preventive maintenance system. DNV class "
            "certificates current. Available on day-rate or turnkey basis."
        ),
    },
    {
        "name": "Crude Oil Storage Tank Farm — 500,000 BBL",
        "category": "storage",
        "static_image": "Crude_Oil_Storage_Tank_Farm.jpg",
        "daily_rate": "12500.00",
        "capacity": "500,000 Barrels Total",
        "location": "Texas City, TX, USA",
        "status": "available",
        "featured": False,
        "description": (
            "Fully operational crude oil tank farm comprising three fixed-roof atmospheric "
            "storage tanks with a combined capacity of 500,000 barrels. Each tank is constructed "
            "to API 650 standard using high-tensile carbon steel with full epoxy internal lining "
            "for corrosion protection. The facility is equipped with secondary containment bunds "
            "rated at 110% tank volume, automatic overfill protection, level gauging, and "
            "continuous leak detection systems.\n\n"
            "All tanks are connected via a dedicated manifold system with ball valve isolation, "
            "allowing flexible blending and segregation of crude grades. The facility includes "
            "two centrifugal pump sets at 2,000 m³/h throughput each, custody transfer metering "
            "to OIML R117 standard, and a full SCADA system for remote monitoring. API 653 "
            "inspection current. Located adjacent to deepwater marine terminal with pipeline "
            "connectivity to three major refineries."
        ),
    },
    {
        "name": "High-Pressure Crude Oil Pipeline — 80km Section",
        "category": "pipeline",
        "static_image": "High-Pressure_Crude_Oil_Pipeline.jpg",
        "daily_rate": "95000.00",
        "capacity": "500,000 BPD Throughput",
        "location": "North Sea, UK Sector",
        "status": "available",
        "featured": False,
        "description": (
            "A certified 36-inch diameter carbon steel crude oil transmission pipeline spanning "
            "80 kilometres, rated to 1,200 PSI maximum allowable operating pressure (MAOP). "
            "Constructed to ASME B31.4 pipeline standard with 3-layer polyethylene external "
            "coating and impressed current cathodic protection system in full operation. The "
            "pipeline is piggable with full-bore geometry, and smart pigging runs are completed "
            "annually for integrity management.\n\n"
            "The section includes 4 intermediate block valve stations, 2 inline inspection "
            "traps, and a SCADA-monitored supervisory control system providing real-time "
            "pressure, temperature, and flow data to a 24/7 control room. Maximum throughput "
            "of 500,000 barrels per day. Available for tariff-based third-party access. HSE "
            "COMAH upper-tier registered. Pipeline integrity management system (PIMS) records "
            "available on request."
        ),
    },
    {
        "name": "Land Drilling Rig — 2,000HP AC Drive",
        "category": "drilling",
        "static_image": "Land_Drilling_Rig.jpg",
        "daily_rate": "55000.00",
        "capacity": "9,000m Depth Rated",
        "location": "Permian Basin, TX, USA",
        "status": "available",
        "featured": False,
        "description": (
            "High-performance land drilling rig powered by a 2,000HP AC variable frequency "
            "drive (VFD) system, rated for drilling to 9,000 metres measured depth in hard "
            "rock formations. The mast has a 750-ton static hook load rating with a 165-foot "
            "clear height, accommodating 5-inch drill pipe stands. The automated pipe-handling "
            "system significantly reduces personnel exposure on the drill floor.\n\n"
            "The rig package includes a 7,500 PSI triplex pump set (3 pumps), a top drive unit "
            "rated to 55,000 ft-lb torque, a fully enclosed drill floor with iron roughneck, "
            "and a 500-tonne draw-works. Camp facilities for 60 personnel are included with the "
            "package. The rig can be rapidly mobilised by road in 14 truckloads and has a "
            "proven rig-up time of under 72 hours. Full drilling BOP stack (5,000 PSI) included. "
            "Available on a day-rate or footage basis."
        ),
    },
    {
        "name": "Beam Pump Jack — Automated Oil Well",
        "category": "industrial",
        "static_image": "Beam_Pump_Jack.jpg",
        "daily_rate": "850.00",
        "capacity": "20 BPD / 300m Depth",
        "location": "Alberta, Canada",
        "status": "available",
        "featured": False,
        "description": (
            "Heavy-duty beam pump jack (sucker rod pump) designed for artificial lift operations "
            "on conventional oil wells producing 15–20 barrels per day from depths up to 300 "
            "metres. The unit features a 456-inch pumping unit with a 120-inch stroke and a "
            "44,000 ft-lb peak torque gearbox, manufactured by Lufkin Industries. The motor is "
            "a 30kW IE3 premium efficiency model with integrated VFD for optimised pump "
            "fillage and energy savings.\n\n"
            "The automated control system monitors downhole pump performance via dynamometer "
            "cards, automatically adjusting pump stroke speed to maximise production while "
            "preventing pump-off. Remote monitoring via 4G telemetry allows well surveillance "
            "from the field office. Complete with sucker rod string, plunger pump assembly, "
            "stuffing box, and production header. Suitable for crude oil, water-cut wells, "
            "and coal-bed methane operations. Trailer-mounted for quick relocation."
        ),
    },
    {
        "name": "Oil Refinery Processing Unit — CDU/VDU",
        "category": "industrial",
        "static_image": "Oil_Refinery_Processing_Unit.jpg",
        "daily_rate": "380000.00",
        "capacity": "50,000 BPD",
        "location": "Jubail Industrial City, Saudi Arabia",
        "status": "available",
        "featured": False,
        "description": (
            "Integrated crude distillation unit (CDU) and vacuum distillation unit (VDU) with "
            "a combined processing capacity of 50,000 barrels per day. The CDU separates crude "
            "oil into LPG, naphtha, kerosene, gas oil, and atmospheric residue fractions using "
            "a 120-tray distillation column with structured packing sections. The VDU further "
            "processes atmospheric residue into vacuum gas oil and vacuum residue suitable for "
            "asphalt production or further upgrading.\n\n"
            "The unit includes a fired heater train with thermal efficiency of 92%, heat "
            "integration via a 24-stage preheat train, desalter package (two-stage electrostatic), "
            "and stabiliser column. All vessels are ASME Section VIII Division 1 certified. "
            "The control system runs on Honeywell Experion PKS DCS with advanced process "
            "control (APC) for yield optimisation. Steam generation capacity of 80 tonnes/hour "
            "included. Full P&ID documentation and operations manual provided."
        ),
    },
    {
        "name": "Tanker Semi-Trailer — Tri-Axle Aluminium",
        "category": "trailer",
        "static_image": "Tanker_Semi_Trailer.jpg",
        "daily_rate": "1200.00",
        "capacity": "38,000 Litres",
        "location": "Miami, FL, USA",
        "status": "available",
        "featured": False,
        "description": (
            "Professional-grade aluminium tanker semi-trailer with a 38,000-litre capacity "
            "divided into 4 compartments for multi-product petroleum delivery. The elliptical "
            "tank is fabricated from 5000-series marine-grade aluminium alloy, giving it "
            "exceptional strength-to-weight ratio and resistance to petroleum product corrosion. "
            "Tri-axle BPW air-suspension axles provide a smooth ride and even load distribution "
            "over varied road conditions.\n\n"
            "The trailer features bottom-loading API adaptors, vapour recovery connections, "
            "emergency shut-off valves activated by pneumatic or cable pull, and 4-inch "
            "stainless steel discharge valves per compartment. Anti-rollover protection and "
            "electronic stability control are integrated with the trailer's brake system. "
            "Suitable for pairing with any 6x4 or 6x2 prime mover with a fifth-wheel coupling. "
            "ADR/Hazmat compliant, current roadworthy certificate. Available for short and "
            "long-term rental or purchase."
        ),
    },
    {
        "name": "FPSO — Floating Production Storage & Offloading",
        "category": "offshore",
        "static_image": "red_and_white_boat.jpg",
        "daily_rate": "750000.00",
        "capacity": "200,000 BOPD / 100,000 DWT Storage",
        "location": "North America — Deepwater Block",
        "status": "available",
        "featured": True,
        "description": (
            "World-class Floating Production, Storage, and Offloading (FPSO) vessel with "
            "200,000 barrels per day oil processing capacity and 100,000 DWT cargo storage. "
            "The FPSO is permanently moored via a turret mooring system, allowing the vessel "
            "to weathervane freely through 360° in all sea states. Topside processing facilities "
            "include a 3-train oil/water/gas separation plant, gas compression and injection "
            "system, produced water treatment to IMO MARPOL standards, and an offloading system "
            "capable of tandem transfer to shuttle tankers at 10,000 m³/hr.\n\n"
            "Power generation is provided by four 20MW dual-fuel generators using produced gas. "
            "Living quarters accommodate 200 personnel. The vessel is classed by Bureau Veritas, "
            "holds DP3 dynamic positioning capability on the turret integrated mooring system, "
            "and is fully certified for harsh environment deepwater operations to 2,000m. "
            "Comes with full offshore crew complement and asset management contract. "
            "Maintenance reserve fund in place. Available on field life-of-project basis."
        ),
    },
    {
        "name": "Gas Compressor Station — 50 MMSCFD",
        "category": "industrial",
        "static_image": "Gas_Compressor_Station.jpg",
        "daily_rate": "48000.00",
        "capacity": "50 MMSCFD / 3,600 PSI Discharge",
        "location": "Midland, TX, USA",
        "status": "available",
        "featured": False,
        "description": (
            "Skid-mounted natural gas compressor station comprising three centrifugal compressor "
            "trains, each driven by a Solar Turbines Saturn 20 gas turbine (1,200kW), delivering "
            "a combined throughput of 50 million standard cubic feet per day (MMSCFD) at "
            "3,600 PSI discharge pressure. The station is designed for gas gathering, "
            "transmission, and reinjection applications.\n\n"
            "Each train is equipped with inlet separation, inter-stage cooling, lube oil system, "
            "dry gas seals, and anti-surge control. The station control system is fully automated "
            "with Siemens S7 PLC, remote SCADA interface, and emergency shutdown (ESD) logic "
            "compliant with IEC 61511. The entire facility is housed within a weather-proof "
            "acoustic enclosure meeting ISO 15664 noise requirements. Fully skidded and modular "
            "for rapid site installation within 4 weeks. Current API 670/671 compliance "
            "certificates available."
        ),
    },
    {
        "name": "Heavy Lift Offshore Crane — 800T Capacity",
        "category": "offshore",
        "static_image": "Heavy_Lift_Offshore_Crane.jpg",
        "daily_rate": "185000.00",
        "capacity": "800 Tonnes / 80m Boom",
        "location": "Aberdeen, Scotland, UK",
        "status": "available",
        "featured": False,
        "description": (
            "ABS-classed heavy lift offshore crane with an 800-tonne main hook load capacity "
            "and 80-metre fully extended boom length. Designed specifically for subsea module "
            "installation, deck module replacements, and pipe lay support operations in up to "
            "Hs 3.5m sea states. The crane features Active Heave Compensation (AHC) rated for "
            "1,200 tonnes, allowing deepwater lifts at up to 3,000 metres depth with precision "
            "control in dynamic conditions.\n\n"
            "Secondary hook load is 100 tonnes on a 120-metre whip line. The crane slew ring "
            "allows 360° rotation with hydraulic brakes on all axes. Control station is climate "
            "controlled with full CCTV monitoring of the hook and load. The crane is permanently "
            "installed on a semi-submersible crane vessel (SSCV) and comes with a full offshore "
            "rigging package including certified slings, shackles, and lift frames. Lift "
            "planning services and marine warranty surveyor (MWS) approval support included."
        ),
    },
    {
        "name": "LNG Carrier Vessel — 140,000 m³ Moss Sphere",
        "category": "tanker",
        "static_image": "LNG_Carrier_Vessel.jpg",
        "daily_rate": "165000.00",
        "capacity": "140,000 m³ LNG",
        "location": "Port of Yokohama, Japan",
        "status": "available",
        "featured": False,
        "description": (
            "Liquefied Natural Gas (LNG) carrier featuring four Moss Rosenberg spherical tanks "
            "with a combined cargo capacity of 140,000 cubic metres. The vessel is designed to "
            "maintain LNG at -163°C using a closed-loop nitrogen refrigeration system with BOG "
            "(boil-off gas) reliquefaction. The Moss-type insulated spherical tanks provide "
            "excellent structural integrity in both full and partial load conditions.\n\n"
            "Propulsion is provided by a dual-fuel diesel electric system consuming LNG boil-off "
            "gas as primary fuel, achieving 19.5 knots service speed with a 28,000nm range. "
            "The vessel holds Ice Class 1C notation for Baltic operations. Reliquefaction "
            "capacity of 3.0 tonne/hour eliminates commercial BOG losses. Full safety systems "
            "include inert gas generators, gas detection throughout cargo spaces, and Type-C "
            "fire and gas suppression. Delivery available from Yokohama or Singapore on a "
            "time-charter basis. Class DNV GL, all certificates current."
        ),
    },
    {
        "name": "Pipeline Excavator — CAT 395 95T",
        "category": "industrial",
        "static_image": "Pipeline_Excavator.jpg",
        "daily_rate": "5800.00",
        "capacity": "95T Machine / 8.5m Reach",
        "location": "Calgary, Alberta, Canada",
        "status": "available",
        "featured": False,
        "description": (
            "Caterpillar 395 large hydraulic excavator, 95-tonne operating weight class, "
            "purpose-configured for pipeline installation and trenching operations. Equipped "
            "with a 60-inch hydraulic side-boom attachment and a 7.8m stick reaching 8.5m "
            "maximum ground-level reach, this machine can handle 42-inch pipeline lowering "
            "operations in a single pass. The Trimble Grade Control system enables GPS-guided "
            "trenching to ±25mm accuracy, reducing survey costs and rework.\n\n"
            "Engine output is 430kW (576HP) running on Stage V emission-compliant diesel. "
            "The machine includes an integrated high-pressure hydraulic circuit for attachment "
            "versatility including clamshell buckets, vibratory plate compactors, and hydraulic "
            "hammers. Remote monitoring via Cat Product Link tracks fuel consumption, working "
            "hours, and maintenance intervals in real time. Full operating crew (operator + "
            "signaller) and site supervisor available with rental. Transport on low-loader "
            "included for moves up to 200km."
        ),
    },
    {
        "name": "Offshore Platform Supply Vessel (PSV) — DP2",
        "category": "offshore",
        "static_image": "Offshore_Platform_Supply_Vessel.jpg",
        "daily_rate": "28500.00",
        "capacity": "4,500 DWT / 1,800m² Deck",
        "location": "Bergen, Norway",
        "status": "available",
        "featured": False,
        "description": (
            "Platform Supply Vessel (PSV) with 4,500 DWT deadweight tonnage and a 1,800 square "
            "metre open deck for bulk cargo, pipe, and module transport. Rated for DP2 dynamic "
            "positioning operations alongside offshore installations in the North Sea and "
            "Barents Sea. The vessel operates on a combined diesel-electric and LNG dual-fuel "
            "propulsion system, achieving a 40% reduction in CO₂ emissions versus conventional "
            "diesel vessels.\n\n"
            "Liquid mud capacity: 1,800 m³ in 6 tanks. Dry bulk: 400 m³ in 8 silos. Potable "
            "water: 500 m³. Fuel oil: 800 m³. The vessel carries full cargo handling equipment "
            "including a 3-tonne ship's crane, forklift, and container lashing gear. ERRV "
            "(emergency response and rescue vessel) notation allows 150-person rescue operations. "
            "Crew of 15 officers and ratings, with 12 spare berths for offshore technicians. "
            "Available on spot or period charter. Class LR, ISM/ISPS certified."
        ),
    },
    {
        "name": "Christmas Tree Wellhead Assembly — 5,000 PSI",
        "category": "drilling",
        "static_image": "Christmas_Tree_Wellhead_Assembly.jpg",
        "daily_rate": "4200.00",
        "capacity": "5,000 PSI WP / 4-1/16\" Bore",
        "location": "Houston, TX, USA",
        "status": "available",
        "featured": False,
        "description": (
            "API 6A compliant wellhead and Christmas tree assembly rated to 5,000 PSI working "
            "pressure with a 4-1/16 inch bore. Manufactured from 60K yield strength carbon "
            "steel with Inconel-clad bore and sealing faces for H₂S service (NACE MR0175). "
            "The assembly includes a casing spool, tubing head spool, master gate valve, swab "
            "valve, two wing valves, and choke manifold — all hydraulically actuated for "
            "remote operation from the surface control panel.\n\n"
            "The tree is rated for 121°C (250°F) maximum operating temperature and H₂S partial "
            "pressure up to 340 kPa (PR1 service). All valves are API 6D full-bore ball valves "
            "with fire-safe design. The hydraulic control unit (HCU) provides fail-safe closure "
            "on loss of hydraulic pressure. Pressure test certificates and material test reports "
            "(MTRs) provided. Suitable for vertical, deviated, and horizontal onshore wells. "
            "Installation crew and pressure testing equipment available."
        ),
    },
    {
        "name": "3-Phase Gas-Oil Separator — 15,000 BPD",
        "category": "industrial",
        "static_image": "3-Phase_Gas-Oil_Separator.jpg",
        "daily_rate": "22000.00",
        "capacity": "15,000 BPD / ASME VIII Rated",
        "location": "Muscat, Oman",
        "status": "available",
        "featured": False,
        "description": (
            "Horizontal three-phase gas-oil-water separator vessel rated at 15,000 barrels per "
            "day liquid throughput. Designed to API 12J and ASME Section VIII Division 1 code, "
            "the vessel operates at 600 PSI working pressure and 120°C design temperature, "
            "suitable for sour service (NACE MR0175) with H₂S up to 500 ppm.\n\n"
            "Internal configuration includes a primary inlet cyclone diverter, secondary "
            "gravity settling compartment, weir with adjustable liquid level controllers, and "
            "a demister mist eliminator pad. Instrumentation includes pressure safety valves, "
            "level gauges, temperature transmitters, and control valves all linked to a local "
            "control panel with 4–20mA HART outputs. The separator package is fully skidded "
            "on a structural steel base with access platforms, handrails, and ladders. Utility "
            "connections include fuel gas, instrument air, drain, and vent. Full dimensional "
            "datasheet and PFD/P&ID available. Delivery within 6 weeks from Oman yard."
        ),
    },
    {
        "name": "Hydraulic Fracturing Fleet — 15,000 PSI Tier 4",
        "category": "drilling",
        "static_image": "Hydraulic_Fracturing_Fleet.jpg",
        "daily_rate": "310000.00",
        "capacity": "1,500HP Per Unit / 15,000 PSI",
        "location": "Midland, TX, USA",
        "status": "available",
        "featured": False,
        "description": (
            "Comprehensive hydraulic fracturing (frac) fleet comprising 12 Tier 4 final "
            "emission-compliant pump trucks, each delivering 1,500 hydraulic horsepower at "
            "up to 15,000 PSI wellhead treating pressure. The fleet is configured for "
            "simultaneous zipper fracturing on multi-well pad sites, with total fleet "
            "capacity of 18,000 HHP. Pump trucks run on dual-fuel (diesel/CNG) for "
            "significant operational cost savings versus diesel-only fleets.\n\n"
            "Supporting equipment includes a 600-barrel blender unit, 8-unit chemical "
            "additive system, data acquisition van with real-time fracture pressure and "
            "rate monitoring, and a 500-barrel proppant storage silo system. Fleet "
            "management software provides job execution monitoring, pressure, rate, "
            "proppant concentration, and density logging in real time. Experienced "
            "frac crew of 18 personnel included. Full wellsite safety management system "
            "(SMS) compliance with ISNetworld and PEC Premier certifications. "
            "Available for unconventional oil/gas, geothermal, and CCUS applications."
        ),
    },
    {
        "name": "Subsea ROV — Work Class 3,000m",
        "category": "offshore",
        "static_image": "Subsea_ROV.jpg",
        "daily_rate": "95000.00",
        "capacity": "3,000m Rated / 150HP / 7-Function Manipulator",
        "location": "Singapore",
        "status": "available",
        "featured": False,
        "description": (
            "Work-class remotely operated vehicle (ROV) rated to 3,000 metres water depth, "
            "delivering 150 hydraulic horsepower for heavy intervention tasks. Equipped with "
            "two 7-function manipulator arms — one force-feedback master-slave arm and one "
            "high-power torque arm capable of 1,200 Nm — enabling complex subsea assembly, "
            "valve operations, and emergency intervention tasks. Vehicle dimensions: "
            "3.2m L × 1.8m W × 1.6m H; weight in air 3,200 kg.\n\n"
            "Navigation and survey payload includes a Doppler velocity log (DVL), high-resolution "
            "sonar, colour and black-and-white cameras (HD low-light), CP probes, and an "
            "inclinometer / heading reference unit. The surface support system includes a "
            "150kVA umbilical power management unit, integrated launch and recovery system "
            "(LARS) rated for Hs 3.0m, and a dedicated HPU. Full subsea tooling package "
            "available (hot stab tools, torque tools, grippers, water jetting, cutting tools). "
            "IMCA R004 compliant ROV crew of 4 included. Deployable from any vessel of opportunity."
        ),
    },
    {
        "name": "Single Point Mooring Buoy System (CALM)",
        "category": "offshore",
        "static_image": "Single_Point_Mooring_Buoy_System.jpg",
        "daily_rate": "68000.00",
        "capacity": "300,000 DWT VLCC Compatible",
        "location": "Gulf of Guinea, West Africa",
        "status": "available",
        "featured": False,
        "description": (
            "Catenary Anchor Leg Mooring (CALM) single point mooring (SPM) buoy system "
            "designed for the loading and offloading of VLCC tankers up to 300,000 DWT in "
            "offshore locations without port infrastructure. The 13-metre diameter steel buoy "
            "provides a stable mooring point via a 4-leg catenary anchor chain system, each "
            "leg comprising 120-metre sections of 132mm Grade R4S studless chain.\n\n"
            "The buoy houses a hydraulic swivel stack allowing the tanker to weathervane "
            "freely while maintaining continuous crude oil flow at 12,000 m³/hour through "
            "a 20-inch swivel and submarine hose system (flexible risers to 60 bar). The "
            "hose string is 230 metres long with an integrated emergency release coupling "
            "(ERC) for safe disconnection under emergency conditions. Telemetry and SCADA "
            "monitoring of buoy position, mooring tensions, and oil flow are transmitted "
            "via satellite to the onshore terminal. Full installation, commissioning, and "
            "marine warranty survey support included in the rental package."
        ),
    },
]


class Command(BaseCommand):
    help = 'Seeds 20 oil & gas equipment items with full descriptions and static images'

    def handle(self, *args, **kwargs):
        created = 0
        updated = 0

        for item in EQUIPMENT_DATA:
            obj, was_created = Equipment.objects.update_or_create(
                name=item['name'],
                defaults={
                    'category':     item['category'],
                    'static_image': item['static_image'],
                    'daily_rate':   item['daily_rate'],
                    'capacity':     item['capacity'],
                    'location':     item['location'],
                    'status':       item['status'],
                    'featured':     item['featured'],
                    'description':  item['description'],
                    'image_url':    '',
                }
            )
            if was_created:
                created += 1
                self.stdout.write(f'  ✅ Created: {obj.name}')
            else:
                updated += 1
                self.stdout.write(f'  🔄 Updated: {obj.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done! {created} created, {updated} updated. Total: {created+updated} equipment items.'
        ))
