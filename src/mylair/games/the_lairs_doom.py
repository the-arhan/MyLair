"""
The Lair's Doom Game for My Lair.

A replayable choice-based terminal adventure.
Navigate through the chambers of The Lair, manage your health and inventory,
make key decisions, and discover multiple unique endings!

Endings:
1. Master of the Lair (Restore the Doom Core and become the dungeon's protector)
2. The Great Escape (Safely vent the Core and escape with treasure)
3. Survivor's Luck (Narrowly flee through a hidden fissure)
4. Retreat & Regroup (Safely carried outside by ancient spirits if health is depleted)

Beginner Customization:
- Rooms, encounters, choices, and items are clearly structured below.
"""

from __future__ import annotations

import random
from typing import List, Set

from mylair.display import (
    NavigationAction,
    clear_screen,
    print_divider,
    print_header,
    prompt_input,
    style_text,
)

MAX_HEALTH = 3


def render_status_bar(health: int, inventory: List[str]) -> str:
    """Render a clean status bar showing current HP and inventory items."""
    hearts = "♥" * health + "░" * (MAX_HEALTH - health)
    items_str = ", ".join(inventory) if inventory else "Empty"
    return f"  Health: [{hearts}] ({health}/{MAX_HEALTH})  |  Inventory: [ {items_str} ]"


def play_the_lairs_doom(
    title_style: str = "slant",
    color_scheme: str = "neon_cyan",
    direct_mode: bool = False,
) -> bool:
    """
    Run an interactive adventure session of The Lair's Doom.

    Returns:
    - True to return to menu / shell cleanly
    - False if user chose to quit the program
    """
    clear_screen()
    print_header(title_style, color_scheme, subtitle="Adventure: The Lair's Doom")

    print(style_text("Welcome to The Lair's Doom!", color_scheme, color_type="accent", bold=True))
    print("An interactive story-driven dungeon crawl deep beneath the terminal.\n")
    print("Prologue:")
    print("  Deep within the ancient subterranean vaults of The Lair, the legendary")
    print("  Doom Core has begun an unstable countdown. Only a cunning explorer can")
    print("  navigate the chambers, gather vital relics, and resolve the doom.\n")
    print("Controls:")
    print("  Enter the number corresponding to your choice at each prompt.")
    print("  Enter 'b' to return to menu, 'q' to quit anytime.\n")
    print_divider(color_scheme)

    while True:
        # Game State
        health = 3
        inventory: List[str] = ["Torch"]
        visited: Set[str] = set()

        print(style_text("★ Your quest begins at the threshold of the underground halls... ★\n", color_scheme, color_type="accent"))

        # ======================================================================
        # SCENE 1: The Vestibule
        # ======================================================================
        while health > 0:
            print_divider(color_scheme)
            print(style_text("ROOM 1: THE VESTIBULE", color_scheme, color_type="accent", bold=True))
            print(render_status_bar(health, inventory))
            print_divider(color_scheme)
            print("You stand inside a vast vaulted stone entrance. Cool air whispers from the dark.")
            print("A stone gargoyle perches beside an archway, and ancient glyphs line the walls.\n")
            print("What do you do?")
            print("  1. Search the carved gargoyle alcove.")
            print("  2. Inspect the glowing wall glyphs.")
            print("  3. Proceed down the central corridor toward the Sunken Library.")

            while True:
                act = prompt_input("Select choice [1-3] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True
                choice = str(act).strip()
                if choice in ("1", "2", "3"):
                    break
                print(style_text("Please enter 1, 2, or 3.", color_scheme, color_type="warning"))

            print()
            if choice == "1":
                if "Brass Key" not in inventory:
                    inventory.append("Brass Key")
                    print(style_text("✨ You reach inside the gargoyle's pedestal and discover a heavy Brass Key!", color_scheme, color_type="success", bold=True))
                else:
                    print("You inspect the gargoyle again, but find only dust and cobwebs.")
            elif choice == "2":
                print(style_text("📜 You decipher the glyphs: 'Only the radiant Crystal Gem can pacify the Core.'", color_scheme, color_type="accent"))
            else:  # choice == "3"
                print("Holding your Torch high, you descend through the archway...")
                break

        # ======================================================================
        # SCENE 2: The Sunken Library
        # ======================================================================
        while health > 0:
            print_divider(color_scheme)
            print(style_text("ROOM 2: THE SUNKEN LIBRARY", color_scheme, color_type="accent", bold=True))
            print(render_status_bar(health, inventory))
            print_divider(color_scheme)
            print("Water drips from high arched ceilings into shallow pools around towering bookcases.")
            print("On a central marble pedestal rests an ironbound chest with a heavy brass padlock.")
            print("An ancient leatherbound codex lies open on a nearby stone lectern.\n")
            print("What do you do?")
            print("  1. Attempt to open the padlock on the chest.")
            print("  2. Read the ancient codex on the lectern.")
            print("  3. Drink fresh water from the glowing fountain basin.")
            print("  4. Press forward toward the subterranean Crystal Chasm.")

            while True:
                act = prompt_input("Select choice [1-4] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True
                choice = str(act).strip()
                if choice in ("1", "2", "3", "4"):
                    break
                print(style_text("Please enter 1, 2, 3, or 4.", color_scheme, color_type="warning"))

            print()
            if choice == "1":
                if "Brass Key" in inventory:
                    if "Crystal Gem" not in inventory:
                        inventory.append("Crystal Gem")
                        print(style_text("🔓 Click! The Brass Key opens the chest! Inside is a pulsing Crystal Gem!", color_scheme, color_type="success", bold=True))
                    else:
                        print("The chest is open and empty.")
                else:
                    print(style_text("🔒 The lock is solidly sealed. You need a key to open it without breaking it.", color_scheme, color_type="warning"))
            elif choice == "2":
                print(style_text("📖 The codex explains: 'Turn the release valves counter-clockwise in an emergency.'", color_scheme, color_type="accent"))
            elif choice == "3":
                if health < MAX_HEALTH:
                    health = min(MAX_HEALTH, health + 1)
                    print(style_text("💧 The enchanted spring water revitalizes you! (+1 HP restored)", color_scheme, color_type="success"))
                else:
                    print("You drink the cool water. You feel completely refreshed.")
            else:  # choice == "4"
                print("You leave the library behind, following the deep hum of subterranean machinery...")
                break

        # ======================================================================
        # SCENE 3: The Crystal Chasm
        # ======================================================================
        while health > 0:
            print_divider(color_scheme)
            print(style_text("ROOM 3: THE CRYSTAL CHASM", color_scheme, color_type="accent", bold=True))
            print(render_status_bar(health, inventory))
            print_divider(color_scheme)
            print("A colossal underground canyon spans before you. Luminescent crystals glow in the dark.")
            print("A narrow stone bridge spans the foggy chasm. Loose rubble litters the ledge.\n")
            print("What do you do?")
            print("  1. Carefully cross the narrow stone bridge.")
            print("  2. Search the crystal ledge for rare mineral formations.")
            print("  3. Throw a stone into the abyss to gauge its depth.")

            while True:
                act = prompt_input("Select choice [1-3] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True
                choice = str(act).strip()
                if choice in ("1", "2", "3"):
                    break
                print(style_text("Please enter 1, 2, or 3.", color_scheme, color_type="warning"))

            print()
            if choice == "1":
                print(style_text("You balance carefully and safely traverse the bridge to the other side!", color_scheme, color_type="success"))
                break
            elif choice == "2":
                if "Crystal Gem" not in inventory:
                    inventory.append("Crystal Gem")
                    print(style_text("💎 You chisel a radiant Crystal Gem from the cavern wall!", color_scheme, color_type="success", bold=True))
                else:
                    print("You gather a handful of harmless glowing crystal dust.")
            else:  # choice == "3"
                print("The stone echoes softly... A sudden rumble causes a loose pebble to strike your shoulder! (-1 HP)")
                health -= 1
                if health <= 0:
                    break

        # Check defeat
        if health <= 0:
            print_divider(color_scheme)
            print(style_text("☠ DEFEAT: Exhausted from your injuries, your vision fades...", color_scheme, color_type="error", bold=True))
            print("Fortunately, the gentle ancient spirits of the Lair rescue you and carry you")
            print("safely back to the surface. You may rest and challenge the Lair another time!")
        else:
            # ======================================================================
            # SCENE 4: The Chamber of Doom (The Core)
            # ======================================================================
            print_divider(color_scheme)
            print(style_text("ROOM 4: THE CHAMBER OF DOOM", color_scheme, color_type="accent", bold=True))
            print(render_status_bar(health, inventory))
            print_divider(color_scheme)
            print("You enter the heart of the Lair. Massive gears churn as the pulsing Doom Core")
            print("glows fiery crimson. A towering Clockwork Guardian stands guard before the control dais!\n")
            print("What is your decisive action?")
            print("  1. Place the radiant Crystal Gem into the Core's empty socket.")
            print("  2. Sprint to the coolant station and turn the emergency release valves.")
            print("  3. Brandish your Torch to distract the Guardian and escape through a fissure.")
            print("  4. Confront the Clockwork Guardian directly.")

            while True:
                act = prompt_input("Select choice [1-4] (b=back, q=quit): ", color_scheme=color_scheme, allow_back=True, allow_quit=True)
                if act == NavigationAction.QUIT:
                    return False
                if act == NavigationAction.BACK:
                    return True
                choice = str(act).strip()
                if choice in ("1", "2", "3", "4"):
                    break
                print(style_text("Please enter 1, 2, 3, or 4.", color_scheme, color_type="warning"))

            print()
            print_divider(color_scheme)

            if choice == "1":
                if "Crystal Gem" in inventory:
                    print(style_text("★ ENDING 1: MASTER OF THE LAIR (Flawless Victory) ★", color_scheme, color_type="success", bold=True))
                    print("You fit the Crystal Gem into the central socket. The fiery crimson glow transforms")
                    print("into a soothing, radiant blue luminescence. The rumbling calms into a peaceful hum.")
                    print("The Clockwork Guardian bows solemnly in reverence before you:")
                    print("  'Welcome home, Master of the Lair.'\n")
                    print("You have unlocked the secrets of the dungeon and saved the realm!")
                else:
                    print(style_text("✗ You reach to your satchel, but you don't possess a Crystal Gem!", color_scheme, color_type="error"))
                    print("The Guardian sweeps you back, and you must hastily retreat through an escape portal.")
                    print(style_text("★ ENDING 3: SURVIVOR'S LUCK ★", color_scheme, color_type="accent", bold=True))
                    print("You escape with your life, eager to explore the Lair again another day!")

            elif choice == "2":
                print(style_text("★ ENDING 2: THE GREAT ESCAPE ★", color_scheme, color_type="accent", bold=True))
                print("You sprint to the emergency valves and wrench them counter-clockwise!")
                print("Huge geysers of cool steam vent throughout the chamber, venting the pressure.")
                print("You grab a handful of ancient silver relics and sprint out the secret escape passage")
                print("just as the vault doors seal safely behind you!")

            elif choice == "3":
                print(style_text("★ ENDING 3: SURVIVOR'S LUCK ★", color_scheme, color_type="accent", bold=True))
                print("You wave your bright Torch, dazzling the Guardian's optical sensors!")
                print("Slipping beneath its arm, you dive through a narrow crack in the wall,")
                print("sliding down a chute that leads out into the sunlit mountain glade.")
                print("You survived to explore another day!")

            else:  # choice == "4"
                if health >= 2:
                    print(style_text("★ ENDING 2: THE GREAT ESCAPE (Warrior's Triumph) ★", color_scheme, color_type="accent", bold=True))
                    print("With quick reflexes, you dodge the Guardian's mechanical hammer and wedge your")
                    print("torch between its drive gears, seizing the emergency lever and neutralizing the Doom!")
                    print("You walk out victorious with your head held high.")
                else:
                    print(style_text("☠ The Guardian's blow is too fierce for your weakened health!", color_scheme, color_type="error"))
                    print("You are knocked unconscious, but wake up safely outside by the entrance spring.")

        print_divider(color_scheme)

        # Replay prompt
        replay_prompt = "Embark on another adventure in The Lair? [y/n] (b=back, q=quit): "
        replay_act = prompt_input(replay_prompt, color_scheme=color_scheme, allow_back=True, allow_quit=True)

        if replay_act == NavigationAction.QUIT:
            return False
        if replay_act == NavigationAction.BACK:
            return True

        if str(replay_act).strip().lower() not in ("y", "yes"):
            print(style_text("\nFarewell, noble explorer! Until your next quest.\n", color_scheme, color_type="accent"))
            return True

        clear_screen()
        print_header(title_style, color_scheme, subtitle="Adventure: The Lair's Doom")
