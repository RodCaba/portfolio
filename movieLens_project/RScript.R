#######################################
# R SCRIPT FOR MOVIELENS PROJECT
# by : RODRIGO CABALLERO ##############
#######################################

#------SETTING UP SETS-------
################################
# Create edx set, validation set
################################

# Note: this process could take a couple of minutes
start_time <- Sys.time()
Sys.sleep(0.5)


if(!require(tidyverse)) install.packages("tidyverse", repos = "http://cran.us.r-project.org")
if(!require(data.table)) install.packages("data.table", repos = "http://cran.us.r-project.org")
library(caret)
library(anytime)
library(lubridate)
library(tree)
library(class)

# MovieLens 10M dataset:
# https://grouplens.org/datasets/movielens/10m/
# http://files.grouplens.org/datasets/movielens/ml-10m.zip

dl <- tempfile()
download.file("http://files.grouplens.org/datasets/movielens/ml-10m.zip", dl)

ratings <- fread(text = gsub("::", "\t", readLines(unzip(dl, "ml-10M100K/ratings.dat"))),
                 col.names = c("userId", "movieId", "rating", "timestamp"))

movies <- str_split_fixed(readLines(unzip(dl, "ml-10M100K/movies.dat")), "\\::", 3)
colnames(movies) <- c("movieId", "title", "genres")
movies <- as.data.frame(movies) %>% mutate(movieId = as.numeric(levels(movieId))[movieId],
                                           title = as.character(title),
                                           genres = as.character(genres))

movielens <- left_join(ratings, movies, by = "movieId")

# Validation set will be 10% of MovieLens data

set.seed(1, sample.kind="Rounding")
# if using R 3.5 or earlier, use `set.seed(1)` instead
test_index <- createDataPartition(y = movielens$rating, times = 1, p = 0.1, list = FALSE)
edx <- movielens[-test_index,]
temp <- movielens[test_index,]

# Make sure userId and movieId in validation set are also in edx set

validation <- temp %>% 
  semi_join(edx, by = "movieId") %>%
  semi_join(edx, by = "userId")

# Add rows removed from validation set back into edx set

removed <- anti_join(temp, validation)
edx <- rbind(edx, removed)

rm(dl, ratings, movies, test_index, temp, movielens, removed)

end_time_setup <- Sys.time()

time_for_setup <- start_time - end_time_setup
#------INTRODUCTION-------
#This project will use the Movielens data set
#We have a train set, close of 10M rows and 6 variables and test set for close of
#10% of the train set

#First let's look at data structure
str(edx)
summary(edx)
#We have in total around 5 features

#userId which is an int. for different users
#movieId which is a number for the different movies
#timestamp: an integer for the time the rating was made
#title: character for the movie title
#genres: character for movie genre

#We have our outcome to predict which is the rating given, is a number
#between 0.5 and 5

#The goal of the algorithm is to reduce the RMSE below 0.8649
#hence we will focus on algorithms for regression and handle
#the target (rating) as a continuous variable. 

#------EXPLORATORY ANALYSIS------
#Let's start by making some plots for exploratory analysis and start to 
#understand better the data we are working with

#I think an strong predictor for the outcome will be the genres of the movie.
#To make code efficient, first we will create data partition of 20K movies
#of the training set to work with in Data exploration


#We have to set.seed for reproducibility
set.seed(1, sample.kind = 'Rounding')

data_exp_index <- createDataPartition(y = edx$rating, times = 1, p = 0.002222,
                                list = FALSE)
data_exp <- edx[data_exp_index,]

#We have also to split the strings in the genre vector
#Several movies does not have several genres associated,
#hence the main genre of the movie will be accounted and the 
#rest would be dropped

data_exp <- data_exp %>% 
  separate(genres, sep = '[|]',extra = 'drop',
           into = 'genres')

#Lets have a look to our data
head(data_exp, 10)

#Good, now the genre vector has a single genre for each row. 
#Let's make a plot of the ratings by each genre

genre_feat <- data_exp %>% 
  group_by(genres) %>% 
  summarize(rating = mean(rating)) %>% 
  arrange(desc(rating))

genre_feat %>% 
  ggplot(aes(x = reorder(genres, -rating), rating)) +
  geom_bar(stat = 'Identity') +
  xlab('Genres')+
  coord_cartesian(ylim = c(3,4)) +
  theme(axis.text.x = element_text(angle = 90))

#So we can see that there are some Genres that are better rated in 
# average than others 

#Number of ratings may also impact on the ratings system, let's take a look
#of the number of ratings per movie

n_feat <- data_exp %>% 
  group_by(title) %>% 
  summarize(n = n(), rating = mean(rating)) %>% 
  arrange(desc(n))

n_feat %>% 
  ggplot(aes(rating, n)) +
  geom_point()

#We can see a normal distribution effect. Movies that are well known are the
#most rated. We see the example of ToyStory, Jurassic Park etc.
#Movies with more ratings have an average rating close to 
#the overall mean (which is 3.5 for the edx dataset), and movies with little 
#ratings have 'uncommon' ratings 

#Now, let's take a look at the overall ratings by the number of ratings
#each user gives. This, for example would tell that if a user is more or less
#active is inclined to give y rating

user_feat <- data_exp %>% 
  group_by(userId) %>% 
  summarize(n = n(), rating = mean(rating)) %>% 
  arrange(desc(n))

user_feat %>% 
  ggplot(aes(rating, n)) +
  geom_point()

#We see a similar efect that in the previous case, the more a single user is 
#active rating in the platform the more close to the average the rating will
#be


data_exp <- data_exp %>% 
  mutate(timestamp = anytime(timestamp))

data_exp %>%
  group_by(timestamp) %>% 
  summarize(mean(rating)) %>% 
  ggplot(aes(timestamp, `mean(rating)`)) +
  geom_point()

#Also the rating of each genre may be a matter of taste of each
#person, so a person may like more an action movie and rated it
#higher than an horror movie for example, so we can include
#the average rating the user gives to certain genres


#Allright! we have a lot of insights of the predictors we can use to fit our
#models, we are done with the exploratory analysis. Let's look at the 
#insights of the predictors.
#userId: the more a user is active in the platform the more likely the mean
#of it's ratings will fall in the overall mean of the ratings
#movieId / title: the more a film is rated the more likely the mean 
#of it's ratings will fall in the overall mean of the ratings
#genres: on average, ratings may vary on the genre of the film,
#as well as the genre each user may be inclined into. 

#-----------PREPROCESING DATA--------

# We add the new predictor variables
#NUserRatings = Number of ratings the user have in platform
#NMovieRatings = Number of ratings movie have in platform
#We transform the genres as a factor
#avg_rating_movie = the average rating a movie has 
#avg_rating_genre = the average rating a genre has.
#avg_rating_user_genre = average rating for a genre each user
#gives. 

data_exp <- data_exp %>%
  group_by(userId) %>% 
  mutate(NUserRatings = n()) %>% 
  ungroup()

data_exp <- data_exp %>% 
  group_by(movieId) %>% 
  mutate(NMovieRatings = n()) %>% 
  ungroup()

data_exp <- data_exp %>% 
  mutate(genres_factor = as.integer(as.factor(genres)))

data_exp <- data_exp %>% 
  group_by(movieId) %>% 
  mutate(avg_rating_movie = mean(rating)) %>% 
  ungroup()

data_exp <- data_exp %>% 
  group_by(genres) %>% 
  mutate(avg_rating_genre = mean(rating)) %>% 
  ungroup()

data_exp <- data_exp %>% 
  group_by(userId, genres) %>% 
  mutate(avg_rating_user_genre = mean(rating)) %>% 
  ungroup()

data_exp <- data_exp %>% 
  select(rating, NUserRatings, NMovieRatings, avg_rating_movie,avg_rating_genre, avg_rating_user_genre)

#We are extracting the y vector 
y_exp <- data_exp['rating']
x_exp <- data_exp[,2:6]

#We normalize the x vectors
x_exp <- as.data.frame(scale(x_exp))


set.seed(1, sample.kind="Rounding")
test_index <- createDataPartition(y = x_exp$NUserRatings,times = 1,p = 0.1,list = FALSE)

#SETS FOR X
train_set_exp <- x_exp[-test_index,]
test_set_exp <- x_exp[test_index,]


#VECTOR OF Y
y_train_exp <- y_exp[-test_index,,drop =TRUE]
y_test_exp <- y_exp[test_index,,drop = TRUE]

#---------RUNNING ALGORITHMS IN THE LOW SCALE----------

#We are running a KNN Algorithm to make predictions on
#test set in the low scale, to calculate RMSE and see if 
#it is an option for the whole edx dataset. 

time0_trainlowscale <- Sys.time()

train_knn <- train(train_set_exp,y = y_train_exp,method = 'knn')


y_hat_knn <- predict(train_knn, test_set_exp)


y_results <- as.data.frame(y_test_exp)
y_results['predicted'] <- as.data.frame(y_hat_knn)

y_results <- y_results %>% 
  mutate(RMSE = ((predicted - y_test_exp)^2)/n())

RMSE_knn9 = sqrt(sum(y_results$RMSE))

time1_trainlowscale <- Sys.time()

#The RMSE for the KNN (9 neighbors)algorithm has good results in the low
#scale

#-----MODIFICATION OF DATA BASED ON EXPLORATORY ANALYSIS--------

#Remove all objects created above
rm(data_exp, data_exp_index, genre_feat, n_feat, user_feat,
   test_index, train_knn, train_set_exp, x_exp, y_exp, y_results,
   RMSE_knn9, y_hat_knn, y_test_exp, y_train_exp, test_set_exp)

#This may take a while, we are executing the command on edx and 
#validation dataset


edx <- edx %>% 
  separate(col = genres, into = 'genres',sep = '[|]',
           extra = 'drop')

validation <- validation %>% 
  separate(col = genres, into = 'genres', sep = '[|]',
           extra = 'drop')


#We are adding the features and preprocessing the data as we 
#did on the low scale for the edx dataset and the validation
#dataset

#First we wrangle de edx dataset

edx <- edx %>% 
  group_by(userId) %>% 
  mutate(NUserRatings = n()) %>% 
  ungroup()

edx <- edx %>% 
  group_by(movieId) %>% 
  mutate(NMovieRatings = n()) %>% 
  ungroup()

edx <- edx %>% 
  mutate(genres_factor = as.integer(as.factor(genres)))

edx <- edx %>% 
  group_by(movieId) %>% 
  mutate(avg_rating_movie = mean(rating)) %>% 
  ungroup()

edx <- edx %>% 
  group_by(genres) %>% 
  mutate(avg_rating_genre = mean(rating)) %>% 
  ungroup()

edx <- edx %>% 
  group_by(userId, genres) %>% 
  mutate(avg_rating_user_genre = mean(rating)) %>% 
  ungroup()

edx <- edx %>% 
  select(rating, NUserRatings, NMovieRatings, avg_rating_movie,avg_rating_genre, avg_rating_user_genre)

#For computing reasons, edx set would be shrinked in random
#scheme for training algorithm

set.seed(1, sample.kind = 'Rounding')

train_index <- createDataPartition(y = edx$rating, times = 1, p = 0.002222*3,
                                      list = FALSE)
edx1 <- edx[train_index,]


#Now we go for the validation dataset

validation <- validation %>% 
  group_by(userId) %>% 
  mutate(NUserRatings = n()) %>% 
  ungroup()

validation <- validation %>% 
  group_by(movieId) %>% 
  mutate(NMovieRatings = n()) %>% 
  ungroup()

validation <- validation %>% 
  mutate(genres_factor = as.integer(as.factor(genres)))

validation <- validation %>% 
  group_by(movieId) %>% 
  mutate(avg_rating_movie = mean(rating)) %>% 
  ungroup()

validation <- validation %>% 
  group_by(genres) %>% 
  mutate(avg_rating_genre = mean(rating)) %>% 
  ungroup()

validation <- validation %>% 
  group_by(userId, genres) %>% 
  mutate(avg_rating_user_genre = mean(rating)) %>% 
  ungroup()

validation <- validation %>% 
  select(rating, NUserRatings, NMovieRatings, avg_rating_movie,avg_rating_genre, avg_rating_user_genre)

#We will get the vectors for the outcome (y) for the edx
#and validation dataset

y_edx <- edx1['rating']
y_validation <- validation['rating']

#We transform outcome in a vector

y_edx <- y_edx[,,drop = TRUE]
y_validation <- y_validation[,,drop = TRUE]

#We also are getting the matrix of the predictors to do the
#preprocesing

x_edx <- edx1[,2:6]
x_validation <- validation[,2:6]

#Now we do preprocesing of the matrix in the edx and validation
#dataset

x_edx <- as.data.frame(scale(x_edx))
x_validation <- as.data.frame(scale(x_validation))

#We will train a knn 9 neighbors algorithm in the edx dataset
#For computing reasons we will train the algorithm in a dataset
#sample, index of sample would be random
start_time_train <- Sys.time()

knn_grid <- expand.grid(k = 9)

train_knn <- train(x = x_edx, y = y_edx, method = 'knn', tuneGrid = knn_grid)


end_time = Sys.time()

#Now we go for the prediction

start_time_pred <- Sys.time()

y_hat_knn <- predict(train_knn, x_validation)


y_results <- as.data.frame(y_validation)
y_results['predicted'] <- as.data.frame(y_hat_knn)

y_results <- y_results %>% 
  mutate(RMSE = ((predicted - y_validation)^2)/n())

RMSE_knn9 = sqrt(sum(y_results$RMSE))

end_time_pred <- Sys.time()


