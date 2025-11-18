#!/usr/bin/env python3
"""
Batch processing script for scraping and embedding multiple celebrities.
Runs Stage 1 (scraping) and Stage 2 (embedding) for each person in sequence.
"""

import subprocess
import sys
from pathlib import Path

# List of celebrities to process (remaining 75)
CELEBRITIES = [
    "Warren Buffett",
    "Mark Cuban",
    "Larry Ellison",
    "Indra Nooyi",
    "Reed Hastings",
    "Travis Kalanick",
    "Andrew Carnegie",
    "John D. Rockefeller",
    "Henry Ford",
    "Sheryl Sandberg",
    "Sophia Amoruso",
    "George Lucas",
    "Dwayne Johnson",
    "Jennifer Lopez",
    "Simon Cowell",
    "Dick Van Dyke",
    "Charlize Theron",
    "Halle Berry",
    "Shonda Rhimes",
    "Lin-Manuel Miranda",
    "Cristiano Ronaldo",
    "Usain Bolt",
    "Pelé",
    "Lance Armstrong",
    "Bethany Hamilton",
    "Jackie Robinson",
    "Magic Johnson",
    "Tiger Woods",
    "Lindsey Vonn",
    "Wilma Rudolph",
    "Nikola Tesla",
    "Thomas Edison",
    "Grace Hopper",
    "Katherine Johnson",
    "Bill Gates",
    "Steve Wozniak",
    "Ada Lovelace",
    "Carl Sagan",
    "Jane Goodall",
    "Alan Turing",
    "Winston Churchill",
    "Franklin D. Roosevelt",
    "Eleanor Roosevelt",
    "John Lewis",
    "Harriet Tubman",
    "Cesar Chavez",
    "Rosa Parks",
    "Harvey Milk",
    "Alexandria Ocasio-Cortez",
    "Greta Thunberg",
    "Desmond Tutu",
    "Mahatma Gandhi",
    "Ernest Hemingway",
    "Virginia Woolf",
    "Georgia O'Keeffe",
    "Pablo Picasso",
    "Harper Lee",
    "Charles Dickens",
    "Mark Twain",
    "Emily Dickinson",
    "Oscar Wilde",
    "Sylvia Plath",
    "Joan Didion",
    "David Bowie",
    "Prince",
    "Mother Teresa",
    "Dalai Lama",
    "Viktor Frankl",
    "Elie Wiesel",
    "Anne Frank",
    "Wangari Maathai",
    "Erin Brockovich",
    "Rigoberta Menchú",
    "Aung San Suu Kyi",
    "Ai Weiwei",
]

def run_command(cmd: list[str], description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")

    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            capture_output=False  # Show output in real-time
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR: Command failed with exit code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


def main():
    """Process all celebrities in sequence."""

    print("="*80)
    print("BATCH PROCESSING: Scraping & Embedding Celebrities")
    print("="*80)
    print(f"Total celebrities: {len(CELEBRITIES)}")
    print(f"Celebrities: {', '.join(CELEBRITIES)}")
    print("="*80)

    results = {
        "success": [],
        "failed": []
    }

    for i, person in enumerate(CELEBRITIES, 1):
        print(f"\n\n{'#'*80}")
        print(f"# [{i}/{len(CELEBRITIES)}] Processing: {person}")
        print(f"{'#'*80}\n")

        # Stage 1: Scraping
        stage1_success = run_command(
            ["python", "stage1_scrape.py", person],
            f"[Stage 1] Scraping {person}"
        )

        if not stage1_success:
            print(f"\n❌ Failed to scrape {person}. Skipping to next person.")
            results["failed"].append(person)
            continue

        # Stage 2: Embedding
        stage2_success = run_command(
            ["python", "stage2_embed.py", person],
            f"[Stage 2] Embedding {person}"
        )

        if not stage2_success:
            print(f"\n❌ Failed to embed {person}.")
            results["failed"].append(person)
            continue

        results["success"].append(person)
        print(f"\n✓ Successfully processed {person}")

    # Print summary
    print("\n\n" + "="*80)
    print("BATCH PROCESSING COMPLETE")
    print("="*80)
    print(f"✓ Successful: {len(results['success'])}/{len(CELEBRITIES)}")
    if results["success"]:
        for person in results["success"]:
            print(f"  - {person}")

    if results["failed"]:
        print(f"\n❌ Failed: {len(results['failed'])}/{len(CELEBRITIES)}")
        for person in results["failed"]:
            print(f"  - {person}")

    print("\n" + "="*80)
    print("Next: Query the database with Stage 3")
    print('      python stage3_query.py "your experience here"')
    print("="*80)

    # Exit with error code if any failed
    if results["failed"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
