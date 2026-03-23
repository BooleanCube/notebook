Machine Learning is the science (and art) of programming computers so they can learn from data.
In today's world, especially after the release of large language models like ChatGPT and Claude, machine learning is everywhere.
Even the spam filter in your inbox is a machine learning program that can learn to flag spam given examples of spam mails (flagged by users) and examples of regular mails.

The examples that the machine learning models use to learn are called the training datasets and each example is called a training *instance* or *sample*.
With most machine learning models, we need a metric to be able to measure how good it is at a certain task.
To measure the "performance" of a model, in this case, we can use the ratio of correctly classified emails.
This particular performance measure is called *accuracy* and it is often used in classification tasks.

More realistically, machine learning is a set of methods that can automatically detect patterns in data, and then use the uncovered patterns to predict future data, or to perform other kinds of decision making under uncertainty.

![mlprocess](https://i.imgur.com/uNjJwZH.png)

Here is a detailed step-by-step explanation of the machine learning process:

1. Identify the question being answered or problem being solved.
2. Identify and gather the appropriate data.
3. Analyze, explore, and understand the data.
4. Prepare the data by cleansing, transforming, and shaping it.
5. Select and train an appropriate machine learning model.
6. Fine-tune and validate the machine learning model to ensure it meets business objectives.
7. Launch, monitor, and maintain the machine learning model.

The first 4 steps (business objectives, data understanding, and data preparation) are definitely the most time consuming and critical parts of the process.
A proper understanding of statistics and probability is highly critical for conducting the four stages correctly as well.

---

# How Do Machines Learn?

## Types of Machine Learning

There are actually many types of machine learning models that solve different type of problems.
The specific problem being solved determines which type of model you want to consider using.
Note: the terms machine learning "algorithms", "models", and "systems" are used interchangeably and are all the same thing.
Note: the terms "sample", "instance", and "observation" are also all the same thing.

### Supervised Learning

In supervised learning, the goal is to learn a mapping of inputs `x` to outputs `y` given a labeled set of inputs-output pairs `D = {(x_i, y_i)} for i=1...N`.
`N` represents the number of samples in the training dataset `D`.
Now the inputs don't necessarily have to be only 1 variable.
Multiple features could be provided as input and therefore we define `X_j` as a feature vector representing all the features/attributes, and `y_i` is the target value/response.
Basically, supervised learning uses labeled examples from the data, comparing its actual output with correct outputs to find errors and modify the model correctly.

Supervised learning is very beneficial to many types of problems but two of those include: classification and regression problems.
In classification, we are labeling the data to a categorical output variable (ordinal or nominal).
In regression, we are labeling the data to a numerical output variable (continuous or discrete).
Most supervised learning algorithms include k-Nearest neighbours, Naive Bayes, Linear Regression, Logistic Regression, Support Vector Machines, Decision Trees, and Neural Networks.

### Unsupervised Learning

In unsupervised learning, the goal is to identify patterns given just the inputs.
There are no output values or historical labels to compare against; the algorithm must figure out what is being shown.
Major applications of unsupervised learning include clustering data (K-Means, DBSCAN, HCA), anomaly detection (One-class SVM, Isolation Forest), and dimensionality reduction (PCA, t-SNE).
The models used for each type of problem are included within the brackets.

### Semi-supervised Learning

This approach uses a small amount of labeled data and a large amount of unlabeled data.
These algorithms generally combine supervised and unsupervised learning techniques together.
A common workflow is to train an initial model on the labeled data, use it to assign pseudo-labels to the unlabeled data, merge the datasets, and retrain the model.
This can be similar to **data imputation** but should not be confused for each other.
Data imputation is the process of filling in missing labeled data whereas in this case we are generating and labeling more data based on what we started with.

### Reinforcement Learning

The learning system, called an agent, observes an environment, performs actions, and gets rewards or penalties in return.
It learns by itself to find the best strategy, called a policy, to maximize rewards over time through trial and error.
A policy defines what action the agent should choose in a given situation.
Reinforcement Learning is commonly used in robotics, gaming, and navigation.

For example, imagine a grid where an agent can start at any cell and the goal is to reach the destination cell.
The agent at any point in time perform an action which is to move 1 cell in any of the four directions: up, down, left, or right.
However, some cells are also blocked off and we call these "walls".
We can use reinforcement learning by dropping the agent within the grid at the start cell and work its way to the goal.
Upon every iteration the agent learns what actions are more rewarding than others in each situation and will start finding shorter paths from the start to the goal.

### Batch vs Online Learning

With batch learning, the system is incapable of learning incrementally and must be trained offline using all the available data at once.
Once launched, the model stops learning and just predicts. To update the model, it must be retrained from scratch on the dataset (whether it has been modified or not).

However, with online learning, the system is trained incrementally by feeding it data instances sequentially (individually or in mini-batches).
It is useful for data that arrives frequently (like stock prices) or when computing resources are limited, as data can be discarded after learning.

### Instance-Based vs Model-Based Learning

With instance-based learning, the systems learn the examples by heart, and generalizes to new cases by comparing them to the learned examples using a similarity measure.
Examples of algorithms that are instance-based are k-Nearest neighbours and case-based medical diagnosis algorithms.

With model-based learning however, the system builds a mathematical model from the training dataset and uses that model to make predictions.
For example, in linear regression, a utility or cost function is used to measure model performance, and the algorithm tweaks model parameters (like `θ_0` and `θ_1`) to fit the data better.

## Challenges of Machine Learning

There are two main types of challenges that data scientists can run into when trying to develop machine learning models and they are: bad data and bad algorithms.

### Data Challenges

- **Insufficient Quantity of Data**: Machine Learning models usually need thousands or even millions of samples to learn and predict properly.
- **Nonrepresentative Training Data**: The training data must be representative of the new cases that we want to generalize to. Flawed sampling methods cause sampling bias, and too small of a sample causes sampling noise.
- **Poor Quality Data**: Based on the "Garbage In, Garbage Out" (GIGO) principle, a system cannot perform well if training data is full of errors, outliers, and noise. Data cleaning is a significant part of a data scientists job.
- **Irrelevant Features**: The model needs relevant features to learn. Feature engineering involves selecting the most useful features, combining existing ones, or even creating new ones.

### Algorithmic Challenges

- **Overfitting**: This occurs when a model performs well on training data but fails to generalize to new instances because it is too complex and detects patterns in the data's noise. Solutions include: simplifying the model, gathering more data, removing redundant/irrelevant data, cleaning up data noise, and applying regularization.
- **Regularization**: The process of constraining a model to keep it simpler and reduce overfitting. The amount of regularization is controlled by a hyperparameter, which is set prior to training and remains constant. Common techniques include: L1 (Lasso) and L2 (Ridge).
- **Underfitting**: This occurs when a model is too simple to learn the underlying structure of the data. Solutions include selecting a more powerful model, feeding better features, or reducing constraints.

## Testing and Validating

Once a model has been built, it needs to be tested and validated before it can be deployed.
The standard approach to this is to split your data into a training dataset and a testing dataset (usually with a 80/20 or 70/30 split).
This way, you can train multiple models on the training data and then test how well it generalizes to data it wasn't trained on with the test set.
The **generalization error** is the error of the model against the testing dataset which indicates how well your model generalizes to new data.

In machine learning models, **parameters** are the variables in the model that are adjusted and learned during training and **hyperparameters** are the variables that are adjusted outside of the training process.
For example, regularization values, number of layers, number of neighbours, are all hyperparamters that can be set before training a model.

Let's say you are hesitating whether to choose a linear or polynomial model for your problem.
You can decide by building two models, test them, and decide based on their performance to generalize to the test set.

Now, let's say you found that the linear model had a smaller generalization error and you decide to go forward with it, but you want to apply regularization because you want to prevent overfitting.
To find the best regularization values we need to perform **hyperparameter tuning** by testing a bunch (maybe 100) of different versions of the same model with different hyperparameter values.
However, you might find that even if you get the best of these 100 models, it might not perform well on other data.
This is because we used the same test set for all 100 models to measure the generalization error.
So the model and hyperparameters likely adapted to just fit the test set better and might not generalize well to new data.
To solve this, just splitting the data into training and testing data isn't enough. We need a third partition called the validation set which we pull from the reduced training dataset.

![datasplit](https://i.imgur.com/T4HgESN.png)

The new process to tune hyperparameters (using 100 different models) works like this: train the models with various hyper parameters on the reduced training set (`full data - testing - validation`), select model with best performance on validation set, train the model with the full training set including the validation set (`full data - testing`), and test with testing set to get the generalization error.

While the above process works well, the size of the validation set impacts the amount of training data we have available.
To prevent the training set from getting too small, **k-fold cross validation** is a common strategy that is applied.

In k-fold cross validation, instead of splitting your training set into a reduced training set and a validation set, it is split into k folds.
One of the folds is selected as the validation set and the model is trained against the union of all other folds. After the model is trained, it measures the error against the preselected validation fold.
That process is repeated such that every fold is the validation fold exactly once (k iterations) and the error is averaged across all iterations of this process for a single measure of performance.
When `k = N-1`, this is called leave-one-out validation (where `N` is the number of instances in the training set).

## Data Mismatch

Your training data might not be representative of the test data.
For example, you would like to build a mobile app that take pictures of a flower and then determine their species.
You train your data based on million of pictures downloaded from web and train the model.
However, they might not perform well on the pictures you are taking with the phone camera.
So, most important is that your test and validation set must be representative of the data you will use in your production.
Let’s say you have some pictures taken by your app, shuffled them and you are using them for test and validation set (50% each).

After training your model on the web pictures, if you observe that the performance of your model on the validation set is disappointing, you will not know whether this is because your model has overfit the training set, or whether this is just due to the mismatch between the web pictures and the mobile app pictures.
One solution is to hold out part of the training pictures (from the web) in yet another set that called train-dev set.
After the model is trained (on the training set, not on the train-dev set), you can evaluate it on the train-dev set: if it performs well, then the model is not overfitting the training set, so if performs poorly on the validation set, the problem must come from the data mismatch.

You can try to tackle this problem by preprocessing the web images to make them look more like the pictures that will be taken by the mobile app, and then retraining the model.
Conversely, if the model performs poorly on the train-dev set, then the model must have overfit the training set, so you should try to simplify or regularize the model, get more training data and clean up the training data, as discussed earlier.

---

# Exploratory Data Analysis

Exploratory Data Analysis (EDA) is the process of summarizing, visualizing, and understanding the data.
It is important to understand what each feature represents (e.g. does "income" mean annually or monthly?).
Ultimately, it answers the question: "Is my data ready for ML?".

EDA is important because it ensures future model results will be meaningful and reliable.
From EDA we might also uncover hidden patterns that might not be inherently obvious, such as sales spiking only on weekends.
Skipping EDA is a common rookie mistake most data scientists make when trying to build a model to solve their problem.

Here is an example of an assignment illustrating the entire EDA process: [A1 EDA](https://colab.research.google.com/drive/1KKf1LwPzr4hsg8aMw2bbV2ux9Kt1Z4Xw?usp=sharing)

## Common EDA Methods and Tasks

- **Univariate analysis**: Studying one variable at a time (e.g. histogram of student grades).
- **Bivariate analysis**: Studying the relationship between a variable and the target (e.g. income vs life satisfaction).
- **Multivariate analysis**: Studying interactions among multiple variables (income + education vs life satisfaction).
- **Dimensionality reduction**: Focusing only on the most informative features, such as using PCA to reduce 50 features down to 5.
- **Summary statistics**: Understanding the scale and spread of data through means and standard deviations.
- **Outlier detection**: Identifying extreme, abnormal values in the dataset.
- **Missing value analysis**: Deciding how to handle gaps in the data.
- **Correlation analysis**: Identifying how features relate to one another.
- **Visualization**: Spotting patterns quickly using plotting tools like scatter plots.

## Data Profiling vs EDA

| Data Profiling                                                                                         | Exploratory Data Analysis (EDA)                                                                       |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------- |
| Focuses on summarizing and assessing data quality.                                                     | A broader process of understanding data and discovering patterns.                                     |
| Answers: What does the data look like? Is it clean?.                                                   | Answers: What is happening in the data and why?                                                       |
| Mostly involves descriptive statistics (mean, median, standard deviation, missing counts, data types). | Includes visualization, observing relationships, and building hypotheses.                             |
| Usually serves as the first step of EDA.                                                               | Goes beyond simple profiling to include correlation analysis, scatter plots, and feature engineering. |

## From Business Problem to Data Structure

Machine learning is used to solve specific business problems.
To determine an ML solution, you must ask what the business goals are, how the business currently works (requiring domain knowledge), and how predictive models can address the problem.
Every potential solution must be evaluated for feasibility:

- Is the data required by the solution available, or could it be made
available?
- Does the right data exist?
  - At the right level of granularity?
  - In the necessary quantities?
  - Within the required time frame?
  - Is it legally obtainable?
  - What is the capacity of the business to utilize the insights that the analytics solution will provide?

![designmatrix](https://i.imgur.com/pvHMZVK.png)

Once you've found and selected a feasible solution, you need to design a structure to store the data called the **Design Matrix**.
In a design matrix, each column stores a feature, and each row represents a single sample or instance of data from the dataset.
For supervised models, we store an additional target matrix or target vector for all the actual values we want to be able to predict accurately based on the sample dataset.

## Data Types

- **Numeric**: Quantitative variables that store real numbers (continuous variables)
  - **Integer**: Genuine whole numbers where arithmetic is meaningful. (e.g. number of children)
- **Interval**: Ordered data with a known 0 point. (e.g. time intervals or tax bracket)
- **Categorical**: Qualitative variables that group variables into certain categories (e.g. color or size)
  - **Ordinal**: Categories with meaningful order (e.g. sizes like small, medium, large)
  - **Nominal**: Categories without mathematical interpretation (e.g. colors labeled 1, 2, 3)
    - **Binary**: Nominal variables restricted to only two values (e.g. alive)
- **Text**: Free form text data
- **Ratio Scaled**: Data where ratios makes sense (e.g. a 10kg weight is twice 5kg)

## Feature Engineering

**Feature engineering** is the process of using domain knowledge to transform raw data into informative features (variables) that enhance the accuracy and performance of machine learning models.
Basically, it involves selecting, modifying, or deriving new variables from existing data to make patterns more accessible to algorithms.
It is an iterative, and often manual, process combining domain knowledge and data analysis to transform raw data into actionable ML models.
Common techniques used in feature engineering include:

- **Imputation**: Filling in missing values using median, mean, mode, or other advanced ML models (like k-Nearest neighbours).
- **Encoding**: Converting categorical text data into numerical format (e.g. one-hot encoding).
- **Scaling**: Normalizing or standardizing numerical data (e.g. Min-Max scaling or Standard scaling) to reduce bias of larger values
- **Transformation**: Applying functions like logarithm to handle skewed data.
- **Derivation**: Creating new features via aggregates (means, maxes), reducing granularity (minutes to hours), creating binary flags, calculating ratios (click through rate), or mapping continuous values to categories.

## Exploring Data

Categorical variables are explored by examining the percentage of their representation (often via bar plots) to find common values.

Continuous or numeric variables are summarized using the mean, standard deviation, histograms, and box plots to describe central tendency and variation.

Common distributions include the uniform distribution (all values are equally likely), normal distribution (they are just frequent in nature), exponential distribution (time until an event).
Be careful when summarizing continuous variables though! Multimodal distributions indicate multiple groups making the mean a misleading metric.

### Data Quality Issues

- **Missing values**: Find the percentage of missing values per column (feature). Missingness can carry a lot of information (sensor failure, integration loss, or intentional ommissions). If a feature is missing more than ~60% of its values, it is generally better to drop it before training the model. Missing values can also be imputed if missingness is less than ~30%, though this can bias data as it is not accurate.
- **Irregular cardinality**: If a categorical feature has a cardinality of 1 (all values are identical), it should be removed. On the other hand, if cardinality equals the dataset size (no values are identical), it might actually be a continuous variable.
- **Outliers**: Outliers can be invalid errors or valid but unusual events and you want to be careful of which outlier appearing entries you erase during data cleaning.
- Outliers can be handled by clamping the values using the whiskers of the box plot or using the mean plus/minus a multiple of the standard deviation. If the value is invalid and the feature is important, consider removing the observation (sample) entirely.

### Feature Relationship

Summarizing and understanding the statistics behind features is very important.
The most common variables that are measured are the mean (average), median (middle), and mode (frequent).
These are self-explanatory as to what each variable describes about the data set.

You can also measure the variance of a dataset which indicates how tightly clustered the data is around the mean. Basically, it quantifies the amount of dispersion in a set of data values.
The variance is measured by finding the average of all the distances squared between every data point and the mean (or E(X) in the figure).
The standard deviation of a data set also represents variance and is measured as the square root of the variance. Standard deviation is more commonly used and preferred over variance primarily because it is in the same units as the original data, making it directly interpretable, intuitive, and easy to compare with the mean.
The normal distribution has nothing to do with the definition of standard deviation, it just happened to cover a fixed ratio of the normal distribution and it became a well-known fact in statistics.

![featrelformulas](https://i.imgur.com/jNtFRu8.png)

Summarizing an individual feature is easy but when you're trying to find the relation of a feature with another, it starts to become confusing.
Covariance measures the linear relationship between variables and the degree to which they deviate from their means together. Refer to the figure above to understand how covariance is calculated.
However, a major issue with covariance is that it maintains the units of each variable, making it difficult to compare relationships across different scales.
Correlation solves this by normalizing the covariance, removing the units, and limiting the range to `[-1, 1]`.
Refer to the figure above to understand how correlation is calculated.

If the correlation is close to -1, it indicates a strong negative relationship between the two variables (as one grows, the other declines).
If the correlation is close to 0, it indicates a weak relationship between the two variables (not really related).
If the correlation is close to 1, it indicates a strong positive relationship between the two variables (as one grows, the other grows too).

If you are wondering how the correlation formula actually normalizes covariance, you're asking the right questions.
To answer your question shortly, the proof is based on simple vector math.
But if you're curious to explore it more, look into the Cauchy-Shwarz inequality which explains the proof.

## Data Preparation

When preparing data for the machine learning models, the most essential procedures are normalization and binning to make sure the data is optimal for the models to learn.
There are many normalization techniques such as min-max scaling and standard scaling.
Min-Max scaling just modifies the range of a feature to fit within a specific scale, like `[0, 1]`.
Standard scaling normalizes features by removing the mean and scaling to unit variance, ensuring each numerical feature has a mean of 0 and a standard deviation of 1.
Normalization is essential for machine learning algorithms that are sensitive to data scale (like KNN, SVM, Linear Regression, etc).

Binning, also called discretization, converts continuous features into categorical features to help algorithms and manage outliers.
Equal-width binning splits values into bins of the exact same size range.
Equal-frequency binning sorts values and places and equal number of data instances into each bin.
Custom binning uses domain knowledge to dictate meaningful boundaries (e.g., defining "rush hour" times).

## Sampling Strategies

Sampling is critical in machine learning when dealing with massive datasets that are computationally expensive to process, imbalanced data that causes bias, or when needing to validate model performance efficiently.
It enables training on a representative subset to reduce training time, prevent overfitting, and ensure fair, accurate models.

The most popular samplings strategies are:

- **Top sampling**: Selecting a flat percentage from the top of the dataset. This is almost always biased based on how the data was ordered.
- **Random sampling**: Randomly selecting a flat percentage. It is better, but does not always preserve data relationships.
- **Stratified sampling**: Grouping the dataset by a variable (strata) and randomly sampling a percentage from each group to preserve relative frequencies.
- **Under-sampling**: Equalizing a dataset by randomly sampling the abundant class to match the size of the smallest minority class.
- **Over-sampling**: Equalizing a dataset by generating synthetic data for the minority class (e.g., using SMOTE) to match the abundant class.

---

# Classification and Evaluation



---

*Written by BooleanCube :]*
