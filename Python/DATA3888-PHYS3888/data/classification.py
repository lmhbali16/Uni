from scipy.io import wavfile
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

time_event = [20000, 45000, 70000, 90000, 110000]
waveLeft = np.load('./data/group_wave/Left5.npy')
left_event = []

waveRight = np.load('./data/group_wave/Right5.npy')
time_right = [21000, 46000, 65000, 90000, 110000]
right_event = []

waveNone = np.load('./data/group_wave/Straight5seconds.npy')
time_none = [5000, 15000, 25000, 35000, 40000]
none_event = []

time_event_LR = [55000, 70000, 90000, 105000, 125000, 145000, 160000, 180000, 200000, 219000, 237000, 257000, 275000, 290000, 305000, 320000, 340000, 365000, 382000, 400000]
waveLeft = np.load('./data/group_wave/LLLLRRRRRRRRLLRRRRLL.npy')
left_right_event = []

for i in time_event_LR:
    left_right_event.append(waveLeft[i-5000:i+5000])
    
reduced_left_right = []


for i in range(len(left_right_event)):
    
    a = left_right_event[i]
    
    b = np.array([a[j] for j in range(len(a)) if j % 5 == 0], dtype= np.float32)
    
    reduced_left_right.append(b)    

for i in range(5):
    none_event.append(waveNone[time_none[i] - 5000:time_none[i] + 5000])
    left_event.append(waveLeft[time_event[i] - 5000:time_event[i] + 5000])
    right_event.append(waveRight[time_right[i] - 5000:time_right[i] + 5000])

for i in range(5):
    left_event[i] = np.array([left_event[i][j] for j in range(len(left_event[i])) if j % 5 == 0], dtype=np.float32)
    right_event[i] = np.array([right_event[i][j] for j in range(len(right_event[i])) if j % 5 == 0], dtype=np.float32)
    none_event[i] = np.array([none_event[i][j] for j in range(len(none_event[i])) if j % 5 == 0], dtype=np.float32)

columns = [str(i) for i in range(2000)]
columns.append("class")
df = pd.DataFrame(columns=columns, index=[i for i in range(35)])

idx = 0
for i in range(0, 15, 3):
    df.iloc[i] = np.append(right_event[idx], 0)  # 0 = R
    df.iloc[i + 1] = np.append(left_event[idx], 1)  # 1 = L
    df.iloc[i + 2] = np.append(none_event[idx], 2)  # 2 = None
    idx += 1

for i in range(15,35):
    if (i >= 15 and i <= 18) or (i == 27 or i ==28) or(i ==33 or i ==34): 
        df.iloc[i] = np.append(reduced_left_right[i-15],1)
    else:
        df.iloc[i] = np.append(reduced_left_right[i-15],0)  

labels = list(df['class'].astype(int))

x_train, x_test, y_train, y_test = train_test_split(df.drop(['class'], axis='columns'), labels, test_size=0.25)

model = RandomForestClassifier(n_estimators=10)
model.fit(x_train, y_train)


def processWave(wave):
    """
    waveList = []

    waveList.append(wave[-10000:])
    waveList.append((wave[-15000:-5000]))
    waveList.append(wave[-20000:-10000])

    for i in range(len(waveList)):
        waveList[i] = [waveList[i][j] for j in range(len(waveList[i])) if j % 5 == 0]

    """
    wave = wave[-15000:-10000]

    wave = [wave[i] for i in range(len(wave)) if i % 5 == 0]

    return wave


def getFinalResult(results):
    if 0 in results and 1 not in results:
        return 0

    elif 0 not in results and 1 in results:
        return 1

    elif 0 not in results and 1 not in results:
        return 2
    else:

        if results.index(0) < results.index(1):
            return 0

        else:
            return 1


def predict(wave):
    wave = processWave(wave)

    results = []



    result = getFinalResult([wave])

    if result == 0:
        return "R"
    elif result == 1:
        return "L"

    else:
        return "none"


print(model.predict([x_test.iloc[0]]))