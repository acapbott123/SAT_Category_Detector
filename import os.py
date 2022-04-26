import os
import shutil
start ="C:\\Users\\booga\OneDrive\\Desktop\\SatCategoryDetector\\Images"
end ="C:\\Users\\booga\\OneDrive\\Desktop\\darknet-master\\darknet-master\\build\\darknet\\x64\\data\\obj"



for foldername in os.listdir(start):
    for filename in os.listdir(start + '\\'+ foldername):
            shutil.copy(start + "\\" + foldername + "\\"+ filename ,end)

    
