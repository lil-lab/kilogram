import os
from shutil import copyfile

FOLDER = "bookscans/cropped/Page5"


# count = 0
# for FOLDER2 in sorted(os.listdir(FOLDER)):
# 	if FOLDER2 != "":
# 		files = os.listdir(FOLDER + "/" + FOLDER2)
# 		filesSorted = sorted(files, key=lambda f: int(f[f.find("m")+1:f.find(".")])) 
# 		for file in filesSorted:
# 			if "jpg" in file:				
# 				newfileName = "page5-" + str(count) + ".jpg"
# 				copyfile(FOLDER + "/" + FOLDER2 +"/" + file,"matchup/" + newfileName)
# 				print(FOLDER2)
# 				print(file)
# 				print(newfileName)
# 				count += 1


FINISHED = "bookscans/testSVGS"
for finished in sorted(os.listdir(FINISHED)):
	print(finished)
	if finished not in os.listdir("matchup/fail-w-svg"):
		info = finished[:finished.find(".")]
		if info + ".jpg" in os.listdir("matchup/fail-no-svg"):
			copyfile("matchup/fail-no-svg/" + info + ".jpg","matchup/fail-w-svg/" + info + ".jpg")
			copyfile(FINISHED + "/" + finished,"matchup/fail-w-svg/" + finished)
			os.remove("matchup/fail-no-svg/" + info + ".jpg")

			print(finished)