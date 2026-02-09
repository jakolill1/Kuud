import csv
from datetime import datetime

INPUT = "2023-03-08_IT22_ExtraBig.csv"
OUTPUT = "tulemus_18_august.csv"

DAY = 18
MONTH = 8


def normalize(text: str) -> str:
    return text.replace("\ufeff", "").lower().strip()


def parse_date(value):
    if not value:
        return None

    value = value.strip()
    if not value:
        return None

    for fmt in ("%Y-%m-%d", "%Y.%m.%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    return None


def format_date(d):
    return d.strftime("%d.%m.%Y") if d else ""


def calculate_age(birth, death):
    years = death.year - birth.year
    if (death.month, death.day) < (birth.month, birth.day):
        years -= 1
    return years


with open(INPUT, encoding="utf-8") as fin, \
     open(OUTPUT, "w", encoding="utf-8", newline="") as fout:

    reader = csv.DictReader(fin, delimiter=";")

    birth_keywords = ("sünd", "sunni", "sünni", "birth", "born", "dob")
    death_keywords = ("surm", "suri", "surma", "death", "died", "dod")

    birth_col = None
    death_col = None

    for col in reader.fieldnames:
        n = normalize(col)
        if birth_col is None and any(k in n for k in birth_keywords):
            birth_col = col
        if death_col is None and any(k in n for k in death_keywords):
            death_col = col

    if birth_col is None or death_col is None:
        raise RuntimeError(f"Veerge ei leitud: {reader.fieldnames}")

    writer = csv.DictWriter(
        fout,
        reader.fieldnames + ["Vanus"],
        delimiter=";"
    )
    writer.writeheader()

    matched = 0

    for i, row in enumerate(reader, start=1):
        if i % 10000 == 0:
            print(f"Töötlen rida {i}... leitud {matched}")

        birth = parse_date(row.get(birth_col))
        death = parse_date(row.get(death_col))

        born_same = birth and birth.day == DAY and birth.month == MONTH
        died_same = death and death.day == DAY and death.month == MONTH

        if not (born_same or died_same):
            continue

        row[birth_col] = format_date(birth)
        row[death_col] = format_date(death)

        if birth and death:
            row["Vanus"] = calculate_age(birth, death)
        else:
            row["Vanus"] = ""

        writer.writerow(row)
        matched += 1

print("VALMIS!")
print("Leitud isikuid:", matched)
print("Fail:", OUTPUT)
