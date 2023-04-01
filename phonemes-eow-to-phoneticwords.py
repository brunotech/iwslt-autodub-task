
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
import sys

file = sys.argv[1]
path = "./"

with open(os.path.join(path, file)) as f:
    lines = f.readlines()
    sentences = []
    for line in lines:
        phonetic_words = []
        phones = line.split('<eow>')
        for phone in phones:
            if phone != '\n':
                # if we don't have durations comment out next line
                phone = phone.split()[::2] if sys.argv[2] == 'durations' else phone.split()
                cleaned_phones = [item for item in phone if item != 'sp']
                phonetic_word = "-".join(cleaned_phones)
                phonetic_words.append(phonetic_word)

        sentences.append(" ".join(phonetic_words))


with open(os.path.join(path, f'{file}.phoneticwords'), 'w') as f:
    for sentence in sentences:
        f.write(f'{sentence}\n')



