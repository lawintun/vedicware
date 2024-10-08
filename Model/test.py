from datetime import timedelta,datetime


planet_span = {
        "1": 6,
        "2": 10,
        "3": 7,
        "8": 18,
        "5": 16,
        "7": 19,
        "4": 17,
        "9": 7,
        "6": 20       
        }
moon = 63.93
nak_lord = {"3": "1",
  "12": "1",
  "21": "1",
  "4": "2",
  "13": "2",
  "22": "2",
  "5": "3",
  "14": "3",
  "23": "3",
  "9": "4",
  "18": "4",
  "27": "4",
  "7": "5",
  "16": "5",
  "25": "5",
  "2": "6",
  "11": "6",
  "20": "6",
  "8": "7",
  "17": "7",
  "26": "7",
  "6": "8",
  "15": "8",
  "24": "8",
  "1": "9",
  "10": "9",
  "19": "9"
}

y = 1996 
m = 1
d = 31
h = 23
min = 5
s = 0

nak_float = moon/(360/27)
nak_int = int(nak_float)
nak_span = nak_float - nak_int
nak = str(int(moon/(360/27))+1)
lord = nak_lord[nak]
span = planet_span[lord]
print("\n  span :  ",span)

bd = datetime(y,m,d,h,min,s)
year_days = {}
year_count = []
for sub in range(span-1):
    year = y-sub-1
    if year/4 == 0 and (year/100 != 0 or year/400 == 0):
      year_days[year] = 366
      year_count.append(year)
    else:
        year_days[year] = 365
        year_count.append(year)



past = nak_span*span
past_int = int(nak_span*span)
past_float = past - past_int
remain = abs(nak_span - past)
print(past, "  : ",remain)
print(past_float)

year_count = []
year_days = {}
for sub in range(int(past)):
    year = y-sub
    if year/4 == 0 and (year/100 != 0 or year/400 == 0):
      year_days[year] = 366
      year_count.append(year)
    else:
        year_days[year] = 365
        year_count.append(year)

print("\n  ",year_count)

bstart = bd
for yr,dy in year_days.items():
    bstart = bstart - timedelta(days=dy)
print(bstart)