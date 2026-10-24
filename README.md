# ModernTech

A modern-technology content pack for **Software Inc.**: AI software, phone apps, graphics cards and processors, modern office PCs, and new employee personalities. Every new market has competitors and realistic unlock years.

Workshop-compatible: TyD data, OBJ models, and one optional `.cs` script that the game compiles itself. No DLLs, no Harmony.

## What's in the box

The game loads data, furniture and code mods from different folders, so ModernTech comes in three parts:

| Part | Folder in this repo | Goes in the game's... | Needed? |
|---|---|---|---|
| **ModernTech** (data) | this folder | `Mods/ModernTech` | Yes |
| **ModernTech PCs** (furniture) | `extras/Furniture/ModernTech PCs` | `Furniture/ModernTech PCs` | Optional |
| **ModernTech Demand** (code: growing demand, AI speed boost, double skills) | `extras/DLLMods/ModernTechDemand` | `DLLMods/ModernTechDemand` | Optional |

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
Coding Assistant and Image Generator can be made **in-house**, and they work as tools, the way vanilla games use a 2D Editor:
- In every other ModernTech product, the code group (System spec) uses a Coding Assistant and the art group (2D spec) uses an Image Generator.
- These groups are optional. When you design a product, add the group and pick your own AI as its tool, or license a competitor's.
- The tool's tech level caps how advanced the features in that group can be, so a better AI lets your team build better products. Your own tool costs no license.
- Until anyone has released an AI tool, those groups can't be added, but the product can still be developed without them.

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

### Industrial printer tiers
Ten more product printers, each with more capacity than the last. They all share the Industrial Product Printer model and differ by colour, price and throughput.

| Printer | Unlock | Copies per load | Print speed | Cost |
|---|---|---|---|---|
| Industrial Printer Mk II | 2010 | 4,000 | 2x | 15,000 |
| Industrial Printer Mk III | 2011 | 5,500 | 2.5x | 27,000 |
| Industrial Printer Mk IV | 2012 | 7,000 | 3x | 39,000 |
| Industrial Printer Mk V | 2013 | 8,500 | 3.5x | 51,000 |
| Industrial Printer Mk VI | 2014 | 10,000 | 4x | 63,000 |
| Industrial Printer Mk VII | 2015 | 11,500 | 4.5x | 75,000 |
| Industrial Printer Mk VIII | 2016 | 13,000 | 5x | 87,000 |
| Industrial Printer Mk IX | 2017 | 14,500 | 5.5x | 99,000 |
| Industrial Printer Mk X | 2018 | 16,000 | 6x | 111,000 |
| Industrial Printer Mk XI | 2019 | 17,500 | 6.5x | 123,000 |

### Personalities
- **Gadgeteer**: RGB Thumb + Forgetful
- **Nocturnal**: Night owl

### Your own AI doubles your team's speed (ModernTech Demand code mod)
Once your company has released any of its own AI products — an **AI Assistant, Coding Assistant or Image Generator**, in-house or for sale — your employees use them and designing and developing software goes **100% faster** (twice as fast). Every category counts, from voice assistants and photo filters to smart autocomplete and coding agents.

**It's an option:** press **Ctrl+Alt+A** in game to switch the boost on or off. The choice is remembered, so it survives saving, loading and starting a new game. The first time it kicks in, the game shows a one-time message explaining the key.

The code mod does this by doubling the difficulty's design and development speed while the boost is on, and the difficulty name shows it, for example "Medium +AI". Because the boosted difficulty is what gets saved, loading a game never doubles the speed twice. The game caps furniture auras at +25%, so this needs the code mod.

### Double skills (ModernTech Demand code mod)
Every employee's skills are doubled once, up to the game's 100% cap, when they join your company or when you first load a game with the code mod. The save remembers who was doubled, so loading a game never doubles anyone twice. Skills already at 50% or more go to 100%.

### Growing demand (ModernTech Demand)
Without the code mod, every market has fixed demand. With it, each new category starts at 25% of its full demand and grows to 100% over 3 to 12 years.

## For modders
- The code mods are plain `.cs` files the game compiles itself. Bind the debug console in Options > Keys, then use `RECOMPILE_DLL_MOD` and `RELOAD_DLL_MOD` to try a change without restarting the game.
- The game's script compiler references `Assembly-CSharp` and Unity's core modules only. The IMGUI types (`GUI`, `GUIStyle`, `TextAnchor`, `GUI.skin`) are **not** available and using them fails the whole code mod with `CS246`, so draw nothing yourself: use `WindowManager.Instance.ShowMessageBox(...)` or `Debug.Log` for feedback.
- Data and furniture packages are picked up from `Mods/` and `Furniture/` as soon as they are there. Code mods also need `<DLLMods>\<folder name>Setting.txt` containing `[Active]` then `True`, or they load but never activate.
- A furniture TyD component node **replaces** the one inherited from its `Base` instead of merging into it. Any enum field you don't restate falls back to its default, not the base's value: `ProductPrinter` without `Type` is a *product* printer, so a component fab must say `Type Component` explicitly.
- `python3 tools/check_tyd.py` checks every TyD file for broken brackets and bad references.
- `tools/build_models.ps1` (Windows) or `blender -b -P tools/build_models.py` rebuilds every model, texture, thumbnail and Workshop preview. The committed assets were built with **Blender 5.2.2 LTS**; the script strips Blender's PNG timestamp metadata, so a rebuild is byte-for-byte identical and shows no diff unless a model really changed.
- `tools/package.ps1` (Windows) or `tools/package.sh` (Linux/macOS) builds clean, upload-ready copies of all three packages in `dist/`, after validating the TyD files and rejecting any file the Workshop uploader would refuse.
- `.gitattributes` keeps Blender's LF models from being converted to CRLF, so rebuilding never produces phantom changes.

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
