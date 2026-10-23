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
| AI Assistant | Voice assistant (2011), Chat assistant (2022), Personal agent (2026) |
| Image Generator | Photo filter app (2016), Text-to-image (2022), Text-to-video (2024) |
| Coding Assistant | Smart autocomplete (2018), AI pair programmer (2021), Coding agent (2025) |
| Self-Driving Software | Driver assistance (2008), Robotaxi (2020) |
| Social App | Social network (2004), Photo sharing (2010), Short video (2016) |
| Messaging App | Instant messenger (1996), Mobile messenger (2009) |
| Mobile Wallet | Mobile banking (2009), Tap to pay (2014) |
| Fitness App | Step tracker (2009), Health coach (2018) |

### Hardware products (designed, manufactured and sold by your company)
| Type | Categories (unlock year) |
|---|---|
| Graphics Card | 3D accelerator (1996), Gaming GPU (2000), AI accelerator (2017) |
| Processor | Desktop CPU (1982), Server CPU (1995), Mobile chip (2007) |

Both have their own 3D product designs.

### Office computers (ModernTech PCs)
| Furniture | Unlock | Speed vs. normal PC | Power use |
|---|---|---|---|
| Mini PC | 2010 | 90% | 300 W |
| Ultrabook | 2012 | 90% | 200 W |
| Workstation Tower | 2012 | 115% | 1000 W |
| AI Workstation | 2023 | 140% | 1800 W |

The case, accent and light colors can be changed in-game. They upgrade like the vanilla computers.

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
