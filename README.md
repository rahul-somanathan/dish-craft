# Recipe Recommendation Engine

## Overview
This project aims to build a recipe recommendation engine using the Food.com dataset. The recommendation engine will help users discover new and delicious recipes based on their preferences, dietary restrictions, and cooking habits.

## Dataset
The dataset used for this project is sourced from Food.com. It contains a vast collection of recipes along with various attributes such as ingredients, cooking methods, ratings, and more. The dataset will be preprocessed and used to train the recommendation engine. 
[Food.com Dataset](https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions)

## Features
- Recipe recommendation based on user preferences
- Streamlit application for ease of use
- Dockerized system

## Architecture
The recommendation engine will be built using python, streamlit, fastAPI, leveraging KNN and SVD for recommendation purposes. The architecture may include components such as data preprocessing, feature extraction, model training, and recommendation generation.

## Usage
To use the recommendation engine, users can select the user id. The engine will provide personalized recipe recommendations based on user input and preferences.

## Installation
To install and run the recommendation engine locally, follow these steps:
1. Clone this repository to your local machine.
2. In your terminal run "docker-compose build" from root directory
3. Once build succeeds run "docker-compose up"
4. Follow the [backend API](http://localhost:8000/) 
5. Follow the [streamlit front end application](http://localhost:8501/) 
6. do run "docker-compose down" to stop the application

## Build Commands

RRE React Front End: docker build --build-arg NODE_VERSION=$(node -pe "require('./package.json').engines.node") -t your-image-name .


## License
Copyright (c) 2024 

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


