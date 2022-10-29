import os
FINAL = "bookscans/finished"
ALLCROPPED = "bookscans/allCropped"

finalSVGS = os.listdir(FINAL)
# print(finalSVGS)
print(len(os.listdir(ALLCROPPED)))
for  filename in sorted(os.listdir(ALLCROPPED)):
    if ".jpg" not in filename:
    	os.remove(ALLCROPPED + "/" + filename)
    	continue
    filesvg = filename.replace("jpg", "svg")
    # print(filesvg)
    if filesvg in finalSVGS:
    	print(filename)
    	os.remove(ALLCROPPED + "/" + filename)