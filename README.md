# ModernTech

A modern-technology content pack for **Software Inc.**: AI software, phone apps, graphics cards and processors, modern office PCs, and new employee personalities. Every new market has competitors and realistic unlock years.

Workshop-compatible: TyD data, OBJ models, and one optional `.cs` script that the game compiles itself. No DLLs, no Harmony.

## What's in the box

The game loads data, furniture and code mods from different folders, so ModernTech comes in three parts:

| Part | Folder in this repo | Goes in the game's... | Needed? |
|---|---|---|---|
| **ModernTech** (data) | this folder | `Mods/ModernTech` | Yes |
| **ModernTech PCs** (furniture) | `extras/Furniture/ModernTech PCs` | `Furniture/ModernTech PCs` | Optional |
| **ModernTech Demand** (code) | `extras/DLLMods/ModernTechDemand` | `DLLMods/ModernTechDemand` | Optional |

## Install

1. Copy this folder to `<Steam>/steamapps/common/Software Inc/Mods/ModernTech`.
2. Optional: copy (or symlink) the two `extras` folders into the game's `Furniture` and `DLLMods` folders, as shown in the table above. On Linux:
   ```sh
   cd "<Steam>/steamapps/common/Software Inc"
   mkdir -p DLLMods
   ln -s "$PWD/Mods/ModernTech/extras/Furniture/ModernTech PCs" "Furniture/ModernTech PCs"
   ln -s "$PWD/Mods/ModernTech/extras/DLLMods/ModernTechDemand" DLLMods/ModernTechDemand
   ```
3. Start the game, open **Options > Mods** and enable the parts you want. The game asks you to read and approve the `.cs` code mod the first time.
4. Start a **new** game. New software types don't appear in old saves.

## Features

### Software (with AI competitors)
| Type | Categories (unlock year) |
|---|---|
| AI Assistant | Voice assistant (2010), Chat assistant (2010), Personal agent (2010) |
| Image Generator | Photo filter app (2010), Text-to-image (2010), Text-to-video (2010) |
| Coding Assistant | Smart autocomplete (2010), AI pair programmer (2010), Coding agent (2010) |
| Self-Driving Software | Driver assistance (2008), Robotaxi (2010) |
| Social App | Social network (2004), Photo sharing (2010), Short video (2010) |
| Messaging App | Instant messenger (1996), Mobile messenger (2009) |
| Mobile Wallet | Mobile banking (2009), Tap to pay (2010) |
| Fitness App | Step tracker (2009), Health coach (2010) |
| Cloud Storage | Object storage (2006), File sync (2007), Team drive (2010) |
| Video Streaming | Video on demand (2007), Live streaming (2010), Short video (2010) |
| Smart Home Hub | Home automation (2010), Home security (2010), Energy manager (2010) |

Every product has 3 to 4 feature groups. Everything ModernTech adds is available by 2010 at the latest. Two new company types, **Cloud services** and **Smart devices**, compete in the new markets.

### Build your own AI tools
Coding Assistant and Image Generator can be made **in-house**. Code-heavy feature groups (System) in ModernTech products list the Coding Assistant as a tool, and art-heavy groups (2D) list the Image Generator, the same way vanilla games use a 2D Editor. Make your own, then pick it as the tool when you design a product. Your teams get its help, and you pay no license to a competitor.

### Hardware products (designed, manufactured and sold by your company)
| Type | Categories (unlock year) |
|---|---|
| Graphics Card | 3D accelerator (1996), Gaming GPU (2000), AI accelerator (2010) |
| Processor | Desktop CPU (1982), Server CPU (1995), Mobile chip (2007) |
| VR Headset | PC VR headset (2010), Standalone headset (2010), Mixed reality headset (2010) |
| Smartwatch | Fitness band (2009), Smart watch (2010), Health watch (2010) |

Each has its own 3D product design.

### Office computers (ModernTech PCs)
| Furniture | Unlock | Speed vs. normal PC | Power use |
|---|---|---|---|
| Mini PC | 2010 | 90% | 300 W |
| Ultrabook | 2010 | 90% | 200 W |
| Workstation Tower | 2010 | 115% | 1000 W |
| AI Workstation | 2010 | 140% | 1800 W |
| VR Dev Station | 2010 | 120% | 900 W |
| Ultrawide Workstation | 2010 | 120% | 600 W |

The case, accent and light colors can be changed in-game. They upgrade like the vanilla computers.

### More furniture (same package)
| Furniture | Unlock | What it does |
|---|---|---|
| AI Assistant Panel | 2010 | Wall screen. Everyone in the room gets +15% effectiveness, +10% skill and +5% mood |
| Blade Server Rack | 2008 | Server Rack footprint, 3x the power (15,000) |
| AI Server Cluster | 2010 | Big Server Rack footprint, 3x the power (150,000) |
| Industrial Product Printer | 2010 | 2x the speed of a Large Product Printer, 2x per load, cheaper copies |
| Rapid Component Fab | 2010 | 2x the speed of a Component Printer, cheaper |
| Smart Fridge, Induction Stove, Bean-to-Cup Machine, Smart Vending Machine | 2010 | Kitchen: work like the vanilla Fridge, Stove, Espresso Machine and Vending Machine |
| Heat Pump Heater, Power Wall, Smart Vent | 2010 | Utility: work like the vanilla Small Heater, Battery and Ventilation |

### Personalities
- **Gadgeteer**: RGB Thumb + Forgetful
- **Nocturnal**: Night owl

### Growing demand (ModernTech Demand)
Without the code mod, every market has fixed demand. With it, each new category starts at 25% of its full demand and grows to 100% over 3 to 12 years.

## For modders
- `python3 tools/check_tyd.py` checks every TyD file for broken brackets and bad references.
- `blender -b -P tools/build_models.py` rebuilds every model, texture, thumbnail and Workshop preview.
- `tools/package.sh` builds clean, upload-ready copies of all three packages in `dist/`.

## Publishing to the Steam Workshop
The in-game uploader sends a mod's **whole folder**, so upload the clean copies from `dist/`, not this development folder.

1. Run `tools/package.sh`.
2. Put the `dist/` copies where the game looks for them, replacing the development versions for now:
   - `dist/ModernTech` → `Mods/ModernTech` (move this repo folder somewhere else first)
   - `dist/ModernTech PCs` → `Furniture/ModernTech PCs`
   - `dist/ModernTechDemand` → `DLLMods/ModernTechDemand`
3. In the game, open **Options > Mods**, pick each package and press upload.
4. The game writes the new Workshop ID (`SteamID`) into each package's `meta.tyd`. Copy those `meta.tyd` files back into the repo and commit them, so future uploads update the same Workshop page. The code mod gets a new `meta.tyd`; keep it next to `ModernTechDemand.cs` in `extras/DLLMods/ModernTechDemand`.
5. Put the development folders back.

## License
- **Code** (`tools/` and every `.cs` file): MIT
- **Everything else** (data, models, textures, images, text): CC BY 4.0. Reuse it freely, as long as you credit "ModernTech by erisparreshi369-dev".

See [LICENSE](LICENSE). Software Inc. belongs to Coredumping, and no game files are included.
