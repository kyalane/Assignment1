import random
import string
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Small built-in word list for memorable passwords
WORDS = [
    'apple','orange','banana','grape','peach','pear','plum','mango','kiwi','lemon',
    'cherry','berry','melon','apricot','avocado','pineapple','coconut','fig','date',
    'lime','papaya','guava','nectarine','persimmon','olive','pomegranate','dragon',
    'radish','carrot','pepper','onion','garlic','lettuce','spinach','kale','cabbage',
    'potato','tomato','cucumber','zucchini','pumpkin','squash','bean','pea','corn',
    'wheat','rice','oat','barley','rye','quinoa','almond','cashew','walnut','peanut',
    'butter','cheese','yogurt','milk','cream','honey','sugar','salt','pepper','herb',
    'sage','rosemary','thyme','basil','mint','parsley','cilantro','dill','chive','oregano',
    'river','mountain','valley','forest','desert','island','ocean','lake','stream','canyon',
    'cloud','sky','star','moon','sun','comet','planet','meteor','galaxy','orbit',
    'river','stone','rock','pebble','cliff','beach','sand','shore','dune','reef',
    'echo','whisper','shadow','light','flame','ember','spark','breeze','gale','storm',
    'aurora','mist','fog','rain','snow','hail','frost','glacier','ice','wave'
]

class PasswordGenerator:
    def __init__(self, base_dir: Optional[Path] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent

    def _timestamp(self) -> str:
        return datetime.now().strftime("%A, %B %d %Y %H:%M:%S")

    def _ensure_dir(self, name: str) -> Path:
        p = self.base_dir / name
        p.mkdir(parents=True, exist_ok=True)
        return p

    def _append_log(self, kind: str, password: str) -> None:
        dir_name = 'Memorable' if kind == 'memorable' else 'Random'
        d = self._ensure_dir(dir_name)
        f = d / 'Generated_Passwords.txt'
        with f.open('a', encoding='utf-8') as fh:
            fh.write(f"{self._timestamp()} - {password}\n")

    def generate_memorable(self, num_words: int = 4, cases: Optional[List[str]] = None) -> str:
        """
        Generate a memorable password composed of `num_words` words.
        Each word has a random 1-digit number appended and words are joined with hyphens.
        `cases` is a list of case options to choose for each word: 'lower','upper','title'.
        """
        if cases is None:
            cases = ['lower', 'title', 'upper']
        chosen = []
        for _ in range(num_words):
            w = random.choice(WORDS)
            case = random.choice(cases)
            if case == 'lower':
                w2 = w.lower()
            elif case == 'upper':
                w2 = w.upper()
            elif case == 'title':
                w2 = w.title()
            else:
                w2 = w
            w2 = f"{w2}{random.randint(0,9)}"
            chosen.append(w2)
        password = '-'.join(chosen)
        self._append_log('memorable', password)
        return password

    def generate_random(self, length: int = 12, include_punct: bool = True, disallowed: str = '') -> str:
        """
        Generate a random password of given `length` using lowercase, uppercase, digits,
        and optionally punctuation. Characters in `disallowed` will be excluded from the pool.
        """
        pool = list(string.ascii_lowercase + string.ascii_uppercase + string.digits)
        if include_punct:
            pool += list(string.punctuation)
        if disallowed:
            pool = [c for c in pool if c not in disallowed]
        if not pool:
            raise ValueError('No characters left to build password after applying disallowed set.')
        password = ''.join(random.choice(pool) for _ in range(length))
        self._append_log('random', password)
        return password

def _interactive_mode(pg: PasswordGenerator) -> None:
    typ = input('Choose password type (memorable/random): ').strip().lower()
    if typ.startswith('m'):
        try:
            n = int(input('Number of words (e.g. 3): ').strip() or '4')
        except ValueError:
            n = 4
        cases_raw = input("Available cases separated by commas (lower,upper,title). Press Enter for default: ").strip()
        cases = [c.strip() for c in cases_raw.split(',')] if cases_raw else None
        pw = pg.generate_memorable(num_words=n, cases=cases)
    else:
        try:
            length = int(input('Password length (e.g. 12): ').strip() or '12')
        except ValueError:
            length = 12
        include_punct = input('Include punctuation? (y/n) [y]: ').strip().lower() != 'n'
        disallowed = input('Characters to disallow (no spaces): ').strip()
        pw = pg.generate_random(length=length, include_punct=include_punct, disallowed=disallowed)
    print('Generated password:', pw)

def demo_generate(pg: PasswordGenerator, count: int = 1000) -> None:
    """Generate `count` passwords randomly choosing type each time to confirm functionality."""
    for i in range(count):
        if random.choice([True, False]):
            # Memorable: pick 2-5 words and default cases
            num_words = random.randint(2, 5)
            pg.generate_memorable(num_words=num_words)
        else:
            # Random: pick length 8-16, random punctuation inclusion, and no disallowed chars
            length = random.randint(8, 16)
            include_punct = random.choice([True, False])
            pg.generate_random(length=length, include_punct=include_punct)

def main(argv=None):
    argv = argv or sys.argv[1:]
    pg = PasswordGenerator()
    if '--demo' in argv:
        demo_generate(pg, count=1000)
        print('Demo complete: 1000 passwords generated into Memorable/ and Random/ directories.')
        return
    if '--interactive' in argv or not argv:
        _interactive_mode(pg)
        return

if __name__ == '__main__':
    main()
