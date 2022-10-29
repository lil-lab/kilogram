## Setup

1. run `npm install` to get dependencies
2. download all test-set (dev set) images to this sub-directory
3. if running on server, prepare database (otherwise skip to 4)
    1. download the four eval_data .json files to eval_data and run preprocess.py
    2. insert resulting stims into database with reset_stim_database.py
    3. run `node store.js` to launch db wrapper listening on port
4. run `node app.js` to launch process listening on port
5. go to `<server>:8887/comprehension.html` in the browser to access expt 
  * this is `localhost:8887/comprehension.html` if running locally
