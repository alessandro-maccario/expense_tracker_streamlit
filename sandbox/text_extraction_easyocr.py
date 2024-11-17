"""
Testing extraction from receipt images by using EasyOCR:
- https://github.com/JaidedAI/EasyOCR
- https://www.jaided.ai/easyocr/
- https://www.jaided.ai/easyocr/documentation/

"""

import easyocr
import time

# start counting the time needed for the script to run
start_time = time.time()

reader = easyocr.Reader(
    ["de", "en"], gpu=False
)  # this needs to run only once to load the model into memory
result = reader.readtext("sandbox/20241116_090948.jpg")
# result_string = ",".join(result)

# with open("sandbox/text_extraction.txt", "w") as f:
#     f.write(result_string)

print(print("--- %s seconds ---" % (time.time() - start_time)))
