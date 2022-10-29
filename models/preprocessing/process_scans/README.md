# tangrams-dev
Unzip bookscans.zip<br>
<h2>Processing</h2>
For processing tangrams, run python main --debug {} --folder {} <br/>
This usually looks like python main.py --debug 0 --folder bookscans/allCropped/<br/>
bookscans/allCropped/ contains tangrams that haven't yielded an SVG yet<br/>
debug=1 will return lots of printouts, and each image as it goes through processing<br/>
debug=0 will spit out svgs in bookscans/testSVGS<br/>
If the SVG looks good, place it in bookscans/finished<br/>
<h2>Post-Processing</h2>
clean.py deletes files in bookscans/allcropped that correspond to bookscans/finished ( All cropped jpgs are in matchup, if you want to restore jpgs in bookscans/allcropped)<br/>
reformat_final.py takes all SVGS in final and moves them to bookscans/finished/fixed, with new coloration<br/>
moveToEdges.py crops the SVGs to exactly fit within their boundaries, and sets the viewbox and width attributes for display<br/>
matching.py takes generated SVGs from either successes or test, and matches them up with thheir JPG, and stores them in the matching directory.<br/>
<br/>
Matchup folder, contains success and likely fail, success shows side by side generated svg with source jpg <br/>

## Note: we omitted image files to save space.
