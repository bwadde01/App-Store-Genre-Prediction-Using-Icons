# App-Store-Genre-Prediction-Using-Icons
Using Kaggle AppStore data^ from the category of strategy games to try to distinguish subcategories (puzzle vs entertainment) based on the app icons. I also wrote a web scraper to pull additional data from the AppStore, which I do not leverage in this project. But I have posted it (scrape_links_and_app_data.py) here because it is thematically related in case anyone would find it useful.

In this project, I:
1. Read in the data (pandas)
2. Preprocess the metadata for the proof of concept (pandas)
3. Load and Preprocess Images (cv2, p_tqdm for multiprocessing)
4. Model the data (keras, tensorflow, gpu, CNN)
5. Tune the number of epochas based on learning curves
6. Discuss the results and problems

From the modeling, we were able to achieve an **accuracy of around 73%**, which is better than the baseline of ~60% (from always guessing entertainment pre-oversampling .242606/(.242606+.157641)). However, there are **two major problems that preclude a higher accuracy**:

1. Overfitting due to the low volume of images
2. High intra-class variation due to the subjective nature of the classes (i.e. what constitutes a puzzle game vs an entertainment game?). Because they are not strictly defined, we would expect higher variation present in the individual classes and overlap between them

^ https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games
