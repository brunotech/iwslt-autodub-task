
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import pickle
import sys
from statistics import mean
from preprocessing_scripts import Bin

ref = sys.argv[1]
hyp = sys.argv[2]

path = "./"
correct_dur_pred, incorrect_dur_pred = 0, 0
durations_hyp = []
durations_ref = []

durations_path = './durations_freq_all.pkl'
if os.path.exists(durations_path):
    with open(durations_path, 'rb') as f:
        duration_freq = pickle.load(f)
        print("loaded durations' freq!")
        bin_instance = Bin(duration_freq, n=100)

with open(os.path.join(path, ref)) as f:
    lines = f.readlines()
    sentences = []
    for line in lines:
        line = " ".join(line.split("<eow>"))
        line_segments = line.split('[pause]')
        counter_line = []

        for segment in line_segments:
            durations = segment.split()[1:][::2]
            counter_segment = sum(int(dur) for dur in durations)
            counter_line.append(counter_segment)
        durations_ref.append(counter_line)

with open(os.path.join(path, hyp)) as f:
    lines = f.readlines()
    sentences = []
    for i, line in enumerate(lines):
        line = " ".join(line.split("<eow>"))
        line_segments = line.split('[pause]')
        counter_line = []
        for segment in line_segments:
            counter_segment = 0
            segments = segment.split()
            num = 0
            for seg in segments:
                if num % 2 != 0:  # odd
                    try:
                        counter_segment += int(seg)
                        # pdb.set_trace()
                    except:
                        print(segments)
                        print(f"Duration is {seg} for line {i}")
                        num += 1
                num += 1

            counter_line.append(counter_segment)

        durations_hyp.append(counter_line)

errors = []
scores = []
count = 0
count_right = 0
one_pause_or_more = 0
differences = []
sampling_rate = 22050
hop_length = 256
large_dif = 0
small_dif = 0
threshold_in_frames = int(0.3 * sampling_rate/hop_length)
# 0.3s corresponds to 25 frames

for i in range(len(durations_ref)):
    # if len(durations_ref[i]) > 0:
    one_pause_or_more +=1
    if len(durations_ref[i]) == len(durations_hyp[i]):
        for j in range(len(durations_ref[i])):
            temp = 1 if durations_ref[i][j] == 0 else durations_ref[i][j]
            abs_diff = abs(durations_hyp[i][j] - temp)
            errors.append(abs_diff/temp)
            if durations_hyp[i][j] < temp:
                scores.append(durations_hyp[i][j]/temp)
            else:
                scores.append(temp/durations_hyp[i][j])
            differences.append(abs_diff)
            if abs_diff >= threshold_in_frames:
                large_dif += 1
            else:
                small_dif += 1
        count_right += 1
    else:
        count += 1
        for j in range(len(durations_ref[i])):
            temp = 1 if durations_ref[i][j] == 0 else durations_ref[i][j]
            abs_diff = abs(0 - temp)
            errors.append(abs_diff/temp)
            scores.append(0.0)
            differences.append(threshold_in_frames + 10)
            large_dif += 1

# print(count)
# print(count_right)
print(f"Metric 1 is {1 - mean(errors)}")
print(f"Metric 2 is {mean(scores)}")
print(f"Metric 3 is {mean(differences)}")

print(f"Segments with diff > 0.3s: {large_dif / (small_dif + large_dif)}")
print(f"How many sentences have 1 or more pauses: {one_pause_or_more}")

print(
    f"Predicted wrong number of pauses in {count} out of {count + count_right} sentences"
)
