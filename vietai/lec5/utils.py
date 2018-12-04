import numpy as np
from matplotlib import pyplot as plt


def generate_data(a, b, train_set_ratio=0.5):
    # Generate data around line y = ax + b
    x = np.arange(-10, 10, 0.2)
    y = a * x + b + 5 * np.random.rand(len(x))

    data_size = len(x)
    x_train = x[: int(data_size * train_set_ratio)]
    y_train = y[: int(data_size * train_set_ratio)]
    x_test = x[int(data_size * (1 - train_set_ratio)):]
    y_test = y[int(data_size * (1 - train_set_ratio)):]

    return x_train, y_train, x_test, y_test


def visualize_data(x, y, viz_trainining=False):
    # Plot data using matplotlib
    plt.plot(x, y, 'bo')
    plt.ylabel('Output Value')
    plt.xlabel('Input Feature')
    if viz_trainining:
        plt.title('Normalized data\tClick on the figure to run Gradient Descent Algorithm')
        plt.waitforbuttonpress()
    else:
        plt.title('Original data')
        plt.show()


def normalize_feature(X, mode, mean=None, std=None):
    if mode == 'train':
        mean = X.mean()
        std = X.std()
        X_norm = (X - mean) / std

        return X_norm, mean, std

    elif mode == 'test':
        assert mean is not None and std is not None
        X_norm = (X - mean) / std
        return X_norm

    else:
        raise NotImplementedError
