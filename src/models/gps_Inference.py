import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from GaussianProcess import GaussianProcess
from kernels import GaussianKernel, RBFKernel, RationalQuadraticKernel, ExponentiatedKernelSineKernel
from data.data_loader import load_mauna_loa_atmospheric_co2, load_international_airline_passengers


# choose a data file
data_file = "data/mauna_loa_atmospheric_co2.csv"
#data_file = "data/international-airline-passengers.csv"

# Load the data
if data_file == "data/mauna_loa_atmospheric_co2.csv":
    features, targets, features_normalized = load_mauna_loa_atmospheric_co2(data_file)
else:
    features, targets, features_normalized = load_international_airline_passengers(data_file)

# Prepare data
features = features_normalized
features_train, features_test, targets_train, targets_test = train_test_split(features, targets, test_size=0.2, random_state=42, shuffle=False)

# creating GP's with different kernels
# and fitting them with training set

# Gaussian kernel
gp_gaussian = GaussianProcess(GaussianKernel())
gp_gaussian.fit(features_train, targets_train)

# RBF kernel
gp_rbf = GaussianProcess(RBFKernel())
gp_rbf.fit(features_train, targets_train)

# Rational Quadratic Kernel
gp_rq = GaussianProcess(RationalQuadraticKernel())
gp_rq.fit(features_train, targets_train)

# Exponentiated Kernel Sine Kernel
gp_es = GaussianProcess(ExponentiatedKernelSineKernel())
gp_es.fit(features_train, targets_train)

# predicting the mean and covariance for each model
mean_gaussian, cov_gaussian = gp_gaussian.predict(features_test)
mean_rbf, cov_rbf = gp_rbf.predict(features_test)
mean_rq, cov_rq = gp_rq.predict(features_test)
mean_es, cov_es = gp_es.predict(features_test)


# Calculate 95% confidence intervals : ± 2 standard deviation for each GP's
std_gaussian = np.sqrt(np.diag(cov_gaussian))
upper_gaussian = mean_gaussian + 2 * std_gaussian
lower_gaussian = mean_gaussian - 2 * std_gaussian

std_rbf = np.sqrt(np.diag(cov_rbf))
upper_rbf = mean_rbf + 2 * std_rbf
lower_rbf = mean_rbf - 2 * std_rbf

std_rq = np.sqrt(np.diag(cov_rq))
upper_rq = mean_rq + 2 * std_rq
lower_rq = mean_rq - 2 * std_rq

std_es = np.sqrt(np.diag(cov_es))
upper_es = mean_es + 2 * std_es
lower_es = mean_es - 2 * std_es


# Plot shaded regions for confidence intervals and the mean for each gp's
plt.figure(figsize=(15, 10))
plt.title("Mean Predictions with Confidence Intervals (95%)")
plt.xticks([])
plt.yticks([])

plt.subplot(2, 2, 1)
plt.scatter(features, targets, color="black", s=1)
plt.plot(features_test , mean_gaussian, label="'mean' Gaussian Kernel", color="blue")
plt.plot(features_test, upper_gaussian, color="blue", alpha=1)
plt.plot(features_test, lower_gaussian, color="blue", alpha=1)
plt.fill_between(features_test.flatten(), upper_gaussian, lower_gaussian, color="blue", alpha=0.5, label="Gaussian Kernel")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()

plt.subplot(2, 2, 2)
plt.scatter(features, targets, color="black", s=1)
plt.plot(features_test, mean_rbf, label="'mean' RBF Kernel", color="red")
plt.plot(features_test, upper_rbf, color="red", alpha=1)
plt.plot(features_test, lower_rbf, color="red", alpha=1)
plt.fill_between(features_test.flatten(), upper_rbf, lower_rbf, color="red", alpha=0.5, label="RBF Kernel")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()

plt.subplot(2, 2, 3)
plt.scatter(features, targets, color="black", s=1)
plt.plot(features_test, mean_rq, label="'mean' Rational Quadratic Kernel", color="green")
plt.plot(features_test, upper_rq, color="green", alpha=1)
plt.plot(features_test, lower_rq, color="green", alpha=1)
plt.fill_between(features_test.flatten(), upper_rq, lower_rq, color="green", alpha=0.5, label="Rational Quadratic Kernel")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()

plt.subplot(2, 2, 4)
plt.scatter(features, targets, color="black", s=1)
plt.plot(features_test, mean_es, label="'mean' Exponentiated Kernel Sine Kernel", color="purple")
plt.plot(features_test, upper_es, color="purple", alpha=1)
plt.plot(features_test, lower_es, color="purple", alpha=1)
plt.fill_between(features_test.flatten(), upper_es, lower_es, color="purple", alpha=0.5, label="Exponentiated Kernel Sine Kernel")
plt.xlabel("X")
plt.ylabel("y")
plt.legend()

plt.show()